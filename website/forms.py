#!  python3
#!  forms.py - Used for making forms to display within html

from stat import FILE_ATTRIBUTE_SPARSE_FILE
from tkinter import E, PhotoImage
from tokenize import String
from flask import Flask, flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegisterForm(FlaskForm):
    firstName = StringField('First Name:', validators= [DataRequired()])
    lastName = StringField('Last Name:', validators= [DataRequired()])
    email = StringField('Email:', validators= [DataRequired(), Email()])
    password = PasswordField('Password',validators= [DataRequired(), ])
    confirm = PasswordField('Confirm Password:', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewPost(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Content:', validators=[DataRequired()])
    post = SubmitField('Post')

class NewPhotoPost(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Content:', validators=[DataRequired()])
    photo = FileField('Sticky Note', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    post = SubmitField('Post')