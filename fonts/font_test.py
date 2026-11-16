from manim import *
from manimpango import register_font
from pathlib import Path
F = Path(r"D:\project\aivids\fonts")
for f in F.glob("*.ttf"):
    print("register", f.name, register_font(str(f)))
class FontTest(Scene):
    def construct(self):
        self.camera.background_color = "#1E242B"
        t1 = Text("สมศักดิ์ ตื่นสาย รีบวิ่งไปขึ้น...", font="IBM Plex Sans Thai", weight=BOLD, color="#F1EFEA", font_size=48)
        t2 = Text("Token #4821  62.4%  T = 0.7", font="JetBrains Mono", weight=MEDIUM, color="#4DB6AC", font_size=36)
        g = VGroup(t1,t2).arrange(DOWN, buff=0.5)
        self.add(g)
        self.wait(0.1)
