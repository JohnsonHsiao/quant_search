from time import time
from tkinter import E
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import json
import os
import datetime

import sys
from pathlib import Path
user_home_path = str(Path.home())
sys.path.append(f'{user_home_path}/dirac-backtest-system')

import configparser
config = configparser.ConfigParser()
config.read(f'{user_home_path}/dirac-backtest-system/config/confidential.ini')
key = config['VECTOR_BT_USAGE']['API_Key']
secret = config['VECTOR_BT_USAGE']['Secret_Key']

# this will remove today later after demo with intern
print(key)
print(secret)

asset = "BTCUSDT"
entry = 25
exit =74
client = Client(key, secret, testnet =True)

# if u want trade in live, u just apply a formal api key and do not use testnet
balance = client.get_asset_balance(asset = 'BTC')

def fetch_klines(asset):
    klines = client.get_historical_klines(asset, Client.KLINE_INTERVAL_1MINUTE,'1 hour ago UTC')
    klines = [[x[0],float(x[4])] for x in klines]
    klines = pd.DataFrame(klines,columns = ['time','price'])
    klines['time'] = pd.to_datetime(klines['time'], unit = 'ms')

    return klines
    '''
    the result of original klines in line14
    1499040000000,      // Kline open time
    "0.01634790",       // Open price
    "0.80000000",       // High price
    "0.01575800",       // Low price
    "0.01577100",       // Close price
    "148976.11427815",  // Volume
    1499644799999,      // Kline Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "0"                 // Unused field, ignore.
    '''
def get_rsi(asset):
    klines = fetch_klines(asset)
    klines['rsi'] = ta.rsi(close=klines['price'],length=14)
    return klines['rsi'].iloc[-1]

def log(msg):
    print('LOG:{msg}')
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    time = now.strftime('%H-%M-%S')
    with open(f'logs/{today}.txt','a+')as log_file:
        log_file.write(f'{time}:{msg}\n')
    print(now)


def create_account():
    account = {
        'is buying':True,
        'asset':{}}
    with open('/Users/johnsonhsiao/dirac-backtest-system/vectorbt/bot_account.json','w') as f:
        f.write(json.dumps(account))

rsi = get_rsi(asset)
old_rsi = rsi

while True:
    try:
        if not os.path.exists('b/Users/johnsonhsiao/dirac-backtest-system/vectorbt/bot_account.json'):
            create_account()
        with open('/Users/johnsonhsiao/dirac-backtest-system/vectorbt/bot_account.json','w') as f:
            account = json.load(f)
        print(account)
        old_rsi = rsi
        rsi = get_rsi(asset)
        if account['is buying']:
            if rsi < entry and old_rsi > entry:
                pass
        else:
            if rsi > exit and old_rsi < exit:
                pass
        print(rsi)
        time.sleep(18)

    except Exception as e:
        #lof error
        log('ERROR' + str(e))
        


