from flask import render_template, Blueprint

about_bp = Blueprint("about", __name__, template_folder="../templates/about")


@about_bp.route("/about/techs")
def techs():
    return render_template("techs.html")

@about_bp.route("/about/author")
def author():
    return render_template("author.html")
