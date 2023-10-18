from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_PATH = os.path.join(BASE_DIR, 'static')
MEDIA = 'media'
UPLOAD_FOLDER = os.path.join(BASE_DIR, MEDIA)

DEBUG = True


APPS = [

]


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(32)
