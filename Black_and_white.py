import cv2
import numpy as np
import sys
import math

def nothing(*arg):
        pass
        
#fn = '/home/vctr/Downloads/Sudoku.jpg'
fn = '/home/vctr/Downloads/field_image.resized.jpg'
src = cv2.imread(fn)

cv2.namedWindow('test')
cv2.createTrackbar('thresh', 'test', 100, 255, nothing)

while True:
	gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	thresh = cv2.getTrackbarPos('thresh', 'test')
	ret,thresh1 = cv2.threshold(gray,thresh,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imshow('test', thresh1)
	ch = cv2.waitKey(5) & 0xFF
	if ch == 27:
		break