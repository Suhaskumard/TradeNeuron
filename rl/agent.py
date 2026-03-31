import gym
import numpy as np
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from typing import Dict, List

class TradingEnv(gym.Env):
    """Custom trading environment"""
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        
        self.df = df.reset_index(drop=True)
        self.current_step = 0
        self.max_steps = len(df) - 1
        self.initial_balance = 100000
        self.balance = self.initial_balance
        self.shares_held = 0
        self.total_shares_sold = 0
        self.total_profit = 0
        
        # Actions: 0=hold, 1=buy, 2=sell
        self.action_space = spaces.Discrete(3)
        
        # State: price, rsi, macd, balance, shares
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32
        )
    
    def reset(self):
        self.current_step = 60  # Skip initial for indicators
        self.balance = self.initial_balance
        self.shares_held = 0
        self.total_shares_sold = 0
        self.total_profit = 0
        return self._get_observation()
    
    def _get_observation(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            row['close'] / 1000,  # Normalize
            row['rsi'] / 100,
            row['macd'],
            self.balance / self.initial_balance,
            self.shares_held,
            row['returns'],
            row['volume_ratio'],
            self.total_profit
        ], dtype=np.float32)
    
    def step(self, action):
        current_price = self.df.iloc[self.current_step]['close']
        reward = 0
        
        if action == 1:  # Buy
            shares_bought = self.balance // current_price
            self.shares_held += shares_bought
            self.balance -= shares_bought * current_price
        
        elif action == 2 and self.shares_held > 0:  # Sell
            self.balance += self.shares_held * current_price
            self.total_profit += self.shares_held * (current_price - self.df.iloc[0]['close'])
            self.total_shares_sold += self.shares_held
            self.shares_held = 0
        
        self.current_step += 1
        done = self.current_step >= self.max_steps or self.balance <= 0
        
        if done:
            reward = self.total_profit
            
        obs = self._get_observation() if not done else np.zeros(8)
        return obs, reward, done, {}

class RLAgent:
    def __init__(self, df):
        self.env = DummyVecEnv([lambda: TradingEnv(df)])
        self.model = PPO("MlpPolicy", self.env, verbose=0)
    
    def train(self, total_timesteps=10000):
        self.model.learn(total_timesteps=total_timesteps)
    
    def predict(self, obs):
        action, _ = self.model.predict(obs)
        actions = ["HOLD", "BUY", "SELL"]
        return actions[action]
    
    def save(self, path="rl_trader.zip"):
        self.model.save(path)
    
    def load(self, path="rl_trader.zip"):
        self.model = PPO.load(path, env=self.env)

