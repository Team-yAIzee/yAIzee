from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color
# Capture and save frames
from pathlib import Path
from time import strftime, localtime, sleep
import numpy as np
from matplotlib.pyplot import imsave

from stream import WebcamStream
from logic import mark_circles_in_image
from typing import Callable


class ScoreBoard(BoxLayout):

    def __init__(self, **kwargs):
        super(ScoreBoard, self).__init__(**kwargs)
        self.size = (500, 600)

        self.point_grid = GridLayout(size_hint=(1.0, 1.0))
        self.add_widget(self.point_grid)

        # Define game rows, dsh ('-') = spacing
        self.game_rows = ['1er', '2er', '3er', '4er', '5er', '6er', '-', 'Dreierpasch', 'Viererpasch', 'Zwei-Paar',
                          'kleine Straße', 'große Straße', 'Full House', 'Chance', 'Kniffel']

        # Define players
        self.players = ['Mensch', 'AI']

        self.point_grid.cols = len(self.players)+1  # all players plus name column
        self.point_grid.rows = len(self.game_rows)+1  # all game rows plus index row

        self.point_grid.add_widget(Label(text=''))  # empty

        self.score_labels = {}  # Backreference to score labels

        for index, cur_player in enumerate(self.players):
            player_label = Label(text=cur_player)
            player_label.color = (1.0, 0.0, 0.0, 1.0) if index % 2 == 1 else (0.0, 1.0, 1.0, 1.0)
            player_label.bold = True
            self.point_grid.add_widget(player_label)

        # build grid
        for cur_game_row in self.game_rows:

            if cur_game_row == '-':  # Use dash for scacing
                for cur_player_index in range(len(self.players)+1):
                    self.point_grid.add_widget(Label())  # add row description
                continue

            self.point_grid.add_widget(Button(text=cur_game_row))  # add row description

            for cur_player in self.players:
                score_label = Label(text='Offen')
                self.score_labels[(cur_player, cur_game_row)] = score_label # Store widget in dictionary as name, row tuple so we can change it later
                self.point_grid.add_widget(score_label)  # add scoring