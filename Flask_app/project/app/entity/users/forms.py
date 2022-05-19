from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,IntegerField,PasswordField,SubmitField,BooleanField ,SelectField,DecimalField
from wtforms.validators import DataRequired,length,Email,EqualTo,ValidationError
from app.Models import User
import wtforms.validators as validators


class RegistrationForm(FlaskForm):
    username =StringField('UserName',
                                validators=[DataRequired(),length(min=4 ,max=20)])
    
    type =SelectField('Type',
                            choices=[('Client', 'Client'), ('Tradeeco', 'Tradeeco'), ('Tradefin', 'Tradefin'),('Admin', 'Admin')])
    email =StringField('Email',
                           validators=[DataRequired(),Email()])
    password =PasswordField('Password',
                                  validators=[DataRequired(),length(min=8 ,max=20)])
    #confirm_password =PasswordField('ConfirmPassword',
                                 # validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')
    
    def validate_username(self,username):  
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('This username is taken.Please choose a different name')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('This email is already used by  another user')

class LoginForm(FlaskForm):
    username =StringField('UserName',
                                     validators=[DataRequired(),length(min=4 ,max=20)] )
    #email =StringField('Email',
                           # validators=[DataRequired(),Email()])
    password =PasswordField('Password',
                                  validators=[DataRequired(),length(min=4 ,max=20)])
    remember = BooleanField('Remember me')                              
    submit = SubmitField('Login')

class Setting(FlaskForm):
    prenom =StringField('prenom',
                                validators=[DataRequired(),length(min=4 ,max=20)])
    adresse =StringField('adresse',
                            validators=[DataRequired()])
    username =StringField('username',
                                validators=[DataRequired(),length(min=4 ,max=20)])
    
    numero =IntegerField('numero',
                           validators=[validators.InputRequired()])

    submit = SubmitField('Modify')


class deposit_(FlaskForm):
    amount =IntegerField('amount',
                           validators=[validators.InputRequired()])

    file=FileField()

    submit = SubmitField('Deposit')

class redraw_(FlaskForm):
    amount =IntegerField('amount',
                           validators=[validators.InputRequired()])

    submit = SubmitField('Redraw')

class invite_(FlaskForm):
    email =StringField('Email',
                           validators=[DataRequired(),Email()])

    submit = SubmitField('Invite')





class interest_perc(FlaskForm):
    pourcentage3 =DecimalField('Pourcentage 3 mois', validators=[validators.InputRequired()])

    IAC=DecimalField('Interet annuel Client', validators=[validators.InputRequired()])

    IA=DecimalField('Interet apporteur', validators=[validators.InputRequired()])

    IATE=DecimalField('Interet Trade', validators=[validators.InputRequired()])

    IATF=DecimalField('Interet annuel Trade fin', validators=[validators.InputRequired()])

    profit =DecimalField('Pourcentage profit', validators=[validators.InputRequired()])

    submit = SubmitField('Modify   ledger')