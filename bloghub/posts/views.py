from flask import render_template, request, Blueprint, url_for, redirect, abort
from posts.forms import PostForm, MessageForm
from posts.models import Post, Follow, Message
from users.models import User
from database import db
from flask_login import current_user, login_required

posts_bp = Blueprint("posts", __name__, template_folder="../templates/posts")

TEMPLATE_DIR = "posts/"


@posts_bp.route("/")
def index():
    posts = list(Post.query.all())[::-1]
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
    post = Post.query.filter_by(id=post_id)
    if not list(post):
        return abort(404)
    post = post.first()
    return render_template("post.html", post=post)


@posts_bp.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username)
    if not list(user):
        return abort(404)

    user = user.first()
    posts = Post.query.filter_by(user=user)

    if current_user.is_authenticated:
        already_follow = bool(list(Follow.query.filter_by(user_id=user.id, follower_id=current_user.id)))
    else:
        already_follow = False

    return render_template("profile.html", user=user, posts=posts, already_follow=already_follow)


@posts_bp.route("/<username>/follow")
@login_required
def follow(username):
    user = User.query.filter_by(username=username)
    if not list(user):
        return abort(404)

    user = user.first()
    if current_user.id == user.id or list(Follow.query.filter_by(user_id=user.id, follower_id=current_user.id)):
        return abort(403)

    follow = Follow(user_id=user.id, follower_id=current_user.id)
    db.session.add(follow)
    db.session.commit()

    return redirect(url_for('posts.profile', username=user.username))


@posts_bp.route("/<username>/unfollow")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username)

    if not list(user):
        return abort(404)

    user = user.first()

    Follow.query.filter_by(user_id=user.id, follower_id=current_user.id).delete()
    db.session.commit()

    return redirect(url_for('posts.profile', username=user.username))


@posts_bp.route("/followings")
@login_required
def followings():
    followings = db.session.query(Follow.user_id).filter_by(follower_id=current_user.id)
    posts = list(db.session.query(Post).filter(Post.user_id.in_(followings)))[::-1]
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

    messages = Message.query.filter_by(user_to_id=user_to.id, user_from_id=current_user.id)

    return render_template("chat.html", messages=messages, username=username, form=form)


@posts_bp.route('/messanger')
@login_required
def messanger():
    users_to_ids = db.session.query(Message.user_to_id).filter(user_from_id=current_user.id)
