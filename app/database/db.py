from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_database():
    load_dotenv()

    MONGO_USER = os.environ.get("DB_USER")
    MONGO_PASSWORD = os.environ.get("DB_PASSWORD")
    MONGO_CONNECTION_TYPE = os.environ.get("DB_CONNECTION")
    MONGO_CLUSTER = os.environ.get("DB_CLUSTER")
    DB_NAME = os.environ.get("DB_NAME")

    try:
        match MONGO_CONNECTION_TYPE:
            case "local":
                URI = "mongodb://localhost:27017/"
            case "cloud":
                URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}.mongodb.net/?retryWrites=true&w=majority"

        client = MongoClient(URI)
        return client[DB_NAME]

    except Exception as e:
        print(f"Error en la conexión de MongoDB: {e}")
        return None
