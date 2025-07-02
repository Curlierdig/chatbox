from flask import Flask
from app.routes.routes import main
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Iniciando Chatbot Educativo...")
    print("📡 Servidor disponible en: http://localhost:5000")
    app.run(debug=True)
