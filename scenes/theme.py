"""Shared visual language for the LLM next-token video.

Palette, typography, cards, headers and the caption bar all live here so the
seven scenes stay pixel-consistent with the production brief.
"""

from __future__ import annotations

import json
from pathlib import Path

from manim import *
from manim.utils.rate_functions import ease_out_quint
from manimpango import register_font

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
AUDIO_DIR = ROOT / "audio"
DURATIONS_FILE = AUDIO_DIR / "durations.json"

# ---------------------------------------------------------------- palette
BG = "#1E242B"          # Warm Deep Slate
SURFACE = "#2A323D"     # Muted Charcoal Blue
SURFACE_2 = "#323C4A"   # one step lighter, token alternation
BORDER = "#3E4856"      # Soft Slate Border
INK = "#F1EFEA"         # Warm Alabaster
MUTED = "#B8C0CC"       # Cool Muted Gray
AMBER = "#E8A856"       # Soft Amber Gold
TEAL = "#4DB6AC"        # Calm Sage Teal
CORAL = "#E07A5F"       # Muted Terracotta Coral
PERIWINKLE = "#7AA2F7"  # Soft Periwinkle Blue
DIM = "#525D6E"         # dimmed / disabled state

# character-only colours (explicitly specified in the brief)
HAIR = "#181C22"
SKIN = "#E5B89B"
SLACKS = "#232B38"
GLASS = "#D8DEE9"

FONT_THAI = "IBM Plex Sans Thai"
FONT_MONO = "JetBrains Mono"

FONT_FILES = [
    "IBMPlexSansThai-Regular.ttf",
    "IBMPlexSansThai-Medium.ttf",
    "IBMPlexSansThai-Bold.ttf",
    "JetBrainsMono-Medium.ttf",
    "JetBrainsMono-Bold.ttf",
]

_registered = False


def register_fonts() -> None:
    global _registered
    if _registered:
        return
    for name in FONT_FILES:
        path = FONT_DIR / name
        if path.exists():
            register_font(str(path))
    _registered = True


def apply_theme() -> None:
    register_fonts()
    config.background_color = BG
    config.frame_width = 16
    config.frame_height = 9
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 30


# ---------------------------------------------------------------- typography
def that_text(
    text: str,
    size: float = 32,
    color: str = INK,
    weight: str = MEDIUM,
    max_width: float | None = None,
    **kwargs,
) -> Text:
    """Thai text in IBM Plex Sans Thai, optionally squeezed to a max width."""
    mob = Text(text, font=FONT_THAI, weight=weight, font_size=size, color=color, **kwargs)
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def mono_text(
    text: str,
    size: float = 26,
    color: str = MUTED,
    weight: str = MEDIUM,
    max_width: float | None = None,
    **kwargs,
) -> Text:
    mob = Text(text, font=FONT_MONO, weight=weight, font_size=size, color=color, **kwargs)
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def upper(text: str, size: float = 22, color: str = MUTED, **kwargs) -> Text:
    return mono_text(text.upper(), size=size, color=color, **kwargs)


# ---------------------------------------------------------------- primitives
def card(
    width: float,
    height: float,
    fill: str = SURFACE,
    stroke: str = BORDER,
    radius: float = 0.18,
    fill_opacity: float = 1.0,
    stroke_width: float = 2.0,
) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=min(radius, min(width, height) / 2 - 0.01),
        fill_color=fill,
        fill_opacity=fill_opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
    )


