from extensions import db

# Модель санатория - набор его критериев
class Sanatorium(db.Model):
    __tablename__ = 'sanatoriums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False) #стоимость за ночь
    price_per_service = db.Column(db.Numeric(10, 2), nullable=True) #стоимость услуг
    country = db.Column(db.String(110), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    resort = db.Column(db.String(100), nullable=False)
    place_to_attractions = db.Column(db.Integer, nullable=False) #расстояние до достопримечательностей
    specialization = db.Column(db.Text, nullable=True)
    equipment = db.Column(db.Text, nullable=True)
    room_types = db.Column(db.Text, nullable=True)
    amenities = db.Column(db.Text, nullable=True) #удобства
    food_type = db.Column(db.String(255), nullable=False)
    food_quality = db.Column(db.Integer, nullable=True)
    has_pool = db.Column(db.Boolean, default=False)
    has_spa = db.Column(db.Boolean, default=False)
    has_entertainment = db.Column(db.Boolean, default=False)
    has_sports_facilities = db.Column(db.Boolean, default=False)
    average_review_score = db.Column(db.Numeric(3, 1), nullable=True) #рейтинг
    phone = db.Column(db.String(191), nullable=True)
    email = db.Column(db.String(191), nullable=True)

