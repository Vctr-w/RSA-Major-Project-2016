import cv2
import numpy as np
import sys
import math
import time
import pickle
import os
#from matplotlib import pyplot as plt

BALL_HEIGHT = 60.0 / 10
SHOULDER_HEIGHT = 439.0 / 10
FIELD_WIDTH = 6000 / 10
FIELD_LENGTH = 9000 / 10

X_OFFSET = int(118.0 / 551 * FIELD_LENGTH)
Y_OFFSET = int(128.0 / 390 * FIELD_WIDTH)

if len(sys.argv) > 1:
    if (sys.argv[1] == "-h"):
        HALF_FIELD_ONLY = True
else:
    HALF_FIELD_ONLY = False

if HALF_FIELD_ONLY:
    FIELD_SIZE_DIVISOR = 2
else:
    FIELD_SIZE_DIVISOR = 1

def nothing(*arg):
        pass

def ball_height_adj(bcorners):
    far_width = (bcorners[0][0] + bcorners[1][0]) / 2
    near_width = (bcorners[2][0] + bcorners[3][0]) / 2

    ratio = 1.0 * BALL_HEIGHT / FIELD_WIDTH

    far_width_adj = ratio * far_width
    near_width_adj = ratio * near_width

    #Move them higher - Since (0, 0) is top left corner, this is subtraction
    bcorners[0][1] -= far_width_adj
    bcorners[1][1] -= far_width_adj
    bcorners[2][1] -= near_width_adj
    bcorners[3][1] -= near_width_adj

    return bcorners

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

def detect_blob(frame, colour):
	HSVLower_dict = {'blue': (92, 155, 150), 'red': (0,150,150), 'yellow': (26, 40, 200), 'orange': (0, 170, 130)}
	HSVUpper_dict = {'blue': (124, 255, 255), 'red': (4,255,255), 'yellow': (31, 255, 255), 'orange': (25, 255, 255)}
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


