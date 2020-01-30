# stream.py
# Stream classes for use in Kivy UI

from abc import ABC, abstractmethod
import cv2
from moviepy.video.VideoClip import VideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import time


class AbstractStream(ABC):
    """
    This class is the base class for all streams. Streams are classes that can be interfered with using their
    read function which returns the current image in the stream. This can for example be used for displaying
    a video of any type in a UI toolkit.
    """

    @abstractmethod
    def read(self):
        """
        Return the image at the current position of the stream. This image shall always be returned in RGB format.
        :rtype: np.ndarray
        :return: A numpy image array in RGB format
        """
        pass

    @property
    @abstractmethod
    def dimensions(self):
        """
        Return a tuple containing the dimensions of the image. The tuple has the format (x, y), where x is the
        horizontal size of the image in pixels and y the vertical size.
        :return: A tuple containing the (x, y) dimensions of the image
        """
        pass


class WebcamStream(AbstractStream):
    """
    This class is used for streaming input from a webcam. It uses the OpenCV library python binding.
    """

    def __init__(self, ncam):
        self.camera: cv2.VideoCapture = cv2.VideoCapture(ncam)
        # Set camera resolution to full HD
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def read(self):
        success, img = self.camera.read()
        if success:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        else:
            raise Exception("camera.read() was unsuccessful")

    @property
    def dimensions(self):
        return self.camera.get(cv2.CAP_PROP_FRAME_WIDTH), self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)


class VideoStream(AbstractStream):
    """
    A class for streaming from a movie file. It uses the moviepy library.
    """

    video: VideoClip
    _start: float

    def __init__(self, filename):
        self.video = VideoFileClip(filename=filename)
        self._start = 0.

    def read(self):
        cur_time = time.time()

        if self._start == 0.:
            self._start = cur_time

        if cur_time - self._start < self.video.duration:
            return self.video.get_frame(cur_time - self._start)
        else:
            self._start = cur_time
            return self.video.get_frame(cur_time - self._start)

    @property
    def dimensions(self):
        return self.video.w, self.video.h
