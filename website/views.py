from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
from .forms import UpdateAccount
import secrets
from PIL import Image
import os
from sqlalchemy.sql import text

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route('/delete-note', methods= ['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
            
    return render_template("home.html", user = current_user)

@views.route('/add_note', methods = ['GET', 'POST'])
@login_required
def addNote():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1: 
            flash('Note is too short!', category= 'error')
        else:
            new_note = Note(data=note, user_id= current_user.id)
            db.session.add(new_note)
            db.session.commit() 
            flash('Note added!', category= 'success')
            return redirect(url_for('views.home'))
    return render_template("add_note.html", user=current_user)

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
def item(id):
    form = Note()
    note_update = Note.query.get_or_404(id)
    if request.method == "POST":
        note_update.data = request.form['note']
        try:
            db.session.commit()
            flash("Note Successfully Updated!", "success")
            return render_template("home.html", form=form, note_update = note_update, user = current_user)
        except:
            db.session.commit()
            flash("Error! Try again.", "error")
            return render_template("edit.html", form=form, note_update = note_update)
    else:
        return render_template("edit.html", form=form, note_update = note_update, user = current_user)
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(views.root_path, 'static/pfp', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    prev_picture = os.path.join(views.root_path, 'static/pfp', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.png':
        os.remove(prev_picture)
    
    return picture_fn 


@views.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='pfp/' + current_user.image_file)
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html',image_file= image_file , user= current_user, form=form)

@views.route('/sort-note', methods= ['GET'])
@login_required
def sort_note():
    print(current_user.id)
    sql_query  = "SELECT note.data as mydata FROM note INNER JOIN user ON note.user_id = user.id WHERE note.user_id = :current_user ORDER BY note.date DESC"
    cursor = db.session.execute(text(sql_query),{'current_user' : current_user.id})
    notess = cursor.fetchall()
    notee = []
    for i in range(len(notess)):
        notee.append(notess[i][i-1])
        user = current_user
    return render_template('home.html', user= current_user)
    # return result
    # note = json.loads(request.data)
    # noteId = note['noteId']
    # note = Note.query.get(noteId)
    # if note:
    #     if note.user_id == current_user.id:
    #         db.session.delete(note)
    #         db.session.commit()
    # return jsonify({note})
    
            
    # return render_template("home.html", user = current_user)

# @staticmethod
# def find_handymans(query):
#     search_job = str(query)

#     sql_query =text("SELECT first_name,last_name, email, user_type,  phone, image, diplome, latitude, longitude, description FROM users, jobs WHERE users.id_job = jobs.id AND jobs.description = :x ")
#     cursor = db.session.execute(sql_query,{'x' : search_job})

#     # Returns a list of product tuples
#     return cursor.fetchall()