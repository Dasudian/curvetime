import numpy as np
from .trading_env import TradingEnv
from curvetime.db.models import Stocks
import logging
import pickle

logger = logging.getLogger(__name__)


WINDOW_SIZE = 48 * 5  #5-days data
TOTAL_STOCKS = 3643
FEATURES_PER_STOCK = 30
ACTIONS = range(-TOTAL_STOCKS, TOTAL_STOCKS+1)
MONEY_SLOTS = 100
SINGLE_CAPITAL = 10000
POSITION_FILE = 'data/models/position.pkl'
POSITION_HISTORY_FILE = 'data/models/position_history.pkl'
MONEY_FILE = 'data/models/money.pkl'
HOLDING_FILE = 'data/models/holding.pkl'



class StockEnv(TradingEnv):
    def __init__(self, oracle, capital=MONEY_SLOTS*SINGLE_CAPITAL, window_size=WINDOW_SIZE, num_stocks=TOTAL_STOCKS, features=FEATURES_PER_STOCK, num_actions=len(ACTIONS)):
        super().__init__((window_size, num_stocks, features), num_actions, capital, oracle)
        self.stocks = Stocks.objects.all()
        self.stocks = sorted([s.code for s in self.stocks])
        self.trade_fee_bid_percent = 0.003  # unit
        self.trade_fee_ask_percent = 0.003  # unit
        self.window_size = window_size
        self.trade = False

        try:
            fileObj = open(POSITION_FILE, 'rb')
            self._position = pickle.load(fileObj)
            fileObj.close()
        except Exception:
            self._position = [0] * TOTAL_STOCKS
        try:
            fileObj = open(POSITION_HISTORY_FILE, 'rb')
            self._position_history = pickle.load(fileObj)
            fileObj.close()
        except Exception:
            self._position_history = [[0]*TOTAL_STOCKS] * self.window_size
        try:
            fileObj = open(MONEY_FILE, 'rb')
            self.money = pickle.load(fileObj)
            fileObj.close()
        except Exception:
            self.money = [SINGLE_CAPITAL] * MONEY_SLOTS
        try:
            fileObj = open(HOLDING_FILE, 'rb')
            self.holding = pickle.load(fileObj)
            fileObj.close()
        except Exception:
            self.holding = []


        self._action_history = []
        self.state = self._get_observation()


    def _get_observation(self):
        df = self.oracle.get_dataframe(self.frame_count, self.window_size)
        if not df:
            return None
        observation = self._process_data(df)
        return observation


    def _process_data(self, df):
        prices = []
        signal_features = []
        positions = self._position_history[-self.window_size:]
        for i in range(len(df)):
            p = []
            f = []
            for j in range(len(df[i])):
                p.append(np.array(df[i][j][2]))
                f.append(np.array(df[i][j]+[positions[i][j]]))
            p = np.array(p)
            f = np.array(f)
            prices.append(p)
            signal_features.append(f)
        self.prices = np.array(prices)
        self.state = np.array(signal_features)

        return self.state


    def _calculate_reward(self, action):
        step_reward = 0
        self.trade = False

        if action > 0:
            if len(self.money) == 0 or self._position[action-1] != 0 or self.prices[-1][action-1] == 0:
                action = 0
            else:
                self.trade = True
                current_price = self.prices[-1][action-1]
                spend = self.money.pop()
                amount = (1-self.trade_fee_ask_percent)*spend/current_price
                self.holding.append({'action': action,
                                     'amount': amount})
                step_reward -= self.trade_fee_ask_percent / MONEY_SLOTS

        if action < 0:
            if self._position[abs(action)-1] == 0 or self.prices[-1][abs(action)-1] == 0:
                action = 0
            else:
                self.trade = True
                current_price = self.prices[-1][abs(action)-1]
                last_trade_price = self._position[abs(action)-1]
                price_diff = current_price - last_trade_price
                for trade in self.holding:
                    if trade['action'] == -action:
                        money = (1-self.trade_fee_bid_percent)*trade['amount']*current_price
                        step_reward += (price_diff/last_trade_price - self.trade_fee_bid_percent) / MONEY_SLOTS
                        self.money.append(money)
                        self.holding.remove(trade)
                        break

        gain_delta = self._update_profit()
        if action == 0:
            step_reward = gain_delta


        self._total_reward += step_reward
        return step_reward



    def _update_profit(self):
        self._total_profit = sum(self.money)
        for trade in self.holding:
            wealth = self.prices[-1][trade['action']] * trade['amount']
            self._total_profit += wealth
        gain = (self._total_profit - MONEY_SLOTS*SINGLE_CAPITAL)/(MONEY_SLOTS*SINGLE_CAPITAL)
        gain_delta = gain - self._total_gain
        self._total_gain = gain
        return gain_delta


    def _action_map(self, action):
        return ACTIONS[action]



    def _update_state(self, action):
        action = self._action_map(action)
        step_reward = self._calculate_reward(action)

        if self.trade:
            if action > 0:
                self._position[action-1] = self.prices[-1][action-1]
            else:
                self._position[abs(action)-1] = 0

        if len(self._action_history) >= self.window_size:
            del self._action_history[:1]
        if len(self._position_history) >= self.window_size:
            del self._position_history[:1]
        self._action_history.append(action)
        new_position = self._position.copy()
        self._position_history.append(new_position)
        self._save_positions()
        return step_reward


    def _save_positions(self):
        fileObj = open(POSITION_FILE, 'wb')
        pickle.dump(self._position, fileObj)
        fileObj.close()
        fileObj = open(POSITION_HISTORY_FILE, 'wb')
        pickle.dump(self._position_history, fileObj)
        fileObj.close()
        fileObj = open(MONEY_FILE, 'wb')
        pickle.dump(self.money, fileObj)
        fileObj.close()
        fileObj = open(HOLDING_FILE, 'wb')
        pickle.dump(self.holding, fileObj)
        fileObj.close()

    def render(self, action, mode='human'):
        action = self._action_map(action)
        if action == 0:
            action = "Frame: " + str(self.frame_count) + ", 等待时机\n"
        elif action > 0:
            if self.trade:
                action = "Frame: " + str(self.frame_count) + ", 买入: " + self.stocks[action-1] + ", 价格: " + str(self.prices[-1][action-1]) + "\n"
            elif len(self.money) == 0 and self.prices[-1][action-1] != 0:
                action = "Frame: " + str(self.frame_count) + ", 欲买入股票: " + self.stocks[action-1] + ", 价格: " + str(self.prices[-1][action-1]) + " 但是没钱了!\n"
            elif self.prices[-1][action-1] == 0:
                action = "Frame: " + str(self.frame_count) + ", 欲买入股票: " + self.stocks[action-1] + " 停牌\n"
            else:
                action = "Frame: " + str(self.frame_count) + ", 欲买入股票: " + self.stocks[action-1] + ", 价格: " + str(self.prices[-1][action-1])+ " 已建仓\n"
        else:
            if self.trade:
                action = "Frame: " + str(self.frame_count) + ", 卖出: " + self.stocks[abs(action)-1] + ", 价格: " + str(self.prices[-1][abs(action)-1]) +  " 上次买入价: " + str(self._position_history[-2][abs(action)-1]) + "\n"
            elif self.prices[-1][abs(action)-1] == 0:
                action = "Frame: " + str(self.frame_count) + ", 欲卖出股票: " + self.stocks[abs(action)-1] + " 停牌\n"
            else:
                action = "Frame: " + str(self.frame_count) + ", 欲卖出股票: " + self.stocks[abs(action)-1] + ", 价格: " + str(self.prices[-1][abs(action)-1])+ " 未建仓\n"

        logger.info(
            action +
            "Total Reward: %.6f" % self._total_reward +
            "      Total Profit: %.6f" % self._total_profit
        )
