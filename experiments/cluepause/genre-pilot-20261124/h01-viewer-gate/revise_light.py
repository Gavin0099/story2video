"""Light-only revision and exhaustive decoded-plane temporal QA; offline.

python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/revise_light.py render
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/revise_light.py verify
"""
from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(HERE.parent / "motion"))
import hybrid_motion as hm
import temporal_qa as tq

SOURCE = REPO / "artifacts/genre-pilot-20261124/h01-v2.1"
OUT = REPO / "artifacts/genre-pilot-20261124/h01-v2.1-r1"
CONFIG = json.loads((HERE / "light-timeline.json").read_text())
SHOTS = json.loads((SOURCE / "shared/shots.json").read_text())
W, H = 1080, 1920
SIZES = [(W, H), (W//2, H//2), (W//2, H//2)]
FRAME_BYTES = W*H*3//2


def executables():
    entries = json.loads((HERE.parent / "motion/tools.lock.json").read_text())
    for e in entries.values():
        p = Path(e["path"])
        assert p.is_file() and p.stat().st_size == e["bytes"]
        assert tq.digest(p) == e["sha256"]
    return {k: v["path"] for k, v in entries.items()}


def run(exe, args):
    # Never persist argv or stderr with host paths. No shell or network.
    r = subprocess.run([exe, *map(str, args)], cwd=REPO, capture_output=True)
    if r.returncode:
        raise RuntimeError(f"Media tool failed: exit {r.returncode}")
    return r.stdout


def frozen():
    assert tq.digest(SOURCE / "shared/urban_horror-v2.1.md") == CONFIG["script_sha256"]
    for cut in ("A", "B"):
        assert tq.digest(SOURCE / cut / "h01-v2.1.mp4") == tq.FROZEN[cut]


def shot_at(n):
    return next(s for s in SHOTS if round(s["start"]*30) <= n < round(s["end"]*30))


def state_at(n):
    return next(s["state"] for s in CONFIG["states"] if s["start_frame"] <= n < s["end_frame"])


def pulse_at(n):
    return any(a <= n < b for a, b in CONFIG["cough_pulses"])


def position(n, cut):
    s = shot_at(n)
    if s["name"] not in CONFIG["registrations"]:
        return None
    x, y, rx, ry = CONFIG["registrations"][s["name"]]
    local = n-round(s["start"]*30)
    z = 1.015+.020*local/max(1, s["frames"]-1)
    if cut == "B" and s["name"] == "flinch":
        # Invert the original 120-pixel mesh's bilinear displacement field.
        dx = math.sin(math.pi*min(1, local/30/.4))*15
        dy = dx*.4
        def weight(a, b):
            l, t = int(a//120)*120, int(b//120)*120
            px, py = (a-l)/120, (b-t)/120
            return sum(math.exp(-((xx-560)/490)**2-((yy-800)/700)**2)*wx*wy
                       for xx, wx in [(l, 1-px), (l+120, px)]
                       for yy, wy in [(t, 1-py), (t+120, py)])
        a, b = x, y
        for _ in range(8):
            w = weight(a, b)
            a, b = x+dx*w, y+dy*w
        l, t = round((W-W/z)/2), round((H-H/z)/2)
        cw, ch = round((W+W/z)/2)-l, round((H+H/z)/2)-t
        return ((a-l)*W/cw, (b-t)*H/ch, rx*W/cw, ry*H/ch)
    # FFmpeg zoompan truncates its crop dimensions and chroma-aligns x/y.
    cw, ch = int(W/z), int(H/z)
    l, t = int(W/2-W/z/2)//2*2, int(H/2-H/z/2)//2*2
    return ((x-l)*W/cw, (y-t)*H/ch, rx*W/cw, ry*H/ch)


def opacity_at(n):
    # Reuse hybrid_motion's smoothstep fade primitive. Pulses never extinguish
    # the standby core; only the local halo brightens, identically in A and B.
    for a, b in CONFIG["cough_pulses"]:
        if a <= n < b:
            return .65+.35*hm.progress(n, a, a+1, "smoothstep")
    return .65


@lru_cache(maxsize=1024)
def staged_glow(size, alpha_bytes):
    """Reuse the motion module's actual alpha/glow staging primitive."""
    core = Image.frombytes("L", size, alpha_bytes)
    key = hashlib.sha256(alpha_bytes + str(size).encode()).hexdigest()
    folder = OUT / "qa/glow-primitives" / key
    folder.mkdir(parents=True, exist_ok=True)
    source = Image.new("RGBA", size, (90, 255, 203, 0))
    source.putalpha(core)
    source.save(folder / "core.png")
    Image.new("RGB", (1, 1)).save(folder / "background.png")
    pivot = [size[0]//2, size[1]//2]
    staged = hm.stage({"background": folder / "background.png", "layers": [{
        "image": folder / "core.png", "size": size, "pivot": pivot,
        "glow_radius": 2.5}]}, folder)
    path, half = staged[0]
    with Image.open(path) as image:
        alpha = image.getchannel("A").crop((half-pivot[0], half-pivot[1],
                                           half-pivot[0]+size[0], half-pivot[1]+size[1]))
    return alpha


def masks(pos, n):
    x, y, rx, ry = pos
    box = (int((x-rx-9)//2)*2, int((y-ry-9)//2)*2,
           int(math.ceil((x+rx+10)/2))*2, int(math.ceil((y+ry+10)/2))*2)
    l, t, r, b = box
    core = Image.new("L", (r-l, b-t))
    d = ImageDraw.Draw(core)
    d.ellipse((x-rx-l, y-ry-t, x+rx-l, y+ry-t), fill=255)
    halo = staged_glow(core.size, core.tobytes())
    halo = halo.point(lambda v: round(v*opacity_at(n)))
    alpha = ImageChops.lighter(core, halo)
    return box, core, alpha


def planes(data):
    offset = 0
    result = []
    for w, h in SIZES:
        length = w*h
        result.append(Image.frombytes("L", (w, h), data[offset:offset+length]))
        offset += length
    return result


@lru_cache(maxsize=1024)
def light_texture(pos, box):
    """Retain the existing photographic lens instead of painting a flat disc."""
    x, y, rx, ry = pos
    l, t, r, b = box
    path = SOURCE / "shared/plates/indicator-element.png"
    assert tq.digest(path) == "5a1cc7dc58805226a21dee3a54867e22c1e5ce00a79e4fae9f920597bf61fe58"
    with Image.open(path) as source:
        texture = source.convert("RGB").resize((round(2*rx+1), round(2*ry+1)), Image.Resampling.LANCZOS)
    patch = Image.new("RGB", (r-l, b-t), (90, 255, 203))
    patch.paste(texture, (round(x-rx-l), round(y-ry-t)))
    yy, cb, cr = patch.convert("YCbCr").split()
    return [yy.point(lambda v: round(16+v*219/255)),
            cb.point(lambda v: round(128+(v-128)*224/255)),
            cr.point(lambda v: round(128+(v-128)*224/255))]


def overlay(data, n, cut):
    pos = position(n, cut)
    if pos is None:
        return data
    box, core, alpha = masks(pos, n)
    result = planes(data)
    # Limited-range BT.601 photographic lens; cough changes only halo opacity.
    for i, (im, color) in enumerate(zip(result, light_texture(tuple(pos), box))):
        q = 1 if i == 0 else 2
        area = tuple(v//q for v in box)
        mask = alpha if q == 1 else alpha.resize((alpha.width//2, alpha.height//2), Image.Resampling.BOX)
        if q == 2:
            color = color.resize(mask.size, Image.Resampling.BOX)
        patch = Image.composite(color, im.crop(area), mask)
        im.paste(patch, area)
    return b"".join(p.tobytes() for p in result)


def decoder(exe, path):
    return subprocess.Popen([exe, "-nostdin", "-v", "error", "-i", str(path),
                             "-map", "0:v:0", "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=REPO)


def frame(stream):
    data = stream.read(FRAME_BYTES)
    assert len(data) == FRAME_BYTES, "Truncated decoded video"
    return data


def render():
    frozen()
    tools = executables()
    assert not OUT.exists(), "Choose a new revision; never overwrite an existing cut"
    OUT.mkdir(parents=True)
    for cut in ("A", "B"):
        dest = OUT / cut
        dest.mkdir()
        original = SOURCE / cut / "h01-v2.1.mp4"
        dec = decoder(tools["ffmpeg"], original)
        enc = subprocess.Popen([tools["ffmpeg"], "-nostdin", "-v", "error", "-n",
            "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", "1080x1920", "-r", "30", "-i", "-",
            "-i", str(original), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
            "-qp", "0", "-preset", "medium", "-threads", "2", "-c:a", "copy", "-color_range", "tv",
            "-bsf:v", "h264_metadata=video_full_range_flag=0:sample_aspect_ratio=1/1",
            "-map_metadata", "-1", "-movflags", "+faststart", str(dest / "h01-v2.1-r1.mp4")],
            stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=REPO)
        try:
            for n in range(1170):
                enc.stdin.write(overlay(frame(dec.stdout), n, cut))
            assert dec.stdout.read() == b""
            enc.stdin.close()
            assert dec.wait() == enc.wait() == 0
        finally:
            for p in (dec, enc):
                if p.poll() is None:
                    p.kill()
        for lang in ("en", "zh-Hant"):
            shutil.copyfile(SOURCE / cut / f"h01-v2.1.{lang}.srt", dest / f"h01-v2.1-r1.{lang}.srt")
        print(f"{cut}: light-only lossless render complete", flush=True)
    frozen()


def verify():
    frozen()
    tools = executables()
    report = {"base_git_sha": "695d7db4aaee1790a71ceff6e26afa124519be41", "cuts": {},
              "timeline_sha256": tq.digest(HERE / "light-timeline.json"),
              "comparison": "All decoded Y/U/V samples, full resolution, all 1170 frames per cut",
              "dense_window_frames": [510, 900], "known_breaks": "All non-light findings retained"}
    for cut in ("A", "B"):
        dest = OUT / cut
        clip = dest / "h01-v2.1-r1.mp4"
        orig = SOURCE / cut / "h01-v2.1.mp4"
        probe = json.loads(run(tools["ffprobe"], ["-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", clip]))
        v = next(s for s in probe["streams"] if s["codec_type"] == "video")
        assert (v["width"], v["height"], v["pix_fmt"], v["r_frame_rate"], int(v["nb_read_frames"])) == (1080, 1920, "yuv420p", "30/1", 1170)
        assert v["color_range"] == "tv" and v["sample_aspect_ratio"] == "1:1"
        assert float(probe["format"]["duration"]) == 39
        pts = json.loads(run(tools["ffprobe"], ["-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", clip]))["frames"]
        assert len(pts) == 1170 and all(abs(float(p["best_effort_timestamp_time"])-n/30)<.000002 for n,p in enumerate(pts))
        def audio(p):
            return run(tools["ffmpeg"], ["-v", "error", "-i", p, "-map", "0:a:0", "-c:a", "copy", "-f", "hash", "-hash", "sha256", "-"]).decode().strip()
        ah = audio(clip)
        assert ah == audio(orig)
        for lang in ("en", "zh-Hant"):
            assert tq.digest(dest / f"h01-v2.1-r1.{lang}.srt") == tq.FROZEN[lang]
        old, new = decoder(tools["ffmpeg"], orig), decoder(tools["ffmpeg"], clip)
        rows, changed, visible = [], 0, 0
        center_min, center_max = [255]*3, [0]*3
        # Every second, plus every frame 17-30s, saved as temporal light crops.
        crops = dest / "qa/light-crops"
        crops.mkdir(parents=True, exist_ok=True)
        sheets = []
        for n in range(1170):
            a, b = frame(old.stdout), frame(new.stdout)
            assert overlay(a, n, cut) == b, f"Encoded overlay mismatch {cut} f{n}"
            pos = position(n, cut)
            outside = 0
            if pos:
                visible += 1
                box, _, _ = masks(pos, n)
                for i, (pa, pb) in enumerate(zip(planes(a), planes(b))):
                    diff = ImageChops.difference(pa, pb)
                    q = 1 if i == 0 else 2
                    diff.paste(0, tuple(v//q for v in box))
                    outside += sum(diff.histogram()[1:])
                x, y = round(pos[0]), round(pos[1])
                pb = planes(b)
                center = [p.getpixel((x//(1 if i == 0 else 2), y//(1 if i == 0 else 2))) for i,p in enumerate(pb)]
                # The retained lens is cyan-green, so Cb can exceed neutral
                # 128. Test actual illumination and low red chroma, not a
                # flat-fill color assumption. Exact overlay equality is above.
                assert center[0] > 120 and 70 < center[1] < 170 and center[2] < 100, f"Light extinguished {cut} f{n}"
                center_min = [min(a,b) for a,b in zip(center_min,center)]
                center_max = [max(a,b) for a,b in zip(center_max,center)]
                if 510 <= n < 900 or n % 30 == 0:
                    # YUV preview is for inspecting tracking; numeric QA above uses native planes.
                    cb = pb[1].resize((W,H)); cr = pb[2].resize((W,H))
                    yy = pb[0].point(lambda z: max(0,min(255,round((z-16)*255/219))))
                    cb = cb.point(lambda z: max(0,min(255,round((z-128)*255/224+128))))
                    cr = cr.point(lambda z: max(0,min(255,round((z-128)*255/224+128))))
                    rgb = Image.merge("YCbCr", (yy,cb,cr)).convert("RGB")
                    crop = rgb.crop((x-48,y-48,x+48,y+48))
                    crop.save(crops / f"{n:04d}.png")
                    if n % 30 == 0 or n in (540,545,546,549,554,555,648,659,660,779,780,839,840,885,886):
                        sheets.append((n,crop))
            else:
                assert a == b, f"Non-light shot changed {cut} f{n}"
            assert outside == 0
            changed += a != b
            rows.append([n, f"{n/30:.6f}", shot_at(n)["name"], state_at(n), int(pulse_at(n)), int(pos is not None), json.dumps([round(p,3) for p in pos]) if pos else "", outside, int(a != b)])
        assert old.stdout.read() == new.stdout.read() == b""
        assert old.wait() == new.wait() == 0
        with (dest / "qa/frame-checks.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["frame","seconds","shot","state","cough_pulse","visible","tracked_xy_rx_ry","outside_changed_samples","frame_changed"])
            writer.writerows(rows)
        sheet = Image.new("RGB",(800, math.ceil(len(sheets)/8)*120),"#151515")
        d=ImageDraw.Draw(sheet)
        for i,(n,crop) in enumerate(sheets):
            x,y=i%8*100,i//8*120
            sheet.paste(crop,(x,y));d.text((x,y+97),f"f{n} {n/30:.2f}",fill="white")
        sheet.save(dest / "qa/light-sequence.png")
        report["cuts"][cut] = {"path": clip.relative_to(REPO).as_posix(), "sha256": tq.digest(clip),
            "frames":1170,"duration_s":39,"visible_light_frames":visible,"changed_frames":changed,
            "video_profile":v["profile"],"color_range":v["color_range"],"sample_aspect_ratio":v["sample_aspect_ratio"],
            "outside_changed_samples":0,"overlay_mismatches":0,"light_center_failures":0,
            "light_center_yuv_min":center_min,"light_center_yuv_max":center_max,
            "audio_packet_hash":ah,"pts":"PASS", "caption_hashes": {k:tq.FROZEN[k] for k in ("en","zh-Hant")}}
        print(f"{cut}: full-length / dense light QA PASS; {visible} visible frames; outside diff zero", flush=True)
    assert report["cuts"]["A"]["audio_packet_hash"] == report["cuts"]["B"]["audio_packet_hash"]
    tq.save(OUT / "light-measurements.json",report)
    frozen()


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("command", choices=("render","verify"))
    {"render":render,"verify":verify}[p.parse_args().command]()
