import cv2
import numpy as np
import sys
import math
import pickle
import os
import time
#from matplotlib import pyplot as plt

FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

def nothing(*arg):
    pass


def main():

    if os.path.exists('/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/field.png'):
        actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/field.png'
    elif os.path.exists('/home/rsa/RSA-Major-Project-2016/field.png'):
        actual_fn = '/home/rsa/RSA-Major-Project-2016/field.png'
    actual_img = cv2.imread(actual_fn)
    actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / 2, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

    log_file = open(sys.argv[1], 'r')
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

        cv2.circle(actual_img_resize, (values['Xpos'], values['Ypos']), 5, (255, 0, 255), -1)

        length = 100
        NAO_Line_end_x = int(values['Xpos'] + length * math.cos(values['HeadingNao']))
        NAO_Line_end_y = int(values['Ypos'] + length * math.sin(values['HeadingNao']))

        cv2.arrowedLine(actual_img_resize, (values['Xpos'], values['Ypos']), (NAO_Line_end_x, NAO_Line_end_y), (255, 0, 255), 2)

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

        if frame + 1 < len(lines) - 1:
            cv2.setTrackbarPos('frame', 'Playback', frame + 1)
            time.sleep(0.1)

        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break

if __name__ == '__main__':
    main()
