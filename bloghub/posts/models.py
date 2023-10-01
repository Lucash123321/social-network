from database import db
from sqlalchemy.orm import backref


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    image = db.Column(db.String)
    user = db.relationship('User', backref=backref('posts'), cascade="all,delete", )

    def __repr__(self):
        return f'{self.title}'


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    user_from = db.relationship('User', backref=backref('sent_messages'), cascade="all,delete",
                                primaryjoin="Message.user_from_id == User.id")
    user_to = db.relationship('User', backref=backref('received_messages'), cascade="all,delete",
                              primaryjoin="Message.user_to_id == User.id")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    text = db.Column(db.Text)
    user = db.relationship('User', backref=backref('user_comments'), cascade="all,delete",
                           primaryjoin="Comment.user_id == User.id")
    post = db.relationship('Post', primaryjoin="Comment.post_id == Post.id")
