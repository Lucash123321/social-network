from flask import render_template, request, Blueprint, url_for, redirect, abort
from posts.forms import PostForm
from posts.models import Post
from users.models import User
from database import db
from flask_login import current_user, login_required

posts_bp = Blueprint("posts", __name__, template_folder="../templates/posts")

TEMPLATE_DIR = "posts/"


@posts_bp.route("/")
def index():
    posts = list(Post.query.all())[::-1]
    return render_template("index.html", posts=posts)


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
    return render_template("profile.html", user=user, posts=posts)
