from database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    image = db.Column(db.String)

    def __repr__(self):
        return f'{self.title}'[:20]
