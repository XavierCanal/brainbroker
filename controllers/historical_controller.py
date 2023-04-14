
from utils.mongo.historical import get
import logging


def get_company(name):
    logging.info(" Getting company %s" % name)
    return get(name)


def get_companies_custom_filter(args):
    logging.info("Getting companies with custom filter %s" % args)
