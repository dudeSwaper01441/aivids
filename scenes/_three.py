from manim import *
from scenes.theme import *
from scenes.character import Somsak
apply_theme()

class Three(Scene):
    def construct(self):
        self.camera.background_color = BG
        for i, p in enumerate(["neutral", "confident", "confused"]):
            self.add(Somsak(position=(-5 + i*3, -2, 0), pose=p))
        self.wait(0.1)
