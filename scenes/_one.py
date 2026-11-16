from manim import *
from scenes.theme import *
from scenes.character import Somsak
apply_theme()

class One(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(Somsak(position=(-1, -2, 0), pose="neutral"))
        self.wait(0.1)
