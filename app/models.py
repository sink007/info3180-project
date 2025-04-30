from . import db
from werkzeug.security import generate_password_hash

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # auto-increment added
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    photo = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime)

    def __init__(self, username, password, name, email, photo, date_joined):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.name = name
        self.email = email
        self.photo = photo
        self.date_joined = date_joined

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # auto-increment added
    user_id_fk = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    description = db.Column(db.String(255))
    parish = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    sex = db.Column(db.String(20))
    race = db.Column(db.String(80))
    birth_year = db.Column(db.Integer)
    height = db.Column(db.Float)
    fav_cuisine = db.Column(db.String(80))
    fav_colour = db.Column(db.String(50))
    fav_school_subject = db.Column(db.String(100))
    political = db.Column(db.Boolean)
    religious = db.Column(db.Boolean)
    family_oriented = db.Column(db.Boolean)

    def __init__(self, user_id_fk, description, parish, biography, sex, race, birth_year, height, 
                 fav_cuisine, fav_colour, fav_school_subject, political, religious, family_oriented):
        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<UserProfile %r>' % (self.user_id_fk)
    

class Favourite(db.Model):
    __tablename__ = 'favourite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # auto-increment added
    user_id_fk = db.Column(db.Integer, nullable=False)
    fav_user_id_fk = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id_fk, fav_user_id_fk):
        self.user_id_fk = user_id_fk
        self.fav_user_id_fk = fav_user_id_fk

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Favourite %r>' % (self.fav_user_id_fk)
