"""Offline tests. Asset contents are local fixtures, never production credentials."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tempfile

import pytest

LOADER = importlib.util.spec_from_file_location("hybrid_motion_tested", Path(__file__).with_name("hybrid_motion.py"))
hm = importlib.util.module_from_spec(LOADER)
LOADER.loader.exec_module(hm)


@pytest.fixture
def shot(tmp_path):
    (tmp_path / "plate.png").write_bytes(b"local-plate-fixture")
    (tmp_path / "element.png").write_bytes(b"local-element-fixture")
    return dict(version=1, frames=90, background="plate.png", layers=[dict(
        id="lever", image="element.png", size=[100, 50], pivot=[10, 25], anchor=[300, 900],
        motions=[dict(type="rotate", start_s=.3, end_s=1.2, easing="smoothstep", **{"from": 0, "to": 90})])])


@pytest.mark.parametrize("kind", sorted(hm.EASINGS))
def test_easing_clamps_and_monotonic(kind):
    values = [hm.ease(i/100, kind) for i in range(-10, 111)]
    assert values[0] == 0 and values[-1] == 1
    assert values == sorted(values)
    assert hm.progress(2, 1, 3, kind) == pytest.approx(hm.ease(.5, kind))


def test_pivot_remains_fixed_and_clockwise():
    assert hm.transformed_point((10, 25), (10, 25), (300, 900), 127) == pytest.approx((300, 900))
    assert hm.transformed_point((20, 25), (10, 25), (300, 900), 90) == pytest.approx((300, 910))
    assert hm.transformed_point((20, 25), (10, 25), (300, 900), 90, (-5, 7)) == pytest.approx((295, 917))


def test_arc_length_path_and_degenerate_points():
    points = [(0, 0), (0, 0), (3, 0), (3, 4)]
    assert hm.path_at(points, 3/7) == pytest.approx((3, 0))
    assert hm.path_at(points, .5) == pytest.approx((3, .5))
    assert hm.path_at(points, -1) == (0, 0)
    assert hm.path_at(points, 2) == (3, 4)
    assert hm.path_at([(2, 3), (2, 3)], .5) == (2, 3)


def test_shake_is_bounded_and_has_no_endpoint_jump():
    for t in (-1, 0, 2, 3):
        assert hm.shake_at(t, 0, 2, (3, 4), 7) == (0, 0)
    for i in range(201):
        x, y = hm.shake_at(i/100, 0, 2, (3, 4), 7)
        assert abs(x) <= 3 and abs(y) <= 4
    assert hm.shake_at(.37, 0, 2, (3, 4), 7) == hm.shake_at(.37, 0, 2, (3, 4), 7)


def test_parse_resolves_relative_paths(shot, tmp_path):
    result = hm.parse_spec(shot, tmp_path)
    assert result["background"] == tmp_path / "plate.png"
    assert result["layers"][0]["image"] == tmp_path / "element.png"
    assert result["frames"] == 90


@pytest.mark.parametrize("mutation", [
    lambda s: s.update(version=True), lambda s: s.update(frames=90.0),
    lambda s: s.update(frames=0), lambda s: s.update(width=1080),
    lambda s: s.update(background="https://example.com/image.png"),
    lambda s: s["layers"][0].update(pivot=[101, 0]),
    lambda s: s["layers"][0].update(anchor=[math.nan, 0]),
    lambda s: s["layers"][0].update(opacity=2),
    lambda s: s["layers"][0].update(glow_radius=100),
    lambda s: s["layers"][0]["motions"][0].update(end_s=.3),
    lambda s: s["layers"][0]["motions"][0].update(end_s=3),
    lambda s: s["layers"][0]["motions"][0].update(easing="spline"),
    lambda s: s["layers"][0]["motions"][0].update(type="morph"),
    lambda s: s["layers"][0]["motions"].append(copy.deepcopy(s["layers"][0]["motions"][0])),
    lambda s: s["layers"].append(copy.deepcopy(s["layers"][0])),
    lambda s: s.update(sound_cues=[dict(file="element.png", time_s=3)]),
])
def test_invalid_spec_fails_closed(shot, tmp_path, mutation):
    mutation(shot)
    with pytest.raises((ValueError, FileNotFoundError)):
        hm.parse_spec(shot, tmp_path)


@pytest.mark.parametrize("kind,fields", [
    ("translate", {"path": [[0, 0], [3, 0], [3, 4]]}),
    ("fade", {"from": 0, "to": 1}), ("glow", {"from": 0, "to": 1}),
    ("shake", {"amplitude": [3, 4], "cycles": 5}),
])
def test_each_primitive_parses(shot, tmp_path, kind, fields):
    shot["layers"][0]["motions"] = [dict(type=kind, start_s=.2, end_s=1.2, **fields)]
    parsed = hm.parse_spec(shot, tmp_path)
    expressions = hm.layer_expressions(parsed["layers"][0])
    assert len(expressions) == 4
    if kind in {"fade", "glow"}:
        assert "T" in expressions[1]


def test_output_boundary():
    assert hm.output_path(hm.OUTPUTS / "clip.mp4").is_relative_to(hm.OUTPUTS)
    for path in (Path("D:/story2video/artifacts/no.mp4"), hm.OUTPUTS / "../../escape.mp4"):
        with pytest.raises(ValueError):
            hm.output_path(path)


def test_cli_bad_binary_binding_never_launches_or_creates_output(tmp_path, monkeypatch):
    binary = tmp_path / "fake-ffmpeg.exe"
    binary.write_bytes(b"not executable")
    lock = tmp_path / "tools.json"
    entry = dict(path=str(binary.resolve()), bytes=binary.stat().st_size, sha256="0"*64)
    lock.write_text(json.dumps(dict(ffmpeg=entry, ffprobe=entry)))
    target = hm.OUTPUTS / "binding-must-not-create" / "clip.mp4"
    monkeypatch.setattr("sys.argv", ["hybrid_motion", "--tools", str(lock), "render", "unused.json", str(target)])
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("Prebinding failure launched child"))
    monkeypatch.setenv("PATH", str(tmp_path))
    with pytest.raises(ValueError, match="binding failed"):
        hm.main()
    assert not target.parent.exists()


def test_legacy_adapter_preserves_groups_and_rejects_gaps(tmp_path):
    for index in (0, 1):
        (tmp_path / f"shot-{index:03d}.mp4").write_bytes(b"fixture")
    (tmp_path / "replacement.mp4").write_bytes(b"fixture")
    data = dict(frames=90, cues=[dict(shot=2, start=0, end=20), dict(shot=2, start=20, end=30), dict(shot=5, start=30, end=90)])
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(data))
    plan = hm.legacy_plan(path, tmp_path, {"1": "replacement.mp4"})
    assert [s["frames"] for s in plan["shots"]] == [30, 60]
    assert plan["shots"][1]["clip"].endswith("replacement.mp4")
    data["cues"][0]["start"] = 1  # Actual reference flow reserves its first frame.
    path.write_text(json.dumps(data))
    assert hm.legacy_plan(path, tmp_path, {})["shots"][0]["frames"] == 30
    with pytest.raises(ValueError):
        hm.legacy_plan(path, tmp_path, {"2": "replacement.mp4"})
    data["cues"][1]["start"] = 21
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="contiguous"):
        hm.legacy_plan(path, tmp_path, {})


@pytest.fixture
def media_renderer(monkeypatch):
    """Exercise parse -> stage -> production filtergraph -> H264 -> decode.

    Only the output dimensions shrink for speed. No mocked tools, expressions,
    encoder or staging, and no helper math supplies the expected measurements.
    Evidence stays in the allowed output tree, including on assertion failure.
    """
    from PIL import Image, ImageDraw
    monkeypatch.setattr(hm, "WIDTH", 256)
    monkeypatch.setattr(hm, "HEIGHT", 256)
    hm.OUTPUTS.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="media-test-", dir=hm.OUTPUTS))
    tools = hm.Tools(hm.HERE / "tools.lock.json")
    Image.new("RGB", (256, 256), "black").save(root / "plate.png")
    for name, size, box in (("dot", (21, 21), (6, 6, 14, 14)),
                            ("arm", (53, 21), (38, 6, 46, 14)),
                            ("pivot", (21, 21), (8, 8, 12, 12))):
        image = Image.new("RGBA", size)
        ImageDraw.Draw(image).rectangle(box, fill="white")
        image.save(root / f"{name}.png")

    def render(layers, frames, samples):
        hm.save(root / "spec.json", dict(version=1, frames=frames, background="plate.png", layers=layers))
        hm.render(root / "spec.json", root / "render.mp4", tools)
        images = {}
        for n in samples:
            path = root / f"frame-{n}.png"
            tools.run("ffmpeg", hm.ffargs() + ["-i", root / "render.mp4", "-vf",
                f"select=eq(n\\,{n})", "-frames:v", 1, path], root)
            with Image.open(path) as image:
                images[n] = image.convert("L")
        return images
    return render


def media_layer(name, motions, anchor=(64, 64), image="dot", **extra):
    return dict(id=name, image=f"{image}.png", size=[53 if image == "arm" else 21, 21],
                pivot=[10, 10], anchor=list(anchor), motions=motions, **extra)


def bright_center(image, box):
    pixels = [(x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2])
              if image.getpixel((x, y)) > 120]
    assert pixels, "Rendered marker disappeared"
    return tuple(sum(p[axis] for p in pixels)/len(pixels) for axis in (0, 1))


def test_rendered_pivot_invariance(media_renderer):
    frames = media_renderer([media_layer("pivot", [dict(type="rotate", start_s=0, end_s=.4,
        **{"from": 0, "to": 360})], image="pivot")], 13, [0, 3, 6, 9, 12])
    for frame in frames.values():
        # Quarter turns preserve the exact marker center, including the 90deg
        # case that moved one pixel with the old even-sized staging canvas.
        assert bright_center(frame, (50, 50, 80, 80)) == pytest.approx((64, 64), abs=.15)


@pytest.mark.parametrize("easing,quarters", [
    ("linear", (.25, .75)), ("smoothstep", (.15625, .84375)),
    ("ease_in", (.0625, .5625)), ("ease_out", (.4375, .9375)),
])
def test_rendered_easing_intermediate(media_renderer, easing, quarters):
    timing = dict(start_s=.2, end_s=1, easing=easing)
    frames = media_renderer([
        media_layer("slide", [dict(type="translate", path=[[0, 0], [128, 0]], **timing)], anchor=(24, 40)),
        media_layer("turn", [dict(type="rotate", **{"from": 0, "to": 90}, **timing)],
                    anchor=(128, 160), image="arm")], 37, [12, 24])
    for n, fraction in zip((12, 24), quarters):
        assert bright_center(frames[n], (0, 20, 200, 60)) == pytest.approx((24+128*fraction, 40), abs=.75)
        angle = math.pi/2*fraction
        assert bright_center(frames[n], (100, 140, 180, 220)) == pytest.approx(
            (128+32*math.cos(angle), 160+32*math.sin(angle)), abs=1)


def test_rendered_unequal_path_segments(media_renderer):
    frames = media_renderer([media_layer("path", [dict(type="translate", start_s=.2, end_s=1,
        path=[[0, 0], [0, 0], [24, 0], [24, 72]])])], 37, [12, 18, 24])
    # 96px total: at 25% the short first segment is complete; 50/75%
    # are 24/48px down the second segment. Equal time per segment fails.
    for n, expected in ((12, (88, 64)), (18, (88, 88)), (24, (88, 112))):
        assert bright_center(frames[n], (40, 40, 120, 140)) == pytest.approx(expected, abs=.75)


def test_rendered_shake_intermediate(media_renderer):
    frames = media_renderer([media_layer("shake", [dict(type="shake", start_s=.2, end_s=1,
        amplitude=[20, 16], cycles=1)])], 37, [0, 6, 12, 18, 24, 30, 36])
    expected = {0: (64, 64), 6: (64, 64), 12: (78.142, 64), 18: (64, 48),
                24: (49.858, 64), 30: (64, 64), 36: (64, 64)}
    for n, center in expected.items():
        # overlay rounds down; sine values infinitesimally below zero can also
        # land one pixel below the nominal integer. A 1px allowance is enough.
        assert bright_center(frames[n], (30, 30, 100, 100)) == pytest.approx(center, abs=1.01)


@pytest.mark.parametrize("kind", ["fade", "glow"])
def test_rendered_opacity_timing(media_renderer, kind):
    frames = media_renderer([media_layer(kind, [dict(type=kind, start_s=.2, end_s=1,
        easing="ease_in", **{"from": .1, "to": .9})], opacity=.8,
        glow_radius=3 if kind == "glow" else 0)], 37, [0, 6, 12, 24, 30, 36])
    for n, opacity in ((0, .08), (6, .08), (12, .12), (24, .44), (30, .72), (36, .72)):
        patch = frames[n].crop((62, 62, 67, 67))
        mean = sum(patch.getdata())/25
        assert mean == pytest.approx(255*opacity, abs=4), (kind, n, mean)
    if kind == "glow":
        # The staged halo is visible outside the original 9px marker and also
        # follows the opacity clock, rather than staying at constant brightness.
        assert frames[30].getpixel((70, 64)) > frames[12].getpixel((70, 64)) + 8
