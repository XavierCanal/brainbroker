from datetime import datetime


from models.Candlestick import Candlestick


class Symbol(Candlestick):
    def __init__(self, name: str, start_date: datetime=None, end_date: datetime=None, interval: str=None):
        super().__init__(start_date, end_date, interval)
        self.name = name
        if start_date is None:
            self.start_date = "1 Jan 1900"
        if end_date is None:
            self.end_date = datetime.now().strftime("%d %b %Y %H:%M:%S")
        self.interval = interval

    def __str__(self):
        return self.name + " " + self.value


