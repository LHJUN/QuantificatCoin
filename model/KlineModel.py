class KlineModel:
    def __init__(self, timestamp, open, high, low, close, volume, currency_volume):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.currency_volume = currency_volume
