from pymongo import MongoClient

client = MongoClient("tu_uri_de_mongodb")
db = client["chatbot"]

temas = {
    "matematicas": [],
    "historia": [],
}

for nombre, subtemas in temas.items():
    db.temas.insert_one({"nombre": nombre, "subtemas": subtemas})
