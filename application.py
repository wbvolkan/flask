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
	data =[]
	url2= "https://94dizayn.com/images/min/"
	url = "https://94dizayn.com/images/min/"
	if request.method == 'POST':
		stand = request.get_json()["stand"]
		solafis = request.get_json()["solafis"]
		sagafis = request.get_json()["sagafis"]
		tv = request.get_json()["tv"]
		logo = request.get_json()["logo"]
		solafis_x = request.get_json()["solafis_x"]
		solafis_y = request.get_json()["solafis_y"]
		saafis_x = request.get_json()["sagafis_x"]
		saafis_y = request.get_json()["sagafis_y"]
		tv_x = request.get_json()["tv_x"]
		tv_y = request.get_json()["tv_y"]
		logo_x = request.get_json()["logo_x"]
		logo_y = request.get_json()["logo_y"]
		data.append(sagafis)
		data.append(solafis)
		data.append(tv)
		data.append(logo)
		for e in data:
			if e != "none" :
				url = url + "/"+e+".jpg"
				print(url)
				urllib.request.urlretrieve(url,e+".png")
				url = url2
		return "İşlem başarılı... /photo adresinde fotoğrafı görebilirsiniz."
	if request.method == 'GET':
		return "Bad request method..."
	return "selam"

if __name__ == '__main__':
    app.run(debug=True)
