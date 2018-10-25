from flask import Flask, request, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

APPLICATION_NAME = 'SellingSocks'


@app.route('/login')
def login():
    return render_template('login.html', auth_details=auth_details)


@app.route('/signup')
def signup():
    return render_template('signup.html', auth_details=auth_details)



@app.route('/')
def runnin_sock():
    return render_template('runnin_sock.html', auth_details=auth_details)

@app.route('/socks')
def socks():
    return render_template('socks.html', auth_details=auth_details)

if __name__ == '__main__':
    auth_details = {'login': 'login', 'signup': 'signup'}
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
