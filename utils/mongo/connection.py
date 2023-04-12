import os
from pymongo import MongoClient


class DatabaseConnection:
    __instance = None

    @staticmethod
    def getInstance():
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
        return DatabaseConnection.__instance

    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection.__instance = MongoClient('localhost', 27017)
