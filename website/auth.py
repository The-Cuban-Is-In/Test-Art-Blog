import secrets, os
from website.models import Admin, Blog, Post
from . import bcrypt, db, app
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from PIL import Image
from website.forms import LoginForm, NewPhotoPost, NewPost, RegisterForm

auth = Blueprint('auth', __name__)  


@auth.route('/login', methods = ['GET', 'POST'])       # -- LOGIN PAGE
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm()
    if request.method == 'POST':
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            flash('Logged in Successfully', category='success')
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('auth.admin'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')      # -- LOGOUT
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin')       # -- ADMIN HOME PAGE
@login_required
def admin():
    return render_template('adminHome.html')

@auth.route('/post/new', methods=['POST', 'GET'])       # -- NEW TEXT POST
def newPost():
    form = NewPost()
    if request.method == 'POST':
        post = Blog(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.blog'))
    return render_template('new_text_post.html', title= 'New Post', form=form)

def savePicture(formPicture):       # --SAVES PHOTO
    try:
        randomHex = secrets.token_hex(8)
        _, fExt = os.path.splitext(formPicture.filename)
        pictureFileName = f'{randomHex}{fExt}'
        picturePath = os.path.join(app.root_path, 'static/posted_images', pictureFileName)
        formPicture.save(picturePath)
        return pictureFileName
    except Exception:
        pass

@auth.route('/post/new-photo', methods=['POST', 'GET'])     # -- SET PHOTO POST
def photoPost():
    form = NewPhotoPost()
    if request.method == 'POST':
        if form.photo.data:
            pictureFile = savePicture(form.photo.data)
            post = Post(title=form.title.data, content=form.content.data, imageFile=pictureFile, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template('new_image_post.html', title= 'New Post', form=form)

@auth.route('/post/delete/<int:id>')        # --DELETE POST ROUTE
def deletePost(id):
    try:
        postToDelete = Post.query.get(id)
        db.session.delete(postToDelete)
        db.session.commit()
        data = Post.query.all()
        return render_template('home.html', post=data)      
    except:
        flash('Somthing went wrong while deleting your post.', 'danger')
        data = Post.query.all()
        print('except delete')
        return redirect(url_for('views.home'))

# @auth.route('/register', methods = ['GET', 'POST'])    # -- REGISTRATION
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('views.home'))

#     form = RegisterForm()
#     if request.method == 'POST':
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         admin = Admin(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_password)
#         db.session.add(admin)
#         db.session.commit()
#         flash('Admin account created')
#         return redirect(url_for('auth.login'))

#     return render_template('register.html', title='Register', form=form)