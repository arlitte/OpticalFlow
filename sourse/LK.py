import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import math
import argparse

def LK():
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15, 15),
                      maxLevel = 2,
                      criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # Create some random colors
    img = cv.imread("frame1130.jpg")  # <opencv_root>/samples/data/blox.jpg
    # Initiate FAST object with default values
    #fast = cv.FastFeatureDetector_create()
    #kp = fast.detect(img, None)
    #img2 = cv.drawKeypoints(img, kp, None, color=(255, 0, 0))
    #cv.imwrite('fast_true.png', img2)

    #SIFT
    #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #sift = cv.SIFT_create()
    #kp, des = sift.detectAndCompute(gray, None)

    # Initiate ORB detector
    #orb = cv.ORB_create()
    # find the keypoints with ORB
    #kp = orb.detect(img, None)
    # compute the descriptors with ORB
    #kp, des = orb.compute(img, kp)

    # Take first frame and find corners in it
    old_frame = cv.imread("frame1130.jpg")
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    #p1 = cv.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    h = old_frame.shape[0]
    w = old_frame.shape[1]
    print(h, w)

    p0 = np.ones(((int((h*w)/100), 1, 2)), dtype=np.float32)
    counter = 0
    for i in range(1, w, 10):
        for j in range(1, h, 10):
            p0[counter][0][0] = float(i)
            p0[counter][0][1] = float(j)
            counter += 1

    #p0 = np.ones(((len(kp),1,2)), dtype=np.float32)
    #counter = 0
    #for i in kp:
    #    p0[counter][0][0] = float(i.pt[0])
    #    p0[counter][0][1] = float(i.pt[1])
    #    counter += 1

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    frame = cv.imread("frame1150.jpg")
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    count = 0
    # Select good points
    if p1 is not None:
        good_new = p1[st==1]
        good_old = p0[st==1]
    # draw the tracks
    ax = plt.axes()
    ang1 = []
    ang2 = []
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        b = -b
        d = -d
        # b = h-b
        # d = h-d
        if b > d:
            ang = math.acos((abs(b - d)) / ((a - c)**2+(b-d)**2)**0.5)
        else:
            ang = 2 * math.pi - math.acos((abs(b - d)) / ((a - c)**2 + (b - d)**2)**0.5)
        if c > w / 2:
            ang1.append(ang)
        else:
            ang2.append(ang)
        #ax.arrow(c, d, a-c, b-d, head_width=2, head_length=1, fc='k', ec='k')
        #mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        #frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
    #plt.show()
    find_move(ang1, ang2)


def find_move(ang1, ang2):
    sum_left = 0
    sum_right = 0
    for i in range(len(ang1)):
        sum_left+= ang1[i]
    sum_left = sum_left/len(ang1)
    for i in range(len(ang2)):
        sum_right += ang2[i]
    sum_right = sum_right/len(ang2)
    print(sum_left, sum_right)
    quaters = (0, 1.57, 3.14, 4.71)
    if sum_left <= quaters[1] and sum_left> quaters[0]:
        left_q = 1
    elif sum_left <= quaters[2] and sum_left> quaters[1]:
        left_q = 2
    elif sum_left <= quaters[3] and sum_left> quaters[2]:
        left_q = 3
    else:
        left_q = 4
    if sum_right <= quaters[1] and sum_right> quaters[0]:
        right_q = 1
    elif sum_right <= quaters[2] and sum_right> quaters[1]:
        right_q = 2
    elif sum_right <= quaters[3] and sum_right > quaters[2]:
        right_q = 3
    else:
        right_q = 4
    print(left_q, right_q)
    if right_q != left_q:
        if left_q == 4:
            print("moving back")
        else:
            print("moving forward")
    print((sum_left+sum_right)/2)