from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import os
import xlwt as xw
import xlrd as xr
from xlutils.copy import copy as x_copy

shapePredictor = "shape_predictor_68_face_landmarks.dat"

def getEyes(in_image):
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(shapePredictor)
	image = cv2.imread(in_image)
	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 1)

	for (i, rect) in enumerate(rects):
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

	left_eye_x, left_eye_y, right_eye_x, right_eye_y = [], [], [], []
	for i in range(6):
		left_eye_x.append(shape[36+i][0])
		left_eye_y.append(shape[36+i][1])
		right_eye_x.append(shape[42+i][0])
		right_eye_y.append(shape[42+i][1])

	return left_eye_x, left_eye_y, right_eye_x, right_eye_y


def writeData(subject_code):
	url = './'+subject_code+'V'
	path, dirs, files = os.walk(url).__next__()
	file_count = len(files)
	openfile = xr.open_workbook('data.xls', formatting_info=True)
	excel_copy = x_copy(openfile)
	sheet = excel_copy.add_sheet(subject_code)
	for i in range(file_count):
		img = url+'/'+subject_code+'V'+str(i)+'.jpg'
		print(img)
		try:
			left_eye_x, left_eye_y, right_eye_x, right_eye_y = getEyes(img)
		except:
			left_eye_x, left_eye_y, right_eye_x, right_eye_y =[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0],[0,0,0,0,0,0]
			print('error in file: ', str(i))
		for j in range(6):
			col = j * 4
			a = str(left_eye_x[j])
			b = str(left_eye_y[j])
			c = str(right_eye_x[j])
			d = str(right_eye_y[j])
			sheet.write(1+i,col+1,a)
			sheet.write(1+i,col+2,b)
			sheet.write(1+i,col+3,c)
			sheet.write(1+i,col+4,d)




	excel_copy.save('data.xls')




#left_eye_x, left_eye_y, right_eye_x, right_eye_y = getEyes("./images/example_01.jpg")
#writeData('E031M')
codes = ['A001']
for code in codes:
	writeData(code)