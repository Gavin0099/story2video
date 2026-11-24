"""Real-media checks with local fixtures plus decoded demo evidence; no services."""
from pathlib import Path
import argparse
import json
import math
import os
import struct
import tempfile
import wave

from PIL import Image, ImageChops, ImageDraw
import hybrid_motion as hm


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--tools", type=Path, default=hm.HERE / "tools.lock.json")
    cli.add_argument("--demo-root", type=Path, default=hm.OUTPUTS)
    cli.add_argument("--skip-demos", action="store_true", help="Run portable local media fixtures only")
    cli.add_argument("--reference-media", type=Path,
                     help="Optional read-only legacy media directory containing timeline.json and cuts/")
    args = cli.parse_args()
    tools = hm.Tools(args.tools)
    root = hm.output_path(args.demo_root)
    root.mkdir(parents=True, exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix="verification-", dir=root))
    plate = Image.new("RGB", (1080, 1920), (65, 45, 30))
    plate.save(fixture / "plate.png")
    element = Image.new("RGBA", (50, 20))
    ImageDraw.Draw(element).rectangle((0, 2, 49, 17), fill=(20, 240, 245, 255))
    element.save(fixture / "element.png")
    spec = dict(version=1, frames=30, background="plate.png", layers=[dict(
        id="all-primitives", image="element.png", size=[50, 20], pivot=[5, 10], anchor=[100, 200], motions=[
            dict(type="rotate", start_s=.1, end_s=.8, **{"from": 0, "to": 90}),
            dict(type="translate", start_s=.1, end_s=.8, path=[[0, 0], [100, 0], [100, 100]]),
            dict(type="fade", start_s=.1, end_s=.8, **{"from": 0, "to": 1}),
            dict(type="shake", start_s=.1, end_s=.8, amplitude=[3, 2], cycles=3),
        ])])
    hm.save(fixture / "all.json", spec)
    # Exact outer renderer with hostile PATH: only pinned absolute binaries can run.
    old_path = os.environ.get("PATH")
    os.environ["PATH"] = str(fixture)
    try:
        evidence = hm.render(fixture / "all.json", fixture / "first.mp4", tools)
        hm.render(fixture / "all.json", fixture / "second.mp4", tools)
    finally:
        if old_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = old_path
    assert hm.digest(fixture / "first.mp4") == hm.digest(fixture / "second.mp4"), "Non-deterministic encode"
    with Image.open(evidence / "start.png") as image:
        r, g, b = image.getpixel((100, 200))
        assert max(abs(a-b) for a, b in zip((r, g, b), (65, 45, 30))) <= 5, "Fade start not hidden"
    with Image.open(evidence / "end.png") as image:
        r, g, b = image.getpixel((200, 330))
        assert g > 200 and b > 200 and r < 70, "Rotation/path endpoint wrong"
        r, g, b = image.getpixel((100, 200))
        assert g < 70, "Stale element remained at original anchor"
    # Original-mix and unchanged selectable-caption splice fixture.
    rate, seconds = 48000, 2
    samples = [int(1600*math.sin(2*math.pi*440*n/rate)) for n in range(rate*seconds)]
    with wave.open(str(fixture / "mix.wav"), "wb") as stream:
        stream.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        stream.writeframes(struct.pack("<"+"h"*len(samples), *samples))
    for lang, text in (("en", "Local fixture."), ("zh-Hant", "本機測試。")):
        (fixture / f"captions.{lang}.srt").write_text(f"1\n00:00:00,100 --> 00:00:01,900\n{text}\n", encoding="utf-8")
    plan = dict(version=1, shots=[dict(clip="first.mp4", frames=30), dict(clip="second.mp4", frames=30)],
                audio="mix.wav", sidecars={lang: f"captions.{lang}.srt" for lang in ("en", "zh-Hant")})
    hm.save(fixture / "timeline.json", plan)
    joined = hm.splice(fixture / "timeline.json", fixture / "joined.mp4", tools)
    for lang in ("en", "zh-Hant"):
        assert hm.digest(fixture / f"captions.{lang}.srt") == hm.digest(fixture / f"joined.{lang}.srt")
    # Different replacement length must fail, never pad/drop a clue or publish a master.
    plan["shots"][1]["frames"] = 31
    hm.save(fixture / "wrong-length.json", plan)
    try:
        hm.splice(fixture / "wrong-length.json", fixture / "must-not-exist.mp4", tools)
    except ValueError as error:
        assert "count mismatch" in str(error)
    else:
        raise AssertionError("Mismatched shot length was accepted")
    assert not (fixture / "must-not-exist.mp4").exists()
    # Portable legacy compatibility fixture: first spoken cue starts at frame 1,
    # adjacent cues group, a non-adjacent reuse is a separate shot occurrence.
    for index, clip in enumerate(("first.mp4", "second.mp4", "first.mp4")):
        (fixture / f"shot-{index:03d}.mp4").write_bytes((fixture / clip).read_bytes())
    hm.save(fixture / "legacy.json", dict(fps=30, frames=90, cues=[
        dict(shot=7, start=1, end=15), dict(shot=7, start=15, end=30),
        dict(shot=9, start=30, end=60), dict(shot=7, start=60, end=90)]))
    legacy = hm.legacy_plan(fixture / "legacy.json", fixture, {"1": "second.mp4"})
    assert [s["frames"] for s in legacy["shots"]] == [30, 30, 30]
    assert Path(legacy["shots"][1]["clip"]) == fixture / "second.mp4"
    hm.save(fixture / "local-legacy-plan.json", legacy)
    reference_check = "SKIPPED; optional --reference-media not supplied"
    if args.reference_media:
        reference = args.reference_media.resolve(strict=True)
        legacy = hm.legacy_plan(reference / "timeline.json", reference / "cuts", {})
        expected = hm.read(reference / "timeline.json")["frames"]
        assert sum(s["frames"] for s in legacy["shots"]) == expected
        hm.save(fixture / "reference-plan.json", legacy)
        reference_check = dict(media=str(reference), frames=expected, result="PASS")
    demos, folders = {}, {}
    names = () if args.skip_demos else ("handle", "intercom", "latch")
    for name in names:
        clip_hash = hm.digest(root / (name+".mp4"))
        folders[name] = next(p for p in root.glob(name+"-*") if (p / "receipt.json").exists()
                             and hm.read(p / "receipt.json")["sha256"] == clip_hash)
        hm.inspect(tools, root / (name+".mp4"), fixture, 90)
    sample_at = {"handle": .675, "intercom": .8, "latch": 1.9}
    sheet = Image.new("RGB", (1080, 2560))
    for row, name in enumerate(names):
        directory = folders[name]
        frame = round(sample_at[name]*30)
        tools.run("ffmpeg", hm.ffargs()+["-i", root / (name+".mp4"), "-vf", f"select=eq(n\\,{frame})", "-frames:v", 1, directory / "action-middle.png"], directory)
        with Image.open(directory / "start.png") as first, Image.open(directory / "end.png") as last:
            assert first.size == last.size == (1080, 1920)
            assert ImageChops.difference(first, last).getbbox(), "No visible motion"
            # A letterbox would leave an entire outer row/column uniformly black.
            for image in (first, last):
                for box in ((0, 0, 1080, 1), (0, 1919, 1080, 1920), (0, 0, 1, 1920), (1079, 0, 1080, 1920)):
                    assert max(image.crop(box).convert("L").getextrema()) > 15
        for col, label in enumerate(("start", "action-middle", "end")):
            with Image.open(directory / (label+".png")) as image:
                sheet.paste(image.resize((360, 640)), (col*360, row*640))
        demos[name] = dict(frames=90, duration_s=3, evidence=str(directory), action_sample_frame=frame,
                           sha256=hm.digest(root / (name+".mp4")), edge_row_column_check="PASS",
                           visual_review="PENDING; machine check is not alignment/text review")
    if names:
        sheet.crop((0, 0, 1080, 1920)).save(root / "frame-check-action.jpg", quality=95)
    result = dict(demos=demos, fixture=dict(directory=str(fixture),
        repeat_sha256=hm.digest(fixture / "first.mp4"), deterministic_repeat="identical MP4 SHA-256",
        combined_rotate_translate_fade_shake="PASS; decoded endpoint pixel and hidden-start pixel",
        hostile_path="PASS; pinned binaries and allowlisted child environment",
        narration_sidecar_splice="PASS; 60 frames, original mix reencoded, SRT bytes identical",
        wrong_length="REJECTED before master output", local_legacy_adapter="PASS; 90 frames, first cue starts at frame 1, repeated/grouped shot IDs",
        external_legacy_adapter=reference_check),
        engineering_acceptance="PASS for checks above; visual review separately recorded",
        market_acceptance="NOT_TESTED")
    hm.save(fixture / "verification.json", result)
    hm.save(root / "verification.json", result)
    print("PASS: deterministic bytes, compiled primitives, hostile PATH, splice audio/SRT, wrong-length rejection, local legacy adapter"
          + (", decoded demo edges" if names else "") + f"; evidence: {fixture}")


if __name__ == "__main__":
    main()
