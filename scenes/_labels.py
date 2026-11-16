from manim import *
from scenes.theme import *
apply_theme()

class Labels(Scene):
    def construct(self):
        self.camera.background_color = BG
        g = VGroup(*[mono_text(p, size=15, color=MUTED) for p in ["neutral","confident","confused","shocked","eureka","dizzy","robot"]])
        g.arrange(RIGHT, buff=0.6)
        self.add(g)
        self.wait(0.1)
