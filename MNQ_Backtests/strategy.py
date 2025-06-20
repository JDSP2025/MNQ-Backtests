import backtrader as bt

class ProfitTestStrategy(bt.Strategy):
    def __init__(self):
        self.order = None
        self.bar_executed = None

    def next(self):
        print(f"Bar {len(self)}, Close: {self.data.close[0]}")
        if not self.position:
            self.order = self.buy()
            self.bar_executed = len(self)
            print(f"📈 BUY SIGNAL at {self.data.close[0]} on bar {self.bar_executed}")
        elif len(self) >= self.bar_executed + 3:
            self.order = self.sell()
            print(f"💰 SELL at {self.data.close[0]} on bar {len(self)}")
