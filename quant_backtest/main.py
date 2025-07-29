from AlgorithmImports import *

class MovingAverageCrossover(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2022, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(100000)

        self.symbol = self.AddEquity("AMZN", Resolution.Daily).Symbol

        self.fast_period = 10
        self.slow_period = 30

        self.fast = self.SMA(self.symbol, self.fast_period, Resolution.Daily)
        self.slow = self.SMA(self.symbol, self.slow_period, Resolution.Daily)

        self.RegisterIndicator(self.symbol, self.fast, Resolution.Daily)
        self.RegisterIndicator(self.symbol, self.slow, Resolution.Daily)

        self.last_action = None

    def OnData(self, data):
        if not self.fast.IsReady or not self.slow.IsReady:
            return

        price = self.Securities[self.symbol].Price

        if self.fast.Current.Value > self.slow.Current.Value and self.last_action != "buy":
            self.SetHoldings(self.symbol, 1)
            self.Plot("Trade Plot", "Buy", price)
            self.last_action = "buy"

        elif self.fast.Current.Value < self.slow.Current.Value and self.last_action != "sell":
            self.Liquidate(self.symbol)
            self.Plot("Trade Plot", "Sell", price)
            self.last_action = "sell"

