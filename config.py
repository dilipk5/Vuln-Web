import os

class Config:
    DEBUG = True
    SECRET_KEY = 'dev1234'

    SESSION_COOKIE_SECURE = False
    SESSION_COOOKIE_HTTPONLY - False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///vulnweb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS= False

    UPLOAD_FOLDER = 'static/uplods'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    DEFAULT_ADMIN_USER = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'admin123'
