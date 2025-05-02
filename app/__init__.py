from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)

# 🔐 Allow secure cookies for cross-site frontend/backend
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

csrf = CSRFProtect()
csrf.init_app(app)

# Allow CORS with cookies for your frontend
CORS(app, origins=["https://info3180-project-1.onrender.com"], supports_credentials=True)

app.config.from_object(Config)
db = SQLAlchemy(app)

from .models import Users, Profile, Favourite
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from app import views
