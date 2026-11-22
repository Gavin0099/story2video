"""Render the local 73H pilot and its two selectable caption tracks."""

import argparse
import hashlib
import json
import os
import subprocess
import time
import wave
from itertools import groupby
from pathlib import Path

FPS = 30
RATE = 24000
FRAME_SAMPLES = RATE // FPS
SOURCE = Path(__file__).with_name("story.json")
ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: English,Segoe UI,54,&H00FFFFFF,&H00FFFFFF,&H00101417,&H64101417,-1,0,0,0,100,100,0,0,1,3,1,2,0,0,0,1
Style: Chinese,Microsoft JhengHei,51,&H00E2EDFF,&H00E2EDFF,&H00101417,&H64101417,-1,0,0,0,100,100,0,0,1,3,1,2,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def verify_file(path, size, sha256):
    if not path.is_absolute() or path.resolve(strict=True) != path:
        raise ValueError(f"Expected a canonical absolute path: {path}")
    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
    if path.stat().st_size != size or actual != sha256:
        raise ValueError(f"File differs from the render manifest: {path.name}")


def srt_time(frame):
    minutes, milliseconds = divmod(round(frame * 1000 / FPS), 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"00:{minutes:02}:{seconds:02},{milliseconds:03}"


def ass_time(frame):
    minutes, centiseconds = divmod(round(frame * 100 / FPS), 6000)
    seconds, centiseconds = divmod(centiseconds, 100)
    return f"0:{minutes:02}:{seconds:02}.{centiseconds:02}"


def make_timeline(work):
    import numpy as np
    from kokoro_onnx import Kokoro

    narrator = Kokoro(
        str(work / "models" / "kokoro-v1.0.int8.onnx"),
        str(work / "models" / "voices-v1.0.bin"),
    )
    script = json.loads(SOURCE.read_text(encoding="utf-8"))
    timeline = []
    parts = [np.zeros(6 * FRAME_SAMPLES, dtype=np.float32)]
    cursor = 6
    for index, cue in enumerate(script):
        text = cue["en"].replace("\n", " ")
        voice, rate = narrator.create(text, voice="am_michael", speed=0.93, lang="en-us")
        if rate != RATE or not len(voice) or not np.isfinite(voice).all():
            raise ValueError(f"Invalid narration for cue {index + 1}")
        speech_frames = (len(voice) + FRAME_SAMPLES - 1) // FRAME_SAMPLES
        pause_frames = round(cue["pause"] * FPS)
        end = cursor + speech_frames + pause_frames
        timeline.append({
            **cue, "start": cursor, "cut": 0 if index == 0 else cursor, "end": end,
        })
        parts.append(np.pad(voice, (0, (end - cursor) * FRAME_SAMPLES - len(voice))))
        cursor = end

    if not 45 * FPS <= cursor <= 60 * FPS:
        raise ValueError(f"Expected 45–60 seconds, got {cursor / FPS:.2f} seconds")

    narration = np.concatenate(parts)
    narration *= 0.79 / np.max(np.abs(narration))
    # Low, continuous rain under the speech, with short ramps at the ends.
    noise = np.random.default_rng(73).standard_normal(len(narration))
    rain = np.convolve(noise, np.ones(13) / 13, mode="same") * 0.024
    ramp = np.linspace(0, 1, RATE // 2)
    rain[:len(ramp)] *= ramp
    rain[-len(ramp):] *= ramp[::-1]
    audio = np.clip(narration + rain, -1, 1)
    with wave.open(str(work / "mix.wav"), "wb") as output:
        output.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        output.writeframes((audio * 32767).astype("<i2").tobytes())
    return timeline


def write_captions(work, timeline):
    tracks = {"en": [], "zh": []}
    events = []
    for index, cue in enumerate(timeline, 1):
        for language, style, y in (("en", "English", 1510), ("zh", "Chinese", 1650)):
            caption = cue[language]
            tracks[language].append(
                f"{index}\n{srt_time(cue['start'])} --> {srt_time(cue['end'])}\n{caption}"
            )
            ass_text = caption.replace("\n", r"\N")
            events.append(
                f"Dialogue: 0,{ass_time(cue['start'])},{ass_time(cue['end'])},"
                f"{style},,0,0,0,,{{\\pos(503,{y})}}{ass_text}\n"
            )
    for language, filename in (("en", "73H.en.srt"), ("zh", "73H.zh-Hant.srt")):
        (work / filename).write_text("\n\n".join(tracks[language]) + "\n", encoding="utf-8")
    (work / "bilingual.ass").write_text(ASS_HEADER + "".join(events), encoding="utf-8")


def render(work, ffmpeg, binding, timeline):
    verify_file(ffmpeg, **binding)
    environment = {key: os.environ[key] for key in ("SystemRoot", "WINDIR") if key in os.environ}
    environment.update({"TEMP": str(work), "TMP": str(work)})

    def encode(*args):
        verify_file(ffmpeg, **binding)
        subprocess.run(
            [str(ffmpeg), "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
             "-filter_threads", "2", *args],
            cwd=work, env=environment, check=True,
        )

    h264 = ("-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-threads", "4",
            "-pix_fmt", "yuv420p")
    segments = []
    for index, (shot, group) in enumerate(groupby(timeline, key=lambda cue: cue["shot"]), 1):
        cues = list(group)
        frames = cues[-1]["end"] - cues[0]["cut"]
        row, column = divmod(shot - 1, 3)
        # Crop inside each panel to keep the neighboring shot out of the frame.
        x, y = 384 * column + 3, 683 * row + 5
        zoom = f"1+0.085*on/{frames}"
        filters = (
            f"crop=378:672:{x}:{y},scale=2160:3840:flags=lanczos,"
            f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
            f"d={frames}:s=1080x1920:fps={FPS},setsar=1"
        )
        name = f"shot-{index:02}.mp4"
        encode("-i", "storyboard.png", "-vf", filters, "-frames:v", str(frames), *h264, name)
        segments.append(f"file '{name}'\nduration {frames / FPS:.9f}\n")

    (work / "shots.txt").write_text("".join(segments), encoding="ascii")
    audio = ("-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", "-c:a", "aac",
             "-b:a", "128k", "-movflags", "+faststart")
    encode("-f", "concat", "-safe", "1", "-i", "shots.txt", "-i", "mix.wav",
           "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", *audio, "73H-master.mp4")
    encode("-i", "73H-master.mp4", "-i", "73H.en.srt", "-i", "73H.zh-Hant.srt",
           "-map", "0:v:0", "-map", "0:a:0", "-map", "1:s:0", "-map", "2:s:0",
           "-c", "copy", "-movflags", "+faststart", "-c:s", "mov_text",
           "-metadata:s:s:0", "language=eng", "-metadata:s:s:0", "handler_name=English",
           "-metadata:s:s:1", "language=zho", "-metadata:s:s:1", "handler_name=Traditional Chinese",
           "-disposition:s:0", "default", "-disposition:s:1", "0", "73H-selectable.mp4")
    encode("-i", "73H-master.mp4", "-vf", "ass=bilingual.ass", *h264,
           "-c:a", "copy", "-movflags", "+faststart", "73H-bilingual.mp4")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--ffmpeg", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    verify_file(args.ffmpeg, **manifest["ffmpeg"])
    work = args.work.resolve(strict=True)
    for name, binding in manifest["inputs"].items():
        verify_file(work / name, **binding)
    start = time.perf_counter()
    timeline = make_timeline(work)
    write_captions(work, timeline)
    (work / "timeline.json").write_text(
        json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tts_seconds = time.perf_counter() - start
    render(work, args.ffmpeg, manifest["ffmpeg"], timeline)
    print(f"{timeline[-1]['end'] / FPS:.2f}s, {len(timeline)} cues per language")
    print(f"Local synthesis and render: {time.perf_counter() - start:.1f}s "
          f"(synthesis/prep {tts_seconds:.1f}s)")


if __name__ == "__main__":
    main()
