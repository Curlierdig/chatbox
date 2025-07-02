# app/utils/respuesta.py
from fuzzywuzzy import fuzz
from app.database.db import get_database
db= get_database()

def buscar_respuesta(pregunta_usuario):
    """
    Busca la respuesta más similar a la pregunta del usuario en MongoDB
    """
    if not pregunta_usuario or not pregunta_usuario.strip():
        return None
        
    mejor_coincidencia = None
    mejor_puntaje = 0
    umbral_minimo = 60
    
    try:
        # Obtener la colección de MongoDB
        collection = db["respuestas"]
        
        # Obtener todos los documentos
        documentos = list(collection.find())
        
        if not documentos:
            print("No hay datos en la colección")
            return None
        
        print(f"🔍 Buscando en {len(documentos)} registros...")
        
        for doc in documentos:
            try:
                pregunta_bd = doc.get('pregunta', '')
                respuesta = doc.get('respuesta', '')
                categoria = doc.get('categoria', 'general')
                
                if not pregunta_bd or not respuesta:
                    continue
                    
                # Calcular similitud
                puntaje = fuzz.ratio(pregunta_usuario.lower().strip(), pregunta_bd.lower().strip())
                
                print(f"'{pregunta_bd}' -> Puntaje: {puntaje}")
                
                if puntaje > mejor_puntaje and puntaje >= umbral_minimo:
                    mejor_puntaje = puntaje
                    mejor_coincidencia = {
                        'id': str(doc.get('_id', '')),
                        'pregunta': pregunta_bd,
                        'respuesta': respuesta,
                        'categoria': categoria,
                        'puntaje': puntaje
                    }
            except Exception as e:
                print(f"Error procesando documento: {e}")
                continue
        
        if mejor_coincidencia:
            print(f"✅ Mejor coincidencia encontrada: {mejor_coincidencia['pregunta']} (Puntaje: {mejor_puntaje})")
        else:
            print(f"❌ No se encontró coincidencia con puntaje >= {umbral_minimo}")
            
        return mejor_coincidencia
        
    except Exception as e:
        return None

def buscar_por_categoria(pregunta, categoria):
    """
    Busca una respuesta dentro de una categoría específica usando coincidencia difusa.
    """
    try:
        collection = db.get_collection()

        # Buscar documentos por categoría
        documentos = list(collection.find({"categoria": categoria}))

        preguntas_respuestas = []
        for doc in documentos:
            p = doc.get('pregunta', '')
            r = doc.get('respuesta', '')

            if p and r:
                preguntas_respuestas.append({
                    'pregunta': p,
                    'respuesta': r
                })

        # Comparar la pregunta con las existentes usando fuzzy matching
        if preguntas_respuestas:
            from rapidfuzz import fuzz, process
            coincidencia, score, match = process.extractOne(
                pregunta,
                [item['pregunta'] for item in preguntas_respuestas],
                scorer=fuzz.partial_ratio
            )

            for item in preguntas_respuestas:
                if item['pregunta'] == coincidencia:
                    return item['respuesta']

        return None

    except Exception as e:
        return None


def obtener_categorias():
    """
    Obtiene todas las categorías disponibles de MongoDB
    """
    try:
        collection = db.get_collection()
        
        # Obtener categorías únicas
        categorias = collection.distinct("categoria")
        
        return categorias
        
    except Exception as e:
        return []