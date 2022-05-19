import os


class Config:
    SECRET_KEY='FABIENCLASSIC'
    SQLALCHEMY_DATABASE_URI ='sqlite:///CBSflask.db'
    MAIL_SERVER ='smtp.infomaniak.com'#'mail.infomaniak.ch'
    MAIL_PORT = 587
    MAIL_USE_TLS =True
    BABEL_DEFAULT_LOCALE='fr'
    MAIL_USERNAME = 'info@resilion.eu'
    MAIL_PASSWORD = 'Vincent123$'
    UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')











class Development(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 8000

class Production(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 80


config = {
    'dev': Development,
    'prod': Production,
    'default': Development
}
