# ui.py
# User interface implementation
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
# Capture and save frames
from pathlib import Path
from time import strftime, localtime, sleep
import numpy as np
from matplotlib.pyplot import imsave
from kivy import graphics

from stream import WebcamStream
from logic import mark_circles_in_image
from game_sidebar import GameSidebar

import cv2


class Video(BoxLayout):
    """
    Video widget.
    This widget displays a video from a given stream.
    """
    wimg: Image
    stream: WebcamStream

    def __init__(self, stream, **kwargs):
        super(Video, self).__init__(**kwargs)

        self.stream = stream
        self.build_ui()

        self.display_mode = 'Normal'  # Camera display mode

        Clock.schedule_interval(self.update, 0.1)  # 10 fps

    def update(self, dt):
        buf = np.flipud(self.stream.read())

        if self.display_mode == 'Canny':  # Canny edge detector
            buf = cv2.cvtColor(buf, cv2.COLOR_RGB2GRAY)
            buf = cv2.Canny(buf, 100, 200)
            buf = cv2.cvtColor(buf, cv2.COLOR_GRAY2RGB)

        if self.display_mode == 'Value':  # Brightness
            buf = cv2.cvtColor(buf, cv2.COLOR_RGB2HSV)
            buf = cv2.cvtColor(buf[:, :, 2], cv2.COLOR_GRAY2RGB)  # Convert only value back to color

        if self.display_mode == 'ThreshValue':  # Brightness
            threshold = 128
            buf = cv2.cvtColor(buf, cv2.COLOR_RGB2HSV)
            buf = cv2.cvtColor(((buf[:, :, 2] > threshold) * 255.0).astype(np.uint8),
                               cv2.COLOR_GRAY2RGB)  # Convert only value back to color

        if self.display_mode == 'HoughTransform':
            buf = mark_circles_in_image(buf)

        texture = Texture.create(size=self.stream.dimensions)
        texture.blit_buffer(buf.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        self.wimg.texture = texture

    def capture(self):
        home = Path.home()
        image = mark_circles_in_image(self.stream.read())
        imsave(str(home) + '/Downloads/IMG' + strftime("%Y%m%d%H%M%S", localtime()) + '.jpg', self.stream.read())

    def build_ui(self):
        self.wimg = Image(size=self.stream.dimensions)
        self.wimg.allow_stretch = True  # MI
        self.wimg.size_hint = (1.0, 1.0)
        self.add_widget(self.wimg)

    def set_display_mode(self, new_mode: str):
        self.display_mode = new_mode


class ContainerWidget(BoxLayout):
    """
    Root widget for this application. All other widgets are parsed as its children.
    """

    wdisplay: Video
    wcapture: Button = Button(text="Capture frame", font_size=30, size_hint=(0.6, 1.))
    anchor_layout: AnchorLayout = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(0., 0.2))

    data = None

    def __init__(self, stream, **kwargs):
        super(ContainerWidget, self).__init__(**kwargs)

        self.orientation = 'horizontal'  # MI

        left_group = BoxLayout(size_hint=(0.8, 1.0), orientation='vertical')  # MI
        side_bar = GameSidebar(size_hint=(0.2, 1.0))  # MI

        self.wdisplay = Video(stream, size=stream.dimensions)
        self.wdisplay.size_hint = (1.0, 1.0)

        self.wcapture.on_press = self.wdisplay.capture

        self.anchor_layout.add_widget(self.wcapture)
        self.anchor_layout.size_hint = (1.0, None)
        self.anchor_layout.size = (200, 50)  # MI

        left_group.add_widget(self.wdisplay)
        left_group.add_widget(self.anchor_layout)
        left_group.add_widget(BoxLayout(size=(10, 20), size_hint=(1.0, None)))  # MI just same space at the bottom

        self.add_widget(left_group)  # MI
        self.add_widget(side_bar)  # MI

        side_bar.on_view_mode_changed = lambda new_mode: self.wdisplay.set_display_mode(
            new_mode)  # MI Define callback in sidebar to notify about view mode change
