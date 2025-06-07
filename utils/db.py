# utils/db.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not set in environment variables.")
    return MongoClient(mongo_uri)

def get_db():
    client = get_mongo_client()
    db_name = os.getenv("MONGO_DB")
    if not db_name:
        raise ValueError("MONGO_DB not set in environment variables.")
    return client[db_name]

def get_collection(collection_name):
    db = get_db()
    return db[collection_name]
