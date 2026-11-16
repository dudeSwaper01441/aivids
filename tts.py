"""Narration generation.

ElevenLabs is the primary provider and is configured **at runtime** from .env.
If no key is present (or a request fails), the line falls back to Edge's Thai
neural voices so the production pipeline can finish end-to-end.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from scenes import narration
from scenes.theme import AUDIO_DIR, ROOT

load_dotenv(ROOT / ".env", override=True)

MANIFEST = AUDIO_DIR / "manifest.json"
DURATIONS = AUDIO_DIR / "durations.json"

ELEVEN_MODEL = os.getenv("ELEVENLABS_MODEL_ID", "eleven_v3").strip() or "eleven_v3"


def _voice_for(speaker: str, provider: str) -> str:
    if provider == "elevenlabs":
        key = "ELEVENLABS_VOICE_SOMSAK" if speaker == "สมศักดิ์" else "ELEVENLABS_VOICE_NARRATOR"
        return os.getenv(key, "").strip()
    key = "EDGE_VOICE_SOMSAK" if speaker == "สมศักดิ์" else "EDGE_VOICE_NARRATOR"
    default = "th-TH-NiwatNeural" if speaker == "สมศักดิ์" else "th-TH-PremwadeeNeural"
    return os.getenv(key, default).strip() or default


def _ffprobe_duration(path: Path) -> float:
    exe = shutil.which("ffprobe") or "ffprobe"
    out = subprocess.check_output(
        [exe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(out.strip())


def _elevenlabs(text: str, voice_id: str, out_path: Path) -> None:
    key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    if not voice_id:
        raise RuntimeError("No ElevenLabs voice ID configured for this speaker")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    payload = {
        "text": text,
        "model_id": ELEVEN_MODEL,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.78,
            "style": 0.25,
            "use_speaker_boost": True,
        },
    }
    # v3/v4 accept an explicit language hint; older models infer it.
    if ELEVEN_MODEL.startswith(("eleven_v3", "eleven_v4")):
        payload["language_code"] = "th"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if len(data) < 2000:
        raise RuntimeError(f"ElevenLabs returned only {len(data)} bytes")
    out_path.write_bytes(data)


def _edge(text: str, voice: str, out_path: Path) -> None:
    import edge_tts

    rate = os.getenv("TTS_RATE", "+0%").strip() or "+0%"

    async def run() -> None:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(str(out_path))

    asyncio.run(run())


def generate(force: bool = False) -> dict:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    durations: dict[str, float] = json.loads(DURATIONS.read_text(encoding="utf-8")) if DURATIONS.exists() else {}
    key = os.getenv("ELEVENLABS_API_KEY", "").strip()

    for item in narration.LINES.values():
        out = AUDIO_DIR / f"{item.key}.mp3"
        entry = manifest.get(item.key, {})
        if out.exists() and out.stat().st_size > 4000 and not force:
            durations[item.key] = round(_ffprobe_duration(out), 3)
            entry.setdefault("provider", "cached")
            manifest[item.key] = entry
            print(f"  cached  {item.key:18s} {durations[item.key]:5.2f}s")
            continue

        providers = []
        if key:
            providers.append(("elevenlabs", _voice_for(item.speaker, "elevenlabs")))
        providers.append(("edge-tts", _voice_for(item.speaker, "edge-tts")))

        last_error = None
        used = None
        for provider, voice in providers:
            for attempt in range(3):
                try:
                    print(f"  {provider:10s} {item.key:18s} attempt {attempt + 1} voice={voice or '(missing)'}")
                    if provider == "elevenlabs":
                        _elevenlabs(item.text, voice, out)
                    else:
                        _edge(item.text, voice, out)
                    used = (provider, voice)
                    break
                except Exception as exc:  # noqa: BLE001 - fall back deliberately
                    last_error = exc
                    print(f"    failed: {type(exc).__name__}: {exc}")
                    time.sleep(1.2)
            if used:
                break

        if not used:
            raise RuntimeError(f"TTS failed for {item.key}: {last_error}")

        duration = _ffprobe_duration(out)
        durations[item.key] = round(duration, 3)
        manifest[item.key] = {
            "provider": used[0],
            "voice": used[1],
            "model": ELEVEN_MODEL if used[0] == "elevenlabs" else "edge-neural",
            "duration": round(duration, 3),
            "text": item.text,
        }
        print(f"  ok      {item.key:18s} {duration:5.2f}s  ({used[0]})")

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    DURATIONS.write_text(json.dumps(durations, ensure_ascii=False, indent=2), encoding="utf-8")
    providers = {v.get("provider") for v in manifest.values()}
    print(f"\nTTS complete. providers={sorted(providers)} total={sum(durations.values()):.1f}s")
    return durations


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="regenerate every line")
    args = parser.parse_args()
    generate(force=args.force)
