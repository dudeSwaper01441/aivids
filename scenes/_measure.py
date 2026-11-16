from manim import *
from scenes.theme import *
apply_theme()
words = ["เช้านี้","สม","ศักดิ์","ตื่น","สาย","เลย","รีบ","วิ่ง","ไป","ขึ้น","รถเมล์","วินมอไซค์","รถไฟฟ้า","แท็กซี่","เรือเหาะ","ทันเวลา","ทำงาน","สมศักดิ์"]
for s in (16,18,20):
    print("size", s)
    for w in words:
        t = that_text(w, size=s)
        print(f"  {w}: {t.width:.3f}")
print("space glyph:", mono_text("␣", size=24).width, mono_text("space", size=12).width)
