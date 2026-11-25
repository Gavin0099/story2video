"""Offline photographic storyboard renderer. No motion-module or hosted API dependency."""
from __future__ import annotations

import argparse
from array import array
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PureWindowsPath
import subprocess
import time
import wave

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUTPUTS = REPO / "artifacts/static-ten-20261124"
FPS, WIDTH, HEIGHT, RATE = 30, 1080, 1920, 24000
MODEL_HASHES = {
    "kokoro-v1.0.int8.onnx": "6e742170d309016e5891a994e1ce1559c702a2ccd0075e67ef7157974f6406cb",
    "voices-v1.0.bin": "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}


def read(path):
    def reject_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject_constant)


def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def local(base, name):
    """Portable, confined input names; never accept absolute paths in manifests."""
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Use a relative POSIX asset name")
    if Path(name).is_absolute() or PureWindowsPath(name).is_absolute():
        raise ValueError("Absolute asset name")
    path = (base / name).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError("Asset escapes story folder")
    return path


def validate(story):
    from jsonschema import Draft202012Validator
    data, refs = read(story / "shots.json"), read(story / "references.json")
    for name, value in (("shots", data), ("references", refs)):
        errors = sorted(Draft202012Validator(read(HERE / f"{name}.schema.json")).iter_errors(value),
                        key=lambda e: str(list(e.path)))
        if errors:
            raise ValueError(f"{name}: {errors[0].json_path}: {errors[0].message}")
    text = (story / "story.md").read_text(encoding="utf-8")
    if not text.startswith("# FICTION") or f"Genre: {data['genre']}" not in text:
        raise ValueError("story.md must start # FICTION and declare matching Genre")
    if "## Script" not in text or "## Shot list" not in text:
        raise ValueError("story.md needs Script and Shot list sections")
    ids = [s["id"] for s in data["shots"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate shot id")
    cues = [c["id"] for c in data["narration"]]
    if len(cues) != len(set(cues)):
        raise ValueError("Duplicate narration id")
    ref_ids = [r["id"] for r in refs["items"]]
    if len(ref_ids) != len(set(ref_ids)):
        raise ValueError("Duplicate reference id")
    reveal = next((i for i, s in enumerate(data["shots"]) if s["function"] == "reveal"), None)
    if reveal is None:
        raise ValueError("A reveal shot is required")
    if not any(s["function"] == "clue" and s["framing"] == "close_up" for s in data["shots"][:reveal]):
        raise ValueError("A clue close-up is required before the reveal")
    for sheet in data["sheets"].values():
        local(story, sheet["file"])
    for item in refs["items"]:
        check_source(item["canonical"], data)
        if set(item["appears_in"]) - set(ids):
            raise ValueError("Reference appears_in contains unknown shots")
    for shot in data["shots"]:
        check_source(shot["source"], data)
        required = set(shot["required_references"])
        if required - set(ref_ids):
            raise ValueError("Unknown required reference id")
        expected = {r["id"] for r in refs["items"] if shot["id"] in r["appears_in"]}
        if required != expected:
            raise ValueError("Missing or inconsistent recurring reference ids")
        for endpoint in (shot["start"], shot["end"]):
            if isinstance(endpoint, dict) and endpoint["cue"] not in cues:
                raise ValueError("Unknown audio cue binding")
        for sound in shot["sfx"]:
            local(story, sound["file"])
    for cue in data["narration"]:
        if "file" in cue:
            local(story, cue["file"])
    return data, refs


def check_source(source, data):
    if source["sheet"] not in data["sheets"]:
        raise ValueError("Unknown source sheet")
    sheet = data["sheets"][source["sheet"]]
    if source["cell"] >= sheet["columns"] * sheet["rows"]:
        raise ValueError("Cell outside sheet")
    x, y, w, h = source["crop"]
    if x + w > 1.0000001 or y + h > 1.0000001:
        raise ValueError("Crop outside cell")


def cell_box(size, sheet, source):
    """Row-major zero-based cell, seam trim in pixels, then normalized xywh crop."""
    w, h = size
    col, row = source["cell"] % sheet["columns"], source["cell"] // sheet["columns"]
    edge = sheet["edge_px"]
    left, top = round(col*w/sheet["columns"])+edge, round(row*h/sheet["rows"])+edge
    right, bottom = round((col+1)*w/sheet["columns"])-edge, round((row+1)*h/sheet["rows"])-edge
    x, y, cw, ch = source["crop"]
    box = (round(left+x*(right-left)), round(top+y*(bottom-top)),
           round(left+(x+cw)*(right-left)), round(top+(y+ch)*(bottom-top)))
    if right <= left or bottom <= top or box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError("Empty cell/crop after seam trim")
    return box


def extract(story, data, source, output):
    from PIL import Image, ImageOps
    sheet = data["sheets"][source["sheet"]]
    path = local(story, sheet["file"])
    with Image.open(path) as image:
        box = cell_box(image.size, sheet, source)
        plate = ImageOps.fit(image.crop(box).convert("RGB"), (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        plate.save(output)
    return {"sheet": source["sheet"], "cell": source["cell"], "pixel_crop": box,
            "sheet_sha256": digest(path), "plate_sha256": digest(output)}


def resolve_time(value, cues):
    if isinstance(value, (int, float)):
        return value
    return cues[value["cue"]][value["edge"]] + value.get("offset", 0)


def timeline(data, cues):
    result, previous = [], 0
    for shot in data["shots"]:
        start = round(resolve_time(shot["start"], cues)*FPS)
        end = round(resolve_time(shot["end"], cues)*FPS)
        if start != previous or end <= start:
            raise ValueError("Shots must be ordered, contiguous, positive, starting at zero")
        result.append({**shot, "start": start/FPS, "end": end/FPS, "frames": end-start})
        previous = end
    if previous < 105:
        raise ValueError("Story must cover the question through 3.5 seconds")
    for cue in cues.values():
        if not 0 <= cue["start"] < cue["end"] <= previous/FPS:
            raise ValueError("Narration outside picture timeline")
    reveal = next(s["start"] for s in result if s["function"] == "reveal")
    if any(c["reveal"] and c["start"] < reveal for c in cues.values()):
        raise ValueError("Answer caption/audio starts before reveal")
    return result


def stamp(seconds):
    ms = round(seconds*1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def srt(cues, field):
    return "\n".join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c[field]}\n"
                     for i, c in enumerate(cues, 1))


def read_pcm(path):
    with wave.open(str(path), "rb") as stream:
        if (stream.getframerate(), stream.getnchannels(), stream.getsampwidth()) != (RATE, 1, 2):
            raise ValueError("Input WAV must be 24kHz mono PCM16")
        pcm = array("h", stream.readframes(stream.getnframes()))
    if not pcm or max(map(abs, pcm)) == 0:
        raise ValueError("Empty/silent source audio")
    return pcm


def write_pcm(path, pcm):
    with wave.open(str(path), "wb") as stream:
        stream.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        stream.writeframes(pcm.tobytes())


def prepare_audio(story, data, out):
    cues, pieces, cursor, tts = {}, {}, 0, None
    for line in data["narration"]:
        dest = out / "cache/voice" / (line["id"] + ".wav")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if "file" in line:
            pcm = read_pcm(local(story, line["file"]))
            write_pcm(dest, pcm)
        else:
            if tts is None:
                models = Path(os.environ["S2V_KOKORO_MODELS"])
                for name, expected in MODEL_HASHES.items():
                    if digest(models/name) != expected:
                        raise ValueError("Kokoro model digest mismatch")
                # This task never downloads models; the installed local provider is optional.
                from kokoro_onnx import Kokoro
                tts = Kokoro(*(str(models/name) for name in MODEL_HASHES))
            values, rate = tts.create(line["en"], voice=line["voice"], speed=line["speed"], lang="en-us")
            if rate != RATE or not all(math.isfinite(float(v)) for v in values):
                raise ValueError("Invalid Kokoro PCM")
            threshold = max(.003, max(map(abs, values))*.017)
            active = [i for i, v in enumerate(values) if abs(v) > threshold]
            if not active:
                raise ValueError("Silent Kokoro output")
            values = values[max(0,active[0]-120):active[-1]+121]
            pcm = array("h", (round(max(-.99,min(.99,float(v)))*32767) for v in values))
            write_pcm(dest, pcm)
        start = max(cursor + line.get("gap_before", .09), line.get("not_before", 0))
        start = round(start*RATE)/RATE
        end = start + len(pcm)/RATE
        cues[line["id"]] = {**line, "start": start, "end": end, "samples": len(pcm), "sha256": digest(dest)}
        pieces[line["id"]] = pcm
        cursor = end
    shots = timeline(data, cues)
    mix = [0.] * round(shots[-1]["end"]*RATE)

    def add(pcm, at, gain):
        index = round(at*RATE)
        if index < 0 or index+len(pcm) > len(mix):
            raise ValueError("Audio would be truncated by picture")
        for i, value in enumerate(pcm):
            mix[index+i] += value*gain

    for key, cue in cues.items():
        add(pieces[key], cue["start"], .82)
    sound_cues = []
    for shot in shots:
        for sound in shot["sfx"]:
            path = local(story, sound["file"])
            pcm = read_pcm(path)
            at = shot["start"] + sound["offset"]
            if at + len(pcm)/RATE > shot["end"] + .00001:
                raise ValueError("SFX crosses its declared shot boundary")
            add(pcm, at, sound["gain"])
            sound_cues.append({**sound, "start": at, "end": at+len(pcm)/RATE, "sha256": digest(path)})
    if max(map(abs, mix)) >= 32767:
        raise ValueError("Mix clips; reduce SFX gain")
    write_pcm(out/"mix.wav", array("h", (round(v) for v in mix)))
    captions = sorted([*cues.values(), *sound_cues], key=lambda c: c["start"])
    for lang, field in (("en", "en"), ("zh-Hant", "zh")):
        (out/f"{data['story_id']}.{lang}.srt").write_text(srt(captions, field), encoding="utf-8")
    save(out/"timeline.json", {"shots": shots, "cues": list(cues.values()), "captions": captions,
                              "peak_dbfs": 20*math.log10(max(map(abs,mix))/32768)})
    return shots, captions


class Tools:
    """Exact A-pilot binary hashes, paths supplied externally. Never use PATH or a shell."""
    def __init__(self, out):
        self.out = out
        self.lock = read(HERE/"tools.lock.json")
        self.paths = {}
        for kind, entry in self.lock.items():
            path = Path(os.environ[entry["environment"]]).resolve(strict=True)
            if not path.is_file() or path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
                raise ValueError(f"Pinned {kind} binding failed")
            self.paths[kind] = path
        self.encodes = 0

    def run(self, kind, args):
        argv = [str(self.paths[kind]), *map(str, args)]
        env = {k: os.environ[k] for k in ("SYSTEMROOT", "WINDIR") if k in os.environ}
        env.update(TEMP=str(self.out/"tmp"), TMP=str(self.out/"tmp"))
        start = time.monotonic()
        result = subprocess.run(argv, cwd=self.out, env=env, shell=False, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=1800)
        # No personal absolute paths in portable command evidence, even in tool diagnostics.
        def scrub(value):
            text = str(value)
            replacements = [(str(self.out), "${STORY_OUTPUT}"), (str(REPO), "${REPO}")]
            replacements += [(str(p), "${"+self.lock[k]["environment"]+"}") for k,p in self.paths.items()]
            for path, token in replacements:
                text = text.replace(json.dumps(path)[1:-1], token)
                text = text.replace(path, token).replace(path.replace("\\", "/"), token)
            return text
        record = {"tool": kind, "argv": [scrub(v) for v in argv], "returncode": result.returncode,
                  "seconds": round(time.monotonic()-start, 3), "stdout": scrub(result.stdout),
                  "stderr": scrub(result.stderr), "temp": "${STORY_OUTPUT}/tmp"}
        with (self.out/"commands.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps(record, ensure_ascii=False)+"\n")
        if kind == "ffmpeg" and "libx264" in args:
            self.encodes += 1
        if result.returncode:
            raise RuntimeError(f"{kind} failed; see commands.jsonl")
        return result.stdout


FF = ["-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-threads", "1", "-filter_threads", "1", "-filter_complex_threads", "1"]
ENCODE = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart"]


def camera(move, frames):
    p = f"on/{max(1,frames-1)}"
    z = f"{move['zoom'][0]}+({move['zoom'][1]-move['zoom'][0]})*{p}"
    x = f"(iw-iw/zoom)*({move['from'][0]}+({move['to'][0]-move['from'][0]})*{p})"
    y = f"(ih-ih/zoom)*({move['from'][1]}+({move['to'][1]-move['from'][1]})*{p})"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1080x1920:fps=30,setsar=1"


def question_plate(data, out):
    from PIL import Image, ImageDraw, ImageFont
    font_path = os.environ["S2V_QUESTION_FONT"]
    font = ImageFont.truetype(font_path, 52)
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    for i, text in enumerate((data["question"]["en"], data["question"]["zh"])):
        if draw.textlength(text, font=font) > 920:
            raise ValueError("Opening question too long for a compact line")
        draw.text((540, 180+i*78), text, font=font, anchor="mm", fill="white", stroke_width=4, stroke_fill="black")
    image.save(out/"cache/question.png")


def render(story, data, shots, out, tools):
    question_plate(data, out)
    provenance = {}
    for shot in shots:
        plate = out/"cache"/(shot["id"]+".png")
        provenance[shot["id"]] = extract(story, data, shot["source"], plate)
        args = FF + ["-loop", "1", "-framerate", "30", "-i", plate]
        move = camera(shot["camera"], shot["frames"])
        if shot["start"] < 3.5 and shot["end"] > 1:
            begin, end = max(0,1-shot["start"]), 3.5-shot["start"]
            args += ["-loop", "1", "-framerate", "30", "-i", out/"cache/question.png", "-filter_complex",
                     f"[0:v]{move}[v];[v][1:v]overlay=enable='gte(t,{begin})*lt(t,{end})':format=auto,format=yuv420p[o]", "-map", "[o]"]
        else:
            args += ["-vf", move]
        tools.run("ffmpeg", args+["-an", "-frames:v", str(shot["frames"]), *ENCODE, out/"cache"/(shot["id"]+".mp4")])
    save(out/"assets.json", provenance)
    # Relative names make concat input reusable and avoid personal paths in files.
    (out/"cache/concat.txt").write_text("".join(f"file '{s['id']}.mp4'\n" for s in shots), encoding="utf-8")
    tools.run("ffmpeg", FF+["-f", "concat", "-safe", "1", "-i", out/"cache/concat.txt", "-i", out/"mix.wav",
              "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
              "-movflags", "+faststart", out/f"{data['story_id']}.mp4"])


def contact(paths, output, columns=6, labels=None):
    from PIL import Image, ImageDraw
    image = Image.new("RGB", (180*columns, (320+(22 if labels else 0))*math.ceil(len(paths)/columns)), "#181818")
    for i, path in enumerate(paths):
        with Image.open(path) as frame:
            x, y = i%columns*180, i//columns*(342 if labels else 320)
            image.paste(frame.convert("RGB").resize((180,320)), (x,y))
        if labels:
            ImageDraw.Draw(image).text((x+2,y+321), labels[i], fill="white")
    image.save(output)


def qa(data, shots, captions, out, tools):
    from PIL import Image
    master = out/f"{data['story_id']}.mp4"
    probe = json.loads(tools.run("ffprobe", ["-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", master]))
    # ffprobe embeds its input filename: replace it before saving portable evidence.
    probe["format"]["filename"] = master.name
    save(out/"qa/probe.json", probe)
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    frames = sum(s["frames"] for s in shots)
    checks = {
        "video": (video["width"],video["height"],video["codec_name"],video["profile"],video["pix_fmt"],video["avg_frame_rate"])
                 == (WIDTH,HEIGHT,"h264","High","yuv420p","30/1"),
        "frames": int(video["nb_read_frames"]) == frames,
        "duration": abs(float(probe["format"]["duration"])-frames/FPS) < .05,
        "audio": audio["codec_name"] == "aac" and audio["sample_rate"] == "48000" and audio["channels"] == 2
                 and abs(float(audio["duration"])-frames/FPS) < .05,
        "no_embedded_subtitles": len(probe["streams"]) == 2,
    }
    # Check MP4 top-level atom order for faststart, independent of encode options.
    atoms = []
    with master.open("rb") as stream:
        while header := stream.read(8):
            size, kind = int.from_bytes(header[:4],"big"), header[4:].decode("ascii")
            if size < 8:
                raise ValueError("Unsupported MP4 atom")
            atoms.append(kind)
            stream.seek(size-8, 1)
    checks["faststart"] = atoms.index("moov") < atoms.index("mdat")
    tools.run("ffmpeg", FF+["-xerror", "-i", master, "-f", "null", "-"])
    checks["full_decode"] = True
    tools.run("ffmpeg", ["-nostdin", "-v", "info", "-i", master, "-af", "ebur128=peak=true", "-f", "null", "-"])
    for lang, field in (("en","en"),("zh-Hant","zh")):
        checks[f"captions_{lang}"] = (out/f"{data['story_id']}.{lang}.srt").read_text(encoding="utf-8") == srt(captions,field)
    checks["caption_bounds"] = all(0 <= c["start"] < c["end"] <= frames/FPS for c in captions)
    # Dense decoded samples: every seventh 30fps frame = 4.286fps, plus each last frame.
    silent = []
    for shot in shots:
        folder = out/"qa"/shot["id"]
        folder.mkdir(parents=True, exist_ok=True)
        count = shot["frames"]
        selector = f"select='not(mod(n,7))+eq(n,{count-1})'"
        tools.run("ffmpeg", FF+["-i", master, "-vf",
                  f"trim=start_frame={round(shot['start']*FPS)}:end_frame={round(shot['end']*FPS)},setpts=PTS-STARTPTS,{selector},scale=270:480",
                  "-fps_mode", "vfr", folder/"%04d.png"])
        paths = sorted(folder.glob("*.png"))
        sampled = sorted(set([*range(0,count,7), count-1]))
        if len(paths) != len(sampled):
            raise ValueError("Dense extraction frame count mismatch")
        save(folder/"samples.json", {"times": [shot["start"]+i/FPS for i in sampled], "minimum_fps": 30/7})
        contact(paths, out/"qa"/(shot["id"]+"-strip.jpg"), labels=[f"{shot['start']+i/FPS:.3f}s" for i in sampled])
        # Silent review uses isolated source cells BEFORE editorial question compositing.
        # No annotations in this image; expected meaning lives only in the companion file.
        silent.append(out/"cache"/(shot["id"]+".png"))
    contact(silent, out/"silent-storyboard.jpg", columns=min(6,len(silent)))
    save(out/"silent-storyboard.json", [{"frame": i+1,"shot": s["id"],"function": s["function"],"should_convey": s["conveys"]}
                                      for i,s in enumerate(shots)])
    report = {"checks": checks, "engineering": "PASS" if all(checks.values()) else "FAIL",
              "master_sha256": digest(master), "dense_sampling_fps": 30/7,
              "alignment_method": "Measured source PCM boundaries; generated SRT exact comparison, not ASR",
              "human_review": {"continuity":"PENDING", "phone_readability":"PENDING", "silent_story":"PENDING", "listening":"PENDING"},
              "market_acceptance": "NOT_TESTED"}
    save(out/"qa/report.json", report)
    if not all(checks.values()):
        raise ValueError("Technical QA failed; see qa/report.json")
    return report


@contextmanager
def owned_output(out):
    out.mkdir(parents=True, exist_ok=True)
    lock = out/".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    cache_env = {name:os.environ.get(name) for name in
                 ("TMP", "TEMP", "HF_HOME", "XDG_CACHE_HOME", "NUMBA_CACHE_DIR")}
    try:
        for name in ("cache", "tmp", "qa"):
            (out/name).mkdir(exist_ok=True)
        os.environ.update(TMP=str(out/"tmp"), TEMP=str(out/"tmp"), HF_HOME=str(out/"cache/huggingface"),
                          XDG_CACHE_HOME=str(out/"cache"), NUMBA_CACHE_DIR=str(out/"cache/numba"))
        yield
    finally:
        for name, value in cache_env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        lock.unlink()


def output_for(story_id):
    out = OUTPUTS/story_id
    if not out.resolve().is_relative_to(OUTPUTS.resolve()):
        raise ValueError("Output escapes artifacts boundary")
    return out


def run_story(story):
    started = time.monotonic()
    data, refs = validate(story)
    out = output_for(data["story_id"])
    with owned_output(out):
        if (out/f"{data['story_id']}.mp4").exists():
            raise FileExistsError("Preserve existing master; use a new story revision id")
        tools = Tools(out)
        status = "FAILED"
        try:
            shots, captions = prepare_audio(story, data, out)
            render(story, data, shots, out, tools)
            qa(data, shots, captions, out, tools)
            status = "PASS"
        finally:
            ledger = ledger_rows(out)
            save(out/"cost.json", {"imagegen_calls": len(ledger), "imagegen_cost": "UNKNOWN" if ledger else 0,
                 "encode_count": tools.encodes, "wall_seconds": round(time.monotonic()-started,3), "result": status,
                 "encode_definition": "libx264 invocations; final stream-copy/AAC mux is separate in commands.jsonl"})
            save(out/"manifest.json", {"story_id": data["story_id"], "fiction": data["fiction"],
                 "inputs": {name:digest(story/name) for name in ("story.md","shots.json","references.json")},
                 "pipeline": {p.name:digest(p) for p in HERE.glob("*.py")},
                 "git_sha": os.environ.get("S2V_GIT_SHA", "UNRECORDED"),
                 "question_font_sha256": digest(Path(os.environ["S2V_QUESTION_FONT"]))
                     if os.environ.get("S2V_QUESTION_FONT") and Path(os.environ["S2V_QUESTION_FONT"]).is_file() else None,
                 "kokoro_models": MODEL_HASHES,
                 "toolchain": read(HERE/"tools.lock.json"), "market_acceptance":"NOT_TESTED"})
    return out


def ledger_rows(out):
    path = out/"images.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []


def build_prompt(data, refs, sheet_id, supports_images=False):
    if sheet_id not in data["sheets"]:
        raise ValueError("Unknown sheet")
    shots = [s for s in data["shots"] if s["source"]["sheet"] == sheet_id]
    used = {rid for s in shots for rid in s["required_references"]}
    canonical = [r for r in refs["items"] if r["id"] in used or r["canonical"]["sheet"] == sheet_id]
    sheet = data["sheets"][sheet_id]
    prompt = [f"Create ONE {sheet['columns']} column x {sheet['rows']} row photographic contact sheet.",
              "Each cell is an independent portrait shot. Edge-to-edge realistic photography, readable exposure, no captions, borders or watermarks.",
              "Maintain identical character, prop and set features. Leave safe room for a 9:16 cover crop. No fiction label inside image."]
    for r in canonical:
        prompt.append(f"CANONICAL {r['id']} ({r['kind']}): {'; '.join(r['invariants'])}. Canonical cell: {json.dumps(r['canonical'],sort_keys=True)}")
    for s in shots:
        prompt.append(f"CELL {s['source']['cell']}: {s['prompt']} Narrative function: {s['function']}. Required references: {', '.join(s['required_references'])}.")
    if not shots:
        prompt.append("REFERENCE SHEET FIRST: show the canonical characters/props/sets clearly in their assigned cells. This sheet will condition later shot sheets.")
    return {"sheet": sheet_id, "purpose": "shot_sheet" if shots else "reference_sheet", "prompt": "\n".join(prompt),
            "reference_items": canonical,
            "reference_images": [f"prompts/references/{r['id']}.png" for r in canonical
                                 if supports_images and r["canonical"]["sheet"] != sheet_id]}


def export_prompts(story, supports_images):
    data, refs = validate(story)
    out = output_for(data["story_id"])
    with owned_output(out):
        (out/"prompts/references").mkdir(parents=True,exist_ok=True)
        for sheet_id in data["sheets"]:
            payload = build_prompt(data, refs, sheet_id, supports_images)
            if supports_images:
                for r in payload["reference_items"]:
                    if r["canonical"]["sheet"] != sheet_id:
                        extract(story,data,r["canonical"],out/"prompts/references"/(r["id"]+".png"))
            payload["prompt_sha256"] = hashlib.sha256(payload["prompt"].encode()).hexdigest()
            save(out/"prompts"/(sheet_id+".json"),payload)


def record_image(story, sheet_id, result, accepted):
    """External generation is manual. Log EVERY completed call, including rejected sheets."""
    data, _ = validate(story)
    if sheet_id not in data["sheets"]:
        raise ValueError("Unknown sheet")
    out = output_for(data["story_id"])
    with owned_output(out):
        rows = ledger_rows(out)
        if len(rows) >= 5 or sum(r["sheet"] == sheet_id for r in rows) >= 2:
            raise ValueError("Image budget exceeded: max 5 calls/story and one correction/sheet")
        payload = read(out/"prompts"/(sheet_id+".json"))
        path = local(story,result)
        row = {"at":datetime.now(timezone.utc).isoformat(),"sheet":sheet_id,"purpose":payload["purpose"],
               "prompt_sha256":payload["prompt_sha256"],"result_filename":result,"result_sha256":digest(path),
               "status":"accepted" if accepted else "rejected","attempt":1+sum(r["sheet"]==sheet_id for r in rows)}
        with (out/"images.jsonl").open("a",encoding="utf-8") as stream:
            stream.write(json.dumps(row)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["validate","prompts","log-image","run"])
    parser.add_argument("story", type=Path)
    parser.add_argument("--supports-images", action="store_true")
    parser.add_argument("--sheet")
    parser.add_argument("--result")
    parser.add_argument("--status", choices=["accepted","rejected"])
    args = parser.parse_args()
    if args.mode == "validate":
        validate(args.story.resolve())
        print("VALID")
    elif args.mode == "prompts":
        export_prompts(args.story.resolve(),args.supports_images)
    elif args.mode == "log-image":
        if not all((args.sheet,args.result,args.status)):
            parser.error("log-image requires --sheet --result --status")
        record_image(args.story.resolve(),args.sheet,args.result,args.status=="accepted")
    else:
        out = run_story(args.story.resolve())
        print(out.relative_to(REPO).as_posix())


if __name__ == "__main__":
    main()
