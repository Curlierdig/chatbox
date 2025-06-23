from flask import Flask
from flask_cors import CORS
from app.database.db import get_database
from app.routes.routes import main

def create_app():
    app = Flask(__name__)
    CORS(app)
    get_database()
    app.register_blueprint(main)
    return app
