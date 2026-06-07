from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

print("MONGODB_URI loaded:", os.getenv("MONGODB_URI"))

#class declaration
class Database: 
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
            cls._client = MongoClient(os.getenv("MONGODB_URI"))
            cls._db = cls._client["favouritebooks"]
        return cls._instance
    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls.get_instance()
        return cls._db