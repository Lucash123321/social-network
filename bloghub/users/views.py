from flask import render_template, Blueprint, request
from .forms import UserForm
from .models import User
from database import db

users_bp = Blueprint("users", __name__, template_folder="../templates/users")


@users_bp.route("/register", methods=['POST', 'GET'])
def user_register():
    form = UserForm()
    if request.method == "POST":

        if not User.query.filter_by(username=request.form['username']) and \
           not User.query.filter_by(email=request.form['email']):

            user = User(username=request.form['username'],
                        email=request.form['email'],
                        password=request.form['password'])

            db.session.add(user)
            db.session.commit()

            return render_template("index.html")

        else:

            if User.query.filter_by(username=request.form['username']):
                current_fild_errors = list(form.username.errors)
                current_fild_errors.append("Это имя пользователя уже используется.")
                form.username.errors = current_fild_errors

            if User.query.filter_by(email=request.form['email']):
                current_fild_errors = list(form.email.errors)
                current_fild_errors.append("Эта почта уже зарегистрирована.")
                form.email.errors = current_fild_errors

    return render_template("user-registration-form.html", form=form)
