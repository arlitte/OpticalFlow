import numpy as np
import cv2 as cv


def drlof():
    #frame1 = cv.imread("up-opencv/frame0-00-00.63.jpg")
    #frame2 = cv.imread("up-opencv/frame0-00-00.42.jpg")
    #frame1 = cv.imread("geo1-opencv/frame0-00-04.20.jpg")
    #frame2 = cv.imread("geo1-opencv/frame0-00-04.40.jpg")
    #frame1 = cv.imread("arctic-opencv/frame0-00-02.60.jpg")
    #frame2 = cv.imread("arctic-opencv/frame0-00-02.84.jpg")
    frame1 = cv.imread("frame1130.jpg")
    frame2 = cv.imread("frame1150.jpg")
    new_h = int(frame1.shape[0]*(1))
    new_w = int(frame1.shape[1]*(1))
    prvs = cv.resize(frame1, (new_w, new_h))
    next = cv.resize(frame2, (new_w, new_h))

    hsv = np.zeros_like(prvs)
    hsv[..., 1] = 255

    m = cv.optflow.DenseRLOFOpticalFlow.create()
    m.setGridStep((6, 6))
    m.setForwardBackward(0)
    flow = m.calc(prvs, next, None)
    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    #find_move(ang)

    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    bgr = cv.resize(bgr, (new_w*1, new_h*1))
    cv.imwrite('res_drlof_11010.jpg', bgr)
    #find_move(ang)

def find_move(ang):
    sum_left = 0
    sum_right = 0
    for i in range(len(ang)):
        for j in range(int(len(ang[0]) / 2)):
            sum_left += ang[i][j]
            sum_right += ang[i][j + int(len(ang[0]) / 2)]
    sum_right = sum_right / (len(ang) * len(ang[0]) / 2)
    sum_left = sum_left / (len(ang) * len(ang[0]) / 2)
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

