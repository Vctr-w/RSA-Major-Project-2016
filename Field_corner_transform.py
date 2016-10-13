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
cv2.createTrackbar('thrs1', 'test', 3000, 10000, nothing)
cv2.createTrackbar('thrs2', 'test', 200, 1000, nothing)
cv2.createTrackbar('thrs', 'test', 1, 100, nothing)
cv2.createTrackbar('minLineLength', 'test', 100, 1000, nothing)
cv2.createTrackbar('maxLineGap', 'test', 10, 100, nothing)

while True:
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thrs1 = cv2.getTrackbarPos('thrs1', 'test')
    thrs2 = cv2.getTrackbarPos('thrs2', 'test')
    edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
    thrs = cv2.getTrackbarPos('thrs', 'test')
    minLineLength = cv2.getTrackbarPos('minLineLength', 'test')
    maxLineGap = cv2.getTrackbarPos('maxLineGap', 'test')
    
    lines = cv2.HoughLinesP(edge,1,np.pi/180,thrs,np.array([]), minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(gray,(x1,y1),(x2,y2),(0,255,0),2)
    '''
    lines = cv2.HoughLinesP(edge, 1, math.pi/180.0, thrs, np.array([]), minLineLength, maxLineGap)
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)
    '''
    cv2.imshow('test', gray)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break


'''
    edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
    vis = src.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow('test', vis)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break

'''


'''
#Code to determine what Canny parameters to use
#3000, 200

fn = '/home/vctr/Downloads/field_image.resized.jpg'
src = cv2.imread(fn)

cv2.namedWindow('test')
cv2.createTrackbar('thrs1', 'test', 0, 100000, nothing)
cv2.createTrackbar('thrs2', 'test', 0, 9000, nothing)

while True:
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thrs1 = cv2.getTrackbarPos('thrs1', 'test')
    thrs2 = cv2.getTrackbarPos('thrs2', 'test')
    edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
    vis = src.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow('test', vis)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break
'''


'''

    thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
    thrs2 = cv2.getTrackbarPos('thrs2', 'edge')

    src = cv2.imread(fn)
    dst = cv2.Canny(src, thrs1, thrs2)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)


    vis = img.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow('test', vis)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break

    cv2.imshow("test", cdst)
    cv2.waitKey(0)




lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
a,b,c = lines.shape
for i in range(a):
    cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)


print(__doc__)

try:
    fn = sys.argv[1]
except:
    fn = 0

def nothing(*arg):
    pass

cv2.namedWindow('edge')
cv2.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
cv2.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)

cap = video.create_capture(fn)
while True:
    flag, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
    thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
    edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
    vis = img.copy()
    vis = np.uint8(vis/2.)
    vis[edge != 0] = (0, 255, 0)
    cv2.imshow('edge', vis)
    ch = cv2.waitKey(5) & 0xFF
    if ch == 27:
        break
cv2.destroyAllWindows()


if True: # HoughLinesP
    lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)

else:    # HoughLines
    lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
    a,b,c = lines.shape
    for i in range(a):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0, y0 = a*rho, b*rho
        pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
        pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
        cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.CV_AA)

cv2.imshow("source", src)
cv2.imshow("detected lines", cdst)
cv2.waitKey(0)
'''