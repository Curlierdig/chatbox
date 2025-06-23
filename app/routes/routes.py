from flask import Blueprint, request, jsonify, current_app,render_template
from app.utils.respuesta import procesar_pregunta, buscar_respuesta_directa

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def chatbot():
    pregunta = None
    respuesta = None

    if request.method == "POST":
        pregunta = request.form.get("pregunta")
        if pregunta:
            respuesta = buscar_respuesta_directa(pregunta)

    return render_template("index.html", pregunta=pregunta, respuesta=respuesta)