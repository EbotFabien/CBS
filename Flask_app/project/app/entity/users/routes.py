from fileinput import filename
from flask import render_template, url_for,flash,redirect,request,abort,Blueprint
from app.entity.users.forms import LoginForm,RegistrationForm,deposit_,Setting,interest_perc,invite_,redraw_
from app.Models import User,Account,Ledger,Accounttype,Interest_percentage
from flask_login import login_user,current_user,logout_user,login_required
from app import bcrypt,db
from datetime import date,timedelta,datetime,timezone 
import random
from app.entity.ledger.utils import time_left
from app.entity.users.utils import send_pdf
from sqlalchemy import or_, and_, desc,asc
from werkzeug.utils import secure_filename
from flask import  url_for,current_app
import os




users =Blueprint('users',__name__)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.type=='Admin':
            return redirect(url_for('users.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        name=User.query.filter_by(login=form.username.data).first()#put login
        if  name and bcrypt.check_password_hash(name.password,form.password.data):
            login_user(name,remember=form.remember.data,duration=timedelta(seconds=30)) 
            next_page=request.args.get('next')
            return redirect (next_page) if next_page else  redirect(url_for('users.dashboard'))
        else:
            flash(f'Mauvais Identifiant ou mot de passe, essayez à nouveau','danger')

    return render_template('fabien-ui/login.html',legend="login",form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))



@users.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if current_user.is_authenticated:
       return redirect(url_for('users.dashboard'))
    form = RegistrationForm()
    acc=['Admin','Client','Tradefin','Tradeeco']
    for i in acc:
        db.session.add(Accounttype(type=i))
        db.session.commit()
    if form.validate_on_submit():#check user 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(login=form.username.data,email=form.email.data,type=form.type.data)
        db.session.add(user)
        db.session.commit()
        user.password=hashed_password
        db.session.commit()
        num=int(random.randrange(100000, 999999))
        typo=Accounttype.query.filter_by(type=user.type).first()
        acc=Account(user_id=user.id,type=typo.id,number=num)
        db.session.add(acc)
        db.session.commit()
        flash(f'Account created you can now login','success')
        return redirect(url_for('users.login'))
    return render_template('fabien-ui/register.html',legend="sign_up",form=form)

@users.route('/<int:id>/settings_user',methods=['GET','POST'])
@login_required
def settings(id):
    if current_user.is_authenticated:
        form=Setting()
        user=User.query.filter_by(id=id).first()
        account=Account.query.filter_by(user_id=id).first()
        if form.validate_on_submit():
            user.username=form.username.data
            user.prenom=form.prenom.data
            user.adresse=form.adresse.data
            user.numero=form.numero.data
            db.session.commit()
            flash(f'Account created you can now login','success')
            return redirect(url_for('users.settings',id=id))
        #return redirect(url_for('users.main'))
        return render_template('fabien-ui/settings.html',legend="sign_up",form=form,user=user,account=account)

@users.route('/<int:id>/settings_all',methods=['GET','POST'])
@login_required
def settings_all(id):
    if current_user.is_authenticated:
        user=User.query.filter_by(id=id).first()
        account=Account.query.filter_by(user_id=id).first()
        ledgers=Ledger.query.filter(or_(Ledger.account_credited==id,Ledger.account_debited==id)).all()
        

        return render_template('fabien-ui/settings_all.html',legend="sign_up",user=user,account=account,trans=ledgers,id=id)

@users.route('/all_accounts',methods=['GET','POST'])
@login_required
def all_accounts():
    if current_user.is_authenticated:
        account=Account.query.all()
        return render_template('fabien-ui/allacounts.html',legend="sign_up",account=account)


@users.route('/<id>/deposit',methods=['GET','POST'])
@login_required
def deposit(id):
    form = deposit_()
    if form.validate_on_submit():
        check_acc=Account.query.filter_by(user_id=id).first()
        check_acc.amount+=form.amount.data
        db.session.commit()
        filename=secure_filename(form.file.data.filename)
        final=os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
        form.file.data.save(final) 
        ledger=Ledger(account_credited=id,Amount=form.amount.data,state_transaction='deposit',type='deposit') #state type of transaction,list of them
        db.session.add(ledger)
        ledger.transaction_number=int(random.randrange(100000, 999999))
        db.session.commit()
        flash(f'Account created you can now login','success')
        return redirect(url_for('users.settings_all',id=id))
    return render_template('fabien-ui/add_cash.html',legend="sign_up",form=form)


@users.route('/<id>/redraw',methods=['GET','POST'])
@login_required
def redraw(id):
    form = redraw_()
    if form.validate_on_submit():
        check_acc=Account.query.filter_by(user_id=id).first()
        check_acc.amount-=form.amount.data
        db.session.commit()
        ledger=Ledger(account_debited=id,Amount=form.amount.data,state_transaction='deposit',type='deposit') #state type of transaction,list of them
        db.session.add(ledger)
        ledger.transaction_number=int(random.randrange(100000, 999999))
        db.session.commit()
        flash(f'Account created you can now login','success')
        return redirect(url_for('users.settings',id=id))
    return render_template('fabien-ui/redraw.html',legend="sign_up",form=form)



@users.route('/invite',methods=['GET','POST'])
@login_required
def invite():
    form = invite_()
    if form.validate_on_submit():
        send_pdf(form.email.data)
        flash(f'email sent','success')
        return redirect(url_for('users.settings',id=current_user.id))
    return render_template('fabien-ui/invite.html',legend="sign_up",form=form)


@users.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    if current_user.type == 'Admin':
        #time_left()
        client=User.query.filter_by(type='Client').count()
        trade_fin=User.query.filter_by(type='Tradefin').count()
        trade_eco=User.query.filter_by(type='Tradeeco').count()

        Cash_all=Account.query.all()
        final=0
        
        for sum in Cash_all:
            if sum.amount !=None:
                final+=sum.amount

        allled=Ledger.query.all()

        return render_template('fabien-ui/index.html',legend="dashboard",final=final,ledger=allled,client=client,trade_fin=trade_fin,trade_eco=trade_eco)
    else:
        #time_left()
        client=User.query.filter_by(type='Client').count()
        trade_fin=User.query.filter_by(type='Tradefin').count()
        trade_eco=0

        Cash_all=Account.query.filter_by(user_id=current_user.id).all()
        final=0
        
        for sum in Cash_all:
            if sum.amount !=None:
                final+=sum.amount
        now_utc = datetime.now(timezone.utc) + timedelta(days=1)#add 1 day
        start=datetime.combine(now_utc,datetime.min.time())

        allled=Ledger.query.filter(or_(Ledger.account_credited==current_user.id,Ledger.account_debited==current_user.id)).all()

        return render_template('fabien-ui/index.html',legend="dashboard",final=final,ledger=allled,late=start,client=client,trade_fin=trade_fin,trade_eco=trade_eco)



@users.route('/modify_interests',methods=['GET','POST'])
@login_required
def modify_interest():
    acc=['Interet annuel Client','Pourcentage 3 mois','Interet apporteur'
    ,'Interet Trade','Interet annuel Trade fin','Pourcentage profit']
    for i in acc:
        db.session.add(Interest_percentage(type=i))
        db.session.commit()
    form=interest_perc()
    interests=Interest_percentage.query.order_by(asc(Interest_percentage.id)).all()
    if form.validate_on_submit():
        pourcentage3=Interest_percentage.query.filter_by(type='Pourcentage 3 mois').first()
        pourcentage3.percentages=form.pourcentage3.data
        IAC=Interest_percentage.query.filter_by(type='Interet annuel Client').first()
        IAC.percentages=form.IAC.data
        IA=Interest_percentage.query.filter_by(type='Interet apporteur').first()
        IA.percentages=form.IA.data
        IATE=Interest_percentage.query.filter_by(type='Interet Trade').first()
        IATE.percentages=form.IATE.data
        IATF=Interest_percentage.query.filter_by(type='Interet annuel Trade fin').first()
        IATF.percentages=form.IATF.data
        profit=Interest_percentage.query.filter_by(type='Pourcentage profit').first()
        profit.percentages=form.profit.data

        db.session.commit()
        return redirect(url_for('users.settings',id=current_user.id))
    return render_template('fabien-ui/modify_interests.html',legend="login",form=form,inter=interests)


@users.route('/create_user',methods=['GET','POST'])
@login_required
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():#check user 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(login=form.username.data,email=form.email.data,type=form.type.data)
        db.session.add(user)
        db.session.commit()
        user.password=hashed_password
        db.session.commit()
        num=int(random.randrange(100000, 999999))
        typo=Accounttype.query.filter_by(type=user.type).first()
        acc=Account(user_id=user.id,type=typo.id,number=num)
        db.session.add(acc)
        db.session.commit()
        flash(f'Account created you can now login','success')
        return redirect(url_for('users.all_accounts'))
    return render_template('fabien-ui/add_user.html',legend="sign_up",form=form)
