from flask import render_template, Blueprint, request, redirect, url_for
from .forms import RegistrationForm, LoginForm
from .models import User
from database import db
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from bloghub import settings

users_bp = Blueprint("users", __name__, template_folder="../templates/users")


@users_bp.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == "POST":

        if not User.query.filter_by(username=request.form.get('username')).first() and \
                not User.query.filter_by(email=request.form.get('email')).first():

            password = generate_password_hash(request.form.get('password'))

            user = User(username=request.form.get('username'),
                        email=request.form.get('email'),
                        password=password)

            if request.files:
                image = request.files['image']
                filename = secure_filename(image.filename)
                path = os.path.join(settings.UPLOAD_FOLDER, 'profile_pictures')
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, filename)
                image.save(path)
                user.image = os.path.join('profile_pictures', filename)

            db.session.add(user)
            db.session.commit()

            return render_template("index.html")

        else:

            if User.query.filter_by(username=request.form.get('username')).first():
                current_field_errors = list(form.username.errors)
                current_field_errors.append("Это имя пользователя уже используется.")
                form.username.errors = current_field_errors

            if User.query.filter_by(email=request.form.get('email')).first():
                current_field_errors = list(form.email.errors)
                current_field_errors.append("Эта почта уже зарегистрирована.")
                form.email.errors = current_field_errors

    return render_template("user-registration-form.html", form=form)


@users_bp.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == "POST":

        user = User.query.filter_by(username=request.form.get('username')).first()

        if User.query.filter_by(username=request.form.get('username')).first() and \
                check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('posts.index'))

    return render_template("login.html", form=form)


@users_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('posts.index'))
