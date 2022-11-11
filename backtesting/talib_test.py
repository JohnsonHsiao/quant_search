import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest,Strategy
from backtesting.lib import crossover

class SMAcross(Strategy):
    n1 = 50
    n2 = 100
    def init(self):
        close = self.data.Close #get data from close price
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
            #if len(self.trade)>0:
            #    self.trades[0].close
            #不做sell

df = yf.download('BTC-USD ',start='2020-01-01')

bt = Backtest(df, SMAcross, cash=1000000, commission=0.002, exclusive_orders = True)

output = bt.run()
output
bt.plot()

optim = bt.optimize(n1 = range(50,160,10),
                    n2 = range(50,160,10),
                    constraint = lambda x: x.n2 - x.n1 > 20,
                    maximize = 'Return [%]')
# u can use any data u want it maximize
bt.plot()

optim

