from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField #, TextAreaField
from wtforms.validators import DataRequired,length,Email,EqualTo,ValidationError
from app.Models import User,Account
import wtforms.validators as validators




class createForm(FlaskForm):
    account_debit =IntegerField('account_debit',
                           validators=[validators.InputRequired()])
    account_credited =IntegerField('account_credited',
                           validators=[validators.InputRequired()])
    amount =IntegerField('amount',
                           validators=[validators.InputRequired()])

    submit = SubmitField('Register ledger')

    def validate_cash(self,id,amount):
        check_accdeb=Account.query.filter_by(user_id=id).first()

        if amount > check_accdeb.amount:
            raise ValidationError('The amount of cash in account is not sufficient')
    
   
class editForm(FlaskForm):
    account_debit =IntegerField('account_debit',
                           validators=[validators.InputRequired()])
    account_credited =IntegerField('account_credited',
                           validators=[validators.InputRequired()])
    amount =IntegerField('amount',
                           validators=[validators.InputRequired()])

    submit = SubmitField('Modify ledger')