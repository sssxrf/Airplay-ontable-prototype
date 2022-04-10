
from threading import Thread
import cv2 as cv
from simple_pyspin import Camera

class VideoGet:
    

    def __init__(self):
        with Camera() as self.cam0:
            self.cam0.start()
            self.frame = self.cam0.get_array()
            self.rateatt = self.cam0.camera_attributes
            self.framespersecond = int(self.rateatt['AcquisitionFrameRate'].GetValue())
            self.cam0.stop()
            self.stopped = False
            

    def start(self):
        Thread(target=self.get, args=(), daemon = True).start()
        return self

    def get(self):
        with Camera() as self.cam:
            self.cam.start()
            while not self.stopped:
                print(1)
                self.frame = self.cam.get_array()
                self.rateatt = self.cam.camera_attributes
                self.framespersecond = int(self.rateatt['AcquisitionFrameRate'].GetValue())

    def stop(self):
        self.stopped = True