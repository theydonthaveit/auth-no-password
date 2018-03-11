import smtplib
import datetime
import time
import base64

from email.mime.text import MIMEText
from flask import Flask, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from passlib.hash import pbkdf2_sha512

from database_setup import Base, Engine, UserAccount
from fake_memcache import user_ids

Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

app = Flask(__name__)
app.secret_key='super'


# def decode_jwt():
#     # this will involve decoding
#     return True

# def check_inactivitey():
#     inactive = 600
#     return True

# def validate_jwt():
#     # this will involve checking
#     return True

def generate_user_id():
    return '123-456-789'

def generate_jwt():
    header = {
        "alg": "SHA512",
        "typ": "JWT"
    }

    user_id = generate_user_id()
    user_ids[user_id] = 'active'
    it = time.time()
    exp = it + 3600

    payload = {
        "sub": "1234567890",
        "uid": user_id,
        "exp": exp,
        "it": it,
    }

    secret = 'xxx'

    signature = pbkdf2_sha512.hash(secret)
    print(user_ids)
    gen_jwt = b'base64.b64encode(header).base64.b64encode(payload).base64.b64encode(signature)'

    return gen_jwt


@app.route('/', methods=['GET'])
def base():
    jjwt = generate_jwt()
    return jjwt


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # we auto_gen a passcode
        def generate_passcode():
            return '888990'

        def twilio_util():

            subject = 'OMG Super Important Message'
            body = 'verify your account'

            email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.close()
            except:
                return 'Something went wrong...'

        send_email()

        def genreate_username():
            return 'not_so_random'

        newUser = UserAccount(
            username=genreate_username(),
            passcode=generate_passcode(),
            mobile=request.json['mobile'],
            email=request.json['email'],
            ip_address=request.environ['REMOTE_ADDR']
        )
        session.add(newUser)
        session.commit()
        # this will be a redirect to LOGIN
        return 'you are signed up'
    else:
        return 'we are in Signup'


# def check_user(user):
#     if request.form['email']:
#         return session.query(UserAccount).filter_by(
#             email=request.form['email']
#         ).first()
#     else:
#         session.query(UserAccount).filter_by(
#             mobile=request.form['mobile']
#         ).first()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userExists = check_user(request.form)
#         if userExists is not None:
#             if userExists.decode_password(request.form['password']):
#                 # token = userExists.encode_auth_token(userExists.id)
#                 # redirect(url_for(authCallback))
#                 return redirect(url_for('dashboard', user_id=userExists.id))
#         else:
#             return redirect(url_for('register'))
#     else:
#         return 'we are in Login'


app.run(
    debug=True,
    host='0.0.0.0',
    port=8080,
    use_reloader=True
)