def chip(
    text: str,
    color: str = TEAL,
    size: float = 24,
    height: float = 0.5,
    font: str = FONT_THAI,
    text_color: str | None = None,
    fill_opacity: float = 0.16,
) -> VGroup:
    label = Text(
        text,
        font=font,
        weight=MEDIUM,
        font_size=size,
        color=text_color or color,
    )
    box = RoundedRectangle(
        width=label.width + 0.42,
        height=height,
        corner_radius=height / 2,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=1.6,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def pill_label(text: str, color: str, size: float = 20, mono: bool = False) -> VGroup:
    label = (
        mono_text(text, size=size, color=color, weight=BOLD)
        if mono
        else that_text(text, size=size, color=color, weight=BOLD)
    )
    box = RoundedRectangle(
        width=label.width + 0.34,
        height=label.height + 0.18,
        corner_radius=(label.height + 0.18) / 2,
        fill_color=color,
        fill_opacity=0.14,
        stroke_color=color,
        stroke_width=1.4,
    )
    label.move_to(box)
    return VGroup(box, label)


def glow(radius: float, color: str, opacity: float = 0.16, layers: int = 4) -> VGroup:
    """Soft, layered halo (never a hard neon ring)."""
    rings = VGroup()
    for i in range(layers, 0, -1):
        r = radius * (1 + i * 0.22)
        rings.add(
            Circle(
                radius=r,
                fill_color=color,
                fill_opacity=opacity / (i * 1.7),
                stroke_width=0,
            )
        )
    return rings


def icon_circle(radius: float, color: str, opacity: float = 0.16) -> Circle:
    return Circle(
        radius=radius,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=1.6,
    )


def divider(width: float, color: str = BORDER, thickness: float = 1.4) -> Line:
    return Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=thickness)


def fit_height(mob: Mobject, max_h: float) -> Mobject:
    if mob.height > max_h:
        mob.scale_to_fit_height(max_h)
    return mob


# ---------------------------------------------------------------- sound timing
_durations: dict[str, float] | None = None


def _load_durations() -> dict[str, float]:
    global _durations
    if _durations is None:
        if DURATIONS_FILE.exists():
            _durations = json.loads(DURATIONS_FILE.read_text(encoding="utf-8"))
        else:
            _durations = {}
    return _durations


def audio_path(key: str) -> Path:
    return AUDIO_DIR / f"{key}.mp3"


def line_duration(key: str, fallback_text: str = "") -> float:
    """Measured TTS duration when available, otherwise a realistic estimate."""
    data = _load_durations()
    if key in data:
        return float(data[key])
    # ~15.5 Thai characters per second, plus a small breath tail
    chars = len(fallback_text or key)
    return max(2.0, chars / 15.5 + 0.35)


def add_line_audio(scene: Scene, key: str) -> None:
    path = audio_path(key)
    if path.exists():
        scene.add_sound(str(path))


def add_sfx(scene: Scene, name: str) -> None:
    path = AUDIO_DIR / "sfx" / f"{name}.wav"
    if path.exists():
        scene.add_sound(str(path))


def base(scene: Scene, index: int, tag: str, thai_tag: str = "") -> tuple[Chrome, CaptionBar]:
    """Background, top chrome and caption bar shared by every scene."""
    scene.camera.background_color = BG
    bg = background_grid()
    chrome = Chrome(index, tag, thai_tag)
    captions = CaptionBar()
    scene.add(bg, chrome, captions)
    return chrome, captions


