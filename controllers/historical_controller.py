
from utils.mongo.historical import get
import logging


def get_company(name):
    logging.info("Getting company %s", name)
    return get(name)
