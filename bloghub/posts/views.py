from flask import render_template, request, Blueprint, url_for, redirect, abort
from posts.forms import PostForm, MessageForm, CommentForm
from posts.models import Post, Follow, Message, Comment
from users.models import User
from database import db
from flask_login import current_user, login_required
import time

posts_bp = Blueprint("posts", __name__, template_folder="../templates/posts")

TEMPLATE_DIR = "posts/"


@posts_bp.route("/")
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts, main=True)


@posts_bp.route("/create-post", methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('text'):
            post = Post(user=current_user,
                        title=request.form.get('title'),
                        text=request.form.get('text'))
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.index'))

        else:
            if not request.form.get('title'):
                current_field_errors = list(form.title.errors)
                current_field_errors.append("Заполните поле!")
                form.title.errors = current_field_errors

            if not request.form.get('text'):
                current_field_errors = list(form.text.errors)
                current_field_errors.append("Заполните поле!")
                form.text.errors = current_field_errors

    return render_template("post-creation-form.html", form=form)


@posts_bp.route("/view-post/<int:post_id>")
def view_post(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return abort(404)

    comments = Comment.query.filter_by(post_id=post.id)

    return render_template("post.html", post=post, form=form, comments=comments)


@posts_bp.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return abort(404)

    posts = Post.query.filter_by(user=user)

    if current_user.is_authenticated:
        already_follow = bool(Follow.query.filter_by(user_id=user.id, follower_id=current_user.id).all())
    else:
        already_follow = False

    return render_template("profile.html", user=user, posts=posts, already_follow=already_follow)


@posts_bp.route("/<username>/follow")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return abort(404)

    if current_user.id == user.id or Follow.query.filter_by(user_id=user.id, follower_id=current_user.id).first():
        return abort(403)

    follow = Follow(user_id=user.id, follower_id=current_user.id)
    db.session.add(follow)
    db.session.commit()

    return redirect(url_for('posts.profile', username=user.username))


@posts_bp.route("/<username>/unfollow")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return abort(404)

    Follow.query.filter_by(user_id=user.id, follower_id=current_user.id).delete()
    db.session.commit()

    return redirect(url_for('posts.profile', username=user.username))


@posts_bp.route("/followings")
@login_required
def followings():
    followings = db.session.query(Follow.user_id).filter_by(follower_id=current_user.id)
    posts = db.session.query(Post).order_by(Post.id.desc()).filter(Post.user_id.in_(followings))
    return render_template("index.html", posts=posts, followings=True)


@posts_bp.route("/messanger/<username>/send-message", methods=['POST', 'GET'])
@login_required
def send_message(username):
    user_to = User.query.filter_by(username=username).first()

    if not user_to:
        return abort(404)

    if request.method == 'POST':
        if request.form.get('text'):
            message = Message(user_from_id=current_user.id,
                              user_to_id=user_to.id,
                              text=request.form.get('text'))
            db.session.add(message)
            db.session.commit()

    return redirect(url_for('posts.chat', username=user_to.username))


@posts_bp.route('/messanger/<username>')
@login_required
def chat(username):
    form = MessageForm()
    user_to = User.query.filter_by(username=username).first()

    if not user_to:
        return abort(404)

    messages = db.session.query(Message).filter(
        (Message.user_to_id == user_to.id) & (Message.user_from_id == current_user.id) |
        (Message.user_to_id == current_user.id) & (Message.user_from_id == user_to.id))

    return render_template("chat.html", messages=messages, username=username, form=form, messanger=True)


@posts_bp.route('/messanger')
@login_required
def messanger():
    subquery = db.session.query(Message).filter((Message.user_to_id == current_user.id) |
                                                (Message.user_from_id == current_user.id))
    subquery = subquery.order_by(Message.time.desc()).cte()
    left_table = db.session.query(subquery).group_by(subquery.c.user_from_id, subquery.c.user_to_id).cte()
    right_table = db.session.query(subquery).group_by(subquery.c.user_from_id, subquery.c.user_to_id).cte()

    resulted_table = db.session.query(left_table.c.id).outerjoin(right_table,
                                                            (right_table.c.user_to_id == left_table.c.user_from_id) &
                                                            (right_table.c.user_from_id == left_table.c.user_to_id))

    resulted_table = resulted_table.filter(right_table.c.time.is_(None) |
                                           (left_table.c.time >= right_table.c.time))

    last_messages = Message.query.filter(Message.id.in_(resulted_table)).order_by(Message.time.desc())

    return render_template("messanger.html", last_messages=last_messages, messanger=True)


@posts_bp.route('/view-post/<int:post_id>/comment', methods=['POST', 'GET'])
@login_required
def send_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return abort(404)

    if request.method == 'POST':
        if request.form.get('text'):
            message = Comment(user_id=current_user.id,
                              post_id=post.id,
                              text=request.form.get('text'))
            db.session.add(message)
            db.session.commit()

    return redirect(url_for('posts.view_post', post_id=post.id))
