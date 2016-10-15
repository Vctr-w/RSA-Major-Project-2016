import cv2
import numpy as np
import sys
import math
#from matplotlib import pyplot as plt

SHOULDER_HEIGHT = 439 / 10
FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def detect_blob(frame, colour):
	HSVLower_dict = {'blue': (92, 155, 0), 'red': (0,200,0), 'yellow': (21, 104, 103)}
	HSVUpper_dict = {'blue': (124, 255, 255), 'red': (19,255,255), 'yellow': (33, 255, 255)}
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
	# if len(cnts) > 0:
        # return cnts;
		# # find the largest contour in the mask, then use
		# # it to compute the minimum enclosing circle and
		# # centroid
		# c = max(cnts, key=cv2.contourArea)
		# ((x, y), radius) = cv2.minEnclosingCircle(c)
		# M = cv2.moments(c)
		# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #
		# # only proceed if the radius meets a minimum size
		# if radius > 10:
		# 	# draw the circle and centroid on the frame,
		# 	# then update the list of tracked points
		# 	cv2.circle(target_frame, (int(x), int(y)), int(radius),
		# 		colour_BGR, 2)
		# 	cv2.circle(target_frame, center, 5, colour_BGR, -1)

	return cnts;

def find_yellow_and_blue(frame, target_frame, min_radius, min_distance):
    Colour_dict = {'blue': (255, 0, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255)}
    bluecnts = detect_blob(frame, 'blue')
    yellowcnts = detect_blob(frame, 'yellow')
    if bluecnts is None or yellowcnts is None:
        return ()
    for bc in bluecnts:
        ((xb, yb), bradius) = cv2.minEnclosingCircle(bc)
        if (bradius < min_radius):
            continue
        bM = cv2.moments(bc)
        bx = int(bM["m10"] / bM["m00"])
        by = int(bM["m01"] / bM["m00"])
        bcentre = (bx, by)
        for yc in yellowcnts:
            ((xy, yy), yradius) = cv2.minEnclosingCircle(yc)
            if (yradius < min_radius):
                continue
            yM = cv2.moments(yc)
            yx = int(yM["m10"] / yM["m00"])
            yy = int(yM["m01"] / yM["m00"])
            ycentre = (yx, yy)
            if (bx - yx)**2 + (by - yy)**2 < min_distance**2:
                cv2.circle(target_frame, (int(xb), int(yb)), int(bradius), Colour_dict['blue'], 2)
                cv2.circle(target_frame, (int(xy), int(yy)), int(yradius), Colour_dict['yellow'], 2)
                cv2.circle(target_frame, bcentre, 5, Colour_dict['blue'], -1)
                cv2.circle(target_frame, ycentre, 5, Colour_dict['yellow'], -1)
                return (bcentre, ycentre)


def main():
    #192.168.1.106:8080
    #http://10.0.18.6:8080/videofeed?dummy=param.mjpg
    cap = cv2.VideoCapture('http://10.0.18.6:8080/videofeed?dummy=param.mjpg')

    cv2.namedWindow('Robot detection')

    while True:
        ret, img = cap.read()

        #Blue on right shoulder
        #yellow on left shoulder
        result = find_yellow_and_blue(img, img, min_radius=5, min_distance=400)
        if result is not None:
            (blue_centre, yellow_centre) = result

            try:
                Location = [(blue_centre[0] + yellow_centre[0]) / 2, (blue_centre[1] + yellow_centre[1]) / 2]
                neg_gradient = (blue_centre[0] - yellow_centre[0] / (yellow_centre[1] - blue_centre[1]))
                Heading = math.atan(neg_gradient)

                Line_end = Location[:]
                run = 100
                Line_end[0] -= run
                Line_end[1] -= run * neg_gradient

                cv2.line(img, (Location[0], Location[1]), (Line_end[0], Line_end[1]), (0, 0, 0), 5)
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
