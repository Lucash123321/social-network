from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Length, NumberRange


class PostForm(FlaskForm):
    title = wtforms.StringField("Заголовок", validators=[Length(min=3, max=30)],
                                render_kw={"placeholder": "Заголовок"})
    text = wtforms.TextAreaField("Текст", render_kw={"placeholder": "Текст"})
    image = wtforms.FileField("Изображение")


class MessageForm(FlaskForm):
    text = wtforms.TextAreaField("Текст", render_kw={"placeholder": "Текст"})

