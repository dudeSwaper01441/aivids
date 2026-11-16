from manim import *
from scenes.theme import *
apply_theme()
class TexTest(Scene):
    def construct(self):
        self.camera.background_color = BG
        f = MathTex(r"P(w_i)=\frac{e^{z_i/T}}{\sum_{j=1}^{V} e^{z_j/T}}", font_size=40, color=INK)
        self.add(f)
        self.wait(0.1)
