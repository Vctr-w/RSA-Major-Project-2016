import cv2
import numpy as np
import sys
import math

def nothing(*arg):
        pass

# filename = '/home/vctr/Downloads/field_image.resized.jpg'
filename = '/home/rsa/RSA-Major-Project-2016/calibrationphoto.jpg'


cv2.namedWindow('test')
cv2.createTrackbar('blocksize', 'test', 1, 100, nothing)
cv2.createTrackbar('k', 'test', 1, 50, nothing)

while True:
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    blocksize = cv2.getTrackbarPos('blocksize', 'test')
    k = 1.0 * cv2.getTrackbarPos('k', 'test') / 100
    dst = cv2.cornerHarris(gray,blocksize,3,k)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('test',img)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        breaks

'''
fn = '/home/vctr/Downloads/field_image.resized.jpg'
src = cv2.imread(fn)

cv2.namedWindow('test')
cv2.createTrackbar('thrs', 'test', 1, 100, nothing)
cv2.createTrackbar('minLineLength', 'test', 1, 100, nothing)
cv2.createTrackbar('maxLineGap', 'test', 1, 100, nothing)

while True:
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 3000, 200, apertureSize=5)
    thrs = cv2.getTrackbarPos('thrs', 'test')
    minLineLength = cv2.getTrackbarPos('minLineLength', 'test')
    maxLineGap = cv2.getTrackbarPos('maxLineGap', 'test')
    lines = cv2.HoughLinesP(edge, 1, math.pi/180.0, thrs, np.array([]), minLineLength, maxLineGap)
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)
    cv2.imshow('test', gray)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break
        '''
