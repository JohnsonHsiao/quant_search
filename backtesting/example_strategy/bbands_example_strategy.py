import numpy as np
import yfinance as yf
import pandas as pd
import talib  as ta
from backtesting import Backtest,Strategy
from backtesting.test import GOOG
import os

from pathlib import Path
import sys
user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/dirac-backtest-system")

save_dir = f'{user_home_path}/dirac-backtest-system/data_center/backtesting_result'
Strategy_class = 'BbandStrategy'

def indicator(data):
    #data is going to be our OHLCV
    upperband, middleband, lowerband = ta.BBANDS(GOOG.Close, timeperiod=10, nbdevup=1, nbdevdn=1, matype=0)
    #bbands = ta.bbands(close = data.Close.s, std=1)
    #print (upperband.to_numpy(), middleband.to_numpy(), lowerband.to_nmpy())
    return upperband, middleband, lowerband

class BbandStrategy(Strategy):
    def init(self):
        self.upperband = self.I(indicator,self.data) 
        self.middleband = self.I(indicator,self.data) 
        self.lowerband = self.I(indicator,self.data)  
        print(self.upperband, self.middleband, self.lowerband)
    def next(self):
        # the logic part 
        if self.position:

            if self.data.Close[-1] > self.upperband [-1][-1]:
                self.position.close()
        else:
            
            if self.data.Close[-1] < self.lowerband[-1][-1]:
                self.buy()

bt = Backtest(GOOG, BbandStrategy, cash=100000)

output = bt.run()
print(output)
bt.plot()
# saving data part
trade_pnl_df = output['_trades']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
trade_pnl_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_trade_pnl_df.csv")

equity_curve_df = output['_equity_curve']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
equity_curve_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_equity_curve.csv")