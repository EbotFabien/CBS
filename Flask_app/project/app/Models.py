from flask import current_app
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from app import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Apporteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Apporteur %r>' %self.id

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    prenom = db.Column(db.String(60))
    login = db.Column(db.String(20))
    email = db.Column(db.String(20))
    adresse = db.Column(db.String(20))
    type = db.Column(db.String(120))
    numero = db.Column(db.Integer)
    password = db.Column(db.String(60))
    apporteur_id= db.Column(db.Integer,db.ForeignKey('apporteur.id'),nullable=True)
    visibility =db.Column(db.Boolean,default=True)


    def get_reset_token(self,expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token) ['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User %r>' %self.id

class Accounttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Accounttype %r>' %self.id



class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer,unique=True)
    type = db.Column(db.Integer,db.ForeignKey('accounttype.id'), nullable=False)
    amount = db.Column(db.DECIMAL(65,2),default=0.00)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    user__data=db.relationship("User", 
        primaryjoin=(user_id  == User.id),
        backref=db.backref('user__data',  uselist=False),  uselist=False)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Account %r>' %self.id


class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_debited = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=True)
    account_debited__data=db.relationship("User", 
        primaryjoin=(account_debited  == User.id),
        backref=db.backref('account_debited__data_',  uselist=False),  uselist=False)
    account_credited = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=True)
    account_credited__data=db.relationship("User", 
        primaryjoin=(account_credited  == User.id),
        backref=db.backref('account_credited__data_',  uselist=False),  uselist=False)
    Amount = db.Column(db.DECIMAL(65,2),default=0.00)
    date = db.Column(db.DateTime(),default=datetime.utcnow)
    transaction_number = db.Column(db.Integer)
    type = db.Column(db.String(60))
    state_transaction = db.Column(db.String(60))#boolean
    stop = db.Column(db.DateTime())
    time_left = db.Column(db.String(60))
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Ledger %r>' %self.id
    

class Interest_percentage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    percentages = db.Column(db.DECIMAL(65,2),default=0.00)#put amt in percentage
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Interest_percentage %r>' %self.id
     
class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cash = db.Column(db.Integer)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    year = db.Column(db.DateTime(),default=datetime.utcnow)
    month = db.Column(db.DateTime(),default=datetime.utcnow)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Interest %r>' %self.id


class Interest_trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.DateTime(),default=datetime.utcnow)
    cash = db.Column(db.Integer)
    month = db.Column(db.DateTime(),default=datetime.utcnow)
    visibility =db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Interest_trade %r>' %self.id





    


