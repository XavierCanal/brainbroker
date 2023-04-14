import json
import os
import logging
from pymongo import MongoClient

from models.Stock import Stock
from utils.mongo.connection import DatabaseConnection

# Connect to MongoDB
db_client = DatabaseConnection.getInstance()

schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'stock.json')

# Load validation schema from JSON file
with open(schema_path) as f:
    schema = json.load(f)


def aggregateCompany(company, data_dict, st: Stock):
    try:
        logging.info(" Updating company %s", company)
        col = db_client.BrainBroker.historical;
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            # If it exists, we update the document
            col.update_one({"index": company}, {"$push": {"data": {"info": st.toJSON(), "candlesticks": data_dict}}})
            return "Updated company %s", company
        else:
            # If it doesn't exist, we create a new document
            col.insert_one({"index": company, "data": [{"info": st.toJSON(), "candlesticks": data_dict}]})
            return "Created company %s", company
    except Exception:
        logging.error(" Failed to update company", exc_info=True)
        return "Failed to update company %s", company


def get(name):
    # Get the collection
    try:
        col = db_client.BrainBroker.historical;
        # First we check if the collection exists with the index name inside the document
        data = col.find_one({"index": name})
        if data:
            return {"ticket": data["index"], "data": data["data"]}
        else:
            return "Company not found"
    except Exception:
        logging.error("Failed to get company", exc_info=True)
        return "Failed to get company"


def stock_info_already_exists(company, st: Stock):
    try:
        col = db_client.BrainBroker.historical;
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            # If it exists, we update the document
            for stock in col.find_one({"index": company})["data"]:
                if stock["info"]["start_date"] == st.start_date and stock["info"]["end_date"] == st.end_date \
                        and stock["info"]["interval"] == st.interval:
                    return True
            return False
        else:
            return False
    except Exception:
        logging.error(" Failed to update company", exc_info=True)
        return False
