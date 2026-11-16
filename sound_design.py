"""Procedural sound design: soft SFX + a warm ambient music bed.

No external samples are required; everything is synthesised with numpy so the
project remains reproducible on any machine.
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

from scenes.theme import AUDIO_DIR

SR = 44100
SFX_DIR = AUDIO_DIR / "sfx"


def _write(path: Path, data: np.ndarray, sr: int = SR) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.asarray(data, dtype=np.float64)
    peak = np.max(np.abs(data)) or 1.0
    data = data / peak * 0.9
    pcm = (data * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as fh:
        fh.setnchannels(1)
        fh.setsampwidth(2)
        fh.setframerate(sr)
        fh.writeframes(pcm.tobytes())


def _env(n: int, attack: float = 0.01, release: float = 0.2, sr: int = SR) -> np.ndarray:
    a = max(1, int(attack * sr))
    r = max(1, int(release * sr))
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    return env


def _noise(n: int) -> np.ndarray:
    rng = np.random.default_rng(7)
    return rng.normal(0, 1, n)


def _lowpass(sig: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    alpha = np.exp(-2 * np.pi * cutoff / sr)
    out = np.empty_like(sig)
    acc = 0.0
    for i, value in enumerate(sig):
        acc = (1 - alpha) * value + alpha * acc
        out[i] = acc
    return out


def _sweep_noise(duration: float, f0: float, f1: float, upward: bool = True) -> np.ndarray:
    n = int(duration * SR)
    noise = _noise(n)
    # crude time-varying one-pole filter
    out = np.empty(n)
    acc = 0.0
    for i in range(n):
        t = i / n
        fc = f0 + (f1 - f0) * (t if upward else 1 - t)
        alpha = np.exp(-2 * np.pi * fc / SR)
        acc = (1 - alpha) * noise[i] + alpha * acc
        out[i] = acc
    return out * _env(n, 0.02, duration * 0.5)


def make_sfx() -> None:
    SFX_DIR.mkdir(parents=True, exist_ok=True)

    # pop -------------------------------------------------------------
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    freq = 480 + 700 * (t / 0.16)
    pop = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t * 34)
    _write(SFX_DIR / "pop.wav", pop * 0.5)

    # click -----------------------------------------------------------
    n = int(0.055 * SR)
    t = np.arange(n) / SR
    click = (np.sin(2 * np.pi * 1900 * t) * 0.6 + _noise(n) * 0.4) * np.exp(-t * 90)
    _write(SFX_DIR / "click.wav", click * 0.45)

    # slice -----------------------------------------------------------
    sl = _sweep_noise(0.22, 5000, 1200, upward=False)
    _write(SFX_DIR / "slice.wav", sl * 0.5)

    # whoosh ----------------------------------------------------------
    wh = _sweep_noise(0.65, 500, 3500)
    _write(SFX_DIR / "whoosh.wav", wh * 0.35)

    # stamp -----------------------------------------------------------
    n = int(0.34 * SR)
    t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * (95 - 35 * t / 0.34) * t) * np.exp(-t * 16)
    slap = _lowpass(_noise(n), 900) * np.exp(-t * 30)
    _write(SFX_DIR / "stamp.wav", (thud * 0.9 + slap * 0.5) * 0.8)

    # chime -----------------------------------------------------------
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    bell = sum(
        np.sin(2 * np.pi * f * t + 0.4 * np.sin(2 * np.pi * 5 * t)) * amp * np.exp(-t * decay)
        for f, amp, decay in ((880, 0.5, 2.4), (1320, 0.28, 3.2), (1760, 0.16, 4.0))
    )
    _write(SFX_DIR / "chime.wav", bell * 0.35)

    # ratchet ---------------------------------------------------------
    parts = []
    for i in range(8):
        n = int(0.045 * SR)
        t = np.arange(n) / SR
        c = (np.sin(2 * np.pi * 1600 * t) + _noise(n) * 0.5) * np.exp(-t * 110)
        parts.append(c)
        parts.append(np.zeros(int(0.035 * SR)))
    _write(SFX_DIR / "ratchet.wav", np.concatenate(parts) * 0.4)

    # horn ------------------------------------------------------------
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    horn = (np.sin(2 * np.pi * 523 * t) + 0.6 * np.sin(2 * np.pi * 659 * t)) * _env(n, 0.02, 0.1)
    horn *= 0.55 + 0.45 * np.sin(2 * np.pi * 18 * t)
    _write(SFX_DIR / "horn.wav", horn * 0.32)

    # riser -----------------------------------------------------------
    n = int(1.3 * SR)
    t = np.arange(n) / SR
    freq = 220 * (1 + 3.0 * t / 1.3)
    riser = np.sin(2 * np.pi * np.cumsum(freq) / SR) * (t / 1.3) ** 2
    riser += _sweep_noise(1.3, 400, 4000) * 0.15
    _write(SFX_DIR / "riser.wav", riser * 0.28)

    # arrive (soft two-note resolution) --------------------------------
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * 523.25 * t) * np.exp(-t * 5)
    b = np.sin(2 * np.pi * 783.99 * t) * np.exp(-np.maximum(0, t - 0.12) * 5) * (t > 0.12)
    _write(SFX_DIR / "arrive.wav", (a * 0.5 + b * 0.45) * 0.4)

    print(f"SFX written to {SFX_DIR}")


def _note(freq: float, duration: float, amp: float, attack: float = 0.8, decay: float = 0.0) -> np.ndarray:
    n = int(duration * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / attack) * np.minimum(1, (duration - t) / max(0.2, attack))
    env = np.clip(env, 0, 1)
    if decay:
        env *= np.exp(-t * decay)
    sig = (
        np.sin(2 * np.pi * freq * t)
        + 0.22 * np.sin(2 * np.pi * freq * 2 * t)
        + 0.06 * np.sin(2 * np.pi * freq * 3 * t)
    )
    # gentle detune shimmer
    sig += 0.12 * np.sin(2 * np.pi * (freq * 1.003) * t)
    return sig * env * amp


def _marimba(freq: float, amp: float = 0.2) -> np.ndarray:
    n = int(1.1 * SR)
    t = np.arange(n) / SR
    env = np.exp(-t * 7.0) * np.minimum(1, t / 0.004)
    return (np.sin(2 * np.pi * freq * t) + 0.28 * np.sin(2 * np.pi * freq * 4 * t)) * env * amp


def make_music(duration: float = 260.0) -> Path:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    total = int(duration * SR)
    music = np.zeros(total + SR * 4)

    chords = [
        (110.00, [110.00, 164.81, 196.00, 261.63, 329.63]),   # Am7
        (87.31, [87.31, 130.81, 164.81, 220.00, 261.63]),     # Fmaj7
        (130.81, [130.81, 196.00, 246.94, 329.63, 392.00]),   # Cmaj7
        (98.00, [98.00, 146.83, 196.00, 246.94, 293.66]),     # G6
    ]
    bar = 8.0
    pos = 0.0
    idx = 0
    melody = [659.25, 587.33, 523.25, 440.00, 392.00, 440.00, 523.25, 587.33]
    while pos < duration:
        root, notes = chords[idx % 4]
        pad = np.zeros(int((bar + 0.5) * SR))
        for i, f in enumerate(notes):
            pad += _note(f, bar + 0.5, amp=0.16 / (i * 0.25 + 1), attack=1.6)
        pad += _note(root / 2, bar + 0.5, amp=0.12, attack=1.8)
        start = int(pos * SR)
        end = min(len(music), start + len(pad))
        music[start:end] += pad[: end - start]

        # sparse marimba, never on every beat
        for beat, note_idx in ((1.0, idx % 8), (3.0, (idx + 3) % 8), (6.0, (idx + 5) % 8)):
            t0 = int((pos + beat) * SR)
            if t0 < len(music):
                m = _marimba(melody[note_idx] / 2, amp=0.10)
                e = min(len(music), t0 + len(m))
                music[t0:e] += m[: e - t0]
        pos += bar
        idx += 1

    # soft air layer (two quiet low sines, no expensive full-track filtering)
    t_all = np.arange(len(music)) / SR
    music += 0.018 * np.sin(2 * np.pi * 55 * t_all) + 0.012 * np.sin(2 * np.pi * 82.41 * t_all)

    # slow global fade in/out
    fade_in = int(3 * SR)
    fade_out = int(6 * SR)
    music[:fade_in] *= np.linspace(0, 1, fade_in)
    music[-fade_out:] *= np.linspace(1, 0, fade_out)
    music = music[: int(duration * SR)]

    out = AUDIO_DIR / "music_bed.wav"
    _write(out, music, SR)
    print(f"music bed written to {out} ({duration:.0f}s)")
    return out


if __name__ == "__main__":
    make_sfx()
    make_music()
