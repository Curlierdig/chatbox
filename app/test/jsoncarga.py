from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client["chatbox"]

temas = {
    "matematicas": ["fracciones", "algebra", "trigonometria"]
}

respuestas = [
    {"tema": "matematicas", "subtema": "fracciones", "pregunta": "¿Qué es una fracción?", "respuesta": "Una fracción representa una parte de un todo."},
    {"tema": "matematicas", "subtema": "algebra", "pregunta": "¿Qué es una ecuación?", "respuesta": "Una ecuación es una igualdad que contiene incógnitas."},
    {"tema": "matematicas", "subtema": "trigonometria", "pregunta": "¿Qué es el seno?", "respuesta": "Es la razón entre el cateto opuesto y la hipotenusa."}
]

for tema, subs in temas.items():
    db.temas.insert_one({"nombre": tema, "subtemas": subs})

db.respuestas.insert_many(respuestas)
