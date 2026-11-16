from manim import *
from scenes.theme import *
from scenes.character import Somsak, Clerk

apply_theme()


class CharacterSheet2(Scene):
    def construct(self):
        self.add(background_grid())
        poses = ["neutral", "confident", "confused", "shocked", "eureka", "dizzy", "robot"]
        for i, p in enumerate(poses):
            self.add(Somsak(position=(-6.2 + i * 1.85, -0.4, 0), pose=p, scale=1.0))
        self.add(Clerk(position=(-5.0, 2.2, 0), scale=1.1))
        self.wait(0.1)
