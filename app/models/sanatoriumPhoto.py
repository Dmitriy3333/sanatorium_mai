from extensions import db

# Модель для хранения фото санаториев. Каждому санаторию сопоставляется строка из таблицы с фото - указывется id самого санатория и пути к фото
class SanatoriumPhoto(db.Model):
    __tablename__ = 'sanatorium_photos'

    id = db.Column(db.Integer, primary_key=True)

    sanatorium_id = db.Column(db.Integer, db.ForeignKey('sanatoriums.id', ondelete='CASCADE'), nullable=False)
    sanatorium = db.relationship('Sanatorium', backref=db.backref('photos', passive_deletes=True, cascade="all, delete"))

    # пути хранения
    file_path = db.Column(db.String(255), nullable=False)

