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
