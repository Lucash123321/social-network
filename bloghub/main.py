from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_login import LoginManager

import bloghub.settings as settings
from core.context_processors.context import context
from database import db
from users.models import User
from posts.views import posts_bp
from users.views import users_bp

app = Flask(__name__, static_url_path='', static_folder='static')
app.register_blueprint(posts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(context)
app.config.from_object(settings.Config)
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/media/<path:filename>')
def media(filename):
    print(app.config['UPLOAD_FOLDER'], '#################')
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=settings.DEBUG)
