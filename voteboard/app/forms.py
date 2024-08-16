from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from .models import User
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import abort

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=0, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        for c in "}{":
            if c in username.data:
                raise ValidationError('Please use valid characters.')
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
class BoardForm(FlaskForm):
    creator = StringField('Username', validators=[DataRequired()])
    title = TextAreaField('Title', validators=[DataRequired(), Length(min=0, max=30)])
    left = TextAreaField('Left Side', validators=[DataRequired(), Length(min=0, max=30)])
    right = TextAreaField('Right Side', validators=[DataRequired(), Length(min=0, max=30)])
    submit = SubmitField('Board')