def find_ball(img, target_frame, actual_corners, ball_corners, min_radius, colour):
    Colour_dict = {'blue': (255, 0, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'orange': (0, 130, 255)}

    pts1 = np.float32(ball_corners)

    pts2 = np.float32(actual_corners)

    M_perspec = cv2.getPerspectiveTransform(pts1,pts2)

    dst_persp = cv2.warpPerspective(img,M_perspec,(FIELD_WIDTH, FIELD_LENGTH))

    M_rot = cv2.getRotationMatrix2D((FIELD_WIDTH / 2, FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR),90,1)
    M_rot[0][2] += FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR- FIELD_WIDTH / 2
    M_rot[1][2] += FIELD_WIDTH / 2 - FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR

    frame = cv2.warpAffine(dst_persp,M_rot, (FIELD_LENGTH / FIELD_SIZE_DIVISOR, FIELD_WIDTH) )

    ballcnts = detect_blob(frame, colour)
    maxbc = None
    maxradius = 0
    for bc in ballcnts:
        ((circlex, circley), circleradius) = cv2.minEnclosingCircle(bc)
        if circleradius > maxradius:
            maxbc = bc
            maxradius = circleradius

    if maxbc is not None:
        ((circlex, circley), circleradius) = cv2.minEnclosingCircle(maxbc)
        M = cv2.moments(maxbc)
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        cv2.circle(target_frame, (int(circlex) + X_OFFSET, int(circley) + Y_OFFSET), int(circleradius), Colour_dict[colour], 2)
        cv2.circle(target_frame, (x + X_OFFSET, y + Y_OFFSET), 5, Colour_dict[colour], -1)

        #return (x + X_OFFSET, y + Y_OFFSET)
        return (x, y)


def find_left_and_right(img, target_frame, actual_corners, adjusted_corners, min_radius, min_distance, left, right, side):
    Colour_dict = {'blue': (255, 0, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'orange': (0, 130, 255)}

    pts1 = np.float32(adjusted_corners)

    pts2 = np.float32(actual_corners)

    M_perspec = cv2.getPerspectiveTransform(pts1,pts2)

    dst_persp = cv2.warpPerspective(img,M_perspec,(FIELD_WIDTH, FIELD_LENGTH / FIELD_SIZE_DIVISOR))

    M_rot = cv2.getRotationMatrix2D((FIELD_WIDTH / 2, FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR),90,1)
    M_rot[0][2] += FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR - FIELD_WIDTH / 2
    M_rot[1][2] += FIELD_WIDTH / 2 - FIELD_LENGTH / 2 / FIELD_SIZE_DIVISOR

    frame = cv2.warpAffine(dst_persp,M_rot, (FIELD_LENGTH / FIELD_SIZE_DIVISOR, FIELD_WIDTH) )
    #print dst_persp_rot.shape

    rightcnts = detect_blob(frame, right)
    leftcnts = detect_blob(frame, left)

    if rightcnts is not None and leftcnts is not None:
        for rc in rightcnts:
            ((xr, yr), rradius) = cv2.minEnclosingCircle(rc)
            if (rradius < min_radius):
                continue
            rM = cv2.moments(rc)
            rx = int(rM["m10"] / rM["m00"])
            ry = int(rM["m01"] / rM["m00"])
            rcentre = (rx + X_OFFSET, ry + Y_OFFSET)
            for lc in leftcnts:
                ((xl, yl), lradius) = cv2.minEnclosingCircle(lc)
                if (lradius < min_radius):
                    continue
                lM = cv2.moments(lc)
                lx = int(lM["m10"] / lM["m00"])
                ly = int(lM["m01"] / lM["m00"])
                lcentre = (lx + X_OFFSET, ly + Y_OFFSET)
                if (rx - lx)**2 + (ry - ly)**2 < min_distance**2:
                    cv2.circle(target_frame, (int(xr) + X_OFFSET, int(yr) + Y_OFFSET), int(rradius), Colour_dict[right], 2)
                    cv2.circle(target_frame, (int(xl) + X_OFFSET, int(yl) + Y_OFFSET), int(lradius), Colour_dict[left], 2)
                    cv2.circle(target_frame, rcentre, 5, Colour_dict[right], -1)
                    cv2.circle(target_frame, lcentre, 5, Colour_dict[left], -1)
                    return (rcentre, lcentre)

    if rightcnts is None and leftcnts is not None:
        sidecnts = detect_blob(frame, side)
        if sidecnts is None:
            return None

        maxbc = None
        maxradius = 0
        for bc in leftcnts:
            ((circlex, circley), circleradius) = cv2.minEnclosingCircle(bc)
            if circleradius > maxradius:
                maxbc = bc
                maxradius = circleradius

        if maxbc is not None:
            ((circlex, circley), circleradius) = cv2.minEnclosingCircle(maxbc)
            M = cv2.moments(maxbc)
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

            for sc in sidecnts:
                ((xl, yl), sradius) = cv2.minEnclosingCircle(sc)
                if (sradius < min_radius):
                    continue
                sM = cv2.moments(sc)
                sx = int(sM["m10"] / sM["m00"])
                sy = int(sM["m01"] / sM["m00"])
                scentre = (sx, sy)
                if (x - sx)**2 + (y - sy)**2 < min_distance**2:
                    cv2.circle(target_frame, (int(circlex) + X_OFFSET, int(circley) + Y_OFFSET), int(circleradius), Colour_dict[colour], 2)
                    cv2.circle(target_frame, (x + X_OFFSET, y + Y_OFFSET), 5, Colour_dict[colour], -1)

                    return ((x + 5 + X_OFFSET, y + 5 + Y_OFFSET), (x + X_OFFSET, y + Y_OFFSET))

    if rightcnts is not None and leftcnts is None:
        sidecnts = detect_blob(frame, side)
        if sidecnts is None:
            return None

        maxbc = None
        maxradius = 0
        for bc in rightcnts:
            ((circlex, circley), circleradius) = cv2.minEnclosingCircle(bc)
            if circleradius > maxradius:
                maxbc = bc
                maxradius = circleradius

        if maxbc is not None:
            ((circlex, circley), circleradius) = cv2.minEnclosingCircle(maxbc)
            M = cv2.moments(maxbc)
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

            for sc in sidecnts:
                ((xl, yl), sradius) = cv2.minEnclosingCircle(sc)
                if (sradius < min_radius):
                    continue
                sM = cv2.moments(sc)
                sx = int(sM["m10"] / sM["m00"])
                sy = int(sM["m01"] / sM["m00"])
                scentre = (sx, sy)
                if (x - sx)**2 + (y - sy)**2 < min_distance**2:
                    cv2.circle(target_frame, (int(circlex) + X_OFFSET, int(circley) + Y_OFFSET), int(circleradius), Colour_dict[colour], 2)
                    cv2.circle(target_frame, (x + X_OFFSET, y + Y_OFFSET), 5, Colour_dict[colour], -1)

                    #return ((x + X_OFFSET, y + Y_OFFSET), (x + 5 + X_OFFSET, y + 5 + Y_OFFSET))
                    return ((x, y), (x + 5, y + 5))


def main():
    if HALF_FIELD_ONLY:
        if os.path.exists('/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'):
            actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_field_half.png'
        elif os.path.exists('/home/rsa/RSA-Major-Project-2016/actual_field_half.png'):
            actual_fn = '/home/rsa/RSA-Major-Project-2016/actual_field_half.png'
    else:
        if os.path.exists('/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_full_field.png'):
            actual_fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/actual_full_field.png'
        elif os.path.exists('/home/rsa/RSA-Major-Project-2016/actual_full_field.png'):
            actual_fn = '/home/rsa/RSA-Major-Project-2016/actual_full_field.png'

    actual_img = cv2.imread(actual_fn)
    actual_img_resize = cv2.resize(actual_img,(FIELD_LENGTH / FIELD_SIZE_DIVISOR, FIELD_WIDTH), interpolation = cv2.INTER_LINEAR)

    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://10.0.18.6:8080/videofeed?dummy=param.mjpg')
    cap = cv2.VideoCapture('http://129.94.233.98/live?dummy=param.mjpg')
    # img = cv2.imread('/Users/Martin/Github/RSA-Major-Project-2016/field_image_colour_cal_2.JPG')

    corners_file = file('corners.txt', 'r')

    #log_file = file('log_file.txt', 'w')

    #Camera view of goal posts at the far end, the corners are from far left going clockwise
    corners = [[int(x) for x in y.split(',')] for y in corners_file.read().split('|')]

    ball_corners = []
    for corner_list in corners:
        ball_corners.append(list(corner_list))

    ball_corners = ball_height_adj(ball_corners)

    adjusted_corners = shoulder_height_adj(corners[:])



    #Orientation such that centre circle is on the bottom
    #Starting from top left corner going clockwise
    #actual_corners = [[-FIELD_LENGTH / 2, -FIELD_WIDTH / 2], [-FIELD_LENGTH / 2, FIELD_WIDTH / 2], \
    #	[0, FIELD_WIDTH / 2], [0, -FIELD_WIDTH / 2]]

    actual_corners = [[0, 0], [FIELD_WIDTH, 0], \
    	[FIELD_WIDTH, FIELD_LENGTH / 2], [0, FIELD_LENGTH / 2]]

    cv2.namedWindow('Robot detection')

    frames = []

    while True:
        ret, img = cap.read()

        actual_img_resize = cv2.resize(actual_img,((FIELD_LENGTH + 2 * X_OFFSET) / FIELD_SIZE_DIVISOR, FIELD_WIDTH + 2 * Y_OFFSET), interpolation = cv2.INTER_CUBIC)

        ball_centre = find_ball(img, actual_img_resize, actual_corners, ball_corners, min_radius = 0, colour='orange')

        Location = None
        Heading = None
        left_centre = None
        right_centre = None

        #Blue on right shoulder
        #yellow on left shoulder
        result = find_left_and_right(img, actual_img_resize, actual_corners, adjusted_corners, min_radius=0, min_distance=50, \
        left='yellow', right='blue', side='red')
        if result is not None:
            (left_centre, right_centre) = result
        # right_centre = detect_blob(dst_persp_rot, actual_img_resize, 'right')
        # left_centre = detect_blob(dst_persp_rot, actual_img_resize, 'left')
        # right_centre = detect_blob(dst_persp_rot, dst_persp_rot, 'right')
        # left_centre = detect_blob(dst_persp_rot, dst_persp_rot, 'left')

            try:
                Location = [(right_centre[0] + left_centre[0]) / 2, (right_centre[1] + left_centre[1]) / 2]
                LR_x = right_centre[0] - left_centre[0]
                LR_y = right_centre[1] - left_centre[1]

                perp_x = - LR_y
                perp_y = LR_x

                if perp_x > 0 and perp_y > 0:
                    Heading = math.atan(1.0 * perp_y / perp_x)

                elif perp_x > 0 and perp_y < 0:
                    Heading = math.atan(1.0 * perp_y / perp_x) + 2 * math.pi

                elif perp_x < 0 and perp_y > 0:
                    Heading = math.atan(1.0 * perp_y / perp_x) + math.pi
                else:
                    Heading = math.atan(1.0 * perp_y / perp_x) + math.pi

                Line_end = Location[:]
                length = 2
                Line_end[0] += perp_x * length
                Line_end[1] += perp_y * length

                cv2.arrowedLine(actual_img_resize, tuple(Location), tuple(Line_end), (255, 255, 255), 2)

                print "Location: " + str(Location)
                print "Heading: " + str(Heading)

                write_dict = {'Time': time.time() * 1000.0, 'Location': Location, 'Heading': Heading, \
                    'Left_centre': left_centre, 'Right_centre': right_centre, "Ball_centre": ball_centre}

                frames.append(write_dict)

            except (TypeError, ZeroDivisionError) as e:
                pass

        # else:
        #     write_dict = {'Time': time.time() * 1000.0, 'Location': None, 'Heading': None, \
        #         'Left_centre': None, 'Right_centre': None}
        #     frames.append(write_dict)



        cv2.imshow('Robot detection', actual_img_resize) #dst_persp_rot)
        # cv2.imshow('Robot detection', dst_persp_rot) #dst_persp_rot)

        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            break

    log_file = open('log_file.txt', 'w')
    pickle.dump(frames, log_file)

if __name__ == '__main__':
	main()
