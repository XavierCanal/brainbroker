import json
import os
import logging
from pymongo import MongoClient
from utils.mongo.connection import DatabaseConnection

# Connect to MongoDB
db_client = DatabaseConnection.getInstance()

schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'stock.json')

# Load validation schema from JSON file
with open(schema_path) as f:
    schema = json.load(f)


def aggregateCompany(company, data_dict):
    try:
        logging.info("Updating company %s", company)
        col = db_client.BrainBroker.historical;
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            print("if")
            # If it exists, we update the document
            col.update_one({"index": company}, {"$set": {"data": data_dict}})
            return "Success, updated"
        else:
            print("else")
            # If it doesn't exist, we create a new document
            col.insert_one({"index": company, "data": data_dict})
            return "Success, created"
    except Exception:
        logging.error("Failed to update company", exc_info=True)
        return "Failed to update company"


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
