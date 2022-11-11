import yfinance as yf
import ta
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
Strategy_class = 'SmaCrossStrategy'

class SmaCrossStrategy(Strategy):
    n1 = 50
    n2 = 100
    def init(self):
        close = self.data.Close #get data from close price
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)
        
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
            """
            if len(self.trade)>0:
            elf.trades[0].close
            postition goes 0 insted of -1 
            """

bt = Backtest(df, SmaCrossStrategy, cash=1000000, commission=0.002, exclusive_orders = True)
output = bt.run()
print(output)
print('---------------------------------------------')
bt.plot()
print(output['_trades'])
optim = bt.optimize(
    n1 = range(50,160,10), # adjust the parameter to simulate the data
    n2 = range(50,160,10),
    constraint = lambda x: x.n2 - x.n1 > 20,
    maximize = 'Return [%]') # u can use any data u want it maximize
print(optim)
print('---------------------------------------------')
bt.plot()

print(optim['_trades'])
print('---------------------------------------------')
print(optim['_equity_curve'])

trade_pnl_df = optim['_trades']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
trade_pnl_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_trade_pnl_df.csv")

equity_curve_df = optim['_equity_curve']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
equity_curve_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_equity_curve.csv")
