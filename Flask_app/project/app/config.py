import os


class Config:
    SECRET_KEY='FABIENCLASSIC'
    SQLALCHEMY_DATABASE_URI ='sqlite:///CBSflask.db'
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:1234@localhost/cbs"
    MAIL_SERVER ='smtp.infomaniak.com'#'mail.infomaniak.ch'
    MAIL_PORT = 587
    MAIL_USE_TLS =True
    BABEL_DEFAULT_LOCALE='fr'
    MAIL_USERNAME = 123
    MAIL_PASSWORD = 123
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
