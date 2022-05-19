from app import mail
from flask import  url_for
from flask_mail import Message
import random
##from PIL import Image 
from flask import  url_for,current_app
import os

app=current_app

def send_pdf(mail1):
    with app.app_context():
        msg = Message('Invitation of ',
                    sender='noreply@demo.com',
                    recipients=[mail1])
        msg.body = f''' This is a contract :

        
                    please ignore it if you didn't initiate it
                    '''
        #file=os.path.join(current_app.config['UPLOAD_FOLDER'],"DRAFT_OF_AI_Colosseum_Survival_GAME-converted.pdf")
        #with current_app.open_resource(file) as fp:
            #msg.attach(file,fp.read())

        mail.send(msg)