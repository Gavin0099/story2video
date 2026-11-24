"""Offline r1 phone deliveries and exhaustive delivery QA; keep masters unchanged.

Run from repo root with `python -B <this file> encode` then `... verify`.
No shell, network, new images, new dependencies, or personal paths in logs.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

from PIL import ImageChops

import revise_light as light
import temporal_qa as tq

REPO, SOURCE, OUT = light.REPO, light.SOURCE, light.OUT
BASE = "h01-v2.1-r1-delivery"
EVIDENCE = OUT / "delivery-qa"
MASTER_HASH = {
    "A": "b98be2d207c2f42115d09f09eb45e28c87112474e5d85b09feedcb62a6ebb9b8",
    "B": "bf0c1c211a914351a00ad8b36780bedb64b958923c6d93cbb0b95433a9c5739a",
}
CENTER_TOLERANCE = (12, 24, 24)  # 8-bit Y/U/V; chroma is subsampled in 4:2:0.
ROI_MAE_TOLERANCE = 6  # Each plane, each visible frame, including pulse halo.


def relative(p):
    return Path(p).relative_to(REPO).as_posix()


def master(cut):
    return OUT / cut / "h01-v2.1-r1.mp4"


def original(cut):
    return SOURCE / cut / "h01-v2.1.mp4"


def delivery(cut):
    return OUT / cut / f"{BASE}.mp4"


def unchanged():
    light.frozen()
    for cut in ("A", "B"):
        assert tq.digest(master(cut)) == MASTER_HASH[cut], "Master changed"


def options(path):
    data = path.read_bytes()
    found = re.findall(rb"x264 - core [^\x00]+", data)
    assert found, "Missing x264 encoder SEI"
    return sorted(set(x.decode("ascii").split("options: ", 1)[1] for x in found))


def source_settings(cut):
    # The final commands.jsonl is a stream-copy mux; walk to its encoders.
    encoders = []
    for line in (SOURCE / cut / "cuts/commands.jsonl").read_text().splitlines():
        argv = json.loads(line).get("argv", [])
        if "-c:v" in argv:
            encoders.append(argv[argv.index("-c:v"):-1])
    unique = {tuple(a) for a in encoders}
    expected = ("-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-threads", "1", "-pix_fmt", "yuv420p", "-r", "30",
                "-map_metadata", "-1", "-movflags", "+faststart")
    assert unique == {expected}, "Original encoder settings differ"
    muxes = [json.loads(s).get("argv", []) for s in
             (SOURCE / cut / "commands.jsonl").read_text().splitlines()]
    mux = next(a for a in reversed(muxes) if a)
    assert mux[mux.index("-c") + 1] == "copy"
    bsf = mux[mux.index("-bsf:v") + 1]
    return list(expected), bsf


def media_run(exe, args, log):
    # Only relative media paths and a symbolic executable are persisted.
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"tool": "ffmpeg (verified tools.lock.json)", "args": args}) + "\n")
    result = subprocess.run([exe, *args], cwd=REPO, capture_output=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"returncode": result.returncode}) + "\n")
    if result.returncode:
        raise RuntimeError(f"Media command failed, exit {result.returncode}; see {relative(log)}")


def encode():
    unchanged()
    tools = light.executables()
    for cut in ("A", "B"):
        settings, bsf = source_settings(cut)
        dest = OUT / cut
        pieces = dest / "delivery-cuts"
        assert not pieces.exists() and not delivery(cut).exists(), "Refuse overwrite"
        pieces.mkdir()
        log = dest / "delivery-commands.jsonl"
        assert not log.exists()
        concat = []
        for shot in light.SHOTS:
            name = f"{shot['index']:02d}-{shot['name']}.mp4"
            piece = pieces / name
            # Encode independently per original shot: same x264 defaults and
            # closed-GOP resets, including the five-frame complete reply.
            args = ["-nostdin", "-v", "error", "-n", "-filter_complex_threads", "1",
                    "-ss", f"{shot['start']:.9f}", "-i", relative(master(cut)),
                    "-map", "0:v:0", "-an", "-vf", "setsar=1", "-frames:v", str(shot["frames"]),
                    *settings, relative(piece)]
            media_run(tools["ffmpeg"], args, log)
            concat.append(f"file 'delivery-cuts/{name}'")
        listing = dest / "delivery-concat.txt"
        listing.write_text("\n".join(concat) + "\n", encoding="utf-8")
        media_run(tools["ffmpeg"], ["-nostdin", "-v", "error", "-n", "-filter_complex_threads", "1",
                  "-f", "concat", "-safe", "0", "-i", relative(listing), "-i", relative(original(cut)),
                  "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-bsf:v", bsf,
                  "-map_metadata", "-1", "-movflags", "+faststart", relative(delivery(cut))], log)
        for lang in ("en", "zh-Hant"):
            path = dest / f"{BASE}.{lang}.srt"
            assert not path.exists()
            shutil.copyfile(dest / f"h01-v2.1-r1.{lang}.srt", path)
        print(f"{cut}: delivery encoded; master retained", flush=True)
    unchanged()


def probe(exe, path):
    return json.loads(light.run(exe, ["-v", "error", "-count_frames", "-show_streams",
                                    "-show_format", "-of", "json", path]))


def faststart(path):
    boxes = []
    with path.open("rb") as f:
        while f.tell() < path.stat().st_size:
            at = f.tell()
            size = int.from_bytes(f.read(4), "big")
            kind = f.read(4).decode("ascii")
            if size == 1:
                size = int.from_bytes(f.read(8), "big")
            assert size >= 8
            boxes.append(kind)
            f.seek(at + size)
    assert boxes.index("moov") < boxes.index("mdat")
    return boxes


def frame_info(exe, path):
    return json.loads(light.run(exe, ["-v", "error", "-select_streams", "v:0", "-show_frames",
        "-show_entries", "frame=best_effort_timestamp_time,key_frame", "-of", "json", path]))["frames"]


def audio_hash(exe, path):
    return light.run(exe, ["-v", "error", "-i", path, "-map", "0:a:0", "-c:a", "copy",
                          "-f", "hash", "-hash", "sha256", "-"]).decode().strip()


def tracked_box(pos):
    # Exact even-aligned bounds of revise_light.masks; avoid restaging its
    # glow PNGs when only the measurement rectangle is needed.
    x, y, rx, ry = pos
    return (int((x-rx-9)//2)*2, int((y-ry-9)//2)*2,
            int(math.ceil((x+rx+10)/2))*2, int(math.ceil((y+ry+10)/2))*2)


def light_checks(exe, cut, folder, enforce=True):
    old, new = light.decoder(exe, master(cut)), light.decoder(exe, delivery(cut))
    rows, deltas, max_mae = [], [0] * 3, [0.] * 3
    mins, maxs = [255] * 3, [0] * 3
    visible = 0
    state_failures, center_failures, roi_failures = [], [], []
    try:
        for n in range(light.CONFIG["frames"]):
            a, b = light.frame(old.stdout), light.frame(new.stdout)
            pos = light.position(n, cut)
            center, diff, maes = [], [], []
            if pos:
                visible += 1
                box = tracked_box(pos)
                aa, bb = light.planes(a), light.planes(b)
                x, y = round(pos[0]), round(pos[1])
                for i, (pa, pb) in enumerate(zip(aa, bb)):
                    q = 1 if i == 0 else 2
                    c = pb.getpixel((x//q, y//q))
                    center.append(c)
                    diff.append(abs(c - pa.getpixel((x//q, y//q))))
                    hist = ImageChops.difference(pa.crop(tuple(v//q for v in box)),
                                                pb.crop(tuple(v//q for v in box))).histogram()
                    maes.append(sum(v*count for v, count in enumerate(hist)) / sum(hist))
                # Same center/position detector as revise_light.verify.
                if not (center[0] > 120 and 70 < center[1] < 170 and center[2] < 100):
                    state_failures.append(n)
                if any(d > t for d, t in zip(diff, CENTER_TOLERANCE)):
                    center_failures.append(n)
                if max(maes) > ROI_MAE_TOLERANCE:
                    roi_failures.append(n)
                deltas = [max(x, y) for x, y in zip(deltas, diff)]
                max_mae = [max(x, y) for x, y in zip(max_mae, maes)]
                mins = [min(x, y) for x, y in zip(mins, center)]
                maxs = [max(x, y) for x, y in zip(maxs, center)]
            rows.append([n, f"{n/30:.6f}", light.shot_at(n)["name"], light.state_at(n),
                         int(light.pulse_at(n)), light.opacity_at(n), int(pos is not None),
                         *center, *diff, *maes])
        assert old.stdout.read() == new.stdout.read() == b""
        assert old.wait() == new.wait() == 0
    finally:
        for p in (old, new):
            if p.poll() is None:
                p.kill()
    with (folder / "light-frames.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["frame", "seconds", "shot", "timeline_state", "cough_pulse", "expected_opacity",
                    "visible", "center_y", "center_u", "center_v", "delta_y", "delta_u", "delta_v",
                    "roi_mae_y", "roi_mae_u", "roi_mae_v"])
        # Explicit blanks for off-camera frames, no claim of observed state.
        w.writerows(row + [""] * (16-len(row)) for row in rows)
    result = {"frames": len(rows), "visible": visible, "unobservable": len(rows)-visible,
            "state_failure_frames": state_failures, "center_failure_frames": center_failures,
            "roi_failure_frames": roi_failures, "timing_tolerance_frames": 0,
            "center_tolerance": CENTER_TOLERANCE, "center_max_abs_error_yuv": deltas,
            "roi_mae_tolerance": ROI_MAE_TOLERANCE, "roi_max_mae_yuv": max_mae,
            "center_min_yuv": mins, "center_max_yuv": maxs}
    tq.save(folder / "light-summary.json", result)
    if enforce:
        assert not (state_failures or center_failures or roi_failures), f"Light QA failed {cut}; see light-summary.json"
    return result


def diagnose_light():
    unchanged()
    tools = light.executables()
    for cut in ("A", "B"):
        label = "-".join(map(str, CENTER_TOLERANCE))
        folder = EVIDENCE / f"diagnostic-tolerance-{label}" / cut
        folder.mkdir(parents=True, exist_ok=True)
        result = light_checks(tools["ffmpeg"], cut, folder, enforce=False)
        print(cut, json.dumps(result), flush=True)
    unchanged()


def rectangles(shot, cut):
    # The union of the SAME tracked light ROI for every frame of this shot.
    # Fixed envelope permits genuine outside-only SSIM crops, without filling
    # an excluded area with identical pixels (which would inflate SSIM).
    boxes = []
    for n in range(round(shot["start"]*30), round(shot["end"]*30)):
        pos = light.position(n, cut)
        if pos:
            boxes.append(tracked_box(pos))
    if not boxes:
        return None, [(0, 0, light.W, light.H)]
    l, t = min(b[0] for b in boxes), min(b[1] for b in boxes)
    r, b = max(b[2] for b in boxes), max(b[3] for b in boxes)
    return [l, t, r, b], [(0, 0, light.W, t), (0, b, light.W, light.H-b),
                         (0, t, l, b-t), (r, t, light.W-r, b-t)]


def stats(path):
    return [dict(re.findall(r"([A-Za-z_]+):([^\s]+)", line))
            for line in path.read_text().splitlines()]


def outside_metrics(exe, cut, folder):
    rows, envelopes = [], []
    for shot in light.SHOTS:
        envelope, rects = rectangles(shot, cut)
        envelopes.append({"shot": shot["name"], "start_frame": round(shot["start"]*30),
                          "frames": shot["frames"], "excluded_xyxy": envelope,
                          "outside_xywh": rects})
        count = len(rects)
        graph = []
        for stream in range(2):
            graph.append(f"[{stream}:v]trim=end_frame={shot['frames']},setpts=PTS-STARTPTS,"
                         f"split={count}" + "".join(f"[v{stream}_{i}]" for i in range(count)))
        outputs = []
        for i, (x, y, w, h) in enumerate(rects):
            for stream in range(2):
                graph.append(f"[v{stream}_{i}]crop={w}:{h}:{x}:{y},split=2[s{stream}_{i}][p{stream}_{i}]")
            stem = f"{shot['index']:02d}-{i}"
            ss, ps = folder / f"{stem}-ssim.log", folder / f"{stem}-psnr.log"
            # Paths are relative to repo and use '/' to avoid filter escaping.
            graph.append(f"[s0_{i}][s1_{i}]ssim=stats_file={relative(ss)}[so{i}]")
            graph.append(f"[p0_{i}][p1_{i}]psnr=stats_file={relative(ps)}[po{i}]")
            outputs += ["-map", f"[so{i}]", "-map", f"[po{i}]"]
        args = ["-nostdin", "-v", "error", "-filter_complex_threads", "1",
                "-ss", f"{shot['start']:.9f}", "-i", relative(delivery(cut)),
                "-ss", f"{shot['start']:.9f}", "-i", relative(original(cut)),
                "-filter_complex", ";".join(graph), *outputs, "-an", "-f", "null", "-"]
        media_run(exe, args, folder / "metric-commands.jsonl")
        ssims, psnrs = [], []
        for i in range(count):
            ssims.append(stats(folder / f"{shot['index']:02d}-{i}-ssim.log"))
            psnrs.append(stats(folder / f"{shot['index']:02d}-{i}-psnr.log"))
            assert len(ssims[-1]) == len(psnrs[-1]) == shot["frames"]
        for n in range(shot["frames"]):
            # FFmpeg SSIM uses 8x8 windows, stride 4. Weight native Y/U/V
            # windows equally, omitting every window that intersects the ROI.
            ssum, windows, error, samples = 0., 0, 0., 0
            for i, (_, _, w, h) in enumerate(rects):
                for plane, q in [("Y", 1), ("U", 2), ("V", 2)]:
                    pw, ph = w//q, h//q
                    nw = (pw//4-1)*(ph//4-1)
                    assert nw > 0
                    ssum += float(ssims[i][n][plane])*nw
                    windows += nw
                    np = pw*ph
                    error += float(psnrs[i][n][f"mse_{plane.lower()}"])*np
                    samples += np
            mse = error / samples
            assert mse > 0
            rows.append([round(shot["start"]*30)+n, shot["name"], ssum/windows,
                         10*math.log10(255**2/mse), mse, samples, windows])
        print(f"{cut}: outside metrics {shot['index']+1}/{len(light.SHOTS)}", flush=True)
    assert [r[0] for r in rows] == list(range(1170))
    with (folder / "outside-frames.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["frame", "shot", "ssim", "psnr_db", "mse", "outside_yuv_samples", "ssim_windows"])
        w.writerows(rows)
    tq.save(folder / "excluded-regions.json", envelopes)
    return {"frames": len(rows), "ssim_min": min(r[2] for r in rows),
            "ssim_mean": sum(r[2] for r in rows)/len(rows),
            "psnr_db_min": min(r[3] for r in rows), "psnr_db_mean": sum(r[3] for r in rows)/len(rows),
            "minimum_outside_fraction": min(r[5] for r in rows)/light.FRAME_BYTES,
            "definition": "Native YUV420, per-shot tracked light ROI union excluded. SSIM: valid 8x8/stride4 window weighted over outside rectangles and planes. PSNR: outside sample weighted MSE; FFmpeg logs round MSE to 0.01. Means are arithmetic means of 1170 frame scores."}


def verify():
    unchanged()
    tools = light.executables()
    EVIDENCE.mkdir(exist_ok=True)
    report = {"base_git_sha": light.run("git", ["rev-parse", "HEAD"]).decode().strip(),
              "timeline_sha256": tq.digest(light.HERE / "light-timeline.json"), "cuts": {}}
    for cut in ("A", "B"):
        folder = EVIDENCE / cut
        folder.mkdir(exist_ok=True)
        op, dp = probe(tools["ffprobe"], original(cut)), probe(tools["ffprobe"], delivery(cut))
        tq.save(folder / "original-ffprobe.json", op)
        tq.save(folder / "delivery-ffprobe.json", dp)
        ov, dv = op["streams"][0], dp["streams"][0]
        fields = ("codec_name", "profile", "level", "pix_fmt", "width", "height", "r_frame_rate",
                  "avg_frame_rate", "sample_aspect_ratio", "color_range", "nb_read_frames", "duration")
        assert all(ov[k] == dv[k] for k in fields)
        assert (dv["profile"], dv["level"], dv["pix_fmt"]) == ("High", 40, "yuv420p")
        assert len(dp["streams"]) == 2
        assert dp["format"]["duration"] == "39.000000"
        assert options(original(cut)) == options(delivery(cut)), "x264 options mismatch"
        source_settings(cut)
        info = frame_info(tools["ffprobe"], delivery(cut))
        assert len(info) == 1170
        assert all(abs(float(p["best_effort_timestamp_time"])-n/30) < .000002 for n, p in enumerate(info))
        keys = [n for n, p in enumerate(info) if p["key_frame"]]
        old_keys = [n for n, p in enumerate(frame_info(tools["ffprobe"], original(cut))) if p["key_frame"]]
        assert keys == old_keys, "Keyframe boundaries differ"
        ah = audio_hash(tools["ffmpeg"], delivery(cut))
        assert ah == audio_hash(tools["ffmpeg"], original(cut))
        assert ah.endswith("97f9ad93d95fd719526e6f7a739f9b4b825bbab520a4998d05fb0a38461b1d66")
        captions = {}
        for lang in ("en", "zh-Hant"):
            path = OUT / cut / f"{BASE}.{lang}.srt"
            captions[lang] = tq.digest(path)
            assert captions[lang] == tq.FROZEN[lang]
        fraction = delivery(cut).stat().st_size / original(cut).stat().st_size
        assert .75 < fraction < 1.25, "Delivery size not comparable"
        report["cuts"][cut] = {
            "delivery": relative(delivery(cut)), "sha256": tq.digest(delivery(cut)),
            "bytes": delivery(cut).stat().st_size, "original_bytes": original(cut).stat().st_size,
            "size_ratio_to_original": fraction, "video": {k: dv[k] for k in fields},
            "video_bit_rate": dv["bit_rate"], "original_video_bit_rate": ov["bit_rate"],
            "audio": {k: dp["streams"][1][k] for k in ("codec_name", "profile", "sample_rate", "channels", "bit_rate")},
            "audio_packet_hash": ah, "caption_sha256": captions,
            "master": relative(master(cut)), "master_sha256": MASTER_HASH[cut], "master_bytes": master(cut).stat().st_size,
            "faststart_box_order": faststart(delivery(cut)), "x264_options": options(delivery(cut)),
            "keyframes_match_original": keys, "pts": "PASS",
            "light": light_checks(tools["ffmpeg"], cut, folder),
            "outside": outside_metrics(tools["ffmpeg"], cut, folder)}
        tq.save(EVIDENCE / "measurements.json", report)
        print(f"{cut}: delivery QA PASS", flush=True)
    unchanged()
    print("Both deliveries verified; originals and r1 masters unchanged", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("encode", "verify", "diagnose-light"))
    parser.add_argument("--center-tolerance", type=int, nargs=3, default=CENTER_TOLERANCE,
                        metavar=("Y", "U", "V"), help="Absolute 8-bit center error; detector thresholds stay fixed")
    args = parser.parse_args()
    CENTER_TOLERANCE = tuple(args.center_tolerance)
    {"encode": encode, "verify": verify, "diagnose-light": diagnose_light}[args.command]()
