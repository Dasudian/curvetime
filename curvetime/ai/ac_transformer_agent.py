import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, model, env, gamma=0.8, history_length=10000, backup_model=1000):
        seed = 42
        self.model = model
        self.env = env
        self.gamma = gamma
        self.history_length = history_length
        self.backup_model = backup_model

        # Experience replay buffers
        self.rewards_history = []
        self.action_probs_history = []
        self.critic_value_history = []
        self.running_reward = 0
        self.episode_count = 0
        self.frame_count = 1
        self.episode_reward = 0
        self.running_reward = 0


    def step(self, env_state=None):
        finish = False
        done = False
        eps = np.finfo(np.float32).eps.item()  # Smallest number such that 1.0 + eps != 1.0
        if not env_state:
            state = np.array(self.env.state)
        else:
            state = np.array(env_state)
        state_shape = self.env.shape
        state = np.reshape(state, (state_shape[0], state_shape[1]*state_shape[2]))
        # env.render()
        with tf.GradientTape() as tape:
            state = tf.convert_to_tensor(state)
            state = tf.expand_dims(state, 0)

            # Predict action probabilities and estimated future rewards
            # from environment state
            action_probs, critic_value = self.model.model(state)
            self.critic_value_history.append(critic_value[0, 0])

            # Sample action from action probability distribution
            action = np.random.choice(self.env.num_actions, p=np.squeeze(action_probs))
            self.action_probs_history.append(tf.math.log(action_probs[0, action]))

            # Apply the sampled action in our environment
            if action == self.env.shape[1]:
                logger.info("----------------Action: 0------------------")
                action = self.env.risk_aversion_action()
                state, reward, done, _ = self.env.step(action)
            else:
                state, reward, done, _ = self.env.step(action)
            self.rewards_history.append(reward)
            self.episode_reward += reward
            self.env.state = state
            self.frame_count += 1

            # Update running reward to check condition for solving
            self.running_reward = 0.05 * self.episode_reward + (1 - 0.05) * self.running_reward

            # Calculate expected value from rewards
            # - At each timestep what was the total reward received after that timestep
            # - Rewards in the past are discounted by multiplying them with gamma
            # - These are the labels for our critic
            returns = []
            discounted_sum = 0
            for r in self.rewards_history[::-1]:
                discounted_sum = r + self.gamma * discounted_sum
                returns.insert(0, discounted_sum)

            # Normalize
            returns = np.array(returns)
            returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
            returns = returns.tolist()

            # Calculating loss values to update our network
            history = zip(self.action_probs_history, self.critic_value_history, returns)
            actor_losses = []
            critic_losses = []
            loss_function = keras.losses.Huber()
            for log_prob, value, ret in history:
                # At this point in history, the critic estimated that we would get a
                # total reward = `value` in the future. We took an action with log probability
                # of `log_prob` and ended up recieving a total reward = `ret`.
                # The actor must be updated so that it predicts an action that leads to
                # high rewards (compared to critic's estimate) with high probability.
                diff = ret - value
                actor_losses.append(-log_prob * diff)  # actor loss

                # The critic must be updated so that it predicts a better estimate of
                # the future rewards.
                critic_losses.append(
                    loss_function(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))
                )

            # Backpropagation
            loss_value = sum(actor_losses) + sum(critic_losses)
            grads = tape.gradient(loss_value, self.model.model.trainable_variables)
            optimizer = keras.optimizers.Adam(learning_rate=1e-4, clipnorm=1.0)
            optimizer.apply_gradients(zip(grads, self.model.model.trainable_variables))

        # Clear the loss and reward history
        if self.frame_count > self.history_length:
            self.action_probs_history = self.action_probs_history[1:]
            self.critic_value_history = self.critic_value_history[1:]
            self.rewards_history = self.rewards_history[1:]

        if self.frame_count % self.backup_model == 0:
            self.model.save()

        if done:
            # Log details
            self.pisode_count += 1
            template = "running reward: {:.2f} at episode {}"
            logger.info(template.format(self.running_reward, self.episode_count))
            self.model.save()

            if self.running_reward > 1000:  # Condition to consider the task solved
                logger.info("Solved at episode {}!".format(self.episode_count))
                finish = True

        return action, reward, finish
