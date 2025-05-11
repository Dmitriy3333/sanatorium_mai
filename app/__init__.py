from flask import Flask
from .routs.main_routes import main_bp
from .routs.user_routes import user_bp
from .routs.sanatorium_routes import sanatoriums_bp
from config import Config

from .models import Sanatorium, User, UserPreferences
from flask_migrate import Migrate
from extensions import db  # для использованя SQLAlchemy и db

migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация Blueprints
    app.register_blueprint(main_bp)  # Blueprint для главной страницы
    app.register_blueprint(user_bp) # Blueprint для пользователя
    app.register_blueprint(sanatoriums_bp, url_prefix='/sanatoriums')  # Blueprint для санаториев

    return app
