from flask import Flask

import bloghub.settings as settings
from posts.views import posts
from core.context_processors.context import context
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='', static_folder='static',)
app.register_blueprint(posts)
app.register_blueprint(context)
app.config.from_object(settings.Config)
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=settings.DEBUG)
