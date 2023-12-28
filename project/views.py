from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Note, Post, User
from . import db
import json
from .forms import UpdateAccount, BlogForm
import secrets
from PIL import Image
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user = current_user
    notes = Note.query.filter_by(user_id=user.id).order_by(Note.date.asc())
    return render_template("home.html", user = current_user, notes = notes)

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
            return redirect(url_for('views.home'))
        except:
            db.session.commit()
            flash("Error! Try again.", "error")
            return render_template("edit.html", form=form, note_update = note_update)
    else:
        return render_template("edit.html", form=form, note_update = note_update, user = current_user)
    
@views.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        post = Post(title= form.title.data, content= form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('views.blog'))
    return render_template("add_post.html", user=current_user, title="New Post", form= form, legend='New Post')

@views.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, user= current_user)

@views.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('views.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("add_post.html", user=current_user, title="Update Post", form= form, legend='Update Post')

@views.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('views.blog'))
    
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

@views.route('/blog', methods=['GET', 'POST'])
def blog():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('blog.html', user= current_user, posts= posts)

@views.route('/user/<string:username>', methods=['GET', 'POST'])
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())

    return render_template('user_posts.html', user=user, posts= posts)




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

