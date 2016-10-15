import cv2
import numpy as np
import sys
import math
import pickle
#from matplotlib import pyplot as plt

FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def nothing(*arg):
	pass

def main():
	actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'
	actual_img = cv2.imread(actual_fn)
 	actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

 	lines = [1, 2, 3]
	cv2.namedWindow('Playback')
	cv2.createTrackbar('frame', 'Playback', 0, len(lines), nothing)

	while True:
		frame = cv2.getTrackbarPos('frame', 'Playback')

		
		cv2.imshow('Playback', actual_img_resize)

		if frame == 1:
			cv2.setTrackbarPos('Playback', 'frame', 2)

		ch = cv2.waitKey(5) & 0xFF
		if ch == 27:
			break

if __name__ == '__main__':
	main()