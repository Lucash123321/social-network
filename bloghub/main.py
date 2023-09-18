from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

import bloghub.settings as settings
from core.context_processors.context import context
from database import db
from posts.views import posts_bp
from users.views import users_bp

app = Flask(__name__, static_url_path='', static_folder='static')
login_manager = LoginManager(app)
login_manager.login = 'users.views.login'


@login_manager.user_loader
def load_user(id):
    return db.User.get(id)


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
