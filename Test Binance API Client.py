import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, plot_heatmaps
from backtesting.test import SMA, GOOG
import datetime as dt
import pandas as pd
from binance.client import Client
from binance.enums import HistoricalKlinesType

API_KEY = "SyWHwZv9BTOiFN3NxJvbTlNjXdRvW9HEQdGJrZp0PFTK4aMekC2tt8d9qRNwUEej"
API_SECRET = "XkryIgFQgZhIg4l77sFfcU6LQjYlklCRqf1Eedo6XJvNJT3rjESgad0gswX8BpZY"
client = Client(API_KEY, API_SECRET)

symbol = "BTCUSDT"
interval="15m"
Client.KLINE_INTERVAL_15MINUTE 
klines = client.get_historical_klines(symbol, interval, "1 Sep,2022",klines_type=HistoricalKlinesType.FUTURES)

data = pd.DataFrame(data = [row[0:5] for row in klines], columns=['open_time','open', 'high', 'low', 'close'],).set_index('open_time')

 # create colums name
data.columns = ['Open', 'High', 'Low', 'Close']
            
# change the timestamp
data.index=pd.to_datetime(data.index + 1, unit="ms")
#data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.open_time]
data=data.sort_index()
data=data.apply(pd.to_numeric,axis=1)
print(data)

#data.to_csv(symbol+'.csv', index = None, header=True)
#convert data to float and plot
#df=data.astype(float)
#df["close"].plot(title = 'DOTUSDT', legend = 'close')

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

bt = Backtest(data, SmaCross,
              cash=1000000, commission=.002,
              exclusive_orders=True)

stats = bt.run()
#print(stats)
print(stats._equity_curve)
bt.plot()


# Walk - forward analysis
def walk_forward(
    strategy, 
    data_full,
    warmup_bars,
    lookback_bars, 
    validation_bars,
    cash=1000000,
    commision=0.002   
    ):

    stats_master = []

    for i in range(lookback_bars + warmup_bars, len(data_full) - validation_bars, validation_bars):
        training_data = data_full.iloc[i-lookback_bars - warmup_bars:i]
        validation_data = data_full.iloc[i-warmup_bars:i+validation_bars]

        bt_training = Backtest(training_data,strategy, cash=cash, commission= commision)
        stats_training = bt.optimize(n1=range(5,10), n2=range(15,30),constraint=lambda p: p.n1 < p.n2,maximize="Profit Factor",return_heatmap=True)

        small_treshold = stats_training._strategy.n1
        large_treshold = stats_training._strategy.n2

        bt_validation = Backtest(validation_data,strategy, cash=cash, commission= commision)
        stats_validation = bt.validation.run(

        )