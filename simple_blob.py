import cv2
import numpy as np
import sys
import math
#from matplotlib import pyplot as plt

SHOULDER_HEIGHT = 439 / 10
FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def detect_blob(frame, colour):
	HSVLower_dict = {'blue': (92, 0, 0), 'red': (0,94,0)}
	HSVUpper_dict = {'blue': (124, 255, 255), 'red': (8,255,255)}
	HSVLower = HSVLower_dict[colour]
	HSVUpper = HSVUpper_dict[colour]

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "blue", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, HSVLower, HSVUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	return center


def main():
	#192.168.1.106:8080
	cap = cv2.VideoCapture('http://10.0.18.44:8080/videofeed?dummy=param.mjpg')

	cv2.namedWindow('Robot detection')

	while True:
		ret, img = cap.read()

		#Blue on right shoulder
		#Red on left shoulder
		blue_centre = detect_blob(img, 'blue')
		red_centre = detect_blob(img, 'red')

		try:
			Location = [(blue_centre[0] + red_centre[0]) / 2, (blue_centre[1] + red_centre[1]) / 2]
			Heading = math.atan((blue_centre[0] - red_centre[0] / (red_centre[1] - blue_centre[1])))

			print "Location: " + str(Location)
			print "Heading: " + str(Heading)
		except (TypeError, ZeroDivisionError) as e:
			pass

		cv2.imshow('Robot detection', img)
		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break

if __name__ == '__main__':
	main()