# ---------------------------------------------------------------- chrome
class Chrome(VGroup):
    """Persistent top chrome: scene tag, running title, progress rule."""

    def __init__(self, index: int, tag: str, thai_tag: str = ""):
        super().__init__()
        self.index = index

        num = mono_text(f"{index:02d}", size=26, color=AMBER, weight=BOLD)
        slash = mono_text("/ 07", size=16, color=MUTED)
        tag_text = upper(tag, size=21, color=INK)
        tag_text.next_to(num, RIGHT, buff=0.22).align_to(num, DOWN)
        slash.next_to(tag_text, RIGHT, buff=0.18).align_to(tag_text, DOWN)

        left = VGroup(num, tag_text, slash)
        if thai_tag:
            th = that_text(thai_tag, size=20, color=MUTED)
            th.next_to(left, RIGHT, buff=0.34).align_to(left, DOWN)
            left.add(th)

        left.move_to([-6.55, 3.42, 0], aligned_edge=LEFT)

        mark = RoundedRectangle(
            width=0.42,
            height=0.42,
            corner_radius=0.1,
            fill_color=AMBER,
            fill_opacity=0.95,
            stroke_color=AMBER,
            stroke_width=1.4,
        )
        mark_txt = mono_text("LLM", size=14, color=BG, weight=BOLD).move_to(mark)
        right = VGroup(mark, mono_text("NEXT-TOKEN LAB", size=15, color=MUTED))
        right.arrange(RIGHT, buff=0.18)
        right.move_to([6.55, 3.42, 0], aligned_edge=RIGHT)

        rule = Line(
            [-6.72, 3.16, 0],
            [6.72, 3.16, 0],
            color=BORDER,
            stroke_width=1.2,
        )
        active_w = 13.44 / 7
        active = Line(
            [-6.72 + active_w * (index - 1), 3.16, 0],
            [-6.72 + active_w * index, 3.16, 0],
            color=AMBER,
            stroke_width=2.4,
        )
        self.add(left, right, rule, active)


class CaptionBar(VGroup):
    """Bottom-right subtitle card with a speaker chip and two Thai lines."""

    def __init__(self):
        super().__init__()
        width, height = 9.2, 1.08
        self.box = card(width, height, fill=BG, fill_opacity=0.93, radius=0.2)
        self.box.move_to([2.18, -3.18, 0])
        accent = Line(
            self.box.get_corner(UL) + RIGHT * 0.02,
            self.box.get_corner(DL) + RIGHT * 0.02,
            color=AMBER,
            stroke_width=2.4,
        )
        self.speaker = mono_text("", size=15, color=AMBER, weight=BOLD)
        self.speaker.move_to([-2.54, -2.85, 0], aligned_edge=LEFT)
        self.body = Text("", font=FONT_THAI, weight=MEDIUM, font_size=25, color=INK, line_spacing=1.02)
        self.body.move_to([-2.54, -3.22, 0], aligned_edge=LEFT)
        self.add(self.box, accent, self.speaker, self.body)

    def set_line(self, speaker: str, subtitle: str) -> None:
        color = AMBER if speaker == "สมศักดิ์" else TEAL
        label = "สมศักดิ์" if speaker == "สมศักดิ์" else "ผู้บรรยาย"
        new_speaker = that_text(label, size=17, color=color, weight=BOLD)
        new_speaker.move_to([-2.54, -2.85, 0], aligned_edge=LEFT)
        new_body = Text(
            subtitle,
            font=FONT_THAI,
            weight=MEDIUM,
            font_size=25,
            color=INK,
            line_spacing=1.02,
        )
        new_body.move_to([-2.54, -3.22, 0], aligned_edge=LEFT)
        max_w = 8.15
        if new_body.width > max_w:
            new_body.scale_to_fit_width(max_w)
        if new_body.height > 0.62:
            new_body.scale_to_fit_height(0.62)
        new_body.move_to([-2.54, -3.22, 0], aligned_edge=LEFT)
        self.remove(self.speaker, self.body)
        self.speaker, self.body = new_speaker, new_body
        self.add(new_speaker, new_body)


def background_grid() -> VGroup:
    """Faint dot grid + a single soft warm glow, no strobing."""
    dots = VGroup()
    for x in range(-7, 8):
        for y in range(-4, 5):
            dots.add(
                Dot(
                    point=[x * 0.82, y * 0.72, 0],
                    radius=0.009,
                    color=BORDER,
                    fill_opacity=0.55,
                )
            )
    halo = Circle(
        radius=3.6,
        fill_color=SURFACE,
        fill_opacity=0.35,
        stroke_width=0,
    ).move_to([2.2, 0.2, 0])
    return VGroup(halo, dots)


def scene_intro(scene: Scene) -> None:
    scene.camera.background_color = BG


def fade_out_scene(scene: Scene) -> None:
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.35)


def ease_out(duration: float) -> float:
    return max(0.25, duration)
