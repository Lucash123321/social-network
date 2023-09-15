from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Length, NumberRange


class UserForm(FlaskForm):
    username = wtforms.StringField("Имя пользователя", validators=[Length(min=3, max=100)])
    email = wtforms.EmailField("Почта")
    password = wtforms.PasswordField()

