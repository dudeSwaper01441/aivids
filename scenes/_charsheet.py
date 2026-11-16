from manim import *
from scenes.theme import *
from scenes.character import Somsak, Clerk, beach_chair

apply_theme()


class CharacterSheet(Scene):
    def construct(self):
        self.add(background_grid())
        poses = ["neutral", "confident", "confused", "shocked", "eureka", "dizzy", "robot"]
        chars = VGroup()
        for i, p in enumerate(poses):
            c = Somsak(position=(-6.2 + i * 1.85, -0.4, 0), pose=p, scale=1.0)
            chars.add(c)
            label = mono_text(p, size=15, color=MUTED).next_to(c, DOWN, buff=0.12)
            chars.add(label)
        self.add(chars)
        clerk = Clerk(position=(-5.0, 2.2, 0), scale=1.1)
        self.add(clerk)
        self.add(mono_text("CLERK", size=15, color=MUTED).next_to(clerk, DOWN, buff=0.12))
        self.wait(0.1)
