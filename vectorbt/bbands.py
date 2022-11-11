import vectorbt as vbt
import talib as ta
import pandas as pd
import numpy as np
import datetime

data = pd.read_csv('/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/00_market_data/crypto/binance/UPERP/daily/BTCUSDT_UPERP_1d.csv')
#data = pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_1h.csv',parse_dates=True)
data['middle'] = data['close'].rolling(window=14).mean()
data['upper'] = data['middle'] + 1.95 * data['middle'].rolling(window=14).std()
data['lower'] = data['middle'] - 1.95 * data['middle'].rolling(window=14).std()

data['middle'] = data['close'].rolling(window=14).mean()
data['upper'] = data['middle'] + 1.95 * data['middle'].rolling(window=14).std()
data['lower'] = data['middle'] - 1.95 * data['middle'].rolling(window=14).std()
data['entry_long'] = np.where(data['close'] > data['lower'] ,True, False)
data['exit_long'] = np.where(data['entry_long'].shift(10) ,True, False)
data['entry_short'] = np.where(data['close'] > data['upper'] ,True, False)
data['exit_short'] = np.where(data['entry_short'].shift(10) ,True, False)  




pf = vbt.Portfolio.from_signals(
    sl_stop = 0.01,  #i'm not sure about this usage
    tp_stop = 0.01,  #i'm not sure about this usage
    #sl_trial = 0.05,
    close = data['close'],
    entries = data['entry_long'],
    exits = data['exit_short'],
    short_entries = data['entry_short'],
    short_exits = data['exit_short'],
    price=data['high'],
    direction = 'both',
    accumulate = True
)

print(pf.stats())
pf.plot().show()


print(data['entry_long'])
print (data.loc[data['entry_long'] == True])
print(pf.positions.records_readable) 
#------------------------------
#maximize

# best_parameters = []
# windows = range(1,50,10)
# lags = range(1, 50, 10)
# trial=[0.001,0.003,0.005]
# tp_profits = [0.002, 0.004, 0.006, 0.008]
# sl_losses = [0.002, 0.004, 0.006, 0.008]

# for window in windows:
#     for lag in lags:
#         for tp in tp_profits:
#             for sl in sl_losses:
#                 for tr in trial:
#                     data['middle'] = data['close'].rolling(window=window).mean()
#                     data['upper'] = data['middle'] + 1.95 * data['middle'].rolling(window=window).std()
#                     data['lower'] = data['middle'] - 1.95 * data['middle'].rolling(window=window).std()
#                     data['entry_long'] = np.where(data['close'] > data['lower'] ,True, False)
#                     data['exit_long'] = np.where(data['entry_long'].shift(10) ,True, False)
#                     data['entry_short'] = np.where(data['close'] > data['upper'] ,True, False)
#                     data['exit_short'] = np.where(data['entry_short'].shift(10) ,True, False)
#                     pf = vbt.Portfolio.from_signals(
#                         sl_stop = sl,  #i'm not sure about this usage
#                         tp_stop = tp,  #i'm not sure about this usage
#                         #sl_trial = 0.005,
#                         close = data['close'],
#                         entries = data['entry_long'],
#                         exits = data['exit_short'],
#                         short_entries = data['entry_short'],
#                         short_exits = data['exit_short'],
#                         direction = 'both',
#                         accumulate = True
#                     )
#                     stats = pf.stats()
#                     if stats['Profit Factor'] > 1.2:
#                         print(f'lag:{lag}, window:{window},sl:{sl},tp:{tp},tr:{tr},return: {stats["Total Return [%]"]}')
#                         best_parameters.append({
#                             'lag' : lag,
#                             'window': window,
#                             'sl' : sl,
#                             'tp' : tp,
#                             'tr' : tr,
#                             'stat' : stats
#                         })
# data.tail(500)[['middle','upper','lower','close']].plot(figsize=(30,5)).show()
# #this line cannot show