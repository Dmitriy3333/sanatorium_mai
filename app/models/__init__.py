# models/__init__.py
from .sanatorium import Sanatorium
from .user import User
from .user_preferences import UserPreferences

__all__ = ['Sanatorium', 'User', 'UserPreferences'] # переменная, которая управляет тем, что будет импортироваться