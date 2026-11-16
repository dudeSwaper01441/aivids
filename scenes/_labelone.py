from manim import *
from scenes.theme import *
apply_theme()

class LabelOne(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(mono_text("eureka", size=15, color=MUTED))
        self.wait(0.1)
