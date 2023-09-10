from flask import Blueprint
from database import db

Blueprint("posts", __name__, template_folder="templates")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    image = db.Column(db.String)

    def __repr__(self):
        return f'{self.title}'[:20]
