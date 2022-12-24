#createOptFlow_DeepFlow()
import numpy as np
import cv2 as cv

def df():
    #frame1 = cv.imread("up-opencv/frame0-00-00.42.jpg")
    #frame2 = cv.imread("up-opencv/frame0-00-00.63.jpg")
    # frame1 = cv.imread("geo1-opencv/frame0-00-04.20.jpg")
    # frame2 = cv.imread("geo1-opencv/frame0-00-04.40.jpg")
    frame1 = cv.imread("arctic-opencv/frame0-00-02.60.jpg")
    frame2 = cv.imread("arctic-opencv/frame0-00-02.84.jpg")
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    optical_flow = cv.optflow.createOptFlow_DeepFlow()
    flow = optical_flow.calc(prvs, next, None)

    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    cv.imwrite('res_df.jpg', bgr)
