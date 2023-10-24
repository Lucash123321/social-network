from flask import render_template, Blueprint

about_bp = Blueprint("about", __name__, template_folder="../templates/about")


@about_bp.route("/about/techs")
def index():
    return render_template("techs.html")
