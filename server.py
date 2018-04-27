import smtplib
import datetime
import time
import base64
import json
import jwt

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

secret_key = 'chicken'

def decode_jwt(encoded_jwt):
    decode = jwt.decode(encoded_jwt, secret_key, algorithms=['HS256'])
    return decode

def check_inactivitey(it, exp, uid):
    # check inactivity
    current_time = time.time()
    if current_time < exp:
        values = validate_jwt(uid)
        return values
    else:
        return 'active'

def validate_jwt(uid):
    # this will involve checking
    if user_ids[uid] is not None:
        if user_ids[uid] == 'active':
            return 'we are fine'
    else:
        return user_ids[uid] == 'inavtive'

@app.route('/jwt', methods=['POST'])
def jwt_decode_test():
    things = decode_jwt(request.headers["Authorization"])
    state = check_inactivitey(things['it'], things['exp'], things['uid'])
    return state

def generate_user_id():
    return '123-456-789'

def generate_jwt():
    header = {
        "alg": "HS256",
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

    gen_jwt = jwt.encode(
        payload,
        secret_key,
        algorithm='HS256',
        headers=header
    )

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

            client = Client("AC0e087aa2bf931060cecc7b44522dd8b1",
                "5e77e5a337f870ca3c5c936f85ea833b")

            client.messages.create(to="+447901648812",
                from_="+447533025324",
                body="Here is your auto_gen passcode: 888990")

        twilio_util()

        def send_email():
            # Create a text/plain message
            gmail_user = 'alanwilliamswastaken@gmail.com'
            gmail_password = 'a@280989aW'

            sent_from = gmail_user
            to = ['theydonthaveit@gmail.com']
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