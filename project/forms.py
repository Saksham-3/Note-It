from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', validators=[DataRequired(), Email()])             
   password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Sign Up')

   def validate_username(self,username):
      user = User.query.filter_by(username = username.data).first()
      if user:
         raise ValidationError('Username is already taken! Please choose another username.')

   def validate_email(self,email):
      user = User.query.filter_by(email= email.data).first()
      if user:
         raise ValidationError('Email is already being used! Please choose another email address.')

class LoginForm(FlaskForm):
   email = StringField('Email', validators=[DataRequired(), Email()])        
   password = PasswordField('Password', validators=[DataRequired()])
   remember = BooleanField('Remember Me')
   submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Information')

    def validate_name(self, name):
        if user.username != current_user.username:
         user = User.query.filter_by(username= user.username).first()

    def validate_email(self, email):
       if email.data != current_user.email:
          user = User.query.filter_by(email=email.data).first()
          if user:
             raise ValidationError('That email addres is already taken!')
          
class BlogForm(FlaskForm):
   title = StringField('Title', validators=[DataRequired()])
   content = TextAreaField('Content', validators=[DataRequired()])
   submit = SubmitField('Post')
