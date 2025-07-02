# routes/main.py
from flask import Blueprint, request, render_template, session, jsonify
from app.utils.respuesta import buscar_respuesta, buscar_por_categoria
from datetime import datetime
import uuid

main = Blueprint('main', __name__, template_folder='../templates')

# Lista para mantener el historial en memoria (más simple que base de datos)
def get_historial():
    """Obtiene el historial de la sesión actual"""
    if 'historial' not in session:
        session['historial'] = []
    return session['historial']

def agregar_mensaje(pregunta, respuesta):
    """Agrega un mensaje al historial"""
    historial = get_historial()
    mensaje = {
        'id': str(uuid.uuid4()),
        'pregunta': pregunta,
        'respuesta': respuesta,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'fecha': datetime.now().strftime('%Y-%m-%d')
    }
    historial.append(mensaje)
    session['historial'] = historial
    session.permanent = True  # Mantener la sesión
    return mensaje

@main.route("/", methods=["GET", "POST"])
def chatbot():
    """Ruta principal del chatbot"""

    if request.method == "POST":
        pregunta = request.form.get("pregunta", "").strip()
        categoria = request.form.get("categoria", "todas")

        print(f"📝 Pregunta recibida: '{pregunta}'")
        print(f"📂 Categoría seleccionada: '{categoria}'")

        respuesta = None

        if pregunta:
            # Buscar respuesta
            if categoria and categoria != "todas":
                respuesta = buscar_por_categoria(pregunta, categoria)
            else:
                respuesta = buscar_respuesta(pregunta)

            # Si no se encontró respuesta, usar mensaje predeterminado
            if not respuesta:
                print("❌ No se encontró una respuesta adecuada.")
                respuesta = "Lo siento, no encontré una respuesta adecuada."

            # Asegurar que sea texto plano
            if isinstance(respuesta, dict):
                texto_respuesta = respuesta.get("respuesta", "Respuesta vacía")
            else:
                texto_respuesta = str(respuesta)

            print(f"💬 Respuesta generada: '{texto_respuesta[:100]}...'")

            # Agregar al historial
            agregar_mensaje(pregunta, texto_respuesta)

    # Obtener historial para mostrar
    historial = get_historial()

    return render_template("index.html", historial=historial)


@main.route("/limpiar_chat", methods=["POST"])
def limpiar_chat():
    """Limpiar el historial del chat"""
    session['historial'] = []
    return jsonify({"status": "success", "message": "Chat limpiado"})

@main.route("/api/pregunta", methods=["POST"])
def api_pregunta():
    """API endpoint para hacer preguntas (para AJAX)"""
    try:
        data = request.get_json()
        pregunta = data.get("pregunta", "").strip()
        categoria = data.get("categoria", "todas")
        
        if not pregunta:
            return jsonify({"error": "Pregunta requerida"}), 400
        
        # Buscar respuesta
        if categoria and categoria != "todas":
            respuesta = buscar_por_categoria(pregunta, categoria)
        else:
            respuesta = buscar_respuesta(pregunta)
        
        # Agregar al historial
        mensaje = agregar_mensaje(pregunta, respuesta)
        
        return jsonify({
            "success": True,
            "mensaje": mensaje,
            "pregunta": pregunta,
            "respuesta": respuesta
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/historial")
def ver_historial():
    """Ver el historial completo en JSON"""
    return jsonify({
        "historial": get_historial(),
        "total_mensajes": len(get_historial())
    })

@main.route("/estadisticas")
def estadisticas():
    """Mostrar estadísticas básicas"""
    historial = get_historial()
    
    # Contar por categorías (si se guardara)
    stats = {
        "total_preguntas": len(historial),
        "sesion_activa": len(historial) > 0,
        "ultima_pregunta": historial[-1]['timestamp'] if historial else None
    }
    
    return jsonify(stats)