from datetime import datetime
from . import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(adminId):
    return Admin.query.get(int(adminId))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    email = db.Column(db.String(20))
    password = db.Column(db.String(100))
    imageFile = db.Column(db.String(100), nullable = False, default ='default.jpg')
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.lastName}', '{self.imageFile}')"

# add likes option to posts after dumping the database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    adminId = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    imageFile = db.Column(db.String(100), nullable = False, default ='default.jpg')

    def __repr__(self):
        return f"Posts('{self.title}', '{self.date_posted}')"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Blog('{self.title}', '{self.date_posted}')"

