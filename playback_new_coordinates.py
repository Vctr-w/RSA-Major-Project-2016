import cv2
import numpy as np
import sys
import math
import pickle
import os
import time
import datetime
#from matplotlib import pyplot as plt

FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

X_OFFSET = int(118.0 / 551 * FIELD_LENGTH)
Y_OFFSET = int(128.0 / 390 * FIELD_WIDTH)

FIELD_SIZE_DIVISOR = 1

def nothing(*arg):
    pass

def draw_observed(frame, left, right, location, ball_centre):
    # draw observed left centre and observed right centre
    cv2.circle(frame, (right[0] + X_OFFSET, right[1] + Y_OFFSET), 5, (0, 255, 255), -1)
    cv2.circle(frame, (left[0] + X_OFFSET, left[1] + Y_OFFSET), 5, (255, 0, 0), -1)

    # draw observed heading
    LR_x = right[0] - left[0]
    LR_y = right[1] - left[1]

    perp_x = - LR_y
    perp_y = LR_x

    Line_end = list(location)
    length = 2
    Line_end[0] += perp_x * length
    Line_end[1] += perp_y * length

    cv2.arrowedLine(frame, tuple((location[0] + X_OFFSET, location[1] +  Y_OFFSET)), tuple((Line_end[0] + X_OFFSET, Line_end[1] + Y_OFFSET)), (255, 255, 255), 2)

    x = tuple(location)[0]
    y = tuple(location)[1]

    if ball_centre is not None:
        cv2.circle(frame, (ball_centre[0] + X_OFFSET, ball_centre[1] + Y_OFFSET), 5, (0, 130, 255), -1)


def draw_nao(frame, x, y, heading, xvar, yvar):
    # draw nao centre
    cv2.circle(frame, (x + X_OFFSET, y + Y_OFFSET), 5, (255, 0, 255), -1)

    # draw nao heading
    length = 100
    NAO_Line_end_x = int(x + length * math.cos(heading))
    NAO_Line_end_y = int(y + length * math.sin(heading))

    cv2.arrowedLine(frame, (x + X_OFFSET, y + Y_OFFSET), (NAO_Line_end_x + X_OFFSET, NAO_Line_end_y + Y_OFFSET), (255, 0, 255), 2)
    cv2.ellipse(frame, (int(x) + X_OFFSET, int(y) + Y_OFFSET), (int(yvar), int(xvar)), float(heading * 180.0/math.pi), 0.0, 360.0, (255, 0, 255), 1)


def draw_nao_object(frame, observed_x, observed_y, observed_h, distance, heading, label, colour):
    object_x = int(observed_x + distance * math.cos(observed_h - heading) / 10)
    object_y = int(observed_y + distance * math.sin(observed_h - heading) / 10)
    if label is None:
        cv2.circle(frame, (object_x + X_OFFSET, object_y + Y_OFFSET), 5, colour, -1)

    cv2.putText(frame, label, (object_x - 5 + X_OFFSET, object_y + 5 + Y_OFFSET), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

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
    isPaused = False

    while True:
        frame = cv2.getTrackbarPos('frame', 'Playback')

        actual_img = cv2.imread(actual_fn)
        actual_img_resize = cv2.resize(actual_img,((FIELD_LENGTH + 2 * X_OFFSET) / FIELD_SIZE_DIVISOR, FIELD_WIDTH + 2 * Y_OFFSET), interpolation = cv2.INTER_CUBIC)

        values = lines[frame]

        intradaytime = datetime.datetime.fromtimestamp(int(values['Time']/1000)).strftime('%H:%M:%S')
        yeartime = datetime.datetime.fromtimestamp(int(values['Time']/1000)).strftime('%d-%m-%Y')
        readabletime = str(intradaytime) + "." + str(values['Time'])[-3:] + " " + str(yeartime)

        cv2.circle(actual_img_resize, (3 + X_OFFSET, 220 + Y_OFFSET), 6, (255, 0, 255), -1)
        cv2.circle(actual_img_resize, (3 + X_OFFSET, 380 + Y_OFFSET), 6, (255, 0, 255), -1)

        if values.get('Location') is not None:

            draw_observed(frame=actual_img_resize, left=values['Left_centre'], right=values['Right_centre'], location=values['Location'], \
                            ball_centre=values.get('Ball_centre'))

        if values.get('Xpos') is not None:

            # cv2.ellipse(actual_img_resize, (int(values['Location'][0]), int(values['Location'][1])), (int(values['Yvar']), int(values['Xvar'])), float(values['Heading'] * 180.0/math.pi), 0.0, 360.0, (255, 0, 255), 1)

            draw_nao(frame=actual_img_resize, x=values['Xpos'], y=values['Ypos'], heading=values['HeadingNao'], xvar=values['Xvar'], yvar=values['Yvar'])

            # draw nao balls from observed perspective (observed from fixed camera)
            list_of_balls = values['Balls']
            for i, ball in enumerate(list_of_balls):
                [b_dist, b_heading, b_orient] = [float(val) for val in ball.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=b_dist, heading=b_heading, label=str(len(list_of_balls) - i), colour=(0, 0, 255))

            # draw nao posts from observed perspective (observed from fixed camera)

            list_of_centres = values['Centre']
            for i, centre in enumerate(list_of_centres):
                [b_dist, b_heading, b_orient] = [float(val) for val in centre.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=b_dist, heading=b_heading, label=str(len(list_of_centres) - i), colour=(0, 0, 255))

            list_of_penalties = values['Penalty']
            for i, penalty in enumerate(list_of_penalties):
                [b_dist, b_heading, b_orient] = [float(val) for val in penalties.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=b_dist, heading=b_heading, label=str(len(list_of_penalties) - i), colour=(0, 0, 255))

            list_of_posts = values['LPost']
            list_of_posts += values['ALPost']
            list_of_posts += values['HLPost']
            for i, post in enumerate(list_of_posts):
                [p_dist, p_heading, p_orient] = [float(val) for val in post.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=p_dist, heading=p_heading, label="L", colour=(0, 255, 255))

            list_of_posts = values['RPost']
            list_of_posts += values['ARPost']
            list_of_posts += values['HRPost']
            for i, post in enumerate(list_of_posts):
                [p_dist, p_heading, p_orient] = [float(val) for val in post.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=p_dist, heading=p_heading, label="R", colour=(255, 0, 0))

            list_of_posts = values['NPost']
            list_of_posts += values['APost']
            list_of_posts += values['HPost']
            for i, post in enumerate(list_of_posts):
                [p_dist, p_heading, p_orient] = [float(val) for val in post.split(",")]
                draw_nao_object(frame=actual_img_resize, observed_x=values['Location'][0], observed_y=values['Location'][1], \
                                observed_h=values['Heading'], distance=p_dist, heading=p_heading, label="N", colour=(0, 0, 0))

        cv2.putText(actual_img_resize, readabletime, (670, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv2.imshow('Playback', actual_img_resize)

        if not isPaused:
            if frame + 1 < len(lines) - 1:
                cv2.setTrackbarPos('frame', 'Playback', frame + 1)
                time.sleep(0.1)

        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break

        elif ch == 32:
            isPaused = not isPaused


if __name__ == '__main__':
    main()
