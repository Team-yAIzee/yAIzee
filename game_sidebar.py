from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
# Capture and save frames
from pathlib import Path
from time import strftime, localtime, sleep
import numpy as np

from typing import Callable
from score_board import ScoreBoard


class GameSidebar(BoxLayout):

    def __init__(self, **kwargs):
        super(GameSidebar, self).__init__(**kwargs)
        
        self.size_hint = (None, 1.0)  # Width is custom defined (so None), vertical is 100%
        self.size = (450, 500)
        
        self.orientation = 'vertical'  # Vertical alignment of elements

        self.score_board = ScoreBoard(size_hint=(1.0, None)) # MI: Add scoreboard
        
        self.on_view_mode_changed: Callable = None  # Callback for view mode changes. Parameters: New view mode

        self.view_spinner = Spinner(size_hint=(1.0, None), size=(200, 50))
        self.view_spinner.values = ['Normal', 'Canny', 'Value', 'ThreshValue', 'HoughTransform', 'DiceRecognition']
        self.view_spinner.text = self.view_spinner.values[0]         
        self.view_spinner.bind(text=self.view_mode_changed)

        self.add_widget(BoxLayout(size_hint=(1.0, None), size=(20, 20)))  # Spacing
        self.add_widget(self.view_spinner)
        self.add_widget(BoxLayout(size_hint=(1.0, None), size=(20, 20)))  # Spacing
        self.add_widget(self.score_board)
        self.add_widget(BoxLayout(size_hint=(1.0, 1.0)))  # MI: Insider: Just add an empty view to top align all
        # previous elements

    def view_mode_changed(self, view, value):
        """
        Triggered from spinner when a new view mode has been selected
        """        
        if self.on_view_mode_changed is not None:  # MI: Call callback function if defined
            self.on_view_mode_changed(value)
