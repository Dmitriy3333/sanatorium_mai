from extensions import db
import json

# модель пользовательских предпочтений. Каждому пользователю сопоставляется строка из таблицы с предпочтениями - указывется id самого человека и описания
class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal = db.Column(db.String(255), nullable=True) #цель отдыха
    budget = db.Column(db.Integer, nullable=True)
    preferred_country = db.Column(db.String(255), nullable=True)
    preferred_region = db.Column(db.String(255), nullable=False, default='Не указано')
    preferred_resort = db.Column(db.String(255), nullable=False, default='Не указано')
    sanatorium_type = db.Column(db.String(255), nullable=True)
    services = db.Column(db.Text, nullable=True)
    importance_factors = db.Column(db.Text, nullable=True)
    place_to_attractions = db.Column(db.Boolean, nullable=False, default=False) #рассотяние до достопримечательностей
    rating = db.Column(db.Integer, nullable=False, default=3)
    treatmentbase = db.Column(db.Text, nullable=False, default='Не указано')
    food = db.Column(db.String(191), nullable=True)

    user = db.relationship('User', backref=db.backref('preferences', lazy=True))
