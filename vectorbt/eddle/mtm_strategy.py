import os
import numpy as np
import pandas as pd           
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import datetime as dt
import time
import vectorbt as vbt
import pandas_ta as ta
import datetime

#this is exactly the same logic as my colab momentum strategy just using vectorbt to backtest



df = pd.read_csv("/Users/edisonalbert/Documents/TWF_Futures_Minute_Trade.txt")
plt.plot(df['Close'], color = 'red', alpha = 0.5, label = 'Close price')
plt.plot(df['TotalVolume'], color = '#01889f', alpha = 0.5, label = 'Volume')
plt.legend(loc='upper left')
plt.title('Volume History');
df.index = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.drop(columns=['Date','Time'])
df.columns = ['open', 'high', 'low', 'close', 'volume']


df['Hour'] = df.index.map(lambda x: x.hour)
rule = '60T'
Morning = df[(df['Hour'] >= 8) & (df['Hour'] <= 12)]
Morning.index = Morning.index + dt.timedelta(minutes=15)
d1 = Morning.resample(rule=rule, closed='right', label='left').first()[['open']]
d2 = Morning.resample(rule=rule, closed='right', label='left').max()[['high']]
d3 = Morning.resample(rule=rule, closed='right', label='left').min()[['low']]
d4 = Morning.resample(rule=rule, closed='right', label='left').last()[['close']]
d5 = Morning.resample(rule=rule, closed='right', label='left').sum()[['volume']]


df_Morning = pd.concat([d1,d2,d3,d4,d5], axis=1)
df_Morning = df_Morning.dropna()
df_Morning.index = df_Morning.index - dt.timedelta(minutes=15)
df_Morning.head()
df_Morning['Hour'] = df_Morning.index.map(lambda x: x.hour)
df_Morning['Day'] = df_Morning.index.map(lambda x: x.date)
trainData = df_Morning[(df_Morning.index >= '2011-01-01 00:00:00') & (df_Morning.index <= '2019-12-31 00:00:00')].copy()


trainData['MA'] = trainData['close'].rolling(window=5, center=False).mean()
trainData['a']=(trainData['close']-trainData['open'])
trainData['F']=(trainData['a']*trainData['volume'])
trainData['Fcum'] = trainData['F'].rolling(window=3, center=False).mean()
trainData['cum']= trainData.groupby('Day')['F'].transform(pd.Series.cumsum)
trainData['MAcum'] = trainData['cum'].rolling(window=3, center=False).mean()
trainData['cumSTD'] = trainData['cum'].rolling(window=12, center=False).std()


settlementDate_= pd.read_csv("/Users/edisonalbert/Documents/settlementDate.txt")
settlementDate_.columns = ['settlementDate', 'futures', 'settlementPrice']
bool_ = [False if 'W' in i else True for i in settlementDate_['futures']]
settlementDate = [i.replace('/','-') for i in list(settlementDate_[bool_]['settlementDate'])]


df_arr = np.array(trainData)
time_arr = np.array(trainData.index)
date_arr = [pd.to_datetime(i).date() for i in time_arr]
BS = None
feePaid=600


for k in range(1,2):


    BS = None
    buy = []
    sell = []
    sellshort = []
    buytocover = []
    profit_list = [0]
    profit_fee_list = [0]
    profit_fee_list_realized = []
    entry_list=[False]
    exit_list=[False]
    short_entry_list=[False]
    short_exit_list=[False]
    K=0.06
    entrySellShort= None
    for i in range(len(df_arr)):


        if i == len(df_arr)-1:
            break
            
        ## 進場邏輯
        entryLong = df_arr[i,-5] > 400000 and df_arr[i,-3]>400000   and df_arr[i,-1]>1000000 
    
        entrySellShort =  df_arr[i,-5] <  -1000000   and df_arr[i,-3]<-400000  and df_arr[i,-1]>1000000   

        





        entryCondition = date_arr[i] not in settlementDate and df_arr[i,5] <= 11
        
        
        ## 出場邏輯
        exitShort = df_arr[i,-3]<0 and df_arr[i,-5] < -2000000  and df_arr[i,-1]>1000000
        exitBuyToCover = df_arr[i,-5] >0 and df_arr[i,-3]>400000   and df_arr[i,-1]>1000000  
        exitCondition = date_arr[i] in settlementDate and df_arr[i,5] >= 11
        
        ## 停利停損邏輯
        if BS == 'B':

            stopLoss = df_arr[i,3] <= df_arr[t,0] * (1-K)
            stopProfit = df_arr[i,3] >= df_arr[t,0] * (1+K)
        elif BS == 'S':

            stopLoss = df_arr[i,3] >= df_arr[t,0] * (1+K)
            stopProfit = df_arr[i,3] <= df_arr[t,0] * (1-K)

    #     if exitCondition == True:
    #         print(f'{time_arr[i]}')

        if BS == None:


            profit_list.append(0)
            profit_fee_list.append(0)
            
            
            if entryLong and entryCondition:

                BS = 'B'
                t = i+1
                buy.append(t)
                entry_list.append(True)
                exit_list.append(False)
                short_entry_list.append(False)
                short_exit_list.append(False)

            elif entrySellShort and entryCondition:

                BS = 'S'
                t = i+1
                sellshort.append(t)
                short_entry_list.append(True)
                entry_list.append(False)
                exit_list.append(False)
                short_exit_list.append(False)
            else:
                entry_list.append(False)
                exit_list.append(False)
                short_entry_list.append(False)
                short_exit_list.append(False)
            
        elif BS == 'B':       
            if exitShort or i == len(df_arr)-2 or exitCondition or stopLoss or stopProfit:
                exit_list.append(True)
                entry_list.append(False)
                short_entry_list.append(False)
                short_exit_list.append(False)
                BS=None
            else:
                exit_list.append(False)
                entry_list.append(False)
                short_entry_list.append(False)
                short_exit_list.append(False)

        elif BS == 'S': 
            if exitBuyToCover or i == len(df_arr)-2 or exitCondition or stopLoss or stopProfit:
                short_exit_list.append(True)
                exit_list.append(False)
                entry_list.append(False)
                short_entry_list.append(False)
                BS=None
            else:
                exit_list.append(False)
                entry_list.append(False)
                short_entry_list.append(False)
                short_exit_list.append(False)
 


#using vectorbt to backtest

traindata= trainData.copy() 
entrydata=pd.DataFrame(entry_list,columns=['entry'],index=trainData.index)
exitdata=pd.DataFrame(exit_list,columns=['exit'] ,index=trainData.index)
shortentrydata=pd.DataFrame(short_entry_list,columns=['short'],index=trainData.index)
shexitentrydata=pd.DataFrame(short_exit_list,columns=['shortexit'], index=trainData.index)
 

traindata=pd.concat([traindata,entrydata,exitdata,shortentrydata,shexitentrydata],axis=1)



pf = vbt.Portfolio.from_signals(traindata['close'], entries=traindata['entry'], exits=traindata['exit'],short_entries =traindata['short'],
    short_exits = traindata['shortexit'],
    direction = 'both', price=traindata['close'],init_cash=3000000, accumulate=True)

print(pf.stats())
pf.plot().show()
print(pf.positions.records_readable)