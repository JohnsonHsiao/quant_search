import vectorbt as vbt
import pandas as pd
import pandas_ta as ta
import numpy as np
import datetime


#trade only  the price above the 200-day moving average 
#entry: place a 3% buy limit order below the prevous day closing price after closing price is below bb
#exit: 2-day RSI cross above 50 or after 10 tradind day
#the logic is merely useful for index

df = pd.read_csv('/Users/edisonalbert/Documents/data4h1day/ETHUSDT_UPERP_1h.csv',parse_dates=True)
df['price'] = np.inf #to record the limit order price





#define function
def build_df(bb_len, rsi_len, rsi_v, buy_signal_cnt_limit):
    entry_list = {} #use dictionary to store the info of entry
    exit_list = {}  #use dictionary to store the info of exit
    
    last_buy_signal_cnt = 0
    in_position = False

    #adding indicator
    df_copy = df.copy() 
    df_copy[['lower','mid','upper','bandwidth','percent']] = ta.bbands(df_copy['close'], length=bb_len, std=2.5)
    df_copy = df_copy.dropna(subset=['lower'])
    df_copy['rsi'] = ta.rsi(df_copy['close'], length=rsi_len)
    df_copy['cross_rsi'] = ta.above_value(df_copy['rsi'], rsi_v)
    df_copy['ma'] = ta.sma(df_copy['close'], length=200)

    #enrty and exit logic
    for i, (index, row) in enumerate(df_copy.iterrows()):
        entry_list[index] = False
        exit_list[index] = False
        if (row['close'] < row['lower']) and (row['close'] > row['ma']):
            # entry conditoin 1
            limit_price = df_copy.loc[df_copy.index[i-1], 'close'] * 0.98 #set the limit price
            
            if row['low'] < limit_price:
                # entry condition 2
                entry_list[index] = True
                in_position = True
                df_copy.at[index, 'price'] = limit_price
                last_buy_signal_cnt = 0
            
        if in_position:
            last_buy_signal_cnt += 0

        if row['cross_rsi'] == 1:
            exit_list[index] = True
            df_copy.at[index,'price'] = row['close']
            last_buy_signal_cnt = 0

        if last_buy_signal_cnt > buy_signal_cnt_limit:
            last_buy_signal_cnt = 0
    
    
    df_copy['entry'] = entry_list.values()
    df_copy['exit'] = exit_list.values()
    
    return df_copy





#optimization
param_list = []

for x in range(15, 30):
    for y in range(2,5):
        df_ = build_df(x, y, 50, 10)
        pf = vbt.Portfolio.from_signals(df_['close'], entries=df_['entry'], exits=df_['exit'], price=df_['price'],init_cash=30000, accumulate=True)
        
        winrate = pf.stats()[r'Win Rate [%]']
        total_return = pf.stats()[r'Total Return [%]']
        total_profit = pf.total_profit()
        max_drawdown = pf.max_drawdown()
        total_trades = len(pf.trades)
        # print('total profit', total_profit)
        print('total_return', total_return)
        # print('total trades', total_trades)

        param_list.append((x,y,total_return,total_trades,winrate))




#using the optimize parameter

df_ = build_df(23, 4, 50, 10)
pf = vbt.Portfolio.from_signals(df_['close'], entries=df_['entry'], exits=df_['exit'], price=df_['price'],
                                    init_cash=30000, accumulate=True)

print(pf.stats())
pf.plot().show()
print(pf.positions.records_readable) 


# print(df_)
# print (df＿.loc[df＿['entry'] == True])
