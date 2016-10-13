import cv2
import numpy as np
import sys
import math

def nothing(*arg):
        pass
        
#fn = '/home/vctr/Downloads/Sudoku.jpg'
fn = '/home/vctr/Downloads/field_image.resized.jpg'
src = cv2.imread(fn)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


cv2.namedWindow('test')
cv2.createTrackbar('thrs1', 'test', 3000, 100000, nothing)
cv2.createTrackbar('thrs2', 'test', 200, 10000, nothing)
cv2.createTrackbar('thrs', 'test', 3, 100, nothing)
cv2.createTrackbar('minLineLength', 'test', 100, 1000, nothing)
cv2.createTrackbar('maxLineGap', 'test', 10, 100, nothing)

while True:
    ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thrs1 = cv2.getTrackbarPos('thrs1', 'test')
    thrs2 = cv2.getTrackbarPos('thrs2', 'test')
    edge = cv2.Canny(thresh1, thrs1, thrs2, apertureSize=5)
    cv2.imshow('test', edge)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break

'''

while True:
    ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thrs1 = cv2.getTrackbarPos('thrs1', 'test')
    thrs2 = cv2.getTrackbarPos('thrs2', 'test')
    edge = cv2.Canny(thresh1, thrs1, thrs2, apertureSize=5)

    thrs = cv2.getTrackbarPos('thrs', 'test')
    minLineLength = cv2.getTrackbarPos('minLineLength', 'test')
    maxLineGap = cv2.getTrackbarPos('maxLineGap', 'test')
    
    lines = cv2.HoughLinesP(edge,1,np.pi/180,thrs,np.array([]), minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(thresh1,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow('test', thresh1)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break
'''