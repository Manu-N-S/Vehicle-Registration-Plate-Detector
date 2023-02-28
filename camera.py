import cv2
from liveVideoDL import object_video

class VideoCamera(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,frame = self.video.read()
        frame = object_video(frame)
        ret,jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes()