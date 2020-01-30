# main.py
# Author: Fabian R.
# Display continously taken images from a connected webcam with Kivy

# Kivy UI
from kivy.app import App
from kivy.clock import Clock

from stream import VideoStream
from ui import *

from kivy.core.window import Window # MI
Window.size = (1800, 1000)  # MI
Window.left = 50  # MI
Window.top = 50  # MI


class WebcamApp(App):

    def build(self):
        container = ContainerWidget(WebcamStream(0))
        return container


if __name__ == '__main__':
    WebcamApp().run()
