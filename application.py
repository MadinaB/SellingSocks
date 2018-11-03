from flask import Flask, request, render_template, request
from flask import redirect, jsonify, url_for, flash, make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import GoogleCredentials
from sqlalchemy import asc, create_engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from socks_db import Base, User, Sock
import json
import random
import requests
import string
import httplib2
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = 'SellingSocks'

"""
    Connecting to db.
"""
engine = create_engine('postgresql://socks:loveforsocks@localhost/sellingsocks')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


"""
    This function is neaded for header update of every page.
"""


def getAuthDetails():
    if login_session.get('access_token') is None:
        return {'signin': 'signin'}
    else:
        return {
            'mysocks': 'mysocks',
            'sell': 'new_sock',
            'signout': 'gdisconnect'}


"""
    Signin page uses gconnect.
"""


@app.route('/signin')
def signin():
    auth_details = getAuthDetails()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template(
        'login.html',
        auth_details=auth_details,
        state=state)


"""
    Signing in via Google.
"""


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    print output
    return output


"""
    Signing out via Google.
"""


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    g_addr = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    url = g_addr % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
    return response


"""
    Creation of a new sock is done here.
"""


@app.route('/sock/new/', methods=['GET', 'POST'])
def new_sock():
    auth_details = getAuthDetails()
    if 'username' not in login_session:
        return redirect('/signin')
    if request.method == 'POST':
        new_sock = Sock(name=request.form['name'],
                        email=login_session['email'],
                        picture=request.form['picture'],
                        price=request.form['price'],
                        description=request.form['description'],
                        seller=login_session['gplus_id'])
        session.add(new_sock)
        session.commit()
        flash('Successfully added the sock.')
        return redirect('/')
    else:
        return render_template('new_sock.html', auth_details=auth_details)


@app.route('/sock/<int:sock_id>/')
def sock(sock_id):
    auth_details = getAuthDetails()
    sock = session.query(Sock).filter_by(id=sock_id).one()
    return render_template('sock.html', auth_details=auth_details, sock=sock)


"""
    Updating a sock with sock_id is done here.
"""


@app.route('/sock/<int:sock_id>/edit/', methods=['GET', 'POST'])
def edit_sock(sock_id):
    auth_details = getAuthDetails()
    sock_to_edit = session.query(Sock).filter_by(id=sock_id).one()
    if 'username' not in login_session:
        return redirect('/signin')
    if sock_to_edit is None:
        return (
            "<script>function f() {alert('Fake path to sock');"
            + " window.history.back();}</script><body onload='f()''>")
    if sock_to_edit.email != login_session['email']:
        return (
            "<script>function f() {alert('Not your sock');"
            + "window.history.back();}</script><body onload='f()''>")
    if request.method == 'POST':
        sock_to_edit.name = request.form['name']
        sock_to_edit.description = request.form['description']
        sock_to_edit.picture = request.form['picture']
        sock_to_edit.price = request.form['price']
        session.add(sock_to_edit)
        session.commit()
        flash('Successfully updated the sock.')
        return redirect('/')
    else:
        return render_template(
            'edit_sock.html',
            auth_details=auth_details,
            sock=sock_to_edit,
            login_session=login_session)


"""
    Deleting a sock with sock_id is done here.
"""


@app.route('/sock/<int:sock_id>/delete/', methods=['GET', 'POST'])
def delete_sock(sock_id):
    auth_details = getAuthDetails()
    sock_to_edit = session.query(Sock).filter_by(id=sock_id).one()
    if 'username' not in login_session:
        return redirect('/signin')
    if sock_to_edit is None:
        return (
            "<script>function f() {alert('Fake path to sock');" +
            " window.history.back();}</script><body onload='f()''>")
    if sock_to_edit.email != login_session['email']:
        return (
            "<script>function f() {alert('Not your sock');"
            + "window.history.back();}</script><body onload='f()''>")
    else:
        session.delete(sock_to_edit)
        session.commit()
        flash('Successfully deleted the sock.')
        return redirect('/')


"""
    These functions represent creation of API endpoints.
"""


@app.route('/socks/JSON/')
def socks_json():
    socks = session.query(Sock).all()
    return jsonify(socks=[sock.serialize() for sock in socks])


@app.route('/sock/<int:sock_id>/JSON/')
def sock_json(sock_id):
    sock = session.query(Sock).filter_by(id=sock_id).one()
    if sock is None:
        return "No sock with this data."
    return jsonify(sock.serialize())


"""
    Main page show funny running socks for a while and
    redirects to the catalog of socks.
"""


@app.route('/')
def runnin_sock():
    auth_details = getAuthDetails()
    return render_template('runnin_sock.html', auth_details=auth_details)


"""
    The catalog of socks. Place where all socks can be seen
"""


@app.route('/socks')
def socks():
    auth_details = getAuthDetails()
    socks = session.query(Sock).all()
    return render_template(
        'socks.html',
        auth_details=auth_details,
        socks=socks)


"""
    The catalog of user's socks.
    If user is logged in, he is able to see own socks here.
"""


@app.route('/mysocks')
def mysocks():
    auth_details = getAuthDetails()
    socks = session.query(Sock).filter_by(email=login_session['email']).all()
    return render_template(
        'mysocks.html',
        auth_details=auth_details,
        socks=socks,
        login_session=login_session)


"""
    Point of entrance for the whole app.
"""
if __name__ == '__main__':
    auth_details = {'signin': 'signin'}
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
