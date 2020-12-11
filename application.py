import requests
from flask import Flask, jsonify, session, render_template, request, redirect, g, url_for, after_this_request
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'yaani' and password == '12345' :
            session['user'] = request.form['username']
            return redirect(url_for('yaani'))        	
        if username == 'albaraka' and password == '123' :
        	session['sifre'] = request.form['username']
        	return redirect(url_for('albaraka'))
        else:
        	value=' Invalid username or password. '
       		return render_template('index.html',value=value)
    return render_template('index.html')


@app.route('/yaani')
def yaani():
    if g.user:
        return render_template('yaani.html')

    return redirect(url_for('index'))

@app.route('/albaraka')
def albaraka():
    if g.sifre:
        return render_template('albaraka.html')
        

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    g.sifre = None
    if 'sifre' in session:
    	g.sifre = session['sifre']

@app.route('/yaanirequest', methods=['POST','GET'])
def yaanireq():
    if request.method == 'POST':
        DATA = request.get_json()
        DATA['chatId'] = 12345
        bot = requests.post('http://31.25.168.85:8894/yaani', json=DATA)
        resp = bot.json()['text']
        return resp


@app.route('/albarakarequest', methods=['POST','GET'])
def albarakareq():
    if request.method == 'POST':
        DATA = request.get_json()
        DATA['chatId'] = 12345
        bot = requests.post('http://31.25.168.85:8899/albaraka', json=DATA)
        resp = bot.json()['text']
        return resp

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    session.pop('sifre', None)
    return redirect(url_for('index')),202

if __name__ == '__main__':
    app.run(debug=True)