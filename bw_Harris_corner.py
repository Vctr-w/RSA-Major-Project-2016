import cv2
import numpy as np
import sys
import math

def nothing(*arg):
        pass

#fn = '/home/vctr/Downloads/Sudoku.jpg'
#fn = '/home/vctr/Downloads/field_image.resized.jpg'
fn = '/home/rsa/RSA-Major-Project-2016/calibrationphoto.jpg'

src = cv2.imread(fn)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('test')
cv2.createTrackbar('blocksize', 'test', 1, 100, nothing)
cv2.createTrackbar('k', 'test', 1, 50, nothing)

while True:
    ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    blocksize = cv2.getTrackbarPos('blocksize', 'test')
    k = 1.0 * cv2.getTrackbarPos('k', 'test') / 100
    dst = cv2.cornerHarris(thresh1,blocksize,3,k)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    thresh1[dst>0.01*dst.max()]=True

    cv2.imshow('test',thresh1)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        breaks
