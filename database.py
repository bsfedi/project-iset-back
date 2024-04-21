
from pymongo import MongoClient
from pymongo.database import Database

db: Database = MongoClient(f"mongodb+srv://fedislimen98:iSCEJ0NTLSdGJlZm@cluster0.z6x5lna.mongodb.net/")["app_db"]