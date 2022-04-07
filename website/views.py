#! python3
#! views.py - Stores a blueprint for the main routes of our website

from flask_login import current_user
from website.models import Admin, Blog, Post
from . import app
from flask import Blueprint, render_template, request, url_for, redirect, flash
from PIL import Image
import os



views = Blueprint('views', __name__)    # -- Initiates the blueprint for views.py

@views.route('/', methods=['GET', 'POST'])
@views.route('/home')
def home():
    posts = posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('index.html', title='Home Page', posts=posts)

@views.route('/posts/view=<int:id>')
def viewPost(id):
    post = Post.query.get(id)
    return render_template('view_post.html', title= post.title, post=post)

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Blog.query.order_by(Blog.date_posted.desc()).paginate(per_page=1, page=page)
    return render_template('blog.html', posts=posts)
