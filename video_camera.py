import cv2
cap = cv2.VideoCapture('http://129.94.233.45/live?dummy=param.mjpg')
# cap = cv2.VideoCapture('http://192.168.1.102:8080/videofeed?dummy=param.mjpg')

while True:
  ret, frame = cap.read()
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    exit(0)
