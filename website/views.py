from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
from .forms import UpdateAccount

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
    
@views.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', user= current_user, form=form)
