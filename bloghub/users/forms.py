from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Length, NumberRange


class RegistrationForm(FlaskForm):
    username = wtforms.StringField("Имя пользователя", validators=[Length(min=3, max=100)],
                                render_kw={"placeholder": "Логин"})
    email = wtforms.EmailField("Почта", render_kw={"placeholder": "Электронная почта"})
    password = wtforms.PasswordField("Пароль", render_kw={"placeholder": "Ваш пароль"})
    image = wtforms.FileField("Изображение")


class LoginForm(FlaskForm):
    username = wtforms.StringField("Имя пользователя")
    password = wtforms.PasswordField("Пароль")

