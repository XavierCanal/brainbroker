from enum import Enum


class Restrictions(Enum):
    """Enum for Yahoo data restrictions."""
    ONE_MINUTE = {"days": 7, "key": "1m"}
    TWO_MINUTES = {"days": 60, "key": "2m"}
    FIVE_MINUTES = {"days": 60, "key": "5m"}
    FIFTEEN_MINUTES = {"days": 60, "key": "15m"}
    THIRTY_MINUTES = {"days": 60, "key": "30m"}
    SIXTY_MINUTES = {"days": 730, "key": "60m"}
    NINETY_MINUTES = {"days": 60, "key": "90m"}
    ONE_HOUR = {"days": 100000, "key": "1h"}
    ONE_DAY = {"days": 100000, "key": "1d"}
    ONE_WEEK = {"days": 100000, "key": "1wk"}
    ONE_MONTH = {"days": 100000, "key": "1mo"}
    ONE_YEAR = {"days": 100000, "key": "1y"}
