
import backtrader as bt
from datetime import datetime, timezone

class UnixTimeCSVData(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%dT%H:%M:%S'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
    )

    def _loadline(self, linetokens):
        dt = datetime.fromtimestamp(float(linetokens[0]), timezone.utc)
        linetokens[0] = dt.strftime('%Y-%m-%dT%H:%M:%S')
        if float(linetokens[5]) <= 0:
            linetokens[5] = "1000"
        return super()._loadline(linetokens)

import csv

class ProfitTestStrategy(bt.Strategy):
    def __init__(self):
        self.buy_price = None
        self.bar_executed = None
        self.trades = []

    def next(self):
        bar = len(self)

        if not self.position:
            self.buy_price = self.data.close[0]
            self.buy()
            self.bar_executed = bar
            print(f"📈 BUY SIGNAL at {self.buy_price} on bar {bar}")
        elif bar == self.bar_executed + 3:
            self.sell()
            sell_price = self.data.close[0]
            print(f"📉 SELL at {sell_price} on bar {bar}")
            self.trades.append((self.bar_executed, self.buy_price, bar, sell_price))

    def stop(self):
        # Save trade log to CSV
        with open('mnq_trades.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Buy Bar', 'Buy Price', 'Sell Bar', 'Sell Price'])
            writer.writerows(self.trades)
        print(f"\n✅ Saved {len(self.trades)} trades to mnq_trades.csv")


cerebro = bt.Cerebro()
cerebro.broker.setcash(6700)
cerebro.broker.setcommission(commission=0.5, mult=2.0)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)

data = UnixTimeCSVData(
    dataname='MNQ_chart.csv',
    timeframe=bt.TimeFrame.Minutes,
    compression=5,
    dtformat='%Y-%m-%dT%H:%M:%S',
    openinterest=-1,
    headers=True
)

cerebro.adddata(data)
cerebro.addstrategy(BuySellOnce)

start_val = cerebro.broker.getvalue()
cerebro.run()
end_val = cerebro.broker.getvalue()

print(f"\nStart: ${start_val}")
print(f"End:   ${end_val}")
cerebro.plot(style='candlestick')
