from extensions import db

# модель пользователя - для регистрации и авторизации.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='user')
    name = db.Column(db.String(255))
    login = db.Column(db.String(40))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False) # для проверки на права админимстратора
    # email = db.Column(db.String(120), unique=True, nullable=False)