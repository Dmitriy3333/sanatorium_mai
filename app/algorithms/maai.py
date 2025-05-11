# app/algorithms/maai.py
from sqlalchemy import String

from app.models.sanatorium import Sanatorium
from app.models.user import User
from app.models.user_preferences import UserPreferences
import random
from extensions import db
from flask import session
import json
import numpy as np


def printInfo(user, preferences):
    print(f"User: {user.name}")  # тут можно обращаться к элементам таблицы через ключи - можно посмотреть в models/
    print(f"Бюджет: {preferences.budget}") #тут можно обращаться к элементам таблицы через ключи - можно посмотреть в models/
    print(f"Предпочтительный регион: {preferences.preferred_region}")
    print(f"Тип санатория: {preferences.sanatorium_type}")
    print(f"Услуги: {preferences.place_to_attractions}")
    print(f"Услуги: {preferences.services}")
    print(f"Услуги: {preferences.treatmentbase}")
    print(f"Услуги: {preferences.importance_factors}")

def checkValid_UserAndPreferences(session):

    ## Проверка на авторизацию пользователя и наличие у него предпочтений.
    ## Если что-то из этого нарушается - обрабатывается False

    user_id_from_session = session.get('user_id')
    if not user_id_from_session:
        print("Пользователь не авторизован")
        return False

    user = db.session.get(User, user_id_from_session)  # Ищем пользователя по user_id

    if not user:
        print("Пользователь не найден")
        return False

    preferences = UserPreferences.query.filter_by(user_id=user.id).first()

    if not preferences:
        print("Предпочтения не найдены")
        return False

    return user, preferences

def comparingMatrix (_preferences):
    ## Матрица попарных сравнений (4.2.1)
    ## Использует факторы важности и сравнивает их между собой
    user_id_from_session = session.get('user_id')

    user = db.session.get(User, user_id_from_session)  # Ищем пользователя по user_id
    preferences = UserPreferences.query.filter_by(user_id=user.id).first()
    factorsWeight = json.loads(preferences.importance_factors)

    criteria_names = list(factorsWeight.keys()) # Строка с названиями факторов
    weights = np.array(list(factorsWeight.values())) # Массив с весом факторов

    n = len(criteria_names)
    matrix = np.ones((n, n))

    ## Заполнение матрицы
    for i in range(n):
        for j in range(n):
            if i != j:
                if weights[i] - weights[j] == 0:
                    matrix[i, j] = 1
                elif weights[i] - weights[j] == 2 or -2:
                    matrix[i, j] = 3 if weights[i] - weights[j] == 2 else 1/3
                elif weights[i] - weights[j] == 4 or -4:
                    matrix[i, j] = 5 if weights[i] - weights[j] == 4 else 1/5
                elif weights[i] - weights[j] == 6 or -6:
                    matrix[i, j] = 7 if weights[i] - weights[j] == 6 else 1/7
                elif weights[i] - weights[j] == 8 or -8:
                    matrix[i, j] = 9 if weights[i] - weights[j] == 8 else 1/9

    return matrixAnalyze(matrix)



def locationScoreMatrix(_preferences, _sanatorium_list):
    ## Начисляет очки иерархии в зависимости от совпадений санаториев с предпочтениями расположений

    n = len(_sanatorium_list)
    matrix = np.ones((n, n))
    scores = []

    for _sanatorium in _sanatorium_list:
        score = 1

        score += 2 if _sanatorium.country == _preferences.preferred_country else 0
        score += 2 if _sanatorium.region == _preferences.preferred_region else 0
        score += 2 if _sanatorium.resort == _preferences.preferred_resort else 0

        scores.append(score)

    for i in range(n):
        for j in range(n):
            if i != j:
                if scores[i] / scores[j] == 1/7:
                    matrix[i, j] = round(1/7, 2)
                elif scores[i] / scores[j] == 1/5:
                    matrix[i, j] = round(1/5, 2)
                elif scores[i] / scores[j] == 1/3:
                    matrix[i, j] = round(1/3, 2)
                elif scores[i] / scores[j] == 1:
                    matrix[i, j] = 1
                elif scores[i] / scores[j] == 3:
                    matrix[i, j] = 3
                elif scores[i] / scores[j] == 5:
                    matrix[i, j] = 5
                elif scores[i] / scores[j] == 7:
                    matrix[i, j] = 7
    return matrixAnalyze(matrix)

