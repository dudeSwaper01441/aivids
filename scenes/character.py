"""Nai Somsak and the tiny server clerk, drawn entirely with Manim vectors."""

from __future__ import annotations

import numpy as np
from manim import *
from manim.constants import CapStyleType

from scenes.theme import (
    AMBER,
    BG,
    BORDER,
    CORAL,
    DIM,
    GLASS,
    HAIR,
    INK,
    MUTED,
    SKIN,
    SLACKS,
    TEAL,
    FONT_THAI,
    that_text,
)


def _round_line(start, end, width: float, color: str) -> Line:
    line = Line(start, end, stroke_width=width, color=color)
    line.set_cap_style(CapStyleType.ROUND)
    return line


class Somsak(VGroup):
    """A friendly Thai office worker with five readable expressions."""

    HEAD = np.array([0.0, 2.62, 0.0])

    def __init__(self, position=(-4.55, -3.55, 0), pose: str = "neutral", scale: float = 1.0):
        super().__init__()
        self.pose_name = pose
        self.offset = np.array(position, dtype=float)

        # lower body
        self.lower = VGroup()
        for side in (-1, 1):
            leg = RoundedRectangle(
                width=0.245,
                height=0.98,
                corner_radius=0.10,
                fill_color=SLACKS,
                fill_opacity=1,
                stroke_color=BORDER,
                stroke_width=1.0,
            ).move_to([side * 0.185, 0.62, 0])
            shoe = RoundedRectangle(
                width=0.42,
                height=0.15,
                corner_radius=0.07,
                fill_color=SLACKS,
                fill_opacity=1,
                stroke_color=BORDER,
                stroke_width=1.2,
            ).move_to([side * 0.185, 0.085, 0])
            self.lower.add(shoe, leg)

        # torso / polo
        self.torso = RoundedRectangle(
            width=0.98,
            height=1.10,
            corner_radius=0.24,
            fill_color=AMBER,
            fill_opacity=1,
            stroke_color=BORDER,
            stroke_width=1.4,
        ).move_to([0, 1.66, 0])
        # gentle shading, same hue, no extra palette colour
        shade = RoundedRectangle(
            width=0.94,
            height=0.44,
            corner_radius=0.2,
            fill_color=BG,
            fill_opacity=0.10,
            stroke_width=0,
        ).move_to([0, 1.39, 0])
        placket = Line([0, 2.13, 0], [0, 1.72, 0], stroke_width=2.2, color=BG).set_opacity(0.35)
        buttons = VGroup(
            *[
                Dot(point=[0, y, 0], radius=0.022, color=BG).set_opacity(0.55)
                for y in (2.05, 1.94, 1.83)
            ]
        )
        collar_l = Polygon(
            [-0.03, 2.16, 0],
            [-0.25, 2.21, 0],
            [-0.17, 2.03, 0],
            fill_color=AMBER,
            fill_opacity=1,
            stroke_color=BORDER,
            stroke_width=1.1,
        )
        collar_r = Polygon(
            [0.03, 2.16, 0],
            [0.25, 2.21, 0],
            [0.17, 2.03, 0],
            fill_color=AMBER,
            fill_opacity=1,
            stroke_color=BORDER,
            stroke_width=1.1,
        )
        vneck = Polygon(
            [-0.055, 2.15, 0],
            [0.055, 2.15, 0],
            [0, 2.05, 0],
            fill_color=SKIN,
            fill_opacity=1,
            stroke_width=0,
        )
        self.torso_group = VGroup(self.torso, shade, placket, buttons, collar_l, collar_r, vneck)

        self.neck = Rectangle(width=0.17, height=0.16, fill_color=SKIN, fill_opacity=1, stroke_width=0)
        self.neck.move_to([0, 2.22, 0])

        # head
        ear_l = Circle(radius=0.075, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to([-0.415, 2.60, 0])
        ear_r = Circle(radius=0.075, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to([0.415, 2.60, 0])
        head = Circle(radius=0.43, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to(self.HEAD)
        hair_pts = []
        for a in np.linspace(165, 15, 26):
            rad = a * DEGREES
            hair_pts.append([0.455 * np.cos(rad), 2.62 + 0.455 * np.sin(rad), 0])
        hair_pts += [
            [0.40, 2.83, 0],
            [0.30, 2.90, 0],
            [0.19, 2.835, 0],
            [0.06, 2.905, 0],
            [-0.06, 2.835, 0],
            [-0.19, 2.90, 0],
            [-0.31, 2.835, 0],
            [-0.42, 2.86, 0],
        ]
        hair_cap = Polygon(
            *hair_pts,
            fill_color=HAIR,
            fill_opacity=1,
            stroke_width=0,
        )
        tuft = Polygon(
            [0.03, 3.02, 0],
            [0.16, 3.08, 0],
            [0.11, 2.98, 0],
            fill_color=HAIR,
            fill_opacity=1,
            stroke_width=0,
        )
        sideburn_l = RoundedRectangle(width=0.07, height=0.17, corner_radius=0.03, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([-0.412, 2.735, 0])
        sideburn_r = RoundedRectangle(width=0.07, height=0.17, corner_radius=0.03, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([0.412, 2.735, 0])

        # thin round glasses
        lens_l = RoundedRectangle(width=0.27, height=0.225, corner_radius=0.07, fill_opacity=0, stroke_color=GLASS, stroke_width=2.0).move_to([-0.155, 2.665, 0])
        lens_r = RoundedRectangle(width=0.27, height=0.225, corner_radius=0.07, fill_opacity=0, stroke_color=GLASS, stroke_width=2.0).move_to([0.155, 2.665, 0])
        bridge = Line([-0.02, 2.665, 0], [0.02, 2.665, 0], stroke_width=2.0, color=GLASS)
        temple_l = Line([-0.29, 2.665, 0], [-0.415, 2.64, 0], stroke_width=1.8, color=GLASS)
        temple_r = Line([0.29, 2.665, 0], [0.415, 2.64, 0], stroke_width=1.8, color=GLASS)
        self.glasses = VGroup(lens_l, lens_r, bridge, temple_l, temple_r)

        self.face = self._build_face(pose)
        self.head_group = VGroup(ear_l, ear_r, head, hair_cap, tuft, sideburn_l, sideburn_r, self.glasses, self.face)

        self.arms, self.arm_extras = self._build_arms(pose)
        self.upper = VGroup(self.torso_group, self.neck, self.head_group, self.arms, self.arm_extras)
        self.lower_group = self.lower

        self.add(self.lower_group, self.upper)
        self.scale(scale, about_point=[0, 0, 0])
        self.shift(self.offset)
        self._scale = scale

    # -------------------------------------------------------------- face
    def _build_face(self, pose: str) -> VGroup:
        g = VGroup()
        eye_y = 2.665
        if pose == "shocked":
            for x in (-0.155, 0.155):
                g.add(Circle(radius=0.062, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, eye_y, 0]))
                g.add(Circle(radius=0.026, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([x, eye_y - 0.004, 0]))
            g.add(Circle(radius=0.052, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([0, 2.455, 0]))
            for side in (-1, 1):
                g.add(_round_line([side * 0.155 - 0.09, 2.815, 0], [side * 0.155 + 0.09, 2.86, 0], 3.4, HAIR))
        elif pose == "eureka":
            for x in (-0.155, 0.155):
                g.add(
                    Arc(
                        radius=0.072,
                        start_angle=20 * DEGREES,
                        angle=140 * DEGREES,
                        stroke_width=3.2,
                        color=HAIR,
                    ).shift([x, 2.645, 0])
                )
            g.add(
                Arc(
                    radius=0.155,
                    start_angle=200 * DEGREES,
                    angle=140 * DEGREES,
                    stroke_width=3.0,
                    color=HAIR,
                ).shift([0, 2.47, 0])
            )
            for side in (-1, 1):
                g.add(_round_line([side * 0.16 - 0.085, 2.83, 0], [side * 0.16 + 0.085, 2.83, 0], 3.2, HAIR))
        elif pose == "confused":
            g.add(Circle(radius=0.028, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([-0.155, eye_y, 0]))
            g.add(
                Arc(radius=0.06, start_angle=210 * DEGREES, angle=120 * DEGREES, stroke_width=2.8, color=HAIR).shift([0.155, 2.645, 0])
            )
            g.add(_round_line([-0.245, 2.805, 0], [-0.075, 2.885, 0], 3.2, HAIR))
            g.add(_round_line([0.075, 2.90, 0], [0.245, 2.855, 0], 3.2, HAIR))
            wave = ParametricFunction(
                lambda t: np.array([(t - 0.5) * 0.20, 2.455 + 0.030 * np.sin(t * 3 * PI), 0]),
                t_range=[0, 1],
                stroke_width=2.6,
                color=HAIR,
            )
            g.add(wave)
        elif pose == "dizzy":
            for x in (-0.155, 0.155):
                spiral = ParametricFunction(
                    lambda t, x=x: np.array(
                        [x + 0.058 * t * np.cos(t * 4.2 * PI), eye_y + 0.058 * t * np.sin(t * 4.2 * PI), 0]
                    ),
                    t_range=[0, 1],
                    stroke_width=2.2,
                    color=HAIR,
                )
                g.add(spiral)
            wave = ParametricFunction(
                lambda t: np.array([(t - 0.5) * 0.22, 2.455 + 0.038 * np.sin(t * 4 * PI), 0]),
                t_range=[0, 1],
                stroke_width=2.6,
                color=HAIR,
            )
            g.add(wave)
            for side in (-1, 1):
                g.add(_round_line([side * 0.16 - 0.08, 2.87, 0], [side * 0.16 + 0.08, 2.84, 0], 3.0, HAIR))
        elif pose == "confident":
            for x in (-0.155, 0.155):
                g.add(Circle(radius=0.027, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([x, eye_y, 0]))
            g.add(_round_line([-0.245, 2.84, 0], [-0.065, 2.875, 0], 3.4, HAIR))
            g.add(_round_line([0.065, 2.89, 0], [0.245, 2.88, 0], 3.4, HAIR))
            g.add(
                Arc(radius=0.105, start_angle=205 * DEGREES, angle=95 * DEGREES, stroke_width=2.8, color=HAIR).shift([0.0, 2.465, 0])
            )
        elif pose == "robot":
            for x in (-0.155, 0.155):
                g.add(_round_line([x - 0.05, eye_y, 0], [x + 0.05, eye_y, 0], 3.0, HAIR))
            g.add(_round_line([-0.085, 2.455, 0], [0.085, 2.455, 0], 2.6, HAIR))
            for side in (-1, 1):
                g.add(_round_line([side * 0.16 - 0.08, 2.83, 0], [side * 0.16 + 0.08, 2.83, 0], 3.0, HAIR))
        else:  # neutral
            for x in (-0.155, 0.155):
                g.add(Circle(radius=0.028, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([x, eye_y, 0]))
            g.add(_round_line([-0.085, 2.46, 0], [0.085, 2.46, 0], 2.6, HAIR))
            for side in (-1, 1):
                g.add(_round_line([side * 0.16 - 0.08, 2.835, 0], [side * 0.16 + 0.08, 2.835, 0], 3.0, HAIR))
        return g

    # -------------------------------------------------------------- arms
    def _build_arms(self, pose: str):
        offset = self.offset
        # pose-specific elbow / hand positions in local coordinates
        if pose == "confident":
            right = dict(elbow=(0.80, 2.08), hand=(1.10, 2.24), point=True)
            left = dict(elbow=(0.64, 1.64), hand=(0.52, 1.52), hip=True)
        elif pose == "confused":
            right = dict(elbow=(0.71, 2.30), hand=(0.40, 2.90), scratch=True)
            left = dict(elbow=(0.62, 1.62), hand=(0.55, 1.26))
        elif pose == "shocked":
            right = dict(elbow=(0.78, 2.20), hand=(0.96, 2.56), fingers=True)
            left = dict(elbow=(0.78, 2.20), hand=(0.96, 2.56), fingers=True)
        elif pose == "eureka":
            right = dict(elbow=(0.66, 1.80), hand=(0.78, 2.14), thumb=True)
            left = dict(elbow=(0.62, 1.62), hand=(0.55, 1.25))
        elif pose == "dizzy":
            right = dict(elbow=(0.84, 2.00), hand=(1.10, 2.20), fingers=True)
            left = dict(elbow=(0.84, 2.00), hand=(1.10, 2.20), fingers=True)
        elif pose == "robot":
            right = dict(elbow=(0.62, 1.60), hand=(0.58, 1.22))
            left = dict(elbow=(0.62, 1.60), hand=(0.58, 1.22))
        elif pose == "point_right":
            right = dict(elbow=(0.76, 1.98), hand=(1.08, 2.04), point=True)
            left = dict(elbow=(0.62, 1.62), hand=(0.55, 1.25))
        elif pose == "point_chart":
            right = dict(elbow=(0.74, 2.05), hand=(1.06, 2.24), point=True)
            left = dict(elbow=(0.62, 1.62), hand=(0.55, 1.25))
        else:
            right = dict(elbow=(0.62, 1.60), hand=(0.57, 1.24))
            left = dict(elbow=(0.62, 1.60), hand=(0.57, 1.24))

        arms = VGroup()
        extras = VGroup()
        for side, spec in ((-1, left), (1, right)):
            shoulder = np.array([side * 0.53, 2.04, 0])
            elbow = np.array([side * spec["elbow"][0], spec["elbow"][1], 0])
            hand = np.array([side * spec["hand"][0], spec["hand"][1], 0])
            sleeve_end = shoulder + (elbow - shoulder) * 0.52

            cap = Circle(radius=0.105, fill_color=AMBER, fill_opacity=1, stroke_color=BORDER, stroke_width=1.0).move_to(shoulder)
            sleeve = _round_line(shoulder, sleeve_end, 21, AMBER)
            upper_skin = _round_line(sleeve_end, elbow, 15, SKIN)
            forearm = _round_line(elbow, hand, 14, SKIN)
            palm = Circle(radius=0.072, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to(hand)
            arm = VGroup(cap, sleeve, upper_skin, forearm, palm)
            arms.add(arm)

            if spec.get("point"):
                direction = hand - elbow
                direction = direction / np.linalg.norm(direction)
                tip = hand + direction * 0.17
                extras.add(_round_line(hand, tip, 7, SKIN))
                thumb_dir = np.array([direction[1], -direction[0], 0])
                extras.add(_round_line(hand, hand + thumb_dir * 0.09, 6, SKIN))
            if spec.get("fingers"):
                for i, ang in enumerate((-0.55, -0.15, 0.25)):
                    d = np.array([np.cos(ang), np.sin(ang), 0])
                    extras.add(_round_line(hand, hand + d * 0.11, 6, SKIN))
            if spec.get("thumb"):
                extras.add(
                    RoundedRectangle(
                        width=0.075,
                        height=0.16,
                        corner_radius=0.035,
                        fill_color=SKIN,
                        fill_opacity=1,
                        stroke_width=0,
                    ).move_to(hand + np.array([0.0, 0.10, 0]))
                )
            if spec.get("hip"):
                extras.add(_round_line(hand, np.array([side * 0.34, 1.48, 0]), 6, SKIN))
            if spec.get("scratch"):
                for ang in (0.4, 1.0, 1.6):
                    d = np.array([np.cos(ang) * side, np.sin(ang), 0])
                    extras.add(_round_line(hand, hand + d * 0.09, 5.5, SKIN))
        return arms, extras

    # -------------------------------------------------------------- api
    def change_pose(self, pose: str, run_time: float = 0.45):
        new_arms, new_extras = self._build_arms(pose)
        new_face = self._build_face(pose)
        # built at local coordinates: apply the character's scale/translation once
        for mob in (new_arms, new_extras, new_face):
            mob.scale(self._scale, about_point=ORIGIN).shift(self.offset)
        self.head_group.add(new_face)
        old_face = self.face
        self.face = new_face
        self.pose_name = pose
        anims = [
            Transform(self.arms, new_arms, run_time=run_time),
            FadeOut(old_face, run_time=run_time * 0.55),
            FadeIn(new_face, run_time=run_time),
        ]
        if self.arm_extras.submobjects:
            anims.append(FadeOut(self.arm_extras, run_time=run_time * 0.5))
        self.upper.remove(self.arm_extras)
        self.arm_extras = new_extras
        self.upper.add(new_extras)
        if new_extras.submobjects:
            anims.append(FadeIn(new_extras, run_time=run_time))
        return AnimationGroup(*anims)

    def glow(self, color: str = AMBER, radius: float = 0.62) -> VGroup:
        halo = VGroup()
        for i in (4, 3, 2, 1):
            halo.add(
                Circle(
                    radius=radius + i * 0.075,
                    fill_color=color,
                    fill_opacity=0.045,
                    stroke_width=0,
                )
            )
        halo.move_to(self.head_group.get_center())
        return halo

    def name_tag(self) -> VGroup:
        label = that_text("นายสมศักดิ์", size=22, color=AMBER, weight=BOLD)
        box = RoundedRectangle(
            width=label.width + 0.34,
            height=0.44,
            corner_radius=0.22,
            fill_color=BG,
            fill_opacity=0.92,
            stroke_color=AMBER,
            stroke_width=1.4,
        )
        label.move_to(box)
        tag = VGroup(box, label)
        tag.next_to(self, RIGHT, buff=0.18).align_to(self, UP).shift(DOWN * 0.34)
        return tag


class Clerk(VGroup):
    """The exhausted miniature admin from Scene 1 (and his beach holiday)."""

    def __init__(self, position=(0, 0, 0), scale: float = 1.0, vacation: bool = False, wave: bool = False):
        super().__init__()
        self.vacation = vacation

        legs = VGroup()
        for side in (-1, 1):
            legs.add(
                RoundedRectangle(width=0.11, height=0.34, corner_radius=0.04, fill_color=SLACKS, fill_opacity=1, stroke_width=0).move_to([side * 0.07, 0.17, 0])
            )

        body = RoundedRectangle(
            width=0.34,
            height=0.46,
            corner_radius=0.10,
            fill_color=PERIWINKLE_CLERK,
            fill_opacity=1,
            stroke_color=BORDER,
            stroke_width=1.0,
        ).move_to([0, 0.60, 0])
        collar = Line([-0.09, 0.80, 0], [0.09, 0.80, 0], stroke_width=1.4, color=BG).set_opacity(0.4)

        head = Circle(radius=0.17, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to([0, 1.02, 0])
        hair = Arc(radius=0.16, start_angle=20 * DEGREES, angle=140 * DEGREES, stroke_width=13, color=HAIR).shift([0, 1.02, 0])
        ear_l = Circle(radius=0.032, fill_color=SKIN, stroke_width=0).move_to([-0.165, 1.00, 0])
        ear_r = Circle(radius=0.032, fill_color=SKIN, stroke_width=0).move_to([0.165, 1.00, 0])

        face = VGroup()
        if vacation:
            face.add(
                RoundedRectangle(width=0.09, height=0.065, corner_radius=0.02, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([-0.062, 1.05, 0]),
                RoundedRectangle(width=0.09, height=0.065, corner_radius=0.02, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([0.062, 1.05, 0]),
                Line([-0.045, 1.05, 0], [0.045, 1.05, 0], stroke_width=1.4, color=HAIR),
                Arc(radius=0.05, start_angle=200 * DEGREES, angle=140 * DEGREES, stroke_width=2.0, color=HAIR).shift([0, 0.935, 0]),
            )
        else:
            face.add(
                Circle(radius=0.018, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([-0.06, 1.04, 0]),
                Circle(radius=0.018, fill_color=HAIR, fill_opacity=1, stroke_width=0).move_to([0.06, 1.04, 0]),
                _round_line([-0.04, 0.955, 0], [0.04, 0.955, 0], 1.8, HAIR),
            )
            # tired eyelids + sweat bead
            face.add(
                _round_line([-0.095, 1.065, 0], [-0.025, 1.06, 0], 2.0, HAIR),
                _round_line([0.025, 1.06, 0], [0.095, 1.065, 0], 2.0, HAIR),
            )
            face.add(
                Circle(radius=0.026, fill_color=TEAL, fill_opacity=0.9, stroke_width=0).move_to([0.145, 1.13, 0])
            )

        # headset
        headset = VGroup()
        if not vacation:
            headset.add(Arc(radius=0.185, start_angle=10 * DEGREES, angle=160 * DEGREES, stroke_width=2.2, color=MUTED).shift([0, 1.02, 0]))
            headset.add(Line([-0.175, 1.08, 0], [-0.20, 0.95, 0], stroke_width=2.0, color=MUTED))
            headset.add(Circle(radius=0.020, fill_color=MUTED, stroke_width=0).move_to([-0.20, 0.94, 0]))

        # arms
        arms = VGroup()
        if wave:
            arms.add(_round_line([0.15, 0.74, 0], [0.34, 0.92, 0], 7, PERIWINKLE_CLERK))
            arms.add(_round_line([0.34, 0.92, 0], [0.48, 1.12, 0], 6, SKIN))
            arms.add(Circle(radius=0.035, fill_color=SKIN, stroke_width=0).move_to([0.48, 1.12, 0]))
            arms.add(_round_line([-0.15, 0.74, 0], [-0.28, 0.55, 0], 7, PERIWINKLE_CLERK))
            arms.add(_round_line([-0.28, 0.55, 0], [-0.24, 0.38, 0], 6, SKIN))
        else:
            for side in (-1, 1):
                arms.add(_round_line([side * 0.15, 0.74, 0], [side * 0.27, 0.56, 0], 7, PERIWINKLE_CLERK))
                arms.add(_round_line([side * 0.27, 0.56, 0], [side * 0.20, 0.44, 0], 6, SKIN))
                arms.add(Circle(radius=0.030, fill_color=SKIN, stroke_width=0).move_to([side * 0.20, 0.43, 0]))

        self.papers = VGroup()
        for i, (x, y, rot) in enumerate(((-0.15, 0.34, -8), (0.0, 0.36, 4), (0.14, 0.33, 12))):
            p = Rectangle(width=0.16, height=0.10, fill_color=INK, fill_opacity=0.85, stroke_color=BORDER, stroke_width=0.8)
            p.rotate(rot * DEGREES).move_to([x, y, 0])
            self.papers.add(p)

        self.add(legs, arms, body, collar, head, ear_l, ear_r, hair, face, headset, self.papers)
        self.scale(scale, about_point=ORIGIN)
        self.shift(position)


# a slightly muted periwinkle for the clerk's uniform, kept within the palette family
PERIWINKLE_CLERK = "#7AA2F7"


def beach_chair() -> VGroup:
    """Folding beach chair, drawn with palette colours."""
    frame_color = MUTED
    fabric = TEAL
    back = Polygon(
        [-0.55, 0.10, 0],
        [-0.42, 0.95, 0],
        [0.10, 0.95, 0],
        [0.02, 0.10, 0],
        fill_color=fabric,
        fill_opacity=0.55,
        stroke_color=fabric,
        stroke_width=1.6,
    )
    seat = Polygon(
        [0.02, 0.10, 0],
        [0.10, 0.95, 0],
        [0.78, 0.62, 0],
        [0.52, 0.10, 0],
        fill_color=fabric,
        fill_opacity=0.75,
        stroke_color=fabric,
        stroke_width=1.6,
    )
    legs = VGroup(
        Line([-0.50, 0.10, 0], [-0.62, -0.02, 0], color=frame_color, stroke_width=3),
        Line([0.48, 0.10, 0], [0.60, -0.02, 0], color=frame_color, stroke_width=3),
        Line([-0.42, 0.72, 0], [-0.55, 0.02, 0], color=frame_color, stroke_width=2.4),
        Line([0.10, 0.72, 0], [0.60, 0.02, 0], color=frame_color, stroke_width=2.4),
    )
    return VGroup(legs, back, seat)
