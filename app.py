import datetime as dt
import pandas as pd
import pandas_datareader as web
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, EURUSD, GOOG


class MySMAStrategy(Strategy):

        def init(self):
                price = self.data.Close
                self.ma1 = self.I(SMA, price, 10)
                self.ma2 = self.I(SMA, price, 20)
                                  
        def next(self):
                if crossover(self.ma1, self.ma2):
                    self.buy()
                elif crossover(self.ma2, self.ma1):
                    self.sell()
start = dt.datetime(2020,1,1)
end = dt.datetime(2022,1,1)

#data = web.DataReader("GOOG","yahoo",start,end)
#data = web.data.get_data_yahoo("GOOGL",start,end)

#data = pd.read_csv(r"C:\Users\PC1\Downloads\BTCUSDT-30m-2023-08.csv", usecols=[0,1,2,3,4])
#data["open_time"]=pd.to_datetime(data["open_time"],unit="ms")
#data.columns = ["Date","Open","High","Low","Close"]
#data.set_index("Date", inplace=True)

#backtest = Backtest(data, MySMAStrategy, commission=0.002, exclusive_orders=True)

backtest = Backtest(EURUSD, MySMAStrategy, commission=.002, exclusive_orders=True)
stats = backtest.run()
print(stats)
backtest.plot()