from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.sanatorium import Sanatorium
from app.models.user import User
from app.models.user_preferences import UserPreferences
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import json
from extensions import db
import re

user_bp = Blueprint('user', __name__)
@user_bp.route('/profile', methods=['GET', 'POST']) # для профиля пользователя
def profile():
    # Проверка наличия пользователя в сессии
    if 'user_id' not in session:
        # flash('Сначала войдите в аккаунт', 'warning')
        return redirect(url_for('user.login'))

    user = User.query.get(session['user_id'])

    # Если пользователя с таким id нет, возвращаем на страницу входа
    if user is None:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('user.login'))

    if request.method == 'POST': # заполнение базы из формы
        user_preferences = UserPreferences.query.filter_by(user_id=user.id).first()
        if not user_preferences:
            user_preferences = UserPreferences()
            user_preferences.user_id = user.id

        user_preferences.preferred_region = request.form.get('region') or 'Не указано'
        user_preferences.preferred_resort = request.form.get('resort') or 'Не указано'
        user_preferences.place_to_attractions = 'place_to_attractions' in request.form
        user_preferences.rating = request.form.get('rating', type=int) or 3
        user_preferences.treatmentbase = ','.join(request.form.getlist('treatment_base[]')) or 'Не указано'

        user_preferences.goal = request.form.get('purpose')
        user_preferences.budget = request.form.get('sum')
        user_preferences.preferred_country = request.form.get('country')
        user_preferences.sanatorium_type = request.form.get('type')

        services_list = request.form.getlist('services[]')
        user_preferences.services = ','.join(services_list) if services_list else None

        importance_factors = {
            'price': request.form.get('фактор_стоимости', type=int) or 3,
            'location': request.form.get('фактор_места', type=int) or 3,
            'treatment': request.form.get('фактор_базы', type=int) or 3,
            'living': request.form.get('фактор_условий', type=int) or 3,
            'entertainment': request.form.get('фактор_развлечений', type=int) or 3
        }
        user_preferences.importance_factors = json.dumps(importance_factors)

        db.session.add(user_preferences)
        db.session.commit()

        flash('Профиль успешно обновлён', 'success')
        return redirect(url_for('user.profile'))

    user_preferences = UserPreferences.query.filter_by(user_id=user.id).first()

    default_factors = { # значения значимости факторов по умолчанию
        'price': 3,
        'location': 3,
        'treatment': 3,
        'living': 3,
        'entertainment': 3
    }

    if user_preferences and user_preferences.importance_factors:
        try:
            factors = json.loads(user_preferences.importance_factors)
            factors = {**default_factors, **factors}
        except json.JSONDecodeError:
            factors = default_factors
    else:
        factors = default_factors

    return render_template('profile.html', user=user, user_preferences=user_preferences, factors=factors)

# @user_bp.route('/signup', methods=['GET', 'POST']) # для регистрации
# def signup():
#     if request.method == 'POST':
#         user = User()
#         user.name = request.form['name']
#         user.login = request.form['login']
#         user.email = request.form['email']
#         user.password = generate_password_hash(request.form['password'])
#         user.is_admin = False
#         db.session.add(user)
#         db.session.commit()
#         flash('Данные сохранены успешно!', 'success')
#         return redirect(url_for('user.login'))

#     return render_template("signup.html")

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name', '').strip()
        login = request.form.get('login', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errors = []

        # Проверка на пустые поля
        if not name or not login or not email or not password or not confirm:
            errors.append("Все поля обязательны для заполнения.")

        # Проверка длины имени
        if len(name) > 50:
            errors.append("Имя слишком длинное. Максимум 20 символов.")

        # Проверка логина
        if len(login) < 4:
            errors.append("Логин должен содержать минимум 4 символа.")

        # Проверка email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Неверный формат email.")

        # Проверка паролей
        if password != confirm:
            errors.append("Пароли не совпадают.")
        if len(password) < 6:
            errors.append("Пароль должен содержать минимум 6 символов.")

        # Проверка уникальности логина
        if User.query.filter_by(login=login).first():
            errors.append("Пользователь с таким логином уже существует.")

        # Если есть ошибки — возвращаем форму с сообщениями
        if errors:
            # for error in errors:
            flash(errors[0], 'danger')
            return render_template("signup.html", name=name, login=login, email=email)

        # Регистрация
        user = User(
            name=name,
            login=login,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        # flash('Регистрация прошла успешно. Теперь войдите в систему.', 'success')
        return redirect(url_for('user.login'))

    return render_template("signup.html")


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login', '').strip()
        password_input = request.form.get('password', '')

        # Проверки
        if not login_input or not password_input:
            flash("Пожалуйста, заполните все поля.", "danger")
            return render_template("login.html", login=login_input)

        user = User.query.filter_by(login=login_input).first()

        if not user:
            flash("Пользователь с таким логином не найден.", "danger")
            return render_template("login.html", login=login_input)

        if not check_password_hash(user.password, password_input):
            flash("Неверный пароль.", "danger")
            return render_template("login.html", login=login_input)

        # Всё хорошо — логиним
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['is_admin'] = user.is_admin
        # flash('Вы успешно вошли!', 'success')
        return redirect(url_for('main.index'))

    return render_template("login.html")

@user_bp.route('/logout') # выход 
def logout():
    session.clear()
    # flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('user.login'))