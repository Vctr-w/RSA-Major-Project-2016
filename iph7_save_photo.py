import cv2
import sys
import numpy


cap = cv2.VideoCapture("http://" + sys.argv[1] + "/live?dummy=param.mjpg")

ret, frame = cap.read()
cv2.imwrite('/home/rsa/RSA-Major-Project-2016/calibrationphoto.jpg', frame)
# cv2.imshow('Frame', frame)
