import cv2 as cv
from VideoGetColor import VideoGetColor
from VideoShow import VideoShow
from simple_pyspin import Camera
import argparse
import math
import socket
import time
import numpy as np
import json
import threaddemo
from functions import *
import logging
import PySpin
import matplotlib.pyplot as plt
from localization import *

def doNothing(x):
    pass

def threadVideoGet():
    Islocalized = 0
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5065
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Track bar
    #cv.namedWindow('Track Bars', cv.WINDOW_NORMAL)
    #cv.createTrackbar('min_blue', 'Track Bars', 0, 255, doNothing)
    #cv.createTrackbar('min_green', 'Track Bars', 0, 255, doNothing)
    #cv.createTrackbar('min_red', 'Track Bars', 0, 255, doNothing)

    #cv.createTrackbar('max_blue', 'Track Bars', 0, 255, doNothing)
    #cv.createTrackbar('max_green', 'Track Bars', 0, 255, doNothing)
    #cv.createTrackbar('max_red', 'Track Bars', 0, 255, doNothing)

    video_getter = VideoGetColor().start()


    while True:
        if (cv.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break      

        # get BGR frame (pixel type can be adjusted in SpinView)
        frame = video_getter.image_result

        # localize 2 points
        if not Islocalized:
            localresult = LocationOfCorners(frame)
            if localresult == 0:
                continue
            else:
                #TO DO: give unity a specific number so that unity know we finish the localization and close the tags
                ##############
                sock.sendto("finish".encode(), (UDP_IP, UDP_PORT))
                ##############
                UpPoint, DownPoint, Islocalized = localresult[0], localresult[1],localresult[2] # choose tag25 as the up point, tag36 as the down point 
        #cv.circle(frame, UpPoint, 6,(255,0,0), 5)  # debug for center localization
        #cv.circle(frame, DownPoint, 6,(255,0,0), 5)       
        #color detection
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Green color
        #low_green = np.array([25, 52, 72])
        #high_green = np.array([102, 255, 255])
        #fgMask = cv.inRange(hsv_frame, low_green, high_green)


        

        # Blue color
        min_blue = 104
        min_green = 194
        min_red = 73
    
        max_blue = 170
        max_green = 255
        max_red = 255

        #reading the trackbar values for thresholds
        #min_blue = cv.getTrackbarPos('min_blue', 'Track Bars')
        #min_green = cv.getTrackbarPos('min_green', 'Track Bars')
        #min_red = cv.getTrackbarPos('min_red', 'Track Bars')
    
        #max_blue = cv.getTrackbarPos('max_blue', 'Track Bars')
        #max_green = cv.getTrackbarPos('max_green', 'Track Bars')
        #max_red = cv.getTrackbarPos('max_red', 'Track Bars')

        
        fgMask = cv.inRange(hsv_frame, np.array([min_blue, min_green, min_red]), np.array([max_blue, max_green, max_red]))

   
    
        #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        fgMask = cv.resize(fgMask,(960,540))
        frame = cv.resize(frame,(960,540))

        #erosion and dilation
        #fgMask = cv.erode(fgMask, np.ones((7,7), np.uint8)) 
        #fgMask = cv.dilate(fgMask, np.ones((5,5), np.uint8)) 

        ret,fgMask = cv.threshold(fgMask,130,255,cv.THRESH_BINARY) 
        #noise remove
        fgMask = cv.boxFilter(fgMask, -1, (5, 5))

        contours, hierarchy = cv.findContours(fgMask, 
        cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  

        n=0
        m={}
        for cnt in contours:
            M = cv.moments(cnt)
            if(M['m00']!= 0):       
            
            
                if (cv.contourArea(cnt) > 500):
                    #find and draw min circle
                    #(cx,cy),radius = cv.minEnclosingCircle(cnt)
                    #center = (int(cx),int(cy))
                    #radius = int(radius)
                    #radius_adjust = radius + 10
                    #cv.circle(fgMask,center,radius_adjust,color =(255,0,0),thickness=10)
                    #m['nums'] = n
                    #m['x'+str(n)] = cx
                    #m['y'+str(n)] = cy  

                    #m['nums'] = n
                    #m['x'+str(n)] = cx
                    #m['y'+str(n)] = cy

                    #n = n+1  
                    
                    (cx,cy),radius = cv.minEnclosingCircle(cnt)
                    detectcenter = (int(cx),int(cy))
                    cv.circle(fgMask,detectcenter,int(radius) + 10 ,color =(255,0,0),thickness=10)
                    x,y = Playpos(UpPoint, DownPoint,detectcenter)
                    m['nums'] = n
                    m['x'+str(n)] = x
                    m['y'+str(n)] = y
                    
                    n = n + 1
                    
                   
                    
        print(m)
        data = json.dumps(m)
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT) )


        cv.imshow("fgMask", fgMask)
        cv.imshow("Green", frame)
        cv.waitKey(1)
       
        


def threadVideoShow():
    

    cam = Camera()
    cam.start()
    frame = cam.get_array()
    video_shower = VideoShow(frame).start()
    #cps = CountsPerSec().start()

    while True:
        frame = cam.get_array()
        if video_shower.stopped:
            video_shower.stop()
            break

        #frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
       # cps.increment()

def threadBoth():

    video_getter = VideoGet().start()
    video_shower = VideoShow(video_getter.frame).start()
    #cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
       # frame = detectmulti.ProcessFrame(frame)
        video_shower.frame = frame
        #cps.increment()

def main():
    threadVideoGet()

if __name__ == "__main__":
    main()
