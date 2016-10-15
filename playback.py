import cv2
import numpy as np
import sys
import math
#from matplotlib import pyplot as plt

FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10




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

	cv2.namedWindow('Playback')

	lines = []

	with open('log.txt') as f:
		for line in f:
			lines.append(line)


		actual_img = cv2.imread(actual_fn)
 		actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)
		
		print line

			'''



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

			cv2.line(actual_img_resize, (Location[0], Location[1]), (Line_end[0], Line_end[1]), (0, 0, 0), 5)

			print "Location: " + str(Location)
			print "Heading: " + str(Heading)
		except (TypeError, ZeroDivisionError) as e:
			pass

		cv2.imshow('Robot detection', actual_img_resize) #dst_persp_rot)
		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break

			'''

if __name__ == '__main__':
	main()