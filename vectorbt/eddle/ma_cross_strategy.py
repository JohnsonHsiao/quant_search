import numpy as np
import pandas as pd
import vectorbt as vbt
import pandas_ta as ta
from datetime import datetime

import sys
from pathlib import Path

user_home_path = str(Path.home())
sys.path.append(f'{user_home_path}/dirac-backtest-system')

btc_price = vbt.YFData.download('BTC-USD',interval='1d')
closing_price = btc_price.get('Close')

Ma_fast=vbt.MA.run(closing_price,10)
Ma_slow = vbt.MA.run(closing_price,50)

entries =Ma_fast .ma_crossed_above(Ma_slow)
exits = Ma_fast.ma_crossed_below(Ma_slow)
# print(entries)
# print(exits)
portfolio = vbt.Portfolio.from_signals(closing_price,entries,exits,init_cash=10000,freq='d')
#portfolio.plot().show()
print(portfolio.stats())

fig=portfolio.plot(subplots=['cum_returns','orders','trade_pnl'])
fig.show()

print(portfolio.positions.records_readable) #這個比較人性化,可是在終端機上看超 難 看,都沒有美化的終端機嗎？