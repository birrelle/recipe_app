from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI")  
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
recipes_collection = db["recipes"]
collections_collection = db["collections"]

recipes_collection.create_index([('ingredients', 1)], sparse=True, background=True)
users_collection.create_index([('username', 1)], unique=True)

def get_db():
    """Return the database instance."""
    return db

def get_collection(collection_name: str):
    """Return the specified collection from the database."""
    return db[collection_name]