from database import db
from sqlalchemy.orm import backref


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    image = db.Column(db.String)
    user = db.relationship('User', backref=backref('user'), cascade="all,delete",)

    def __repr__(self):
        return f'{self.title}'[:20]
