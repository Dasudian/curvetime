import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import logging

logger = logging.getLogger(__name__)


class TradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, shape, num_actions, capital, oracle=None):
        """
        A general environment for financial tradings
        shape: a tuple represents the input data dimensions
        num_actions: the number of action options
        capital: the initial money to invest
        oracle: the object that provides data for the trading environment
        """
        self.seed()
        self.shape = shape
        self.num_actions = num_actions
        self.action_space = spaces.Discrete(num_actions)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)
        self.oracle = oracle
        self.frame_count = 1
        self._done = False
        self._total_reward = 0
        self._total_profit = capital

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def reset(self):
        self._done = False
        self.frame_count = 1
        self._total_reward = 0
        self._total_profit = capital
        self.state = self._get_observation()


    def step(self, action):
        self._done = False
        step_reward = self._update_state(action)
        self.render(action)
        self.frame_count += 1
        observation = self._get_observation()
        info = (self._total_reward, self._total_profit)
        if observation is None:
            self._done = True
        return observation, step_reward, self._done, info


    def action_sample(self):
        return self.action_space.sample()


    def render(self, action, mode='human'):
        print(action, self.state, self._total_reward, self._total_profit)


    def _get_observation(self):
        return self.observation_space.sample()


    def _update_state(self, action):
        step_reward = self._calculate_reward(action)
        self._update_profit()
        return step_reward


    def _calculate_reward(self, action):
        step_reward = 0
        self._total_reward += step_reward
        return step_reward


    def _update_profit(self):
        self._update_profit += 0
