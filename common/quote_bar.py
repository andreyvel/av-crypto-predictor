
class QuoteBar:
    date: str
    open: float
    high: float
    low: float
    close: float
    vol: float

    def __init__(self, json_row=None) -> None:
        if json_row:
            self._load(json_row)

    def _load(self, json_row):
        # {'date': '2023-07-12T01:05', 'high': 27778.76, 'vol': 0, 'low': 27707.3, 'close': 27740.01, 'open': 27715.68}
        self.date = json_row["date"]
        self.open = json_row["open"]
        self.high = json_row["high"]
        self.low = json_row["low"]
        self.close = json_row["close"]
        self.vol = json_row["vol"]
