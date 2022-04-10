from threading import Thread
import cv2 as cv

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=(), daemon = True).start()
        return self

    def show(self):
        while not self.stopped:
            print(2)
            cv.imshow("frame", self.frame)
            cv.waitKey(1)
            #if cv.waitKey(1) == ord("q"):
            #    self.stopped = True

    def stop(self):
        self.stopped = True
