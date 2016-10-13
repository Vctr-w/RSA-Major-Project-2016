import cv2
import numpy as np
import sys
import math
#from matplotlib import pyplot as plt

SHOULDER_HEIGHT = 439 / 10
FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def nothing(*arg):
        pass

def shoulder_height_adj(corners):
	far_width = (corners[0][0] + corners[1][0]) / 2
	near_width = (corners[2][0] + corners[3][0]) / 2

	ratio = 1.0 * SHOULDER_HEIGHT / FIELD_WIDTH

	far_width_adj = ratio * far_width
	near_width_adj = ratio * near_width

	#Move them higher - Since (0, 0) is top left corner, this is subtraction
	corners[0][1] -= far_width_adj
	corners[1][1] -= far_width_adj
	corners[2][1] -= near_width_adj
	corners[3][1] -= near_width_adj

	return corners

def detect_blob(frame, target_frame, colour):
	HSVLower_dict = {'blue': (92, 155, 0), 'red': (0,200,0), 'yellow': (21, 104, 103)}
	HSVUpper_dict = {'blue': (124, 255, 255), 'red': (19,255,255), 'yellow': (33, 255, 255)}
	Colour_dict = {'blue': (255, 0, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255)}
	colour_BGR = Colour_dict[colour]
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
			cv2.circle(target_frame, (int(x), int(y)), int(radius),
				colour_BGR, 2)
			cv2.circle(target_frame, center, 5, colour_BGR, -1)
	return center


def main():
	actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'
	actual_img = cv2.imread(actual_fn)
 	actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

	cap = cv2.VideoCapture('http://10.0.18.6:8080/videofeed?dummy=param.mjpg')

	corners_file = file('corners.txt', 'r')

	#Camera view of goal posts at the far end, the corners are from far left going clockwise
	corners = [[int(x) for x in y.split(',')] for y in corners_file.read().split('|')]

	corners = shoulder_height_adj(corners[:])

	#Orientation such that centre circle is on the bottom
	#Starting from top left corner going clockwise
	#actual_corners = [[-FIELD_LENGTH / 2, -FIELD_WIDTH / 2], [-FIELD_LENGTH / 2, FIELD_WIDTH / 2], \
	#	[0, FIELD_WIDTH / 2], [0, -FIELD_WIDTH / 2]]

	actual_corners = [[0, 0], [FIELD_WIDTH, 0], \
		[FIELD_WIDTH, FIELD_LENGTH / 2], [0, FIELD_LENGTH / 2]]

	cv2.namedWindow('Robot detection')

	while True:
		ret, img = cap.read()

		pts1 = np.float32(corners)

		pts2 = np.float32(actual_corners)

		M_perspec = cv2.getPerspectiveTransform(pts1,pts2)

		dst_persp = cv2.warpPerspective(img,M_perspec,(FIELD_WIDTH, FIELD_LENGTH / 2))

		M_rot = cv2.getRotationMatrix2D((FIELD_WIDTH / 2, FIELD_LENGTH / 4),90,1)
		M_rot[0][2] += FIELD_LENGTH / 4 - FIELD_WIDTH / 2
		M_rot[1][2] += FIELD_WIDTH / 2 - FIELD_LENGTH / 4

		dst_persp_rot = cv2.warpAffine(dst_persp,M_rot, (FIELD_LENGTH / 2, FIELD_WIDTH) )
		#print dst_persp_rot.shape

		actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_CUBIC)

		#Blue on right shoulder
		#Red on left shoulder
		blue_centre = detect_blob(dst_persp_rot, actual_img_resize, 'blue')
		yellow_centre = detect_blob(dst_persp_rot, actual_img_resize, 'yellow')

		try:
			Location = [(blue_centre[0] + yellow_centre[0]) / 2, (blue_centre[1] + yellow_centre[1]) / 2]
			neg_Gradient = (blue_centre[0] - yellow_centre[0] / (yellow_centre[1] - blue_centre[1]))
			Heading = math.atan(neg_Gradient)

			Line_end = Location[:]
			run = 100
			Line_end[0] += run
			Line_end[1] += run * neg_Gradient

			#cv2.line(actual_img_resize, Location, Line_end, (0, 0, 0), 5)

			print "Location: " + str(Location)
			print "Heading: " + str(Heading)
		except (TypeError, ZeroDivisionError) as e:
			pass

		cv2.imshow('Robot detection', actual_img_resize) #dst_persp_rot)
		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break

if __name__ == '__main__':
	main()