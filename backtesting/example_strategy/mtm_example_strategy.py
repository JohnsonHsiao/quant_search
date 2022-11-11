from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import numpy as np
import pandas_ta as ta
import os

from pathlib import Path
import sys
user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/dirac-backtest-system")

save_dir = f'{user_home_path}/dirac-backtest-system/data_center/backtesting_result'
Strategy_class = 'MtmStrategy'

def indicator(data):
    # data is going to be our OHLCV
    return data.Close.s.pct_change(periods = 7)*100

class MtmStrategy(Strategy):
    def init(self):
        self.pct_change = self.I(indicator,self.data)   
    def next(self):
        change = self.pct_change[-1]
        if self.position:
            if change<0:
                self.position.close()
        else:
            if change > 5 and self.pct_change[-2] > 5: # to-do understand why?
                self.buy()

bt = Backtest(GOOG,MtmStrategy, cash=10000)
output = bt.run()
bt.plot()
print(output)

trade_pnl_df = output['_trades']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
trade_pnl_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_trade_pnl_df.csv")

equity_curve_df = output['_equity_curve']
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
equity_curve_df.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_equity_curve.csv")
