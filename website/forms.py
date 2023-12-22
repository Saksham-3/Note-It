from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from flask_login import current_user
import email_validator



class UpdateAccount(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update Information')

    def validate_name(self, name):
        if user.first_name != current_user.first_name:
         user = User.query.filter_by(first_name= user.first_name).first()

    def validate_email(self, email):
       if email.data != current_user.email:
          user = User.query.filter_by(email=email.data).first()
          if user:
             raise ValidationError('That email addres is already taken!')