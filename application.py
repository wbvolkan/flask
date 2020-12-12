from PIL import Image, ImageDraw, ImageFilter
import sys
import numpy
import cv2
import requests
from flask import Flask, jsonify, session, render_template, request, redirect, g, url_for, after_this_request, make_response
import os
import pathlib
import urllib.request

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/photo', methods=['POST','GET'])
def indexrequest():
	return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		url = "https://94dizayn.com/images/min/11.jpg"
		urllib.request.urlretrieve(url,"deneme"+".png")
		return "çalıştı"
	return"bad req"


if __name__ == '__main__':
    app.run(debug=True)
