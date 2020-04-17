# main.py
# Display continously taken images from a connected webcam with Kivy

# Kivy UI
from kivy.app import App
from kivy.clock import Clock

from configuration import obtain_configuration
from stream import VideoStream
from ui import *

from kivy.core.window import Window  # MI
Window.size = (obtain_configuration()["window"]["width"], obtain_configuration()["window"]["height"])
Window.left = 50  # MI
Window.top = 50  # MI


class WebcamApp(App):

    def build(self):
        container = ContainerWidget(WebcamStream(0))
        return container


if __name__ == '__main__':
    WebcamApp().run()
