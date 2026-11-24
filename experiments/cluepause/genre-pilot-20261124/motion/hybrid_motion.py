"""Local, deterministic 2D layer animation. No AI/network/publishing calls."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUTPUTS = REPO / "artifacts/genre-pilot-20261124/motion"
WIDTH, HEIGHT, FPS = 1080, 1920, 30
EASINGS = {"linear", "smoothstep", "ease_in", "ease_out"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Expected a finite number")
    return value


def integer(value, minimum=1, maximum=108000):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"Expected integer in [{minimum}, {maximum}]")
    return value


def pair(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("Expected [x, y]")
    return tuple(number(x) for x in value)


def keys(data, required, optional=()):
    if not isinstance(data, dict) or set(required) - data.keys() or data.keys() - set(required) - set(optional):
        raise ValueError(f"Missing/unknown fields; required={required}, optional={optional}")


def ease(p, kind="linear"):
    p = min(1.0, max(0.0, p))
    if kind == "linear":
        return p
    if kind == "smoothstep":
        return p * p * (3 - 2 * p)
    if kind == "ease_in":
        return p * p
    if kind == "ease_out":
        return 1 - (1 - p) ** 2
    raise ValueError("Unknown easing")


def progress(t, start, end, easing="linear"):
    if end <= start:
        raise ValueError("Animation interval must be positive")
    return ease((t - start) / (end - start), easing)


def path_at(points, p):
    """Piecewise linear path, measured by arc length, including repeated points."""
    p = min(1.0, max(0.0, p))
    segments = [(a, b, math.dist(a, b)) for a, b in zip(points, points[1:])]
    length = sum(s[2] for s in segments)
    if not length:
        return tuple(points[0])
    distance = p * length
    for a, b, span in segments:
        if span and distance <= span:
            return tuple(x + (y - x) * distance / span for x, y in zip(a, b))
        distance -= span
    return tuple(points[-1])


def transformed_point(point, pivot, anchor, degrees, offset=(0, 0)):
    """Positive rotation is clockwise in image coordinates (y points down)."""
    x, y = point[0] - pivot[0], point[1] - pivot[1]
    a = math.radians(degrees)
    return (anchor[0] + offset[0] + x * math.cos(a) - y * math.sin(a),
            anchor[1] + offset[1] + x * math.sin(a) + y * math.cos(a))


def shake_at(t, start, end, amplitude, cycles):
    if not start < t < end:
        return 0.0, 0.0
    p = (t - start) / (end - start)
    envelope = math.sin(math.pi * p)
    return (amplitude[0] * envelope * math.sin(2 * math.pi * cycles * p),
            amplitude[1] * envelope * math.sin(2 * math.pi * cycles * p + math.pi / 2))


def asset(base, name):
    if not isinstance(name, str) or not name or "://" in name:
        raise ValueError("Assets must be local paths")
    p = (base / name).resolve(strict=True)
    if not p.is_file():
        raise ValueError(f"Not a file: {p}")
    return p


def parse_spec(data, base):
    keys(data, ["version", "frames", "background", "layers"], ["id", "sound_cues", "notes"])
    if type(data["version"]) is not int or data["version"] != 1:
        raise ValueError("Only shot spec version 1 is supported")
    frames = integer(data["frames"])
    duration = frames / FPS
    plate = asset(base, data["background"])
    if not isinstance(data["layers"], list) or len(data["layers"]) > 16:
        raise ValueError("layers must be a list with at most 16 elements")
    layers, names = [], set()
    for layer in data["layers"]:
        keys(layer, ["id", "image", "size", "pivot", "anchor", "motions"], ["opacity", "glow_radius"])
        if not isinstance(layer["id"], str) or not layer["id"] or layer["id"] in names:
            raise ValueError("Layer ids must be unique nonempty strings")
        names.add(layer["id"])
        size = pair(layer["size"])
        for s in size:
            integer(s, 1, 4096)
        pivot, anchor = pair(layer["pivot"]), pair(layer["anchor"])
        if any(not 0 <= p <= s for p, s in zip(pivot, size)):
            raise ValueError("Pivot must lie inside resized layer")
        opacity, radius = number(layer.get("opacity", 1)), number(layer.get("glow_radius", 0))
        if not 0 <= opacity <= 1 or not 0 <= radius <= 80:
            raise ValueError("Opacity/glow radius out of bounds")
        if not isinstance(layer["motions"], list):
            raise ValueError("motions must be a list")
        kinds = set()
        for m in layer["motions"]:
            kind = m.get("type") if isinstance(m, dict) else None
            required = {"rotate": ["from", "to"], "translate": ["path"],
                        "fade": ["from", "to"], "glow": ["from", "to"],
                        "shake": ["amplitude", "cycles"]}
            if kind not in required:
                raise ValueError("Unknown motion type")
            keys(m, ["type", "start_s", "end_s", *required[kind]], ["easing"])
            if kind in kinds or (kind in {"fade", "glow"} and kinds & {"fade", "glow"}):
                raise ValueError("Only one motion of each type and one opacity motion per layer")
            kinds.add(kind)
            start, end = number(m["start_s"]), number(m["end_s"])
            if not 0 <= start < end <= (frames - 1) / FPS:
                raise ValueError("Motion must end by the last sampled frame")
            if m.get("easing", "linear") not in EASINGS:
                raise ValueError("Unknown easing")
            if kind == "translate":
                if not isinstance(m["path"], list) or not 2 <= len(m["path"]) <= 32:
                    raise ValueError("Path requires 2..32 points")
                for point in m["path"]:
                    pair(point)
            elif kind == "shake":
                amp = pair(m["amplitude"])
                if any(not 0 <= a <= 30 for a in amp) or not 0 < number(m["cycles"]) <= 50:
                    raise ValueError("Shake amplitude/cycles out of bounds")
                if m.get("easing", "linear") != "linear":
                    raise ValueError("Shake uses its own sine envelope; easing must be linear")
            else:
                a, b = number(m["from"]), number(m["to"])
                if kind in {"fade", "glow"} and not (0 <= a <= 1 and 0 <= b <= 1):
                    raise ValueError("Fade/glow values are opacity in [0,1]")
        layers.append({**layer, "image": asset(base, layer["image"]), "size": size,
                       "pivot": pivot, "anchor": anchor, "opacity": opacity, "glow_radius": radius})
    sounds = []
    if not isinstance(data.get("sound_cues", []), list):
        raise ValueError("sound_cues must be a list")
    for cue in data.get("sound_cues", []):
        keys(cue, ["file", "time_s"], ["gain"])
        at, gain = number(cue["time_s"]), number(cue.get("gain", 1))
        if not 0 <= at < duration or not 0 <= gain <= 2:
            raise ValueError("Sound cue out of bounds")
        sounds.append({"file": asset(base, cue["file"]), "time_s": at, "gain": gain})
    return {**data, "background": plate, "layers": layers, "sound_cues": sounds}


def output_path(path):
    p = Path(path).resolve()
    if OUTPUTS.resolve() != OUTPUTS.absolute() or not p.is_relative_to(OUTPUTS.absolute()):
        raise ValueError(f"All generated files must stay below {OUTPUTS}")
    return p


class Tools:
    """Pinned local executables; no PATH lookup, shell or network-capable adapters."""
    def __init__(self, lock):
        self.entries = read(lock)
        keys(self.entries, ["ffmpeg", "ffprobe"])
        self.verify()

    def verify(self):
        for item in self.entries.values():
            keys(item, ["path", "bytes", "sha256"])
            p = Path(item["path"])
            if not p.is_absolute() or p.resolve(strict=True) != p or p.is_symlink() or not p.is_file():
                raise ValueError("Binary must be an absolute canonical regular file")
            if p.stat().st_size != item["bytes"] or digest(p) != item["sha256"]:
                raise ValueError(f"Binary binding failed: {p}")

    def run(self, kind, args, directory):
        self.verify()
        directory = output_path(directory)
        argv = [self.entries[kind]["path"], *map(str, args)]
        env = {k: os.environ[k] for k in ("SYSTEMROOT", "WINDIR") if k in os.environ}
        env.update(TEMP=str(directory), TMP=str(directory))
        with (directory / "commands.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({"argv": argv, "environment_keys": sorted(env)}) + "\n")
        result = subprocess.run(argv, cwd=directory, env=env, shell=False, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=1800)
        with (directory / "commands.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({"returncode": result.returncode, "stdout": result.stdout,
                                  "stderr": result.stderr}) + "\n")
        if result.returncode:
            raise RuntimeError(f"{kind} exited {result.returncode}: {result.stderr[-3000:]}")
        return result.stdout


def fmt(x):
    return f"{x:.10g}"


def progress_expr(m, variable="t"):
    p = f"clip(({variable}-{fmt(m['start_s'])})/{fmt(m['end_s']-m['start_s'])},0,1)"
    kind = m.get("easing", "linear")
    return {"linear": p, "smoothstep": f"({p})*({p})*(3-2*({p}))",
            "ease_in": f"({p})*({p})", "ease_out": f"1-(1-({p}))*(1-({p}))"}[kind]


def path_expr(points, p, axis):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    total = sum(lengths)
    if not total:
        return fmt(points[0][axis])
    value, cumulative = fmt(points[-1][axis]), total
    for i in reversed(range(len(lengths))):
        span = lengths[i]
        cumulative -= span
        if not span:
            continue
        a, b = points[i][axis], points[i+1][axis]
        part = f"{fmt(a)}+{fmt(b-a)}*(({p})*{fmt(total)}-{fmt(cumulative)})/{fmt(span)}"
        value = f"if(lte(({p})*{fmt(total)},{fmt(cumulative+span)}),{part},{value})"
    return value


def layer_expressions(layer):
    angle, opacity = "0", fmt(layer["opacity"])
    x, y = map(fmt, layer["anchor"])
    for m in layer["motions"]:
        p = progress_expr(m)
        kind = m["type"]
        if kind == "rotate":
            angle = f"({fmt(m['from'])}+({fmt(m['to']-m['from'])})*({p}))*PI/180"
        elif kind == "translate":
            x += f"+({path_expr(m['path'], p, 0)})"
            y += f"+({path_expr(m['path'], p, 1)})"
        elif kind in {"fade", "glow"}:
            q = progress_expr(m, "T")
            opacity += f"*({fmt(m['from'])}+({fmt(m['to']-m['from'])})*({q}))"
        elif kind == "shake":
            # Bound to interval, zero displacement at both endpoints; fixed phase.
            for axis in (0, 1):
                shake = (f"if(between(t,{fmt(m['start_s'])},{fmt(m['end_s'])}),"
                         f"{fmt(m['amplitude'][axis])}*sin(PI*({p}))*"
                         f"sin(2*PI*{fmt(m['cycles'])}*({p})+{fmt(axis*math.pi/2)}),0)")
                if axis == 0:
                    x += f"+({shake})"
                else:
                    y += f"+({shake})"
    return angle, opacity, x, y


def stage(spec, directory):
    from PIL import Image, ImageFilter, ImageOps
    with Image.open(spec["background"]) as source:
        # Opaque full-cover crop only: no fit, background blur, padding or boxes.
        rgba = source.convert("RGBA")
        if rgba.getchannel("A").getextrema() != (255, 255):
            raise ValueError("Background plate must be fully opaque")
        plate = ImageOps.fit(rgba.convert("RGB"), (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        plate.save(directory / "plate.png")
    staged = []
    for index, layer in enumerate(spec["layers"]):
        with Image.open(layer["image"]) as image:
            if "A" not in image.getbands() or image.getchannel("A").getextrema()[0] == 255:
                raise ValueError(f"Element needs genuine alpha: {layer['id']}")
            image = image.convert("RGBA").resize(layer["size"], Image.Resampling.LANCZOS)
        px, py = layer["pivot"]
        radius = max(math.dist((px, py), corner) for corner in
                     ((0, 0), (image.width, 0), (0, image.height), image.size))
        half = math.ceil(radius + layer["glow_radius"] * 3 + 4)
        if half > 4096:
            raise ValueError("Padded layer too large")
        canvas = Image.new("RGBA", (half * 2, half * 2))
        # Subpixel pivot is preserved by an affine translation, rather than rounded paste.
        canvas = image.transform(canvas.size, Image.Transform.AFFINE,
                                 (1, 0, px-half, 0, 1, py-half), Image.Resampling.BICUBIC)
        if layer["glow_radius"]:
            halo = canvas.filter(ImageFilter.GaussianBlur(layer["glow_radius"]))
            canvas = Image.alpha_composite(halo, canvas)
        path = directory / f"layer-{index:02d}.png"
        canvas.save(path)
        staged.append((path, half))
    return staged


def ffargs():
    return ["-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-filter_complex_threads", "1"]


def encode_args():
    return ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "1",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-map_metadata", "-1", "-movflags", "+faststart"]


def inspect(tools, clip, directory, frames):
    probe = json.loads(tools.run("ffprobe", ["-v", "error", "-show_streams", "-show_format", "-of", "json", clip], directory))
    videos = [s for s in probe["streams"] if s["codec_type"] == "video"]
    if len(videos) != 1:
        raise ValueError("Exactly one video stream required")
    v = videos[0]
    actual = (v["width"], v["height"], v["avg_frame_rate"], int(v["nb_frames"]), v["pix_fmt"], v.get("sample_aspect_ratio"))
    if actual != (WIDTH, HEIGHT, "30/1", frames, "yuv420p", "1:1") or v["codec_name"] != "h264":
        raise ValueError(f"Clip format/frame count mismatch: {actual}")
    if any(s["codec_type"] not in {"video", "audio"} for s in probe["streams"]):
        raise ValueError("Master cannot contain embedded subtitle/data streams")
    tools.run("ffmpeg", ["-nostdin", "-v", "error", "-xerror", "-i", clip, "-f", "null", "-"], directory)
    return probe


def render(spec_path, output, tools):
    spec_path, output = Path(spec_path).resolve(), output_path(output)
    tools.verify()  # Before creating output or staging roots.
    spec = parse_spec(read(spec_path), spec_path.parent)
    if output.exists():
        raise FileExistsError(f"Choose a new output name: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=output.stem + "-", dir=output.parent))
    staged = stage(spec, work)
    args = ffargs() + ["-loop", "1", "-framerate", str(FPS), "-i", work / "plate.png"]
    for path, _ in staged:
        args += ["-loop", "1", "-framerate", str(FPS), "-i", path]
    for cue in spec["sound_cues"]:
        args += ["-i", cue["file"]]
    graph = ["[0:v]setsar=1,format=rgba[base0]"]
    for i, (layer, (_, half)) in enumerate(zip(spec["layers"], staged)):
        angle, opacity, x, y = layer_expressions(layer)
        effects = "format=rgba"
        if angle != "0":
            effects += f",rotate=a='{angle}':ow=iw:oh=ih:c=none:bilinear=1"
        if opacity != "1":
            effects += f",geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*({opacity})'"
        graph.append(f"[{i+1}:v]{effects}[el{i}]")
        graph.append(f"[base{i}][el{i}]overlay=x='{x}-{half}':y='{y}-{half}':"
                     f"eval=frame:format=auto:shortest=1[base{i+1}]")
    graph.append(f"[base{len(staged)}]format=yuv420p,setsar=1[video]")
    if spec["sound_cues"]:
        graph.append("anullsrc=r=48000:cl=stereo[silence]")
        for i, cue in enumerate(spec["sound_cues"]):
            graph.append(f"[{len(staged)+1+i}:a]aresample=48000,volume={fmt(cue['gain'])},"
                         f"adelay={round(cue['time_s']*48000)}S:all=1[a{i}]")
        sources = "[silence]" + "".join(f"[a{i}]" for i in range(len(spec["sound_cues"])))
        graph.append(f"{sources}amix=inputs={len(spec['sound_cues'])+1}:normalize=0[audio]")
    (work / "filtergraph.txt").write_text(";\n".join(graph), encoding="utf-8")
    args += ["-filter_complex", ";".join(graph), "-map", "[video]"]
    if spec["sound_cues"]:
        args += ["-map", "[audio]", "-c:a", "aac", "-ar", "48000", "-ac", "2"]
    else:
        args += ["-an"]
    temporary = work / "clip.mp4"
    args += ["-frames:v", spec["frames"], "-t", fmt(spec["frames"]/FPS), *encode_args(), temporary]
    tools.run("ffmpeg", args, work)
    probe = inspect(tools, temporary, work, spec["frames"])
    for label, frame in (("start", 0), ("middle", spec["frames"]//2), ("end", spec["frames"]-1)):
        tools.run("ffmpeg", ffargs() + ["-i", temporary, "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1", work / f"{label}.png"], work)
    inputs = [spec_path, spec["background"], *(l["image"] for l in spec["layers"]), *(c["file"] for c in spec["sound_cues"])]
    save(work / "receipt.json", {"spec": str(spec_path), "frames": spec["frames"], "probe": probe,
         "sha256": digest(temporary), "inputs": {str(p): digest(p) for p in inputs},
         "tools": tools.entries, "visual_review": "PENDING; inspect decoded PNGs",
         "market_acceptance": "NOT_TESTED"})
    temporary.replace(output)
    print(json.dumps({"clip": str(output), "evidence": str(work)}))
    return work


def legacy_plan(timeline_path, cuts, replacements):
    """Adapter for private-five/build.py's contiguous cue/shot grouping, no imports."""
    timeline_path = Path(timeline_path).resolve()
    timeline = read(timeline_path)
    keys(replacements, [], [str(i) for i in range(10000)])
    groups, previous = [], 0
    if timeline.get("fps", FPS) != FPS:
        raise ValueError("Legacy FPS must be 30")
    for index, cue in enumerate(timeline["cues"]):
        start, end = integer(cue["start"], 0), integer(cue["end"])
        if (index and start != previous) or end <= start:
            raise ValueError("Legacy cues must be contiguous after the first cue")
        previous = end
        if groups and groups[-1][0] == cue["shot"]:
            groups[-1][2] = end
        else:
            groups.append([cue["shot"], start if index else 0, end])
    if not groups or previous != timeline["frames"]:
        raise ValueError("Legacy frame count mismatch")
    if set(replacements) - {str(i) for i in range(len(groups))}:
        raise ValueError("Replacement index does not exist")
    shots = []
    for i, (_, start, end) in enumerate(groups):
        clip = replacements.get(str(i), str((Path(cuts).resolve() / f"shot-{i:03d}.mp4")))
        shots.append({"clip": str(asset(timeline_path.parent, clip)), "frames": end-start})
    return {"version": 1, "shots": shots}


