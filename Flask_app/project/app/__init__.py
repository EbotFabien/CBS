from flask import Flask, render_template, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
from flask_mail import Mail
from app.config import Config



db=SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view ='users.login' #check route 
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.entity.ledger.routes import ledger
    from app.entity.users.routes import users
    from app.entity.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(ledger)
    app.register_blueprint(errors)


    return app