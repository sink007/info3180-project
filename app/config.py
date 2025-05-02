import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret')
