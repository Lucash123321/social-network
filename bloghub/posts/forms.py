from flast_wtf import FlaskForm
import wtforms
from wtforms.validators import Length, NumberRange


class PostForm(FlaskForm):
    name = wtforms.StringField("Заголовок", validators=[Length(min=3, max=100)])
    text = wtforms.TextAreaField("Текст")
    image = wtforms.FileField()
