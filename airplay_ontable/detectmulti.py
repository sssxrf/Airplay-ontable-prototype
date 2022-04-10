
from __future__ import print_function
import cv2 as cv
import argparse
import math
import socket
import time
import numpy as np
import json
import threaddemo
import VideoGet
from functions import *
from simple_pyspin import Camera
import logging

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='KNN')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

def ProcessFrame(frame):
    return frame

# try:
with Camera() as cam: # Acquire and initialize Camera
    cam.start() # Start recording
        
    while True:
        
        frame = cam.get_array()
        
     
        #start_time = time.clock()

        fgMask = backSub.apply(frame)
        
        #end_time = time.clock()
        #proccess_time = end_time - start_time
        #logging.basicConfig(level=logging.DEBUG, filename="logfile_backsub", filemode="a+",
        #               format="%(asctime)-15s %(levelname)-8s %(message)s")
        #logging.info(proccess_time)

    
        # get frame rate of camera
        rateatt = cam.camera_attributes
        framespersecond = int(rateatt['AcquisitionFrameRate'].GetValue())
    
        cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        cv.putText(frame, str(framespersecond), (15, 15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
        fgMask = cv.resize(fgMask,(960,540))
        frame = cv.resize(frame,(960,540))

        #erosion and dilation
        #fgMask = cv.erode(fgMask, np.ones((7,7), np.uint8)) 
        #fgMask = cv.dilate(fgMask, np.ones((5,5), np.uint8)) 
        
        #noise remove
        fgMask = cv.boxFilter(fgMask, -1, (5, 5))

        ret,fgMask = cv.threshold(fgMask,150,255,cv.THRESH_BINARY) #real time threshold(fgMask,125,255,cv.THRESH_BINARY

        contours, hierarchy = cv.findContours(fgMask, 
        cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    

        n=0
        m={}
        for cnt in contours:
            M = cv.moments(cnt)
            if(M['m00']!= 0):       
            
            
                if (cv.contourArea(cnt) > 500):
                    
                    rect = cv.minAreaRect(cnt)
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    cv.drawContours(fgMask,[box],0,(255,0,0),10)

                    cx, cy = findwheelcenter(box, half_disinpixel = 45)
                    center = (int(cx),int(cy))
                    centercircle = cv.cvtColor(fgMask, cv.COLOR_GRAY2BGR)
                    if cx is not None and cy is not None:
                        cv.circle(centercircle, center, radius =10 ,color =(0,0,255),thickness=5)

                    m['nums'] = n
                    m['x'+str(n)] = cx
                    m['y'+str(n)] = cy

                    n = n+1       
        print(m)
        data = json.dumps(m)
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT) )

        cv.imshow('detected center', centercircle)
        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)
        
        cv.waitKey(20)

        

        #if keyboard == 'q' or keyboard == 27:
        #    break
         
    cam.stop() # Stop recording
#except:
#    capture = cv.VideoCapture(0)
#    while True:
#        ret, img = capture.read()
#        #img, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
#        #print(imgs[0].shape, imgs[0].dtype) # Each image is a numpy array!
#        cv.imshow("try",img)
#        keyboard = cv.waitKey(30)
#        if keyboard == 'q' or keyboard == 27:
#            break

    
   


