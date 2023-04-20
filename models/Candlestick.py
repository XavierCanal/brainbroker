from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Candlestick(ABC):
    def __init__(self, start_date: datetime, end_date: datetime, interval: str):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
