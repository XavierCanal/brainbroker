class Ticker:
    def __init__(self, ticker, price=None, change=None,
                 change_percent=None, volume=None, market_cap=None,
                 last_updated=None):
        self.ticker = ticker
        self.price = price
        self.change = change
        self.change_percent = change_percent
        self.volume = volume
        self.market_cap = market_cap
        self.last_updated = last_updated

    def __repr__(self):
        return f"{self.ticker} {self.price} {self.change} {self.change_percent} {self.volume} {self.market_cap} {self.last_updated}"

    def __str__(self):
        return f"{self.ticker} {self.price} {self.change} {self.change_percent} {self.volume} {self.market_cap} {self.last_updated}"