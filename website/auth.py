from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm
import email_validator

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', category='error')
    return render_template("login.html", user = current_user, form=form)
    
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
        
    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             flash('Logged in successfully!', category='success')
    #             login_user(user, remember=True)
    #             return redirect(url_for('views.home'))
    #         else:
    #             flash('Incorrect password or email.', category='error')
    #     else:
    #         flash('Email does not exist.', category='error')

    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out!")
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data, email= form.email.data, password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()            
        flash('Your account was successfully created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template("sign_up.html", user = current_user, title = 'Sign Up', form=form)
          


