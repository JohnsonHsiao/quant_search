import yfinance as yf
import talib as ta
import pandas as pd
from backtesting import Backtest,Strategy
from backtesting.lib import crossover
import os

from pathlib import Path
import sys
user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/dirac-backtest-system")

df = yf.download('BTC-USD ',start='2020-01-01')
save_dir = f'{user_home_path}/dirac-backtest-system/data_center/backtesting_result'
Strategy_class = 'KdCrossStrategy'

class KdCrossStrategy(Strategy):
    def init(self):
        self.slowk, self.slowd = self.I(
            ta.STOCH, self.data.High, self.data.Low,    
            self.data.Close ,fastk_period=9, slowk_period=3, slowd_period=3)
    def next(self):
        if crossover(self.slowk, self.slowd):
            self.buy()
        elif crossover(self.slowd, self.slowk):
            self.sell()
            
bt = Backtest(df, KdCrossStrategy, cash = 1000000, exclusive_orders=True)
output = bt.run()
print(output)
bt.plot()
print(output['_trades'])

trade_pnl_df = output['_trades']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
trade_pnl_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_trade_pnl_df.csv")

equity_curve_df = output['_equity_curve']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
equity_curve_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_equity_curve.csv")