from database import db
from flask_login import LoginManager, UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)

    def __repr__(self):
        return f'{self.username}'