def budgetScoreMatrix (_preferences, _sanatorium_list):

    # Проверяет количество дней, которые можно прожить в санатории на выделенный бюджет

    n = len(_sanatorium_list)
    matrix = np.ones((n, n))
    days = []
    for s in _sanatorium_list:
        days.append(_preferences.budget // s.price_per_night)

    for i in range(n):
        for j in range(n):
            if i != j:
                if days[i] / days[j] < 10/30:
                    matrix[i, j] = round(1/9, 2)
                elif days[i] / days[j] < 10/20:
                    matrix[i, j] = round(1/7, 2)
                elif days[i] / days[j] < 10/15:
                    matrix[i, j] = round(1/5, 2)
                elif days[i] / days[j] < 10/11:
                    matrix[i, j] = round(1/3, 2)
                elif days[i] / days[j] < 1.1:
                    matrix[i, j] = 1
                elif days[i] / days[j] < 1.5:
                    matrix[i, j] = 3
                elif days[i] / days[j] < 2:
                    matrix[i, j] = 5
                elif days[i] / days[j] < 3:
                    matrix[i, j] = 7
                elif days[i] / days[j] > 3:
                    matrix[i, j] = 9
    return matrixAnalyze(matrix)

def healingScoreMatrix(_preferences, _sanatorium_list):

    # Проверяет количество совпадений среди предпочитаемого лечения
    # И лечением, которое есть в каждом санатории

    n = len(_sanatorium_list)
    matrix = np.ones((n, n))

    treatment = [t.strip().lower() for t in _preferences.treatmentbase.split(',')]
    score = []
    for sanatorium in _sanatorium_list:
        specializationList = [s.strip().lower() for s in sanatorium.specialization.split(',')]
        current_score = 1
        matches = len(set(treatment) & set(specializationList))
        current_score += 2 * matches
        score.append(current_score)

    for i in range(n):
        for j in range(n):
            if i != j:
                ratio = score[i] / score[j]  # Отношение баллов лечения

                if ratio <= 1 / 9:
                    matrix[i, j] = 1 / 9
                elif ratio <= 1 / 7:
                    matrix[i, j] = 1 / 7
                elif ratio <= 1 / 5:
                    matrix[i, j] = 1 / 5
                elif ratio <= 1 / 3:
                    matrix[i, j] = 1 / 3
                elif ratio <= 0.9:
                    matrix[i, j] = 1 / 3
                elif ratio < 3:
                    matrix[i, j] = 1
                elif ratio < 5:
                    matrix[i, j] = 3
                elif ratio < 7:
                    matrix[i, j] = 5
                elif ratio < 9:
                    matrix[i, j] = 7
                elif ratio >= 9:
                    matrix[i, j] = 9
    return matrixAnalyze(matrix)

def entertainmentScoreMatrix (_preferences, _sanatorium_list):

    # Проверяет, есть ли рядом развлечения (в пределах 75км)
    # И есть ли развлечения в самом санатории

    n = len(_sanatorium_list)
    matrix = np.ones((n, n))
    scores = []
    if _preferences.place_to_attractions:
        for s in _sanatorium_list:
            finalScore = 1
            if s.has_entertainment: finalScore += 2
            if s.place_to_attractions < 75: finalScore += 2
            scores.append(finalScore)


    for i in range(n):
        for j in range(n):
            if i != j:
                ratio = scores[i] / scores[j]

                if ratio <= 0.1:
                    matrix[i, j] = 1 / 9
                elif ratio <= 0.2:
                    matrix[i, j] = 1 / 7
                elif ratio <= 0.3:
                    matrix[i, j] = 1 / 5
                elif ratio <= 0.6:
                    matrix[i, j] = 1 / 3
                elif ratio <= 0.9:
                    matrix[i, j] = 1
                elif ratio < 1.1:
                    matrix[i, j] = 1
                elif ratio < 5:
                    matrix[i, j] = 3
                elif ratio < 7:
                    matrix[i, j] = 5
                elif ratio < 9:
                    matrix[i, j] = 7
                elif ratio >= 9:
                    matrix[i, j] = 9

    matrix = np.round(matrix, 1)
    return matrixAnalyze(matrix)

def livingScoreMatrix (_preferences, _sanatorium_list):

    # Делает лист сервисов.
    # За каждый сервис начисляет очки, так же сравнивая оценку санатория с желаемой

    servicesList = [s.strip().lower() for s in _preferences.services.split(',')]
    scores = []

    for s in _sanatorium_list:
        finalScore = 1
        if "спа" in servicesList and s.has_spa:
            finalScore += 2
        if "бассейн" in servicesList and s.has_pool:
            finalScore += 2
        if "питание" in servicesList:
            finalScore += round(0.2 * s.food_quality, 1)
        if s.average_review_score > _preferences.rating:
            finalScore += 1
        if s.has_sports_facilities:
            finalScore += 1
        if type(s.amenities) == String:
                amenities = [s.amenities.split(',')]
                if finalScore < 9: finalScore += round(len(amenities) / 2, 1)
        scores.append(finalScore)

    n = len(_sanatorium_list)
    matrix = np.ones((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                ratio = scores[i] / scores[j]
                if ratio <= 0.1:
                    matrix[i, j] = 1 / 9
                elif ratio <= 0.2:
                    matrix[i, j] = 1 / 7
                elif ratio <= 0.666:
                    matrix[i, j] = 1 / 5
                elif ratio <= 0.9:
                    matrix[i, j] = 1 / 3
                elif ratio < 1.1:
                    matrix[i, j] = 1
                elif ratio < 1.5:
                    matrix[i, j] = 3
                elif ratio < 2:
                    matrix[i, j] = 5
                elif ratio < 3:
                    matrix[i, j] = 7
                elif ratio >= 3:
                    matrix[i, j] = 9

    return matrixAnalyze(matrix)



def matrixAnalyze(matrix):

    ## Пункт 5.1 в презентации

    n = len(matrix)
    normalizedMatrix = np.empty((n, n))
    columnSum = np.zeros(n)
    lineSum = np.zeros(n)


    # Подсчёт суммы столбцов матрицы
    # Сумма столбца i записывается i-тым элементом в массив columnSum[]

    for i in range(n):
        for j in range(n):
            columnSum[i] += round(matrix[j][i], 5)

    # Нормирование матрицы и вычисление суммы каждой строки
    # Тот же метод что и в сумме столбцов

    for i in range(n):
        for j in range(n):
            normalizedMatrix[i, j] = round((matrix[i][j] / columnSum[j]), 3)
            lineSum[i] += round(normalizedMatrix[i][j], 5)

    # В lineSum записываем среднее значение по строке
    for i in range(n):
        lineSum[i] = round(lineSum[i] / n,3)
    return lineSum

def alternativeWeightMatrix(priceWeight, locationWeight, treatmentWeight, livingWeight, entertainmentWeight, sanatoriumList):
    altWeightMatrix = np.column_stack((priceWeight, locationWeight, treatmentWeight, livingWeight, entertainmentWeight))

    return(altWeightMatrix)




def calculate_itog(all_sanatoriums):
    user_id_from_session = session.get('user_id')
    user = db.session.get(User, user_id_from_session)

    if not user:
        print("Пользователь не найден")
        return {}

    all_sanatoriums = Sanatorium.query.all()

    print(f"Вывод санаториев")
    for s in all_sanatoriums:
        print(f"{s.id}: {s.name}")

    result = checkValid_UserAndPreferences(session)
    if not result:
        return {}

    user, preferences = result

    #   Веса всех критериев для каждого санатория
    #   Каждая переменная содержит в себе массив из n критериев
    #   Где n = количество санаториев

    priceW = budgetScoreMatrix(preferences, all_sanatoriums)
    locationW = locationScoreMatrix(preferences, all_sanatoriums)
    treatmentW = entertainmentScoreMatrix(preferences, all_sanatoriums)
    livingW = livingScoreMatrix(preferences, all_sanatoriums)
    entertainmentW = entertainmentScoreMatrix(preferences, all_sanatoriums)

    #   Передаём всё в матрицу альтернативных сравнений записывая в матрицу MatrixA
    #   Так же записываем в массив VectorB веса критериев
    #   Затем перемножаем и получаем итоговый вес для санаториев

    MatrixA = alternativeWeightMatrix(priceW, locationW, treatmentW, livingW, entertainmentW, all_sanatoriums)
    VectorB = comparingMatrix(preferences)

    sanatoriumWeight = MatrixA @ VectorB
    print(f"{sanatoriumWeight}")

    if not preferences:
        print("Предпочтения не найдены")
        return {}  # <-- ВАЖНО! Без предпочтений ничего не считаем


    itog = {}
    i = 0
    for i, sanatorium in enumerate(all_sanatoriums):
        # Получаем вес санатория с учетом индекса i
        itog[sanatorium.id] = round(100 * sanatoriumWeight[i], 2)
    # print(matrixAnalyze(livingScoreMatrix(preferences, all_sanatoriums)))
    return itog

