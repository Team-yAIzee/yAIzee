# diceui.py
# Graphics implementation for displaying virtual dice (Kivy)

import kivy
kivy.require("1.0.6")

from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window


class DiceDisplay(Widget):
    def __init__(self, **kwargs):
        super().__init__()

        # self.size_hint = (1.0, 1.0)
        self.size = (600, 480)

        layout = AnchorLayout(size_hint=(1.0, 0.5), anchor_x='center', anchor_y='top')
        button = Button(text="Hallo Welt!")
        layout.add_widget(button)
        self.add_widget(layout)

        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=(self.center_x, 0), size_hint=(1.0, 1.0))


# All code below is only for testing purposes
class DiceApp(App):
    def build(self):
        widget = Widget()
        widget.size_hint = (1., 1.)
        widget.add_widget(Button(text="Hello World {1}"))
        print(widget.size)
        return widget
        # return DiceDisplay()


if __name__ == '__main__':
    DiceApp().run()
