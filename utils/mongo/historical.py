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
        col = db_client.BrainBroker.historical
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            # If it exists, we update the document
            if stock_info_already_exists(company, st) and st.interval == "1h" or st.interval == "1m":
                logging.info(" Pushing new elements in %s", company)
                col.update_one({"index": company, "data.info.interval": st.toJSON().get("interval")},
                               {"$push": {"data.$.candlesticks": {"$each": data_dict}}})
            else:
                col.update_one({"index": company},
                               {"$push": {"data": {"info": st.toJSON(), "candlesticks": data_dict}}})
            return "Updated company %s", company
        else:
            # If it doesn't exist, we create a new document
            col.insert_one({"index": company, "data": [{"info": st.toJSON(), "candlesticks": data_dict}]})
            return "Created company %s", company
    except Exception as e:
        logging.error(" Failed to update company:" + str(e), exc_info=True)
        return False


def aggregateCompanyCollection(company, data_dict, st: Stock):
    try:
        logging.info(" Updating company %s", company)
        col = db_client.BrainBroker["historical_" + company]
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            """ 
            If we find one or more, we check if any of them candlesticks has less than 40000 elements, if it has, we update it
            If it doesn't have any with less than 40000 elements, we create a new document
            """
            cursor = col.find({})
            for document in cursor:
                doc_id = document["_id"]
                if document["completed"] is False:
                    if len(document["data"][0]["candlesticks"]) < 40000:
                        logging.info(" Pushing new elements in %s", company)
                        # Now we push in the document that has less than 40000 elements

                        col.update_one({"_id": doc_id}, {"$push": {"data.0.candlesticks": {"$each": data_dict}}})
                        return "Updated company %s", company
                    else:
                        # We change document["completed"] to True
                        col.update_one({"_id": doc_id}, {"$set": {"completed": True}})

            else:
                col.insert_one(
                    {"index": company, "completed": False, "data": [{"info": st.toJSON(), "candlesticks": data_dict}]})
            return "Updated company %s", company
        else:
            # If it doesn't exist, we create a new document
            col.insert_one({"index": company, "data": [{"info": st.toJSON(), "candlesticks": data_dict}]})
            return "Created company %s", company

    except Exception as e:
        logging.error(" Failed to update company:" + str(e), exc_info=True)
        return False


def update_completed_status(company):
    try:
        logging.info(" Updating company %s", company)
        col = db_client.BrainBroker["historical_" + company]
        # First we check if the collection exists with the index name inside the document
        if col.find_one({"index": company}):
            """ 
            If we find one or more, we check if any of them candlesticks has less than 40000 elements, if it has, we update it
            If it doesn't have any with less than 40000 elements, we create a new document
            """
            logging.info(" Updating completed status in %s", company)
            cursor = col.find({})
            for document in cursor:
                doc_id = document["_id"]
                if document.get("completed") is None:
                    print("None")
                    col.update_one({"_id": doc_id}, {"$set": {"completed": False}})
                if document.get("completed") is False or document.get("completed"):
                    print("False or exists")
                    if len(document["data"][0]["candlesticks"]) < 40000:
                        print("Less than 40000")
                        logging.info(" Pushing new elements in %s", company)
                        # Now we push in the document that has less than 40000 elements

                        col.update_one({"_id": doc_id}, {"$set": {"completed": True}})
                        return "Updated company %s", company
            else:
                return "Updated company %s", company

    except Exception as e:
        logging.error(" Failed to update company:" + str(e), exc_info=True)
        return False


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
                if stock["info"]["start_date"].strftime("%Y-%m-%d") == st.start_date.strftime("%Y-%m-%d") \
                        and stock["info"]["end_date"].strftime("%Y-%m-%d") == st.end_date.strftime("%Y-%m-%d") \
                        and stock["info"]["interval"] == st.interval:
                    return True
            return False
        else:
            return False
    except Exception:
        logging.error(" Failed to update company", exc_info=True)
        return False
