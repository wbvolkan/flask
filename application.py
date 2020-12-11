import requests
from flask import Flask, jsonify, session, render_template, request, redirect, g, url_for, after_this_request
import os
import time
import urllib.request
import pathlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = 'https://94dizayn.com/images/ateslogo.png'
        urllib.request.urlretrieve(url,".png")
        return "tamamlandı"
    return "metod get"

if __name__ == '__main__':
    app.run(debug=True)