def splice(plan_path, output, tools):
    """Decode/concat same-length replacements; keep narration and SRT timecodes."""
    import shutil
    plan_path, output = Path(plan_path).resolve(), output_path(output)
    tools.verify()
    plan = read(plan_path)
    keys(plan, ["version", "shots"], ["audio", "sidecars"])
    if type(plan["version"]) is not int or plan["version"] != 1 or not isinstance(plan["shots"], list) or not plan["shots"]:
        raise ValueError("Invalid timeline version/shots")
    base, shots = plan_path.parent, []
    for shot in plan["shots"]:
        keys(shot, ["clip", "frames"])
        shots.append((asset(base, shot["clip"]), integer(shot["frames"])))
    sidecars = plan.get("sidecars", {})
    keys(sidecars, [], ["en", "zh-Hant"])
    captions = {lang: asset(base, p) for lang, p in sidecars.items()}
    if any(p.suffix.lower() != ".srt" for p in captions.values()):
        raise ValueError("Sidecars must be SRT")
    audio = asset(base, plan["audio"]) if plan.get("audio") else None
    destinations = {lang: output.with_suffix(f".{lang}.srt") for lang in captions}
    if any(p.exists() for p in (output, *destinations.values())):
        raise FileExistsError("Choose a new output name; output/sidecar exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=output.stem + "-splice-", dir=output.parent))
    for clip, count in shots:
        inspect(tools, clip, work, count)
    args, graph = ffargs(), []
    for i, (clip, _) in enumerate(shots):
        args += ["-i", clip]
        graph.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}]")
    graph.append("".join(f"[v{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[video]")
    total = sum(count for _, count in shots)
    if audio:
        # Preserve original audio stream; cue sounds on replacement clips are intentionally ignored.
        args += ["-i", audio]
        probe = json.loads(tools.run("ffprobe", ["-v", "error", "-show_streams", "-of", "json", audio], work))
        streams = [s for s in probe["streams"] if s["codec_type"] == "audio"]
        if not streams or abs(float(streams[0].get("duration", 0)) - total/FPS) > 1/FPS:
            raise ValueError("Narration length must match timeline within one frame")
    temporary = work / "master.mp4"
    args += ["-filter_complex", ";".join(graph), "-map", "[video]"]
    args += ["-map", f"{len(shots)}:a:0", "-c:a", "aac", "-ar", "48000", "-ac", "2"] if audio else ["-an"]
    args += ["-frames:v", total, "-t", fmt(total/FPS), *encode_args(), temporary]
    tools.run("ffmpeg", args, work)
    probe = inspect(tools, temporary, work, total)
    save(work / "receipt.json", {"frames": total, "probe": probe, "sha256": digest(temporary),
         "plan_sha256": digest(plan_path), "shots": [{"path": str(p), "sha256": digest(p), "frames": f} for p, f in shots],
         "audio": {"path": str(audio), "sha256": digest(audio)} if audio else None,
         "sidecars": {k: digest(p) for k, p in captions.items()}, "clip_audio": "discarded; use original timeline mix"})
    for lang, path in captions.items():
        shutil.copyfile(path, destinations[lang])
    temporary.replace(output)
    print(json.dumps({"master": str(output), "evidence": str(work)}))
    return work


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--tools", type=Path, default=HERE / "tools.lock.json")
    sub = cli.add_subparsers(dest="mode", required=True)
    for name in ("render", "splice"):
        p = sub.add_parser(name)
        p.add_argument("spec", type=Path)
        p.add_argument("output", type=Path)
    p = sub.add_parser("legacy-plan")
    p.add_argument("timeline", type=Path)
    p.add_argument("cuts", type=Path)
    p.add_argument("replacements", type=Path, help='JSON mapping group index to replacement clip')
    p.add_argument("output", type=Path)
    args = cli.parse_args()
    tools = Tools(args.tools)
    if args.mode == "render":
        render(args.spec, args.output, tools)
    elif args.mode == "splice":
        splice(args.spec, args.output, tools)
    else:
        plan = legacy_plan(args.timeline, args.cuts, read(args.replacements))
        target = output_path(args.output)
        if target.exists():
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        save(target, plan)


if __name__ == "__main__":
    main()
