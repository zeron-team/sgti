import os

class Config:
    SECRET_KEY = os.environ.get('0f240025d7f4cc6392751980b8a6d7dc') or 'nunca-la-vas-adininar-p&t@'
    SQLALCHEMY_DATABASE_URI = os.environ.get('localhost:3308') or 'mysql://rantonioli:9157N4t4l10@localhost:3308/sgti'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
