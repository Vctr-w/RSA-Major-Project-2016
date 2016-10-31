import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import pickle
import os
import time

# load and unpickle the log file
log_file = open(sys.argv[1], 'r')
lines = pickle.load(log_file)

stats = {}
stats['time'] = []
stats['nao_location_error'] = []
stats['nao_heading_error'] = []
stats['ball_location_error'] = []

max_nao_location_error = -sys.maxint - 1
min_nao_location_error = sys.maxint

max_nao_heading_error = -sys.maxint - 1
min_nao_heading_error = sys.maxint

max_ball_location_error = -sys.maxint - 1
min_ball_location_error = sys.maxint


for line in lines:
    stats['time'].append(line['Time'])

    stats['nao_location_error'].append(math.sqrt((line['Location'][0] - line['Xpos']) ** 2 + \
    (line['Location'][1] - line['Ypos']) ** 2))
    if stats['nao_location_error'] > max_nao_location_error:
        max_nao_location_error = stats['nao_location_error']
    if stats['nao_location_error'] < min_nao_location_error:
        min_nao_location_error = stats['nao_location_error']

    stats['nao_heading_error'].append(abs(line['Heading']) - line['HeadingNao'])
    if stats['nao_heading_error'] > max_nao_heading_error:
        max_nao_heading_error = stats['nao_heading_error']
    if stats['nao_heading_error'] < min_nao_heading_error:
        min_nao_heading_error = stats['nao_heading_error']

    if line['Balls'] and line['Ball_centre'] is not None:
        [bdistance, bheading, borientation] = [float(val) for val in str(line['Balls'][-1]).split(",")]
        nao_ball_x = int(line['Location'][0] + bdistance * math.cos(line['Heading'] - bheading) / 10)
        nao_ball_y = int(line['Location'][1] + bdistance * math.sin(line['Heading'] - bheading) / 10)

        stats['ball_location_error'].append(math.sqrt((line['Ball_centre'][0] - nao_ball_x) ** 2 + \
        (line['Ball_centre'][1] - nao_ball_y) ** 2))

        if stats['ball_location_error'] > max_ball_location_error:
            max_ball_location_error = stats['ball_location_error']
        if stats['ball_location_error'] < min_ball_location_error:
            min_ball_location_error = stats['ball_location_error']

    else:
        stats['ball_location_error'].append(None)

plt.plot(stats['time'], stats['ball_location_error'])
plt.show()
