from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import talib as ta
import os
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys

user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/dirac-backtest-system")

save_dir = f'{user_home_path}/dirac-backtest-system/data_center/backtesting_result'
Strategy_class = 'Rsi1'

def optim_func(series): #example
    if series["# Trades"] < 10:
        return -1 
        # ? dun know
        # let discuss this tmr/today
    return series["Equity Final [$]"] / series['Exposure Time [%]']

class RsiOscillatorStrategy(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    def init(self):
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window )
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

bt = Backtest(GOOG, RsiOscillatorStrategy, cash=100000)

optim, heatmap = bt.optimize(
    upper_bound = range(55,85,1),
    lower_bound = range(10,45,1),
    rsi_window =  14,
    maximize = 'Return [%]',
    constraint = lambda x:x.upper_bound > x.lower_bound,
    return_heatmap = True
    # max_tries = 100 #use limitation to see the differnces
    )

print(optim)
bt.plot()
   
hm = heatmap.groupby(['upper_bound','lower_bound']).mean().unstack()
sns.heatmap(hm)
plt.show()
# plot_heatmaps(heatmap)

# saving data part
os.makedirs(save_dir + f"/{Strategy_class}", exist_ok=True)
hm.to_csv(save_dir + f"/{Strategy_class}/{Strategy_class}_hm.csv")

# there is a problem, we cannot end the code



 