from manim import *
from scenes.theme import *
from scenes.character import Somsak, Clerk
apply_theme()

class Two(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(background_grid())
        self.add(Somsak(position=(-4, -2, 0)))
        self.wait(0.1)
