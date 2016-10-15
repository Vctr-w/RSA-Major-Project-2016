import cv2
import numpy as np
import sys
import math
import pickle
import os
#from matplotlib import pyplot as plt

FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def nothing(*arg):
        pass

def main():

    if os.path.exists('/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'):
        actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'
    elif os.path.exists('/home/rsa/RSA-Major-Project-2016/actual_field_half.png'):
        actual_fn = '/home/rsa/RSA-Major-Project-2016/actual_field_half.png'
	actual_img = cv2.imread(actual_fn)
 	actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

	log_file = open('log_file.txt', 'r')
	lines = pickle.load(log_file)

	cv2.namedWindow('Playback')
	cv2.createTrackbar('frame', 'Playback', 0, len(lines) - 1, nothing)

	while True:
		frame = cv2.getTrackbarPos('frame', 'Playback')

		actual_img = cv2.imread(actual_fn)
		actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

		values = lines[frame]

		left_centre = values['Left_centre']
		right_centre = values['Right_centre']

		cv2.circle(actual_img_resize, left_centre, 5, (0, 130, 255), -1)
		cv2.circle(actual_img_resize, right_centre, 5, (255, 0, 0), -1)

		LR_x = right_centre[0] - left_centre[0]
		LR_y = right_centre[1] - left_centre[1]

		perp_x = - LR_y
		perp_y = LR_x

		Location = values['Location']
		Line_end = Location[:]
		length = 2
		Line_end[0] += perp_x * length
		Line_end[1] += perp_y * length

		cv2.arrowedLine(actual_img_resize, tuple(Location), tuple(Line_end), (255, 255, 255), 2)

		cv2.imshow('Playback', actual_img_resize)

		#cv2.setTrackbarPos('Playback', 'frame', frame + 1)

		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break




	'''


		milliseconds | xpos | xvar | ypos | yvar | heading | headingvar | balls | rrcoord (distance heading ) |
			posts | rrcoord |

		ball | rrcoord (distance heading ) | ball | rrcoord (distance heading ) |

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
