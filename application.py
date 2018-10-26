from flask import Flask, request, render_template, request, redirect, jsonify, url_for, flash, make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import GoogleCredentials
from sqlalchemy import asc,create_engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from socks_db import Base
import json
import requests
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'SellingSocks'

engine = create_engine('sqlite:///selling_socks.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def checkAccessToken():
    access_token = None #session.get('access_token')
    if access_token is None:
        auth_details = {'login': 'login', 'signup': 'signup'}
        return False
    else:
        auth_details = {'mysocks': 'mysocks', 'logout': 'logout'}
        return True


@app.route('/login')
def login():
    checkAccessToken()
    state = ''.join(random.choice(string.ascii_uppercase+string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', auth_details=auth_details, state=state)


@app.route('/signup')
def signup():
    checkAccessToken()
    return render_template('signup.html', auth_details=auth_details)


@app.route('/socks')
def socks():
    checkAccessToken()
    return render_template('socks.html', auth_details=auth_details)

@app.route('/')
def runnin_sock():
    return render_template('runnin_sock.html', auth_details=auth_details)


if __name__ == '__main__':
    auth_details = {'login': 'login', 'signup': 'signup'}
    checkAccessToken()
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)


