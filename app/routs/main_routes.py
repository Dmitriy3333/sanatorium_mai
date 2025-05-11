# app/routs/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.sanatorium import Sanatorium
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.algorithms.maai import calculate_itog
from app.models.sanatoriumPhoto import SanatoriumPhoto
from extensions import db

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
@main_bp.route('/index') # для главной страницы
def index():
    sanatoriums = Sanatorium.query.all() # получение санатриев

    user = None
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id) # получение зарегистрированного пользователя

    # Проверяем, есть ли у пользователя заполненный профиль
    has_prefs = False
    if user:
        prefs = UserPreferences.query.filter_by(user_id=user.id).first() #получение предпочтений
        has_prefs = prefs is not None


    photos_dict = {} #для утсановки фото санаториев
    for sanatorium in sanatoriums:
        photo = SanatoriumPhoto.query.filter_by(sanatorium_id=sanatorium.id).first()
        if photo:
            photos_dict[sanatorium.id] = photo.file_path

    user_id_from_session = session.get('user_id')
    user = db.session.get(User, user_id_from_session) if user_id_from_session else None

    itog = None  # будущий массив с весами санаториев
    sorted_sanatoriums = sanatoriums

    if user and UserPreferences.budget:
        itog = calculate_itog(sanatoriums) # массив с весами санаториев
        sorted_sanatoriums = sorted( # сортировка плашек санаториев
            sanatoriums,
            key=lambda x: itog.get(x.id, 0),
            reverse=True
        )


    return render_template('index.html', sanatoriums=sorted_sanatoriums, photos=photos_dict, itog=itog, user=user, has_prefs=has_prefs)

