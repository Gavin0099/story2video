"""Offline tests. Asset contents are local fixtures, never production credentials."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess

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
