import vectorbt as vbt
import pandas as pd
from datetime import datetime

# shit this is really good lol good job

def check_order_status():
    print('{} - checking order status'.format(datetime.now().isoformat()))
def send_order(side):
    print('{} - sending {} order'.format(datetime.now().isoformat()),side)
# get min bar or sec bar from ccxt(crypto)
def get_bar():
    print('{} - getting bars'.format(datetime.now().isoformat()))
    data = vbt.CCXTData.download(['SOLUSDT'],start = '30 minutes ago', timeframe = '1m')
    df = data.get()
    df.ta.stoch(append = True)
    print(df)
    # last_k = df['STOCH_14_3_3'].iloc[-1]
    # last_d = df['STOCH_14_3_3'].iloc[-1]
    # last_close = df['Close'].iloc[-1]

manager = vbt.ScheduleManager()
# manager.every().do(check_order_status)
manager.every().minutes.at(":00").do(get_bar)
manager.start()

