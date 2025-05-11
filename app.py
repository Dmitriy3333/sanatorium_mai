# app.py
from flask import Flask
from extensions import db, migrate
from app.routs.main_routes import main_bp
from app.routs.user_routes import user_bp
from app.routs.sanatorium_routes import sanatoriums_bp



app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)

# регистрация blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(sanatoriums_bp)

# Создание всех таблиц
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)