import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, model, target_model, env, gamma=0.8, epsilon=1, epsilon_min=0.1, epsilon_degrade_rate=0.99998, batch_size=32, max_memory_length=100000, update_after_actions=4, update_target_network=1000):
        self.model = model
        self.target_model = target_model
        self.env = env
        self.gamma = gamma
        self.epsilon_min = epsilon_min
        self.epsilon = epsilon
        self.epsilon_degrade_rate = epsilon_degrade_rate
        self.batch_size = batch_size
        self.max_memory_length = max_memory_length
        self.update_after_actions = update_after_actions
        self.update_target_network = update_target_network

        # Experience replay buffers
        self.action_history = []
        self.state_history = []
        self.state_next_history = []
        self.rewards_history = []
        self.done_history = []
        self.episode_reward_history = []
        self.running_reward = 0
        self.episode_count = 0
        self.frame_count = 1
        self.episode_reward = 0


    def step(self, env_state=None):
        optimizer = keras.optimizers.Adam(learning_rate=1e-4, clipnorm=1.0)
        # Using huber loss for stability
        loss_function = keras.losses.CategoricalCrossentropy()
        if not env_state:
            state = np.array(self.env.state)
        else:
            state = np.array(env_state)
        state_shape = self.env.shape
        state = np.reshape(state, (state_shape[0], state_shape[1]*state_shape[2]))
        done = False
        # env.render()
        # Use epsilon-greedy for exploration
        if self.epsilon > np.random.rand(1)[0]:
            # Take random action
            action = self.env.action_sample()
        else:
            # Predict action Q-values from environment state
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = self.model.model(state_tensor, training=False)
            # Take best action
            action = tf.argmax(action_probs[0]).numpy()
            logger.info('Q value elected action:' + str(action))

        # Decay probability of taking random action
        self.epsilon *= self.epsilon_degrade_rate
        self.epsilon = max(self.epsilon, self.epsilon_min)

        # Apply the sampled action in environment
        state_next, reward, done, _ = self.env.step(action)
        if done:
            state_next = np.array(state)
        else:
            state_next = np.array(state_next)

        self.env.state = state_next
        state_next = np.reshape(state_next, (state_shape[0], state_shape[1]*state_shape[2]))

        self.frame_count += 1
        self.episode_reward += reward

        # Save actions and states in replay buffer
        self.action_history.append(action)
        self.state_history.append(state)
        self.state_next_history.append(state_next)
        self.done_history.append(done)
        self.rewards_history.append(reward)

        # Update every fourth frame and once batch size is over 32
        if self.frame_count % self.update_after_actions == 0 and len(self.done_history) > self.batch_size:
            # Get indices of samples for replay buffers
            indices = np.random.choice(range(len(self.done_history)), size=self.batch_size)

            # Using list comprehension to sample from replay buffer
            state_sample = np.array([self.state_history[i] for i in indices])
            state_next_sample = np.array([self.state_next_history[i] for i in indices])
            rewards_sample = [self.rewards_history[i] for i in indices]
            action_sample = [self.action_history[i] for i in indices]
            done_sample = tf.convert_to_tensor(
                [float(self.done_history[i]) for i in indices]
            )

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = self.target_model.model.predict(state_next_sample)
            # Q value = reward + discount factor * expected future reward
            updated_q_values = rewards_sample + self.gamma * tf.reduce_max(
                future_rewards, axis=1
            )

            # If final frame set the last value to -1
            updated_q_values = updated_q_values * (1 - done_sample) - done_sample

            # Create a mask so we only calculate loss on the updated Q-values
            masks = tf.one_hot(action_sample, self.env.num_actions)

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = self.model.model(state_sample)

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Backpropagation
            grads = tape.gradient(loss, self.model.model.trainable_variables)
            optimizer.apply_gradients(zip(grads, self.model.model.trainable_variables))

        if self.frame_count % self.update_target_network == 0:
            # update the the target network with new weights
            self.target_model.model.set_weights(self.model.model.get_weights())
            logger.info("Episode: " + str(self.episode_count) +
                    " Frame: " + str(self.frame_count) +
                    " Episode reward:" + str(self.episode_reward))
            self.episode_count += 1
            self.model.save()
            self.target_model.save()


        # Limit the state and reward history
        if len(self.rewards_history) > self.max_memory_length:
            del self.rewards_history[:1]
            del self.state_history[:1]
            del self.state_next_history[:1]
            del self.action_history[:1]
            del self.done_history[:1]

        if done:
            # Update running reward to check condition for solving
            self.episode_reward_history.append(episode_reward)
            if len(self.episode_reward_history) > 10000:
                del episode_reward_history[:1]
            self.running_reward = np.mean(self.episode_reward_history)
            logger.info("Episode: "+str(self.episode_count)+" finshed, with running reward: "+
                    str(self.running_reward))
            self.episode_count += 1
            self.model.save()
            self.target_model.save()

        return action, state_next.tolist(), reward
