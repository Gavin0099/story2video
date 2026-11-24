"""Read frozen masters; extract ALL frames, never encode or modify a cut.

Run from the repository root: python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/temporal_qa.py
Requires Pillow. Evidence goes exclusively into ignored artifacts/.
"""
from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
import wave

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[4]
PILOT = REPO / "experiments/cluepause/genre-pilot-20261124"
MEDIA = REPO / "artifacts/genre-pilot-20261124/h01-v2.1"
OUT = REPO / "artifacts/genre-pilot-20261124/h01-viewer-gate"
FROZEN = {
    "A": "fbe60ff93d13cd8f8fac105b7c0da78445aca2fab3ef76d5891f7ab7d3402412",
    "B": "2d636b0304c4e3744b32e424a40ee940bf59f4136f96f0f10ea4b25b369f11fd",
    "en": "c36c869765801e49088a75346d2bdc91b2b4b32d0b51e1d65ab3a15c5833ff2a",
    "zh-Hant": "ab0a17dc4884f6ab2b1533b855d35059d09e6a85626626c4fac7e555ca792707",
    "script": "83df72c03352d74ceb6977bcc665f0d6a715e37fae0ad10b81f6e1e8720c7bce",
    "mix": "d1fe9f6dd57641ab143951d22286303b51e7fb941711e94770f18edee8177422",
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(exe, args):
    # No shell; executables are digest checked against the existing lock.
    result = subprocess.run([str(exe), *map(str, args)], cwd=REPO,
                            capture_output=True, check=True)
    return result.stdout


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def correlation(a, b):
    assert len(a) == len(b) and len(a) > 0
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    aa = sum((x - ma) ** 2 for x in a)
    bb = sum((x - mb) ** 2 for x in b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(aa * bb)


def wav(path):
    with wave.open(str(path), "rb") as stream:
        assert stream.getsampwidth() == 2 and stream.getnchannels() == 1
        rate = stream.getframerate()
        samples = array.array("h", stream.readframes(stream.getnframes()))
    return rate, samples


def stamp(s):
    h, m, rest = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest.replace(",", "."))


def main(revision=False):
    global OUT
    cut_media, basename, expected = MEDIA, "h01-v2.1", FROZEN
    if revision:
        cut_media = MEDIA.parent / "h01-v2.1-r1"
        basename = "h01-v2.1-r1"
        OUT = cut_media / "temporal-qa"
        light = read(cut_media / "light-measurements.json")
        expected = {**FROZEN, **{cut: light["cuts"][cut]["sha256"] for cut in ("A", "B")}}
        for cut in ("A", "B"):
            assert digest(MEDIA / cut / "h01-v2.1.mp4") == FROZEN[cut]
    OUT.mkdir(parents=True, exist_ok=True)
    lock = read(PILOT / "motion/tools.lock.json")
    tools = {}
    for name, entry in lock.items():
        path = Path(entry["path"])
        assert path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"]
        tools[name] = path
    ffmpeg, ffprobe = tools["ffmpeg"], tools["ffprobe"]
    timeline = read(MEDIA / "shared/timeline.json")
    shots = read(MEDIA / "shared/shots.json")
    assert digest(MEDIA / "shared/urban_horror-v2.1.md") == FROZEN["script"]
    assert digest(MEDIA / "shared/mix.wav") == FROZEN["mix"]
    summary = {"tool_hashes": {k: v["sha256"] for k, v in lock.items()},
               "extraction": "Every decoded frame, 30 fps; indices zero based; intervals half open",
               "cuts": {}, "plates": {},
               "source_script_sha256": FROZEN["script"], "source_mix_sha256": FROZEN["mix"]}
    source_rate, tail = wav(MEDIA / "shared/nia-saved-two-words.wav")
    _, full = wav(MEDIA / "shared/nia-full-reply.wav")
    assert full[-len(tail):] == tail
    _, cough = wav(MEDIA / "shared/cough.wav")
    for cut in ("A", "B"):
        clip = cut_media / cut / f"{basename}.mp4"
        initial_hash = digest(clip)
        assert initial_hash == expected[cut], "Selected master differs; do not proceed"
        dest = OUT / cut
        frames = dest / "frames"
        pages = dest / "sequence"
        frames.mkdir(parents=True, exist_ok=True)
        pages.mkdir(parents=True, exist_ok=True)
        probe = json.loads(run(ffprobe, ["-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", clip]))
        video = next(s for s in probe["streams"] if s["codec_type"] == "video")
        audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
        assert int(video["nb_read_frames"]) == 1170 and video["r_frame_rate"] == "30/1"
        assert (video["width"], video["height"]) == (1080, 1920)
        pts = json.loads(run(ffprobe, ["-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", clip]))["frames"]
        assert len(pts) == 1170
        assert all(abs(float(p["best_effort_timestamp_time"]) - i/30) < 0.000002 for i, p in enumerate(pts))
        run(ffmpeg, ["-nostdin", "-v", "error", "-y", "-i", clip, "-map", "0:v:0", "-vf", "scale=360:640", "-fps_mode", "passthrough", "-start_number", "0", "-q:v", "2", frames / "%04d.jpg"])
        assert len(list(frames.glob("*.jpg"))) == 1170
        # One second per page, row-major temporal order. These are exhaustive
        # sequence pages, not sparse shot representatives. Inspect each in order.
        for second in range(39):
            page = Image.new("RGB", (1800, 1035), "#151515")
            draw = ImageDraw.Draw(page)
            for j in range(30):
                n = second * 30 + j
                with Image.open(frames / f"{n:04d}.jpg") as frame:
                    page.paste(frame.resize((180, 320)), ((j % 10)*180, (j // 10)*345))
                draw.text(((j % 10)*180+3, (j // 10)*345+322), f"{cut} {n/30:09.6f} f{n}", fill="white")
            page.save(pages / f"{second:02d}.jpg", quality=90)
        audio_hash = run(ffmpeg, ["-nostdin", "-v", "error", "-i", clip, "-map", "0:a:0", "-c:a", "copy", "-f", "hash", "-hash", "sha256", "-"]).decode().strip()
        pcm = run(ffmpeg, ["-nostdin", "-v", "error", "-i", clip, "-map", "0:a:0", "-ac", "1", "-ar", source_rate, "-c:a", "pcm_s16le", "-f", "s16le", "-"])
        decoded = array.array("h", pcm)
        checks = []
        voice_checks = []
        for event in timeline["events"]:
            source = MEDIA / "shared/voice" / (event["key"] + ".wav")
            assert digest(source) == event["sha256"]
            rate, samples = wav(source)
            assert rate == source_rate and len(samples) == event["samples"]
            assert abs(event["end"] - event["start"] - len(samples)/rate) < 1e-8
            offset = round(event["start"] * rate)
            corr = correlation(decoded[offset:offset+len(samples)], samples)
            assert corr > .97
            voice_checks.append({"event":event["key"], "start_s":event["start"],
                                 "end_s":event["end"], "correlation":corr})
        for key, at, source in [("mother_cough",17.2,cough), ("device_cough",18.0,cough), ("refusal_tail",28.808375,tail), ("saved_playback",29.517875,tail), ("final_playback",36.1,tail)]:
            offset = round(at * source_rate)
            corr = correlation(decoded[offset:offset+len(source)], source)
            assert corr > .97
            checks.append({"event":key, "at_s":at, "decoded_master_source_correlation":corr})
        captions = {}
        for lang, column in [("en", "en"), ("zh-Hant", "zh")]:
            path = cut_media / cut / f"{basename}.{lang}.srt"
            assert digest(path) == FROZEN[lang], "Frozen captions differ"
            blocks = path.read_text(encoding="utf-8-sig").strip().split("\n\n")
            assert len(blocks) == len(timeline["cues"]) == 20
            max_error = 0
            previous_end = 0
            for block, cue in zip(blocks, timeline["cues"]):
                lines = block.splitlines()
                start, end = map(stamp, lines[1].split(" --> "))
                assert start >= previous_end and end > start and end <= 39
                assert " ".join(lines[2:]) == cue[column]
                max_error = max(max_error, abs(start-cue["start"]), abs(end-cue["end"]))
                previous_end = end
            assert max_error <= .000501
            captions[lang] = {"path": path.relative_to(REPO).as_posix(), "sha256": digest(path), "cues":20, "max_boundary_error_s":max_error}
        # Original-size, lossless boundary frames for plot-prop confirmation.
        anchors = sorted(set([0,11,20,21,104,105,209,210,239,240,329,330,359,360,419,420,449,450,479,480,516,537,539,540,599,600,647,648,659,660,719,720,779,780,839,840,848,849,862,863,880,881,885,886,903,904,914,929,930,1049,1050,1109,1110,1169]))
        anchor_dir = dest / "anchors"
        anchor_dir.mkdir(exist_ok=True)
        select = "+".join(f"eq(n\\,{n})" for n in anchors)
        run(ffmpeg, ["-nostdin", "-v", "error", "-y", "-i", clip, "-vf", f"select={select}", "-fps_mode", "vfr", "-start_number", "0", anchor_dir / "%03d.png"])
        save(dest / "anchors.json", [{"file": f"anchors/{i:03d}.png", "frame": n, "seconds":n/30} for i,n in enumerate(anchors)])
        assert digest(clip) == initial_hash
        summary["cuts"][cut] = {"path":clip.relative_to(REPO).as_posix(), "sha256":initial_hash,
            "duration":probe["format"]["duration"], "video": {k:video.get(k) for k in ("codec_name","pix_fmt","width","height","r_frame_rate","avg_frame_rate","nb_read_frames")},
            "audio":{k:audio.get(k) for k in ("codec_name","sample_rate","channels","channel_layout","duration","bit_rate")},
            "stream_types":[s["codec_type"] for s in probe["streams"]], "audio_packet_hash":audio_hash,
            "captions":captions, "decoded_audio_checks":checks, "extracted_frames":1170, "sequence_pages":39}
        summary["cuts"][cut]["voice_event_checks"] = voice_checks
        save(dest / "frame-index.json", [{"frame":i,"seconds":i/30,"file":f"frames/{i:04d}.jpg","shot":next(s["name"] for s in shots if round(s["start"]*30)<=i<round(s["end"]*30))} for i in range(1170)])
        print(f"{cut}: 1170 frames, 39 ordered pages, audio/caption alignment PASS", flush=True)
    assert summary["cuts"]["A"]["audio_packet_hash"] == summary["cuts"]["B"]["audio_packet_hash"]
    for path in sorted((MEDIA / "shared/plates").glob("*.png")):
        summary["plates"][path.relative_to(REPO).as_posix()] = digest(path)
    # Existing command logs contain argv and returncode but no command clocks.
    logs = []
    for path in sorted(MEDIA.rglob("commands.jsonl")):
        entries = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        keys = sorted(set().union(*(e.keys() for e in entries)))
        logs.append({"path":path.relative_to(REPO).as_posix(), "entries":len(entries), "keys":keys})
    summary["existing_command_logs"] = logs
    save(OUT / "measurements.json", summary)
    print("Selected cuts unchanged; measurements.json written; no render invoked.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--r1", action="store_true", help="QA light-only r1 cuts in a new evidence folder")
    main(revision=parser.parse_args().r1)
