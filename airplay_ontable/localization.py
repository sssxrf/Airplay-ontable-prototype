#import sys

#locate_python = sys.exec_prefix

#print(locate_python)

import pupil_apriltags as apriltag
import cv2 as cv

import numpy as np
import sys
tag25_detector = apriltag.Detector(families='tag25h9') #for tag25h9
tag36_detector = apriltag.Detector(families='tag36h11') #for tag36h11

def LocationOfCorners(img):

    #img =cv.imread("tags.png")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9') )#for linux
    
    tag25 = tag25_detector.detect(gray)
    if len(tag25) == 0:
        return 0
    else:
        center25 = tuple(tag25[0].center.astype(int))
    #cv.circle(img, tuple(tag25[0].center.astype(int)), 4,(255,0,0), 2) # draw center for debug

    
    tag36 = tag36_detector.detect(gray)
    if len(tag36) == 0:
        return 0
    else:
        center36 = tuple(tag36[0].center.astype(int))

    flag = 1

    return center25, center36, flag
    #cv.circle(img, tuple(tag36[0].center.astype(int)), 4,(255,0,0), 2) # draw center for debug

    #cv.imshow("tag",img)
    #cv.waitKey()

def Playpos(pointup, pointdown, detectpoint):
    #change to normal coordinator
    PU = np.array([pointup[0], -pointup[1]])
    PD = np.array([pointdown[0], -pointdown[1]])
    detectP = np.array([detectpoint[0], -detectpoint[1]])
    Px, Py = detectpoint[0], -detectpoint[1]

    # l1: PU PD
    deltaUD = PU - PD
    if deltaUD[0] == 0:
        # don't need to judge side, negative represents left, down
        x_dis = Px - PU[0]
        y_dis = PD[0] - Py
    else:
        k = deltaUD[1] / deltaUD[0]
        b = PD[1] - k * PD[0]
        # foot point (intersection point of l1, l2: detectpoint)
        foot_x = (Px/k + Py - b) / (k + 1/k)
        foot_y = k * foot_x + b
        foot = np.array([foot_x, foot_y])
    
        # distance: foot point to pointdown ; foot point to detectpoint
        x_dis = np.linalg.norm(detectP - foot)
        y_dis = np.linalg.norm(foot - PD)


        # l2: PD and perpendicular to l1
        k1 = -1 / k
        b1 = PD[0] / k + PD[1]

        # detectpoint on which side, 4 situation when we choose pointdown as the origin
        if k > 0:
            if k * Px + b <= Py:   #left side
                if k1 * Px + b1 <= Py: # up side
                    x_dis = -x_dis
                else:             #left down side   
                    x_dis = -x_dis    
                    y_dis = -y_dis
        
            if k * Px + b > Py:   #right side
                if k1 * Px + b1 > Py: # down side
                    y_dis = -y_dis
                # right up do nothing

        if k < 0:
            if k * Px + b >= Py:   #left side
                if k1 * Px + b1 <= Py: # up side
                    x_dis = -x_dis
                else:             #left down side   
                    x_dis = -x_dis    
                    y_dis = -y_dis
        
            if k * Px + b < Py:   #right side
                if k1 * Px + b1 > Py: # down side
                    y_dis = -y_dis
                # right up do nothing
     
    # normlize: calculate the relative distance by distance of two tags
    tag_dis = np.linalg.norm(deltaUD)
    x = x_dis / tag_dis
    y = y_dis / tag_dis

    #
    return x, y 