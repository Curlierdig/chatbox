from rapidfuzz import fuzz
from app.database.db import get_database

db = get_database()

def buscar_respuesta_directa(pregunta_usuario: str):
    respuestas = db.respuestas.find()
    
    mejor_score = 0
    mejor_respuesta = "Lo siento, no encontré una respuesta adecuada."

    for doc in respuestas:
        score = fuzz.partial_ratio(pregunta_usuario.lower(), doc["pregunta"].lower())
        if score > mejor_score:
            mejor_score = score
            mejor_respuesta = doc["respuesta"]

    return mejor_respuesta

