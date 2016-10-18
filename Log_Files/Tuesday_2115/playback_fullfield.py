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

def draw_observed(frame, left, right, location, ball_centre):
    # draw observed left centre and observed right centre
    cv2.circle(frame, right, 5, (0, 255, 255), -1)
    cv2.circle(frame, left, 5, (255, 0, 0), -1)

    # draw observed heading
    LR_x = right[0] - left[0]
    LR_y = right[1] - left[1]

    perp_x = - LR_y
    perp_y = LR_x

    Line_end = list(location)
    length = 2
    Line_end[0] += perp_x * length
    Line_end[1] += perp_y * length

    cv2.arrowedLine(frame, tuple(location), tuple(Line_end), (255, 255, 255), 2)

    if ball_centre is not None:
        cv2.circle(frame, ball_centre, 5, (0, 130, 255), -1)


def draw_nao(frame, x, y, heading):
    # draw nao centre
    cv2.circle(frame, (x, y), 5, (255, 0, 255), -1)

    # draw nao heading
    length = 100
    NAO_Line_end_x = int(x + length * math.cos(heading))
    NAO_Line_end_y = int(y + length * math.sin(heading))

    cv2.arrowedLine(frame, (x, y), (NAO_Line_end_x, NAO_Line_end_y), (255, 0, 255), 2)


def draw_nao_object(frame, observed_x, observed_y, observed_h, distance, heading, label, colour):
    object_x = int(observed_x + distance * math.cos(observed_h - heading) / 10)
    object_y = int(observed_y + distance * math.sin(observed_h - heading) / 10)
    cv2.circle(frame, (object_x, object_y), 5, colour, -1)

def main():

    if os.path.exists('/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_full_field.png'):
        actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_full_field.png'
    elif os.path.exists('/home/rsa/RSA-Major-Project-2016/actual_full_field.png'):
        actual_fn = '/home/rsa/RSA-Major-Project-2016/actual_full_field.png'

    # load and unpickle the log file
    log_file = open(sys.argv[1], 'r')
    lines = pickle.load(log_file)

    cv2.namedWindow('Playback')
    cv2.createTrackbar('frame', 'Playback', 0, len(lines) - 1, nothing)

    while True:
        frame = cv2.getTrackbarPos('frame', 'Playback')

        actual_img = cv2.imread(actual_fn)
        actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

        values = lines[frame]

        draw_observed(frame=actual_img_resize, left=values['Left_centre'], right=values['Right_centre'], location=values['Location'], \
                        ball_centre=values.get('Ball_centre'))

        if values.get('Xpos') is not None:

            draw_nao(frame=actual_img_resize, x=values['Xpos'], y=values['Ypos'], heading=values['HeadingNao'])

            # draw nao balls from observed perspective (observed from fixed camera)
            list_of_balls = values['Balls']
            for i, ball in enumerate(list_of_balls):
                [b_dist, b_heading, b_orient] = [float(val) for val in ball.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=b_dist, heading=b_heading, label=i, colour=(0, 0, 255))

            # draw nao posts from observed perspective (observed from fixed camera)
            list_of_posts = values['Posts']
            for i, post in enumerate(list_of_posts):
                [p_dist, p_heading, p_orient] = [float(val) for val in post.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=p_dist, heading=p_heading, label=i, colour=(0, 255, 255))


        cv2.imshow('Playback', actual_img_resize)

        if frame + 1 < len(lines) - 1:
            cv2.setTrackbarPos('frame', 'Playback', frame + 1)
            time.sleep(0.1)

        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break

if __name__ == '__main__':
    main()
