import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG') == 'True'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqllite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

ACCESS_TOKEN_MINUTES = int(os.environ.get('ACCESS_TOKEN_MINUTES') or '15')
REFRESH_TOKEN_DAYS = int(os.environ.get('REFRESH_TOKEN_DAYS') or '7')
REFRESH_TOKEN_IN_COOKIE = os.environ.get('REFRESH_TOKEN_IN_COOKIE') == 'True'
REFRESH_TOKEN_IN_BODY = os.environ.get('REFRESH_TOKEN_IN_BODY') == 'True'
RESET_TOKEN_MINUTES = int(os.environ.get('RESET_TOKEN_MINUTES') or '15')
PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL') or 'http://localhost:5000/reset'

APIFAIRY_TITLE = 'CostWise Fitec API'
APIFAIRY_VERSION = '1.0'
APIFAIRY_UI = os.environ.get('APIFAIRY_UI') or 'swagger'
APIFAIRY_TAGS = ['tokens', 'users', 'projects']

MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'dev@dev.com'
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')
MAIL_USE_TLS = True

