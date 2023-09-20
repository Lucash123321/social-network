from flask import render_template, request, Blueprint
from posts.forms import PostForm
from posts.models import Post
from database import db
from users.models import User
from flask_login import current_user


posts_bp = Blueprint("posts", __name__, template_folder="../templates/posts")

TEMPLATE_DIR = "posts/"


@posts_bp.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@posts_bp.route("/create-post", methods=['POST', 'GET'])
def create_post():
    form = PostForm()
    if request.method == 'POST':
        post = Post(title=request.form['title'],
                    text=request.form['text'])
        db.session.add(post)
        db.session.commit()
    return render_template("post-creation-form.html", form=form)
