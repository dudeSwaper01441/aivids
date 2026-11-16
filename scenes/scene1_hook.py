"""Scene 1 — The Hook: the tiny admin inside the server."""

from __future__ import annotations

import numpy as np
from manim import *

from scenes import narration
from scenes.character import Clerk, Somsak
from scenes.icons import ctrl_key, filing_cabinet, server_icon
from scenes.theme import (
    AMBER,
    BG,
    BORDER,
    CORAL,
    DIM,
    INK,
    MUTED,
    PERIWINKLE,
    SURFACE,
    SURFACE_2,
    TEAL,
    CaptionBar,
    Chrome,
    add_line_audio,
    add_sfx,
    apply_theme,
    base,
    card,
    chip,
    divider,
    glow,
    mono_text,
    pill_label,
    that_text,
)

apply_theme()


class Scene1Hook(Scene):
    def construct(self):
        chrome, captions = base(self, 1, "THE HOOK", "ความเข้าใจผิด")

        # ---------------------------------------------------------- intro
        somsak = Somsak(position=(-5.05, -3.52, 0), pose="neutral")
        name = somsak.name_tag()
        name.next_to(somsak.head_group, RIGHT, buff=0.16).shift(UP * 0.02)

        chat = card(8.35, 4.55, fill=SURFACE, radius=0.26).move_to([2.03, 0.52, 0])
        top_bar = RoundedRectangle(
            width=8.35,
            height=0.52,
            corner_radius=0.26,
            fill_color=SURFACE_2,
            fill_opacity=1,
            stroke_width=0,
        ).move_to([2.03, 2.53, 0])
        top_bar.set_height(0.5)
        dots = VGroup(
            *[
                Circle(radius=0.055, fill_color=c, fill_opacity=0.9, stroke_width=0).move_to([-1.35 + i * 0.17, 2.53, 0])
                for i, c in enumerate((CORAL, AMBER, TEAL))
            ]
        )
        chat_title = mono_text("AI CHAT", size=17, color=MUTED, weight=BOLD).move_to([2.60, 2.53, 0])
        status = VGroup(
            Circle(radius=0.045, fill_color=TEAL, fill_opacity=1, stroke_width=0),
            mono_text("ONLINE", size=12, color=TEAL),
        )
        status.arrange(RIGHT, buff=0.10).move_to([5.48, 2.53, 0])

        prompt_box = card(7.55, 0.92, fill=BG, radius=0.16, fill_opacity=0.55)
        prompt_box.move_to([2.00, 1.58, 0])
        prompt_label = mono_text("PROMPT", size=13, color=MUTED).move_to([-1.55, 1.86, 0], aligned_edge=LEFT)
        prompt = that_text(
            "เช้านี้สมศักดิ์ตื่นสาย เลยรีบวิ่งไปขึ้น...",
            size=30,
            color=INK,
            max_width=6.9,
        ).move_to([-1.55, 1.55, 0], aligned_edge=LEFT)
        cursor = Line([-1.55, 1.36, 0], [-1.55, 1.70, 0], color=AMBER, stroke_width=2.6)

        send = VGroup(
            Circle(radius=0.30, fill_color=AMBER, fill_opacity=0.9, stroke_width=0),
            Triangle(fill_color=BG, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-90 * DEGREES).shift(RIGHT * 0.03),
        ).move_to([5.55, 1.55, 0])

        response = card(7.55, 2.35, fill=SURFACE_2, radius=0.16, fill_opacity=0.55)
        response.move_to([2.00, -0.62, 0])
        typing_dots = VGroup(
            *[Dot(point=[1.55 + i * 0.16, -0.55, 0], radius=0.035, color=MUTED) for i in range(3)]
        )
        typing_label = mono_text("AI TYPING...", size=14, color=MUTED).move_to([0.55, -0.55, 0])
        typing_group = VGroup(typing_label, typing_dots)

        chat_group = VGroup(chat, top_bar, dots, chat_title, status, prompt_box, prompt_label, prompt, cursor, send, response, typing_group)
        chat_group.shift(RIGHT * 0.6).set_opacity(0)

        self.play(
            FadeIn(somsak, shift=UP * 0.15),
            FadeIn(name, shift=UP * 0.1),
            run_time=0.9,
        )
        self.play(
            chat_group.animate.shift(LEFT * 0.6).set_opacity(1),
            run_time=0.9,
        )
        self.play(Write(prompt, run_time=1.6), Create(cursor, run_time=0.4), run_time=1.7)
        self.play(*[dot.animate.set_color(AMBER) for dot in typing_dots], run_time=0.4)
        self.play(
            Circle(radius=0.42, color=AMBER, stroke_width=2, fill_opacity=0).move_to(send).animate.scale(1.5).set_opacity(0),
            run_time=0.6,
        )
        self.wait(1.4)

        # ---------------------------------------------------------- Somsak's misconception
        d = narration.dur("s1_somsak")
        line = narration.line("s1_somsak")
        captions.set_line(line.speaker, line.subtitle)
        add_line_audio(self, line.key)
        self.play(
            FadeOut(name, run_time=0.3),
            somsak.change_pose("confident"),
            run_time=0.55,
        )

        xray = card(7.55, 2.35, fill=SURFACE_2, radius=0.16).move_to([2.00, -0.62, 0])
        xray_title = mono_text("X-RAY · INSIDE THE AI SERVER", size=15, color=CORAL, weight=BOLD)
        xray_title.move_to([-1.40, 0.36, 0], aligned_edge=LEFT)

        tint = RoundedRectangle(
            width=7.45,
            height=2.22,
            corner_radius=0.13,
            fill_color=CORAL,
            fill_opacity=0.075,
            stroke_color=CORAL,
            stroke_width=1.0,
        ).move_to([2.00, -0.62, 0])

        clerk = Clerk(position=(0.05, -1.42, 0), scale=0.82)
        cabinets = VGroup(
            filing_cabinet(scale=0.84, color=CORAL).move_to([1.55, -0.62, 0]),
            filing_cabinet(scale=0.84, color=CORAL).move_to([2.48, -0.62, 0]),
            filing_cabinet(scale=0.84, color=CORAL).move_to([3.41, -0.62, 0]),
        )
        ctrl = ctrl_key(scale=1.35).move_to([0.75, 0.02, 0])
        papers = VGroup()
        for i, (x, y, rot) in enumerate(((0.30, -0.55, -12), (0.62, -0.80, 18), (0.05, -0.95, 6))):
            p = Rectangle(width=0.2, height=0.13, fill_color=INK, fill_opacity=0.5, stroke_color=CORAL, stroke_width=0.8)
            p.rotate(rot * DEGREES).move_to([x, y, 0])
            papers.add(p)
        myth = pill_label("MYTH", CORAL, size=22, mono=True).move_to([4.85, 0.40, 0])

        fantasy = VGroup(xray, xray_title, tint, clerk, cabinets, ctrl, papers)
        self.play(
            FadeOut(typing_group),
            FadeIn(xray),
            FadeIn(xray_title),
            FadeIn(tint),
            LaggedStart(
                FadeIn(clerk), FadeIn(cabinets[0]), FadeIn(cabinets[1]), FadeIn(cabinets[2]),
                lag_ratio=0.18,
            ),
            FadeIn(ctrl),
            FadeIn(papers),
            FadeIn(myth, scale=0.9),
            run_time=1.8,
        )
        self.play(
            *[p.animate.shift(UP * 0.12 + RIGHT * 0.05) for p in papers],
            ctrl.animate.scale(1.12),
            run_time=max(1.0, d * 0.28),
        )
        self.play(
            *[p.animate.shift(DOWN * 0.20 + RIGHT * 0.08).rotate(12 * DEGREES) for p in papers],
            ctrl.animate.scale(1 / 1.12),
            run_time=max(0.8, d * 0.20),
        )
        remaining = d - 0.55 - 1.8 - max(1.0, d * 0.28) - max(0.8, d * 0.20) - 0.3
        self.play(
            VGroup(clerk, cabinets, ctrl).animate.shift(UP * 0.02),
            run_time=max(0.5, remaining),
        )

        # ---------------------------------------------------------- narrator debunks
        d2 = narration.dur("s1_narrator")
        line = narration.line("s1_narrator")
        captions.set_line(line.speaker, line.subtitle)
        add_line_audio(self, line.key)
        add_sfx(self, "stamp")
        self.play(somsak.change_pose("confused"), run_time=0.6)

        # stamp the myth badge hard (short, no strobe)
        self.play(
            myth.animate.scale(1.35).rotate(-4 * DEGREES).move_to([4.55, 0.38, 0]),
            Flash(myth, color=CORAL, flash_radius=0.55, line_length=0.12, num_lines=8, run_time=0.5),
            run_time=0.55,
        )
        self.play(myth.animate.scale(1 / 1.25).rotate(4 * DEGREES).move_to([4.85, 0.40, 0]), run_time=0.4)

        # cabinets dissolve into numbers and probability bars
        numbers = VGroup()
        for i, txt in enumerate(("4821", "9104", "0.62", "24.1", "0.01", "7732")):
            n = mono_text(txt, size=20, color=TEAL, weight=BOLD)
            n.move_to([0.9 + (i % 3) * 1.15 + 0.1 * (i // 3), -0.25 - 0.55 * (i // 3), 0])
            numbers.add(n)
        bars = VGroup(
            *[
                RoundedRectangle(
                    width=0.55 + i * 0.15,
                    height=0.09,
                    corner_radius=0.04,
                    fill_color=TEAL,
                    fill_opacity=0.55,
                    stroke_width=0,
                ).move_to([2.15, -1.25 + i * 0.18, 0])
                for i in range(4)
            ]
        )
        add_sfx(self, "whoosh")
        self.play(
            FadeOut(cabinets, shift=UP * 0.25),
            FadeOut(papers, shift=UP * 0.2),
            FadeOut(ctrl),
            FadeOut(tint),
            FadeOut(xray_title),
            FadeOut(myth),
            FadeOut(clerk, shift=DOWN * 0.15),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in numbers], lag_ratio=0.12),
            LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.12),
            run_time=1.0,
        )
        self.play(
            numbers.animate.shift(UP * 0.25).set_opacity(0.35),
            bars.animate.shift(UP * 0.05),
            run_time=max(0.8, d2 * 0.20),
        )

        # clean pipeline reveal
        pipeline_title = mono_text("THE REAL PIPELINE", size=15, color=TEAL, weight=BOLD)
        pipeline_title.move_to([2.0, 0.30, 0])
        pipeline = VGroup()
        labels = ("TEXT", "TOKENS", "TRANSFORMER", "NEXT TOKEN")
        colors = (MUTED, TEAL, PERIWINKLE, AMBER)
        for i, (lab, col) in enumerate(zip(labels, colors)):
            box = RoundedRectangle(
                width=1.42 if lab != "TRANSFORMER" else 1.78,
                height=0.56,
                corner_radius=0.14,
                fill_color=BG,
                fill_opacity=0.75,
                stroke_color=col,
                stroke_width=1.5,
            )
            t = mono_text(lab, size=13, color=col, weight=BOLD)
            t.move_to(box)
            pipeline.add(VGroup(box, t))
        pipeline.arrange(RIGHT, buff=0.30).move_to([2.0, -0.38, 0])
        arrows = VGroup()
        for i in range(3):
            arrows.add(
                Arrow(
                    pipeline[i].get_right(),
                    pipeline[i + 1].get_left(),
                    buff=0.04,
                    stroke_width=2.4,
                    color=TEAL,
                    max_tip_length_to_length_ratio=0.35,
                )
            )
        pipeline.add(arrows)
        statement = that_text("ไม่ได้ค้นคำตอบ — มันทายทีละ Token", size=25, color=INK, weight=BOLD)
        statement.move_to([2.0, -1.42, 0])

        self.play(
            FadeOut(numbers),
            FadeOut(bars),
            FadeOut(xray),
            FadeIn(pipeline_title, shift=UP * 0.08),
            FadeIn(pipeline[0], shift=UP * 0.1),
            run_time=0.7,
        )
        for i in range(1, 4):
            self.play(
                GrowArrow(arrows[i - 1]),
                FadeIn(pipeline[i], shift=RIGHT * 0.12),
                run_time=0.5,
            )
        add_sfx(self, "chime")
        self.play(
            FadeIn(statement, shift=UP * 0.08),
            pipeline.animate.shift(UP * 0.04),
            run_time=max(0.7, d2 - 0.6 - 1.2 - 1.0 - max(0.8, d2 * 0.20) - 0.7 - 1.5 - 0.7),
        )
        self.play(somsak.change_pose("eureka"), run_time=0.6)
        self.play(
            Flash(pipeline[2], color=TEAL, flash_radius=0.8, line_length=0.12, num_lines=6),
            run_time=0.5,
        )
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.35)
