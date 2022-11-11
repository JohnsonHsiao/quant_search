from turtle import filling
import vectorbt as vbt
import numpy as np
import datetime

import sys
from pathlib import Path



# how to customize our own indicators?

#first and foremost ,define indicators and logic
#second,  because there is no such a indicator in vecorbt, we need to put the indicator into vectorbt's factory in order to process
#third, we have to define the parameter which could be an interval of numbers
#furthermore, define logic adapted to vectorbt
#finally ,put the all stuff into vbt.Portfolio.from_signals


#get data
#it is now!!!!!!
end_date= datetime.datetime.now()
start_date=end_date - datetime.timedelta(days=20)

btc_price= vbt.YFData.download(['BTC-USD'],interval='1m',statr=start_date,end=end_date,missing_index='drop').get('Close')

#setting up the indicators factory

def seld_defined_indicator(close,top_1,down_1,top_2,down_2,rsi_window_1,rsi_window_2):

    #resample the dataframe
    close=close['Close']
    close_1=close.resample('1min').last()
  
    close_2 = close.resample('5min').last()
    #calculate indicators and add to data frame

    rsi_1=vbt.RSI.run(close_1,rsi_window_1).rsi
    rsi_1,_=rsi_1.align(close,broadcast_axis=0,method='ffill',join='right')  # what is align?
    rsi_1=rsi_1.to_numpy() #why?
    rsi_2 = vbt.RSI.run(close_2, window=rsi_window_2).rsi
    rsi_2, _ = rsi_2.align(close, broadcast_axis=0,method='ffill', join='right')
    rsi_2 = rsi_2.to_numpy()

    #calculate signals (logic)

    signal=np.where(  (rsi_1<down_1)  &  (rsi_2>down_2),1 ,0 )
    signal=np.where(  (rsi_2<top_1)  &  (rsi_2>down_2),-1 ,signal)

    #return signals in numpy anaray?

    return signal



# setting up indicator factory
ind = vbt.IndicatorFactory(
    class_name='Combination',
    short_name='comb',
    input_names=['Close'],
    param_names=['top_1', 'down_1', 'top_2',
                 'down_2', 'rsi_window_1', 'rsi_window_2'],
    output_names=['value']).from_apply_func(seld_defined_indicator,
    top_1=60, down_1=15,   # values here are not important!!!! just give a random number
    top_2=60, down_2=20,
    rsi_window_1=7, rsi_window_2=7,
    keep_pd=True
)



#define strategy using indicaor factory

res = ind.run(btc_price,top_1=np.arange(60,90,10),
                        down_1=np.arange(10,40,10),
                        top_2=np.arange(60,90,10),
                        down_2=np.arange(10,40,10),
                        rsi_window_1=np.arange(10,20,5),
                        rsi_window_2=np.arange(10,20,5),
                        param_product=True)

# define trading logic

entries=res.value_crossed_above(0)
exits=res.value_crossed_below(0)

entries_short=res.value_crossed_below(0)
exits_short=res.value_crossed_above(0)


#calculate portfolio

pf=vbt.Portfolio.from_signals(close=btc_price,
                              entries=entries,
                              exits=exits,
                              short_entries=entries_short,
                              short_exits=exits_short,
                              fees=0.001  )        
                                
                            
#print the best parameters

returns=pf.total_return()

print(returns.max())
print(returns.idxmax())

# analyse parameters of seld defined indicators to understand profit zone

#super cool
fig= returns.vbt.volume(x_level='comb_top_1',y_level='comb_down_1',z_level='comb_rsi_window_1',height=400,width=1700)

fig.show()

#using the optimized parameters

res = ind.run(
    btc_price,
    top_1=returns.idxmax()[0],
    down_1=returns.idxmax()[1],
    top_2=returns.idxmax()[2],
    down_2=returns.idxmax()[3],
    rsi_window_1=returns.idxmax()[4],
    rsi_window_2=returns.idxmax()[5],
    param_product=True
)
entries = res.value_crossed_above(0)
exits = res.value_crossed_below(0)

entries_short = res.value_crossed_below(0)
exits_short = res.value_crossed_above(0)
pf = vbt.Portfolio.from_signals(
    close=btc_price,
    entries=entries,
    exits=exits,
    short_entries=entries_short,
    short_exits=exits_short,
    fees=0.001
)
print(pf.stats())
pf.plots().show()











