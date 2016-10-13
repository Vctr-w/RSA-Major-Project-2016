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

def pad_adjust(corners, x_pad, y_pad):
	corners[0][0] += x_pad
	corners[1][0] -= x_pad
	corners[2][0] -= x_pad
	corners[3][0] += x_pad
	corners[0][1] += y_pad
	corners[1][1] += y_pad
	corners[2][1] -= y_pad
	corners[3][1] -= y_pad

	return corners

def rotate_clock(corners):
	return [corners[3], corners[0], corners[1], corners[2]]

def main():
	fn = '/home/vctr/Dropbox/_UNSW/Robocup/field_image_half_field.jpg'
	img = cv2.imread(fn)
	#fn = '/home/vctr/Downloads/field_image.resized.jpg'

	#img = cv2.imread(fn)
	#rows,cols,ch = img.shape

	corners_file = file('corners.txt', 'r')

	#Camera view of goal posts at the far end, the corners are from far left going clockwise
	corners = [[int(x) for x in y.split(',')] for y in corners_file.read().split('|')]

	#corners = shoulder_height_adj(corners[:])

	#Orientation such that centre circle is on the bottom
	#Starting from top left corner going clockwise
	#actual_corners = [[-FIELD_LENGTH / 2, -FIELD_WIDTH / 2], [-FIELD_LENGTH / 2, FIELD_WIDTH / 2], \
	#	[0, FIELD_WIDTH / 2], [0, -FIELD_WIDTH / 2]]

	actual_corners = [[0, 0], [FIELD_WIDTH, 0], \
		[FIELD_WIDTH, FIELD_LENGTH / 2], [0, FIELD_LENGTH / 2]]

	cv2.namedWindow('Transformed image')

	cv2.createTrackbar('x_pad', 'Transformed image', 0, 1000, nothing)
	cv2.createTrackbar('y_pad', 'Transformed image', 0, 1000, nothing)
	#cv2.createTrackbar('width', 'Transformed image', 800, 1000, nothing)
	#cv2.createTrackbar('height', 'Transformed image', 300, 1000, nothing)


	while True:
	  
		x_pad = cv2.getTrackbarPos('x_pad', 'Transformed image')
		y_pad = cv2.getTrackbarPos('y_pad', 'Transformed image')
		#width = cv2.getTrackbarPos('width', 'Transformed image')
		#height = cv2.getTrackbarPos('height', 'Transformed image')

		#new_corners = [[c00_x, c00_y], [c01_x, c01_y], [c11_x, c11_y], [c10_x, c10_y]]
		pts1 = np.float32(corners)

		#print "corners: " + str(corners)
		#print "actual corners: " + str(actual_corners)

		actual_corners_copy = [coord[:] for coord in actual_corners]

		pts2 = np.float32(pad_adjust(actual_corners_copy[:], x_pad, y_pad))
		#pts2 = np.float32(actual_corners)

		M_perspec = cv2.getPerspectiveTransform(pts1,pts2)

		dst_persp = cv2.warpPerspective(img,M_perspec,(FIELD_WIDTH, FIELD_LENGTH / 2))

		M_rot = cv2.getRotationMatrix2D((FIELD_WIDTH / 2, FIELD_LENGTH / 4),90,1)
		M_rot[0][2] += FIELD_LENGTH / 4 - FIELD_WIDTH / 2
		M_rot[1][2] += FIELD_WIDTH / 2 - FIELD_LENGTH / 4

		dst_persp_rot = cv2.warpAffine(dst_persp,M_rot, (FIELD_LENGTH / 2, FIELD_WIDTH) )
		#print dst_persp_rot.shape
		cv2.imshow('Transformed image', dst_persp_rot)
		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break


if __name__ == '__main__':
	main()