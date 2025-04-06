# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField,  IntegerField, FloatField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Optional, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    name= StringField('Username', validators=[InputRequired()])
    email= StringField('Username', validators=[InputRequired()])
    photo = FileField('Photo',validators=[FileRequired(),FileAllowed(['jpg','png', 'jpeg'],'Images only!')])

class ProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    parish = StringField('Parish', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    race = StringField('Race', validators=[DataRequired()])
    birth_year = IntegerField('Birth Year', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    height = FloatField('Height (inches)', validators=[DataRequired(), NumberRange(min=24, max=96)])
    fav_cuisine = StringField('Favourite Cuisine', validators=[DataRequired()])
    fav_colour = StringField('Favourite Colour', validators=[DataRequired()])
    fav_school_subject = StringField('Favourite School Subject', validators=[DataRequired()])
    political = BooleanField('Political', default=False)
    religious = BooleanField('Religious', default=False)
    family_oriented = BooleanField('Family Oriented', default=False)

class SearchForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    birth_year = IntegerField('Birth Year', validators=[Optional()])
    sex = SelectField('Sex', choices=[('', 'Any'), ('Male', 'Male'), ('Female', 'Female')], validators=[Optional()])
    race = StringField('Race', validators=[Optional()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])