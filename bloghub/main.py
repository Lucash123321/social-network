from flask import Flask
from flask_migrate import Migrate

import bloghub.settings as settings
from core.context_processors.context import context
from database import db
from posts.views import posts_bp
from users.views import users_bp
from posts.models import Post

app = Flask(__name__, static_url_path='', static_folder='static')
app.register_blueprint(posts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(context)
app.config.from_object(settings.Config)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=settings.DEBUG)
