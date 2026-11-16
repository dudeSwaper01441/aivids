from manim import *
from scenes.theme import *
from scenes.character import Somsak
apply_theme()

class Four(Scene):
    def construct(self):
        self.camera.background_color = BG
        for i, p in enumerate(["shocked", "eureka", "dizzy", "robot"]):
            self.add(Somsak(position=(-6 + i*3, -2, 0), pose=p))
        self.wait(0.1)
