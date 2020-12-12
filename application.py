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
		return "data"
		urllib.request.urlretrieve(url,solafis+".png")
		stand1(solafis, sagafis, tv, logo, solafis_x, solafis_y, saafis_x, saafis_y, tv_x, tv_y, logo_x, logo_y)
		return "İşlem başarılı... /photo adresinde fotoğrafı görebilirsiniz."
	if request.method == 'GET':
		return "Bad request method..."

def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def stand1(solafis,sagafis, tv, logo, solafis_x, solafis_y, saafis_x, saafis_y, tv_x, tv_y, logo_x, logo_y): # perskeptif hale getirilip importlanacak fotoğrafların isimlerini parametre olarak bekliyoruz

	# ----------------------- sol afişin başlangıç kodları ---------------------------------
	if os.path.exists(solafis+".png"):
		photo1 = Image.open(solafis+".png").convert("RGBA")   									# fonksiyondaki solafis parametresine gelen ismi açıyoruz
		width,height = photo1.size														# fotoğrafın genişlik ve yüksekliğinin değerini değişkene atıyoruz
		coeffs = find_coeffs(
			[(0, 0), (width, 0), (width, height), (0, height)],
			[(0, height * 0.066), (width, 0), (width, height), (0, height * 0.98)]) 			# fotoğrafın oynanmamış ölçülerini 1. listede , perspektif değerlerinide 2. listede find_coeffs fonksiyonuna gönderiyoruz

		transform = photo1.transform((width,height),Image.PERSPECTIVE, coeffs,Image.BICUBIC) 	# perspektif verilen fotoğrafı bir değişkene atıyoruz
		transform = transform.resize((161, 199),Image.ANTIALIAS)  								# perspektif verilen fotoğrafı yeniden boyutlandırıyoruz
		transform.save('transform_photo1.png') 													# perspektif verilen fotoğrafı kayıt ediyoruz

	# ----------------------- sol afişin sonu ---------------------------------

	# ----------------------- sağ afişin başlangıç kodları ---------------------------------
	if os.path.exists(sagafis+".png"):
		photo2 = Image.open(sagafis+".png").convert("RGBA")
		width,height = photo2.size
		coeffs = find_coeffs(
			[(0, 0), (width, 0), (width, height), (0, height)],
			[(0, 0), (width, height * 0.048), (width, height * 0.979), (0,height)])


		transform = photo2.transform((width,height),Image.PERSPECTIVE, coeffs,Image.BICUBIC)
		transform = transform.resize((156, 195),Image.ANTIALIAS)
		transform.save('transform_photo2.png')

	# ----------------------- sağ afişin sonu ---------------------------------

	# ----------------------- televizyon başlangıç  ---------------------------------
	if os.path.exists(tv+".png"):
		photo3 = Image.open(tv+".png").convert("RGBA")
		width,height = photo3.size
		coeffs = find_coeffs(
			[(0, 0), (width, 0), (width, height), (0, height)],
			[(0, 0), (width, 0), (width, height), (0,height)])


		transform = photo3.transform((width,height),Image.PERSPECTIVE, coeffs,Image.BICUBIC)
		transform = transform.resize((137, 65),Image.ANTIALIAS)
		transform.save('transform_photo3.png')

	# ----------------------- televizyon bitiş  ---------------------------------

	# ----------------------- logo başlangıç  ---------------------------------
	if os.path.exists(logo+".png"):
		photo4 = Image.open(logo+".png").convert("RGBA")
		width,height = photo4.size
		coeffs = find_coeffs(
			[(0, 0), (256, 0), (256, 256), (0, 256)],
			[(0, 30), (256, 0), (256, 256), (0, 256)])


		transform = photo4.transform((width,height),Image.PERSPECTIVE, coeffs,Image.BICUBIC)
		transform = transform.resize((60, 40),Image.ANTIALIAS)
		transform.save('transform_photo4.png')

	# ----------------------- logo bitiş  ---------------------------------

	
	im1 = Image.open('stand.png')
	back_im = im1.copy()

	if os.path.exists("transform_photo1.png"):
		im2 = Image.open('transform_photo1.png').convert("RGBA")
		back_im.paste(im2, (solafis_x, solafis_y),im2)

	if os.path.exists("transform_photo2.png"):
		im2 = Image.open('transform_photo2.png').convert("RGBA")
		back_im.paste(im2, (saafis_x, saafis_y),im2)

	if os.path.exists ('transform_photo3.png'):
		im4 = Image.open('transform_photo3.png').convert("RGBA")
		back_im.paste(im4, (tv_x, tv_y),im4)

	if os.path.exists ('transform_photo4.png'):
		im5 = Image.open('transform_photo4.png').convert("RGBA")
		back_im.paste(im5, (logo_x, logo_y),im5)

	if os.path.exists("transform_photo1.png"):
		os.remove("transform_photo1.png")

	if os.path.exists("transform_photo2.png"):
		os.remove("transform_photo2.png")

	if os.path.exists("transform_photo3.png"):
		os.remove("transform_photo3.png")

	if os.path.exists("transform_photo4.png"):
		os.remove("transform_photo4.png")					

	#back_im.save('static/rocket_pillow_paste.png', quality=95)
	transform = back_im.resize((4096, 2048),Image.ANTIALIAS)
	transform.save('static/rocket_pillow_paste.png')

		



if __name__ == '__main__':
    app.run(debug=True)
