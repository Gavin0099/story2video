"""Render the gated visual PoC with an existing, matching voice timeline."""

import argparse
import math
import shutil
import subprocess
from pathlib import Path

from visual_poc import Project, digest, read_json, write_json

FPS = 30
TRACKS = ("en.srt", "en.vtt", "zh-Hant-TW.srt", "zh-Hant-TW.vtt")


def ass_clock(ms):
    centiseconds = math.ceil(ms / 10)
    elapsed_seconds, fraction = divmod(centiseconds, 100)
    minutes, seconds = divmod(elapsed_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02}:{seconds:02}.{fraction:02}"


def write_captions(path, timeline):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,58,&H00F5F5F5,&H00F5F5F5,&H0518110E,&H45000000,-1,0,0,0,100,100,0,0,1,4,2,8,110,162,1315,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    rows = []
    for entry in timeline["segments"]:
        inline = " ".join(entry["en_caption"].split())
        if any(character in inline for character in "{}\\"):
            raise ValueError(f"Unsupported ASS control character in {entry['id']}")
        start = ass_clock(entry["caption_start_ms"])
        end = ass_clock(entry["caption_end_ms"])
        rows.append(f"Dialogue: 0,{start},{end},Caption,,0,0,0,,{inline}")
    path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


def frame_at(ms):
    return (ms * FPS + 999) // 1000


def plan_frames(assets, timeline):
    by_segment = {entry["id"]: entry for entry in timeline["segments"]}
    reveal = by_segment[assets["reveal_segment"]]
    if (assets["reveal_timing"] != "at_or_after_spoken_reveal"
            or timeline["reveal_ms"] < reveal["audio_end_ms"]
            or timeline["reveal_ms"] != reveal["caption_start_ms"]):
        raise ValueError("The visual reveal must wait until the answer is spoken")
    starts = []
    for shot in assets["shots"]:
        ms = by_segment[shot["segment"]]["audio_start_ms"]
        if shot["stage"] == "reveal_or_later":
            ms = max(ms, timeline["reveal_ms"])
        starts.append(frame_at(ms))
    total = frame_at(timeline["duration_ms"])
    if not starts or starts[0] != 0 or starts != sorted(set(starts)) or starts[-1] >= total:
        raise ValueError("Shots must start at frame zero and have positive, ordered durations")
    return [
        {**shot, "start_frame": start, "frames": end - start}
        for shot, start, end in zip(assets["shots"], starts, starts[1:] + [total])
    ], total


def render(project, voice_dir, output):
    gate = project.gate()
    if gate["status"] != "PASS":
        raise ValueError("Visual QA blocked the render: " + "; ".join(gate["failures"]))
    assets = gate["render_input"]
    timeline = read_json(voice_dir / "segments.json")
    voice = read_json(voice_dir / "provenance.json")
    if (voice["episode_sha256"] != assets["story_sha256"]
            or timeline["episode_id"] != project.story["episode_id"]
            or digest(voice_dir / "narration.wav") != voice["narration_sha256"]):
        raise ValueError("Voice timeline or narration does not match the approved story or audio hash")
    frames, total = plan_frames(assets, timeline)
    output.mkdir(parents=True, exist_ok=False)
    for name in ("narration.wav", "segments.json", *TRACKS):
        shutil.copyfile(voice_dir / name, output / name)
    write_captions(output / "captions.ass", timeline)

    filters = []
    inputs = []
    for index, shot in enumerate(frames):
        inputs.extend(["-i", str(project.local(shot["file"]))])
        duration = shot["frames"]
        filters.append(
            f"[{index}:v]scale=2160:3840:flags=lanczos,setsar=1,"
            f"zoompan=z='1.012+0.053*on/{duration}':x='(iw-iw/zoom)*0.56':"
            f"y='(ih-ih/zoom)*0.45':d={duration}:s=1080x1920:fps={FPS},setsar=1[v{index}]"
        )
    count = len(frames)
    join = "".join(f"[v{index}]" for index in range(count))
    filters.append(f"{join}concat=n={count}:v=1:a=0,setpts=N/({FPS}*TB),subtitles=captions.ass,format=yuv420p[video]")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-xerror",
        "-filter_complex_threads", "2", *inputs, "-i", "narration.wav",
        "-filter_complex", ";".join(filters), "-map", "[video]", "-map", f"{count}:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-af", "apad",
        "-t", f"{total/FPS:.6f}", "-movflags", "+faststart", "render.mp4",
    ], cwd=output, check=True)
    write_json(output / "render-provenance.json", {
        "visual_qa_status": gate["status"],
        "story_sha256": assets["story_sha256"],
        "voice": voice["voice"],
        "narration_sha256": voice["narration_sha256"],
        "renderer": "FFmpeg zoompan and libass",
        "fps": FPS,
        "total_frames": total,
        "spoken_answer_end_ms": next(row["audio_end_ms"] for row in timeline["segments"] if row["id"] == assets["reveal_segment"]),
        "shots": frames,
        "output_sha256": digest(output / "render.mp4"),
        "upload": "NOT_UPLOADED",
    })
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--voice-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(f"Rendered {render(Project(args.project_root), args.voice_dir.resolve(), args.output.resolve())} frames.")


if __name__ == "__main__":
    main()
