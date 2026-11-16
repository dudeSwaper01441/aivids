"""End-to-end build: TTS -> Manim scenes -> concat -> music mix.

Usage:
    python build_video.py                 # full 1080p30 render
    python build_video.py --preview       # 960x540 / 15fps preview
    python build_video.py --scenes Scene1Hook Scene2Tokenizer
    python build_video.py --skip-tts --skip-render --mix-only
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)

MEDIA = ROOT / "build" / "media"
BUILD = ROOT / "build"
AUDIO = ROOT / "audio"

SCENES = [
    ("Scene1Hook", ROOT / "scenes" / "scene1_hook.py"),
    ("Scene2Tokenizer", ROOT / "scenes" / "scene2_tokenizer.py"),
    ("Scene3Attention", ROOT / "scenes" / "scene3_attention.py"),
    ("Scene4Softmax", ROOT / "scenes" / "scene4_softmax.py"),
    ("Scene5Temperature", ROOT / "scenes" / "scene5_temperature.py"),
    ("Scene6Loop", ROOT / "scenes" / "scene6_loop.py"),
    ("Scene7Summary", ROOT / "scenes" / "scene7_summary.py"),
]


def run(cmd: list[str], desc: str = "") -> None:
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"Command failed ({proc.returncode}){' — ' + desc if desc else ''}")
    print(f"  done in {time.time() - started:.1f}s")


def ffprobe(path: Path) -> dict:
    exe = shutil.which("ffprobe") or "ffprobe"
    out = subprocess.check_output(
        [
            exe,
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    return json.loads(out)


def clean_text_cache() -> None:
    texts = MEDIA / "texts"
    if not texts.exists():
        return
    removed = 0
    for svg in texts.glob("*.svg"):
        if svg.stat().st_size == 0:
            svg.unlink(missing_ok=True)
            removed += 1
    if removed:
        print(f"Removed {removed} empty text-cache SVG(s)")


def render_scene(scene: str, path: Path, preview: bool) -> Path:
    if not path.exists():
        raise SystemExit(f"Missing scene file: {path}")
    if not preview:
        cmd = [
            sys.executable,
            "-m",
            "manim",
            str(path),
            scene,
            "--media_dir",
            str(MEDIA),
            "-r",
            "1920,1080",
            "--frame_rate",
            "30",
            "--disable_caching",
            "-v",
            "WARNING",
        ]
    else:
        cmd = [
            sys.executable,
            "-m",
            "manim",
            str(path),
            scene,
            "--media_dir",
            str(MEDIA),
            "-r",
            "960,540",
            "--frame_rate",
            "15",
            "--disable_caching",
            "-v",
            "WARNING",
        ]
    run(cmd, f"render {scene}")

    matches = sorted(MEDIA.glob(f"videos/**/{scene}.mp4"), key=lambda p: p.stat().st_mtime)
    if not matches:
        raise SystemExit(f"Rendered file not found for {scene}")
    return matches[-1]


def concat(scene_files: list[Path], out: Path) -> None:
    listing = BUILD / "concat.txt"
    with listing.open("w", encoding="utf-8") as fh:
        for file in scene_files:
            safe = str(file.resolve()).replace("\\", "/").replace("'", "'\\''")
            fh.write(f"file '{safe}'\n")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(listing),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(out),
    ]
    run(cmd, "concat scenes")
    info = ffprobe(out)
    print(f"  concatenated: {out}  {float(info['format']['duration']):.1f}s")


def mix_music(video: Path, out: Path) -> None:
    music = AUDIO / "music_bed.wav"
    if not music.exists():
        raise SystemExit("Missing audio/music_bed.wav (run sound_design.py)")
    info = ffprobe(video)
    duration = float(info["format"]["duration"])
    fade_start = max(0.0, duration - 4.5)
    filter_complex = (
        f"[1:a]volume=0.13,afade=t=in:st=0:d=3,"
        f"afade=t=out:st={fade_start:.2f}:d=4.5[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-i",
        str(music),
        "-filter_complex",
        filter_complex,
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(out),
    ]
    run(cmd, "mix music")
    final = ffprobe(out)
    print(f"\nFINAL: {out}")
    print(f"  duration : {float(final['format']['duration']):.2f}s")
    print(f"  size     : {int(final['format']['size']) / 1_000_000:.1f} MB")
    for stream in final["streams"]:
        if stream["codec_type"] == "video":
            print(f"  video    : {stream['codec_name']} {stream['width']}x{stream['height']} @ {stream['r_frame_rate']}")
        else:
            print(f"  audio    : {stream['codec_name']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--scenes", nargs="*", default=None)
    parser.add_argument("--skip-tts", action="store_true")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--mix-only", action="store_true")
    parser.add_argument("--skip-sfx", action="store_true")
    args = parser.parse_args()

    BUILD.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)
    clean_text_cache()

    if not args.skip_sfx and not args.mix_only:
        import sound_design

        sound_design.make_sfx()
        sound_design.make_music(duration=260.0)

    if not args.skip_tts and not args.mix_only:
        import tts

        tts.generate(force=False)

    selected = [(name, path) for name, path in SCENES if not args.scenes or name in args.scenes]

    outputs: list[Path] = []
    if not args.skip_render and not args.mix_only:
        for name, path in selected:
            outputs.append(render_scene(name, path, args.preview))
            clean_text_cache()

    concat_file = BUILD / f"concat_{'preview' if args.preview else 'final'}.mp4"
    if args.mix_only:
        concat_file = BUILD / "concat_final.mp4"
        if not concat_file.exists():
            raise SystemExit(f"Missing {concat_file}; render first")
    else:
        if not outputs:
            raise SystemExit("No scenes rendered")
        concat(outputs, concat_file)

    target = BUILD / f"how_llms_predict_next_token{'_preview' if args.preview else ''}.mp4"
    mix_music(concat_file, target)
    final_copy = ROOT / f"how_llms_predict_next_token{'_preview' if args.preview else ''}.mp4"
    shutil.copy2(target, final_copy)
    print(f"Copied to {final_copy}")


if __name__ == "__main__":
    main()
