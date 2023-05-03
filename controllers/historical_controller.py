from utils.mongo import historical
import logging


def get_company(name):
    logging.info(" Getting company %s" % name)
    return historical.get(name)


def get_company_interval(name, interval):
    logging.info(" Getting company %s with interval %s" % (name, interval))
    return historical.get_custom_interval(name, interval)


def get_companies_custom_filter(args):
    logging.info("Getting companies with custom filter %s" % args)
