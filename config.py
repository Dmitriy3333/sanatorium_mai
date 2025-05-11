import os
basedir = os.path.abspath(os.path.dirname(__file__))

# конфигурации использования бд
class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'sanatoriums.db') # ипользование sqlite
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1386@localhost:5432/sanatoriums' # ипользование postgresql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
