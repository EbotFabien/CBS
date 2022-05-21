from flask import render_template, url_for,flash,redirect,request,abort,Blueprint
from app.entity.ledger.forms import createForm
from app.Models import User,Ledger,Account,Interest
from flask_login import login_user,current_user,logout_user,login_required
from app import bcrypt,db
from datetime import date,timedelta,datetime,timezone 
from dateutil import relativedelta
from sqlalchemy import or_, and_, desc,asc
import random
from app.entity.ledger.utils import time_left,reinvest,redraw





ledger =Blueprint('ledger',__name__)

@ledger.route('/create_ledger',methods=['GET','POST'])
@login_required
def create_ledger():
    form = createForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            #account_debited=User.query.filter_by(login=form.account_debit.data).first()
            #account_credited=User.query.filter_by(login=form.account_credited.data).first()
            check_accdeb=Account.query.filter_by(number=form.account_debit.data).first()
            form.validate_cash(check_accdeb.user_id,form.amount.data)
            check_accdeb.amount-=form.amount.data
            db.session.commit()
            check_acccred=Account.query.filter_by(number=form.account_credited.data).first()
            check_acccred.amount+=form.amount.data
            db.session.commit()
            ledger=Ledger(account_debited=check_accdeb.user_id,account_credited=check_acccred.user_id,Amount=form.amount.data,state_transaction='processing',type='3 Months')
            db.session.add(ledger)
            ledger.transaction_number=int(random.randrange(100000, 999999))
            db.session.commit()
            ledger.stop=ledger.date + timedelta(days=100)
            db.session.commit()
            delta= relativedelta.relativedelta(ledger.stop,ledger.date)
            ledger.time_left=delta.months + (delta.years * 12)
            db.session.commit()

            return redirect(url_for('ledger.allledger'))

    return render_template('fabien-ui/ledger-form.html',legend="login",form=form)

@ledger.route('/all_ledger',methods=['GET','POST'])
@login_required
def allledger():
    allled=Ledger.query.all()
    return render_template('fabien-ui/allledger.html',legend="login",ledger=allled)

@ledger.route('/all_interests',methods=['GET','POST'])
@login_required
def all_interests():
    allled=Interest.query.all()
    return render_template('fabien-ui/interests.html',legend="login",interests=allled)





@ledger.route('/<id>/individual_interests',methods=['GET','POST'])
@login_required
def individual_interests(id):
    allled=Interest.query.filter_by(user_id=id).all()
    return render_template('fabien-ui/interests.html',legend="login",interests=allled)


@ledger.route('/<ledger>/<Type>/invest_redraw',methods=['GET','POST'])
@login_required
def invest_redraw(ledger,Type):
    ledgerr=Ledger.query.filter_by(id=int(ledger)).first()
    if Type == 'invest':
        reinvest(ledgerr)
        return redirect(url_for('users.dashboard'))
    if Type == 'redraw':
        redraw(ledgerr)
        return redirect(url_for('users.dashboard'))


