"""Small vector icons used by the seven scenes."""

from __future__ import annotations

import numpy as np
from manim import *

from scenes.theme import AMBER, BG, BORDER, CORAL, INK, MUTED, PERIWINKLE, SURFACE, TEAL, mono_text


def _wheel(center, r=0.13):
    return VGroup(
        Circle(radius=r, fill_color=BG, fill_opacity=1, stroke_color=MUTED, stroke_width=3),
        Circle(radius=r * 0.38, fill_color=MUTED, fill_opacity=1, stroke_width=0),
    ).move_to(center)


def bus_icon(scale: float = 1.0, color: str = PERIWINKLE) -> VGroup:
    body = RoundedRectangle(
        width=1.55,
        height=0.78,
        corner_radius=0.14,
        fill_color=color,
        fill_opacity=0.95,
        stroke_color=color,
        stroke_width=1.5,
    )
    window = RoundedRectangle(
        width=0.42,
        height=0.34,
        corner_radius=0.06,
        fill_color=BG,
        fill_opacity=0.85,
        stroke_width=0,
    ).move_to([-0.40, 0.12, 0])
    windows = VGroup(
        window,
        RoundedRectangle(width=0.56, height=0.34, corner_radius=0.06, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to([0.14, 0.12, 0]),
        RoundedRectangle(width=0.28, height=0.34, corner_radius=0.06, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to([0.61, 0.12, 0]),
    )
    stripe = Line([-0.72, -0.16, 0], [0.72, -0.16, 0], stroke_width=3, color=TEAL)
    wheels = VGroup(_wheel([-0.45, -0.42, 0]), _wheel([0.48, -0.42, 0]))
    lights = VGroup(
        Circle(radius=0.045, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([0.74, -0.14, 0])
    )
    icon = VGroup(body, windows, stripe, wheels, lights)
    return icon.scale(scale)


def motorcycle_icon(scale: float = 1.0, color: str = PERIWINKLE) -> VGroup:
    wheels = VGroup(_wheel([-0.45, -0.35, 0], 0.15), _wheel([0.48, -0.35, 0], 0.15))
    frame = VGroup(
        Line([-0.40, -0.30, 0], [-0.05, 0.05, 0], stroke_width=6, color=color),
        Line([-0.05, 0.05, 0], [0.25, -0.30, 0], stroke_width=6, color=color),
        Line([0.25, -0.30, 0], [0.46, -0.30, 0], stroke_width=5, color=color),
    )
    seat = RoundedRectangle(width=0.42, height=0.12, corner_radius=0.05, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0.05, 0.12, 0])
    handle = VGroup(
        Line([0.30, 0.02, 0], [0.40, 0.30, 0], stroke_width=4, color=MUTED),
        Line([0.30, 0.30, 0], [0.52, 0.30, 0], stroke_width=4, color=MUTED),
    )
    helmet = Circle(radius=0.10, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([0.05, 0.33, 0])
    return VGroup(wheels, frame, seat, handle, helmet).scale(scale)


def train_icon(scale: float = 1.0, color: str = PERIWINKLE) -> VGroup:
    body = RoundedRectangle(width=1.45, height=0.82, corner_radius=0.24, fill_color=color, fill_opacity=0.95, stroke_color=color, stroke_width=1.5)
    window = RoundedRectangle(width=0.44, height=0.30, corner_radius=0.08, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to([-0.36, 0.13, 0])
    window2 = RoundedRectangle(width=0.44, height=0.30, corner_radius=0.08, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to([0.22, 0.13, 0])
    nose = Line([0.62, 0.32, 0], [0.78, 0.0, 0], stroke_width=5, color=color)
    stripe = Line([-0.66, -0.16, 0], [0.66, -0.16, 0], stroke_width=3, color=TEAL)
    wheels = VGroup(_wheel([-0.42, -0.44, 0], 0.11), _wheel([0.42, -0.44, 0], 0.11))
    rail = Line([-0.75, -0.56, 0], [0.80, -0.56, 0], stroke_width=2.5, color=MUTED)
    panto = VGroup(
        Line([0.05, 0.42, 0], [0.22, 0.58, 0], stroke_width=3, color=MUTED),
        Line([0.22, 0.58, 0], [0.40, 0.42, 0], stroke_width=3, color=MUTED),
    )
    return VGroup(body, window, window2, nose, stripe, wheels, rail, panto).scale(scale)


def taxi_icon(scale: float = 1.0, color: str = PERIWINKLE) -> VGroup:
    body = RoundedRectangle(width=1.45, height=0.42, corner_radius=0.15, fill_color=color, fill_opacity=0.95, stroke_color=color, stroke_width=1.5)
    cabin = RoundedRectangle(width=0.80, height=0.40, corner_radius=0.16, fill_color=color, fill_opacity=0.95, stroke_color=color, stroke_width=1.5).move_to([-0.05, 0.28, 0])
    glass = RoundedRectangle(width=0.58, height=0.24, corner_radius=0.07, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to([-0.05, 0.30, 0])
    sign = RoundedRectangle(width=0.32, height=0.14, corner_radius=0.05, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([-0.05, 0.53, 0])
    wheels = VGroup(_wheel([-0.45, -0.26, 0], 0.13), _wheel([0.45, -0.26, 0], 0.13))
    lights = VGroup(Circle(radius=0.04, fill_color=AMBER, stroke_width=0).move_to([0.70, 0.02, 0]))
    return VGroup(body, cabin, glass, sign, wheels, lights).scale(scale)


def airship_icon(scale: float = 1.0, color: str = CORAL, gondola_color: str = PERIWINKLE) -> VGroup:
    blimp = Ellipse(width=1.75, height=0.72, fill_color=color, fill_opacity=0.92, stroke_color=color, stroke_width=1.5)
    fin_top = Polygon([-0.70, 0.22, 0], [-0.98, 0.52, 0], [-0.92, 0.16, 0], fill_color=color, fill_opacity=0.9, stroke_width=0)
    fin_bottom = Polygon([-0.70, -0.22, 0], [-0.98, -0.52, 0], [-0.92, -0.16, 0], fill_color=color, fill_opacity=0.9, stroke_width=0)
    gondola = RoundedRectangle(width=0.58, height=0.22, corner_radius=0.10, fill_color=gondola_color, fill_opacity=1, stroke_color=gondola_color, stroke_width=1.2).move_to([0.06, -0.44, 0])
    window = RoundedRectangle(width=0.36, height=0.075, corner_radius=0.03, fill_color=BG, fill_opacity=0.9, stroke_width=0).move_to([0.06, -0.42, 0])
    prop = VGroup(
        Line([0.86, -0.38, 0], [1.05, -0.38, 0], stroke_width=3, color=MUTED),
        Ellipse(width=0.07, height=0.42, fill_color=MUTED, fill_opacity=0.8, stroke_width=0).move_to([1.05, -0.38, 0]),
    )
    return VGroup(fin_top, fin_bottom, blimp, gondola, window, prop).scale(scale)


def tree_icon(scale: float = 1.0, color: str = TEAL) -> VGroup:
    trunk = RoundedRectangle(width=0.16, height=0.55, corner_radius=0.05, fill_color=AMBER, fill_opacity=0.55, stroke_width=0).move_to([0, -0.30, 0])
    foliage = VGroup(
        Circle(radius=0.30, fill_color=color, fill_opacity=0.65, stroke_color=color, stroke_width=1.2).move_to([-0.20, 0.18, 0]),
        Circle(radius=0.38, fill_color=color, fill_opacity=0.65, stroke_color=color, stroke_width=1.2).move_to([0.18, 0.28, 0]),
        Circle(radius=0.26, fill_color=color, fill_opacity=0.65, stroke_color=color, stroke_width=1.2).move_to([0.04, 0.58, 0]),
    )
    return VGroup(trunk, foliage).scale(scale)


def cloud_icon(scale: float = 1.0, color: str = MUTED) -> VGroup:
    puffs = VGroup(
        Circle(radius=0.26, fill_color=color, fill_opacity=0.28, stroke_color=color, stroke_width=1.4).move_to([-0.30, 0.0, 0]),
        Circle(radius=0.36, fill_color=color, fill_opacity=0.28, stroke_color=color, stroke_width=1.4).move_to([0.05, 0.14, 0]),
        Circle(radius=0.24, fill_color=color, fill_opacity=0.28, stroke_color=color, stroke_width=1.4).move_to([0.40, -0.02, 0]),
        RoundedRectangle(width=0.95, height=0.24, corner_radius=0.12, fill_color=color, fill_opacity=0.28, stroke_width=0).move_to([0.05, -0.12, 0]),
    )
    halo = Ellipse(width=0.42, height=0.12, stroke_color=AMBER, stroke_width=5, fill_opacity=0).move_to([0.05, 0.62, 0])
    return VGroup(halo, puffs).scale(scale)


def server_icon(scale: float = 1.0, color: str = CORAL) -> VGroup:
    rack = RoundedRectangle(width=0.9, height=1.3, corner_radius=0.10, fill_color="#2A323D", fill_opacity=0.9, stroke_color=color, stroke_width=2.0)
    units = VGroup()
    for i in range(4):
        y = 0.44 - i * 0.28
        units.add(Line([-0.34, y, 0], [0.34, y, 0], stroke_width=2, color=BORDER))
        units.add(Circle(radius=0.028, fill_color=color, fill_opacity=0.9, stroke_width=0).move_to([-0.27, y + 0.08, 0]))
        units.add(Line([-0.12, y + 0.08, 0], [0.30, y + 0.08, 0], stroke_width=3, color=MUTED))
    return VGroup(rack, units).scale(scale)


def filing_cabinet(scale: float = 1.0, color: str = CORAL) -> VGroup:
    body = RoundedRectangle(width=0.75, height=1.35, corner_radius=0.06, fill_color=color, fill_opacity=0.25, stroke_color=color, stroke_width=1.8)
    drawers = VGroup()
    for i in range(4):
        y = 0.47 - i * 0.29
        drawers.add(RoundedRectangle(width=0.61, height=0.23, corner_radius=0.03, fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=1.0).move_to([0, y, 0]))
        drawers.add(Line([-0.12, y, 0], [0.12, y, 0], stroke_width=3, color=color))
    return VGroup(body, drawers).scale(scale)


def ctrl_key(scale: float = 1.0) -> VGroup:
    label = mono_text("Ctrl+F", size=19, color=CORAL, weight=BOLD)
    key = RoundedRectangle(
        width=label.width + 0.28,
        height=label.height + 0.20,
        corner_radius=0.07,
        fill_color=SURFACE,
        fill_opacity=1,
        stroke_color=CORAL,
        stroke_width=1.8,
    )
    label.move_to(key)
    return VGroup(key, label).scale(scale)


def office_icon(scale: float = 1.0, color: str = PERIWINKLE) -> VGroup:
    tower = RoundedRectangle(width=0.78, height=1.15, corner_radius=0.05, fill_color=color, fill_opacity=0.22, stroke_color=color, stroke_width=1.6)
    windows = VGroup()
    for row in range(3):
        for col in range(2):
            windows.add(
                RoundedRectangle(width=0.18, height=0.15, corner_radius=0.02, fill_color=color, fill_opacity=0.7, stroke_width=0).move_to([-0.18 + col * 0.36, -0.28 + row * 0.33, 0])
            )
    door = Rectangle(width=0.22, height=0.26, fill_color=BG, fill_opacity=0.9, stroke_width=0).move_to([0, -0.44, 0])
    return VGroup(tower, windows, door).scale(scale)


def clock_icon(scale: float = 1.0, color: str = TEAL) -> VGroup:
    rim = Circle(radius=0.34, fill_color=BG, fill_opacity=0.4, stroke_color=color, stroke_width=2.4)
    hands = VGroup(
        Line([0, 0, 0], [0, 0.20, 0], stroke_width=3, color=color),
        Line([0, 0, 0], [0.15, -0.04, 0], stroke_width=3, color=color),
    )
    return VGroup(rim, hands).scale(scale)


def check_icon(scale: float = 1.0, color: str = TEAL) -> VGroup:
    return VGroup(
        Circle(radius=0.20, fill_color=color, fill_opacity=0.16, stroke_color=color, stroke_width=1.6),
        Line([-0.09, 0.0, 0], [-0.02, -0.08, 0], stroke_width=3.4, color=color),
        Line([-0.02, -0.08, 0], [0.10, 0.09, 0], stroke_width=3.4, color=color),
    ).scale(scale)


def cross_icon(scale: float = 1.0, color: str = CORAL) -> VGroup:
    return VGroup(
        Circle(radius=0.20, fill_color=color, fill_opacity=0.16, stroke_color=color, stroke_width=1.6),
        Line([-0.07, 0.07, 0], [0.07, -0.07, 0], stroke_width=3.4, color=color),
        Line([-0.07, -0.07, 0], [0.07, 0.07, 0], stroke_width=3.4, color=color),
    ).scale(scale)
