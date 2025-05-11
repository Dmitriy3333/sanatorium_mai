from flask import Flask
from extensions import db, migrate
from app.routs.main_routes import main_bp
from app.routs.user_routes import user_bp
from app.routs.sanatorium_routes import sanatoriums_bp
from config import Config

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config) # применение конфигурации из файла

    db.init_app(app) # инициализация приложения
    migrate.init_app(app, db) # установка миграций

    #регистрация blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(sanatoriums_bp, url_prefix='/sanatoriums')

    return app