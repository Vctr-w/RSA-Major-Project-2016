import cv2
import sys
import numpy, os

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " [CAMERA IP]")
    exit(1)

cap = cv2.VideoCapture("http://" + sys.argv[1] + "/live?dummy=param.mjpg")

ret, frame = cap.read()
cv2.imwrite(os.getcwd() + '/calibrationphoto.jpg', frame)
print("frame saved as calibrationphoto.jpg")
# cv2.imshow('Frame', frame)
