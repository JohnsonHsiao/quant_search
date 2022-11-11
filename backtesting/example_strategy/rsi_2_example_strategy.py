from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, resample_apply
import talib as ta
import os
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys

user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/dirac-backtest-system")

save_dir = f'{user_home_path}/dirac-backtest-system/data_center/backtesting_result'
Strategy_class = 'Rsi1'

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    def init(self):
        self.daily_rsi = self.I(ta.RSI, self.data.Close, self.rsi_window )
        self.weekly_rsi = resample_apply(
            "W-FRI", ta.RSI, self.data.Close, self.rsi_window
        )
    def next(self):
        if (crossover(self.daily_rsi, self.upper_bound)
            and (self.weekly_rsi[-1]> self.upper_bound)):
            self.position.close()
        elif (crossover(self.lower_bound, self.daily_rsi)
            and (self.weekly_rsi[-1] < self.lower_bound)):
            self.buy(size=0.1) # % of cash 

bt = Backtest(GOOG, RsiOscillator, cash=100000)

output = bt.run()
bt.plot()
print(output).head(5)
print(output['_trades'])