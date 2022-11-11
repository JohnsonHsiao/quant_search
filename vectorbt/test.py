import vectorbt as vbt
import pandas as pd
import numpy as np
import talib as ta
from datetime import datetime

in_position_quantity = 0
pending_orders = {}
dollar_amount = 10000
logfile = 'trade.log'

data = pd.read_csv('/Users/johnsonhsiao/Library/CloudStorage/OneDrive-個人/00_market_data/crypto/binance/UPERP/daily/BTCUSDT_UPERP_1d.csv')
high = data['high']
low = data['low']
close = data['close']
fastk_period = 9
slowk_matype = 0
slowk_period = 3
slowd_period = 3
# J = 3*K - 2*D
#delta = data.r_[data.nan, data.diff(J)]

def STOCH(data, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
    slowk, slowd = ta.STOCH(high, low, close, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
    #data = pd.DataFrame({'STOCH_SLOWK': slowk, 'STOCH_SLOWD': slowd}, index=data.index)
    data['STOCH_SLOWK']=slowk 
    data['STOCH_SLOWD']=slowd
    print(data)
    return(data) 
STOCH(data)
print("-------")


data['20']=20
data['80']=80
data['entries'] = np.where((data['STOCH_SLOWD'] < data['20']) & (data['STOCH_SLOWK'] > data['STOCH_SLOWD']) ,True, False)
data['exits'] = np.where((data['STOCH_SLOWD'] > data['80']) & (data['STOCH_SLOWK'] < data['STOCH_SLOWD']) ,True, False)
pf = vbt.Portfolio.from_signals(
    close = data['close'],
    entries = data['entries'],
    exits = data['exits'],
    init_cash=10000
    )
print(pf.stats())
pf.plot().show()

