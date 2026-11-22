"""Build the phone pilot from the verified WhyNest Lab coin master."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import secrets
import shutil
import subprocess

from PIL import Image, ImageDraw


MASTER_HASH = "00fd53d863ae7c9bc539821053473f973abc3d3afe09681fc9ff4b7da7a2bc5c"
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "artifacts/science-shorts/public-20-20261122/05"
OUTPUT = ROOT / "artifacts/science-shorts/coin-viewer-gate"
VIEWER = OUTPUT / "viewer"
TILE = 300
FPS = 30
OPENING_FRAMES = 3 * FPS


def lerp(a, b, t):
    return a + (b - a) * max(0, min(1, t))


def scene_setup():
    size = 600
    scene = Image.new("RGB", (size, size))
    pixels = scene.load()
    for y in range(size):
        for x in range(size):
            light = max(0, 1 - math.hypot((x - 307) / 410, (y - 244) / 350))
            n = ((x * 23 + y * 79 + (x ^ y) * 13) % 13 - 6) * 0.24
            pixels[x, y] = tuple(int(base + lift * light + n) for base, lift in [(16, 28), (15, 22), (29, 33)])
    draw = ImageDraw.Draw(scene)
    for spread in range(34, 0, -2):
        draw.ellipse((91 - spread, 435 - spread // 3, 516 + spread, 495 + spread // 2),
                     fill=(18 + spread // 8, 15 + spread // 10, 31 + spread // 7))
    draw.ellipse((73, 246, 527, 374), fill="#111f33", outline="#6e82aa", width=5)
    draw.ellipse((90, 255, 510, 358), fill="#172b45", outline="#375777", width=3)
    return scene


def cup_frame(base, t):
    frame = base.copy()
    draw = ImageDraw.Draw(frame)
    fill = min(1, max(0, (t - 0.44) / 1.70))
    if fill:
        water_y = int(lerp(356, 296, fill))
        water_width = int(lerp(224, 371, fill))
        left = 300 - water_width // 2
        right = 300 + water_width // 2
        draw.ellipse((left, water_y - 16, right, water_y + 49), fill="#295671", outline="#69a8ba", width=3)
        draw.arc((left + 12, water_y - 11, right - 12, water_y + 47), 187, 335, fill="#9fd6db", width=2)
        for i in range(3):
            progress = (t * 1.6 + i / 3) % 1
            spread = int(9 + progress * min(80, 28 + fill * 54))
            color = (int(lerp(120, 45, progress)), int(lerp(203, 97, progress)), int(lerp(215, 128, progress)))
            draw.ellipse((392 - spread, water_y + 18 - spread // 6,
                          392 + spread, water_y + 18 + spread // 6), outline=color, width=2)
        # Fixed coin on the bottom. Only its apparent position changes behind the opaque rim.
        coin_y = int(397 - 69 * fill**0.85)
        draw.ellipse((244, coin_y - 14, 330, coin_y + 17), fill="#ac6b29", outline="#e4a65a", width=2)
        draw.ellipse((245, coin_y - 17, 328, coin_y + 12), fill="#e9aa50", outline="#ffe2a0", width=3)
        draw.ellipse((255, coin_y - 12, 317, coin_y + 7), outline="#ae722d", width=2)
        draw.arc((275, coin_y - 8, 300, coin_y + 3), 203, 537, fill="#fbda8a", width=2)

    # The cup's front wall occludes the model at the same coordinates in every frame.
    draw.polygon([(73, 312), (85, 333), (107, 348), (148, 359), (198, 367),
                  (249, 372), (301, 373), (355, 372), (405, 367), (457, 357),
                  (495, 346), (516, 332), (527, 310), (507, 408), (477, 460),
                  (438, 471), (358, 481), (240, 481), (160, 470), (123, 456),
                  (96, 411)], fill="#142941")
    for inset, color in [(6, "#243e5a"), (13, "#203852"), (22, "#1d334d")]:
        draw.arc((79 + inset, 252, 521 - inset, 376 - inset // 2), 8, 172, fill=color, width=6)
    draw.arc((73, 246, 527, 374), 0, 180, fill="#8facc8", width=6)
    draw.arc((84, 254, 517, 370), 106, 162, fill="#c9dae4", width=2)
    draw.arc((95, 390, 508, 479), 38, 140, fill="#415e7a", width=3)

    # Add the stream in front of the rear edge. Its endpoint follows the water surface.
    if 0.27 <= t < 2.18:
        lead = min(1, (t - 0.27) / 0.20)
        fade = min(1, (2.18 - t) / 0.20)
        end_y = min(346, int(lerp(369, 311, fill)))
        junction = int(lerp(5, end_y, lead))
        points = [(int(424 - 31 * y / max(1, end_y) + 3 * math.sin(y / 26 - t * 15)), y)
                  for y in (*range(0, junction, 4), junction)]
        if len(points) > 1:
            draw.line(points, fill="#5b9faa", width=max(2, int(12 * fade)))
            draw.line([(x - 2, y) for x, y in points], fill="#caedf0", width=max(1, int(4 * fade)))
        if lead == 1:
            for n in range(6):
                age = (t * 3 + n / 6) % 1
                x = int(392 + (n - 2.5) * 23 * age)
                y = end_y - int(69 * age * (1 - age))
                r = 3 if age < 0.55 else 2
                draw.ellipse((x - r, y - r, x + r, y + r), fill="#b4dbe1")
    return frame


def webvtt(name):
    content = (SOURCE / (name + ".srt")).read_text(encoding="utf-8-sig")
    content = re.sub(r"(\d\d:\d\d:\d\d),(\d{3})", r"\1.\2", content)
    (VIEWER / (name + ".vtt")).write_text("WEBVTT\n\n" + content, encoding="utf-8")


def prepare_assignments():
    # Keep participant codes stable when rebuilding media for this pilot.
    assignment_file = VIEWER / "assignments.json"
    if assignment_file.exists():
        assignments = json.loads(assignment_file.read_text(encoding="utf-8"))
    else:
        slots = {
            "normal": ["A"] * 12 + ["B"] * 12,
            "muted": ["A"] * 4 + ["B"] * 4,
        }
        assignments = {}
        for cohort, variants in slots.items():
            secrets.SystemRandom().shuffle(variants)
            for variant in variants:
                code = secrets.token_hex(4).upper()
                while code in assignments:
                    code = secrets.token_hex(4).upper()
                assignments[code] = {"cohort": cohort, "variant": variant}
        assignment_file.write_text(json.dumps(assignments, indent=2), encoding="utf-8")
    with (OUTPUT / "host-assignments.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["participant_code", "cohort", "variant"])
        writer.writerows((code, data["cohort"], data["variant"]) for code, data in assignments.items())


def run(ffmpeg):
    master = SOURCE / "master.mp4"
    assert hashlib.file_digest(master.open("rb"), "sha256").hexdigest() == MASTER_HASH
    VIEWER.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(master, VIEWER / "source.mp4")
    shutil.copyfile(Path(__file__).with_name("index.html"), VIEWER / "index.html")
    webvtt("zh-Hant")
    prepare_assignments()

    base = scene_setup()
    frames = [cup_frame(base, n / FPS).resize((TILE, TILE), Image.Resampling.LANCZOS)
              for n in range(OPENING_FRAMES)]
    for second in range(3):
        atlas = Image.new("RGB", (TILE * 5, TILE * 6))
        for index, frame in enumerate(frames[second * FPS:(second + 1) * FPS]):
            atlas.paste(frame, (index % 5 * TILE, index // 5 * TILE))
        atlas.save(VIEWER / f"hook-{second}.webp", quality=94, method=5)

    # Presentation-only preview. The controlled test uses the shared source with frame overlays.
    raw = b"".join(frame.tobytes() for frame in frames)
    subprocess.run([str(ffmpeg), "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{TILE}x{TILE}", "-r", str(FPS),
                    "-i", "-", "-i", str(master), "-filter_complex",
                    "[0:v]scale=910:910:flags=lanczos,format=yuv420p[hook];"
                    "[1:v][hook]overlay=x=85:y=563:enable='lt(t,3)':eof_action=pass[out]",
                    "-map", "[out]", "-map", "1:a:0", "-map_metadata", "-1",
                    "-c:a", "copy", "-c:v", "libx264", "-threads", "4", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUTPUT / "B-preview.mp4")],
                   input=raw, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", required=True, type=Path)
    run(parser.parse_args().ffmpeg)


