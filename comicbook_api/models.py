from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid


from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    user_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    comic = db.relationship('Comic', backref='owner', lazy = True)

    def __init__(self, user_name, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.user_name = user_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


class Comic(db.Model):
    id = db.Column(db.String, primary_key = True)
    publisher = db.Column(db.String(50))
    title = db.Column(db.String(100))
    volume_num = db.Column(db.String(3))
    issue_num = db.Column(db.String(5))
    print_num = db.Column(db.String(20))
    cover_date = db.Column(db.String(15))
    cover_price = db.Column(db.String(10))
    condition = db.Column(db.String(15))
    comments = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, publisher, title, volume_num, issue_num, print_num,
                cover_date, cover_price, condition, comments, user_token, id = ''):
        
        self.id = self.set_id()
        self.publisher = publisher
        self.title = title
        self.volume_num = volume_num
        self.issue_num = issue_num
        self.print_num = print_num
        self.cover_date = cover_date
        self.cover_price = cover_price
        self.condition = condition
        self.comments = comments
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())


class ComicSchema(ma.Schema):
    class Meta:
        fields = ['id', 'publisher','title', 'volume_num', 'issue_num', 'print_num', 'cover_date', 'cover_price', 'condition', 'comments']

comic_schema = ComicSchema()
comics_schema = ComicSchema(many=True)