import vectorbt as vbt
import talib as ta
import pandas as pd
import numpy as np
import datetime



#get data
data = pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_1h.csv',parse_dates=True)
closing_price = data['close']


#macd signal
MACD=vbt.MACD.run(
    closing_price,
    fast_window=12,
    slow_window=26,
    signal_window=9,
    macd_ewm=True,
    signal_ewm=True,
    short_name='macd',
    hide_params=None,
    hide_default=True,
    )



#entry condition
entries=MACD.signal_above(
    MACD.macd,
    level_name=None,
    allow_multiple=True,
    )
#close condition
exits=MACD.signal_below(
    MACD.macd,
    level_name=None,
    allow_multiple=True,
    )





#calculate portfolio
pf = vbt.Portfolio.from_signals(
    sl_stop = 0.5,  
    tp_stop = 0.5,  
    #sl_trial = 0.05,
    close = data['close'],
    entries = entries,
    exits = exits,
    accumulate = True
    )
print(pf.stats())
pf.plot().show()
print(pf.positions.records_readable) 