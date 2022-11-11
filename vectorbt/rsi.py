import numpy as np
import pandas as pd
import vectorbt as vbt
import pandas_ta as ta
from datetime import datetime

import sys
from pathlib import Path
user_home_path = str(Path.home())
sys.path.append(f'{user_home_path}/dirac-backtest-system')

#simple example

btc_price = vbt.YFData.download('BTC-USD',interval='1d') #add interval to clear the time scale
closing_price = btc_price.get('Close')
rsi = vbt.RSI.run(closing_price,14) #add windows to clear the time scale
entries = rsi.rsi_crossed_below(50)
exits = rsi.rsi_crossed_above(80)
# print(entries)
# print(exits)
portfolio = vbt.Portfolio.from_signals(closing_price,entries,exits,init_cash=10000)
portfolio.plot().show()
print(portfolio.stats())




#optimization process

num = 10
metric = 'total_return'

btc_price = pd.read_csv(f'{user_home_path}/dirac-backtest-system/BTCUSDT_UPERP_1h.csv')[['datetime','close']]
btc_price = btc_price.set_index('datetime')['close']
rsi = vbt.RSI.run(btc_price, window=14,short_name='rsi')

entry_points = np.linspace(1,45,num=num)
exits_points = np.linspace(55,99,num=num)

grid = np.array(np.meshgrid(entry_points, exits_points)).T.reshape(-1,2)

entries = rsi.rsi_crossed_below(list(grid[:, [0]]))
exits = rsi.rsi_crossed_above(list(grid[:, [1]]))

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
print(pf.stats())
pf_perf = pf.deep_getattr(metric)
pf_perf_matrix = pf_perf.vbt.unstack_to_df(index_levels = 'rsi_crossed_above',
                                          column_levels = 'rsi_crossed_below')
pf_perf_matrix.vbt.heatmap(
     xaxis_title = "exit",
     yaxis_title = "entry").show()
print(pf_perf_matrix)

