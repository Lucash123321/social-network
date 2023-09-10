from flask import Flask
from posts.views import posts
from core.context_processors.context import context


app = Flask(__name__, static_url_path='', static_folder='static',)
app.register_blueprint(posts)
app.register_blueprint(context)


if __name__ == "__main__":
    app.run(debug=True)
