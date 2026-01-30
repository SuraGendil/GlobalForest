from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]
    return db

def get_collection(collection_name: str = None):
    db = get_db_connection()
    if collection_name:
        return db[collection_name]
    return db[os.getenv("COLLECTION_NAME")]