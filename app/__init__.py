from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import Users, Profile, Favourite
from app import views

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_folder, path)

    if path != "" and os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(static_folder, path)

    return send_from_directory(static_folder, 'index.html')