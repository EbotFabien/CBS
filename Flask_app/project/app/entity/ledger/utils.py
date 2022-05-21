from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,current_app
from app.entity.users.forms import LoginForm,RegistrationForm,deposit_,Setting
from app.Models import User,Account,Ledger,Interest_percentage
from flask_login import login_user,current_user,logout_user,login_required
from app import bcrypt,db
from datetime import date,timedelta,datetime,timezone 
from dateutil import relativedelta
import random

app=current_app



def time_left():
    with app.app_context():
        
        ledg=Ledger.query.filter_by(state_transaction='processing').all()
        now_utc = datetime.now(timezone.utc) + timedelta(days=1)#add 1 day
        start=datetime.combine(now_utc,datetime.min.time())
        reinve=datetime.now(timezone.utc) + timedelta(days=11)
        
        for i in ledg:
            #val=reinve - i.stop
            #if val >=10:
                #reinvest(i)
            if  start > i.stop :
               
                client_cash(i)
            else:
                delta= relativedelta.relativedelta(start,i.stop)
                i.time_left=delta.months + (delta.years * 12)
                db.session.commit()

def client_cash(ledger):
    with app.app_context():
        
        check_acccpro=Account.query.filter_by(id=1).first()
        interest=Interest_percentage.query.all()

        acc_deb=ledger.account_credited
        check_accdeb=Account.query.filter_by(user_id=acc_deb).first()
        
        for inte in interest:
            if inte.type == 'Pourcentage profit':
                check_acccpro.amount+=ledger.Amount*inte.percentages
                ledger=Ledger(account_credited=check_acccpro.user_id,Amount=ledger.Amount*inte.percentages,state_transaction='processing',type='Pourcentage profit')
                db.session.add(ledger)
                db.session.commit()
            if inte.type == 'Interet Trade':#create trading account fin
                check_accdeb.amount+=ledger.Amount*inte.percentages
                ledger=Ledger(account_credited=check_accdeb.user_id,Amount=ledger.Amount*inte.percentages,state_transaction='processing',type='Interest trade')
                db.session.add(ledger)
                db.session.commit()
            #check sense interests rates for all accounts 


def redraw(ledger):
        with app.app_context():
            acc_cre=ledger.account_debited
            acc_deb=ledger.account_credited

            check_accdeb=Account.query.filter_by(user_id=acc_deb).first()
            check_accdeb.amount-=ledger.Amount
            ledger.state_transaction='finish processing'
            db.session.commit()

            check_acccred=Account.query.filter_by(user_id=acc_cre).first()
            check_acccred.amount+=ledger.Amount
            db.session.commit()
            check_acccred=Account.query.filter_by(type=acc_cre).first()
            ledger=Ledger(account_debited=check_accdeb.user_id,account_credited=check_acccred.user_id,Amount=ledger.Amount,state_transaction='done',type='3 Months')
            db.session.add(ledger)
            db.session.commit()
            interest=Interest_percentage.query.all()
            for inte in interest:
                if inte.type == 'Pourcentage 3 mois':
                    acc_cre.amount+=ledger.Amount*inte.percentages
                    ledger=Ledger(account_credited=acc_cre.user_id,Amount=ledger.Amount*inte.percentages,state_transaction='done',type='Pourcentage 3 mois')
                    db.session.add(ledger)
                    db.session.commit()
        


def reinvest(ledger):
    with app.app_context():
        acc_deb=ledger.account_debited
        acc_cred=ledger.account_credited
        interest=Interest_percentage.query.all()
        amt=0
        amt+=ledger.Amount
        for inte in interest:
            if inte.type == 'Pourcentage 3 mois':
                amt+=ledger.Amount*inte.percentages
        ledger.state_transaction='finish processing'
        db.session.commit()
        ledger=Ledger(account_debited=acc_deb,account_credited=acc_cred,Amount=amt,state_transaction='reinvest',type='3 Months')
        db.session.add(ledger)
        db.session.commit()
        ledger.transaction_number=int(random.randrange(100000,999999))
        db.session.commit()
        ledger.stop=ledger.date + timedelta(days=100)
        db.session.commit()
        delta= relativedelta.relativedelta(ledger.stop,ledger.date)
        ledger.time_left=delta.months + (delta.years * 12)
        db.session.commit()