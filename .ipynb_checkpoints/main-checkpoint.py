from backtesting import Backtest, Strategy
from backtesting.lib import crossover, plot_heatmaps

from backtesting.test import SMA, GOOG


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


bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)

#output = bt.run()

output, heatmap = bt.optimize(n1=range(5,15), n2=range(10,40),constraint=lambda p: p.n1 < p.n2,maximize="Sharpe Ratio",return_heatmap=True)

print(heatmap)


#bt.plot()
#plot_heatmaps(heatmap,agg="mean")

#test