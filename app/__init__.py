from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS  # ✅ CORS import
from .config import Config

# Initialize app and extensions
app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

# ✅ Enable CORS for your frontend URL on Render
CORS(app, origins=["https://info3180-project-1.onrender.com"], supports_credentials=True)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader callback
from .models import Users, Profile, Favourite

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Import views after app setup
from app import views
