from flask import Blueprint, render_template, request
from forms import PostForm


posts = Blueprint("posts", __name__, template_folder="templates")

TEMPLATE_DIR = "posts/"


@posts.route("/")
def index():
    return render_template(TEMPLATE_DIR + "index.html", form=PostForm())
