from pymongo import MongoClient

def get_database():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client["chatbot"]  # Reemplaza "chatbot" por el nombre real de tu base
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        return None
