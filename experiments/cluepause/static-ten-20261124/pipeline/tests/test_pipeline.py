import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("static_storyboard", HERE/"static_storyboard.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


@pytest.fixture
def story(tmp_path):
    for name in ("shots.json", "references.json", "story.md"):
        (tmp_path/name).write_bytes((HERE/"template"/name).read_bytes())
    return tmp_path


def mutate(story, callback, filename="shots.json"):
    data = p.read(story/filename)
    callback(data)
    p.save(story/filename,data)


def test_valid(story):
    assert p.validate(story)[0]["genre"] == "puzzle"


@pytest.mark.parametrize("change,match", [
    (lambda d:d["shots"][0].pop("function"), "function"),
    (lambda d:d["shots"][3].update(function="transition"), "reveal"),
    (lambda d:d["shots"][1].update(framing="wide"), "clue close-up"),
    (lambda d:d["shots"][1].update(function="reaction"), "clue close-up"),
    (lambda d:d["shots"][0].update(required_references=[]), "recurring reference"),
    (lambda d:d["shots"][0].update(required_references=["unknown"]), "Unknown required"),
    (lambda d:d["shots"][1].update(id="shot-01"), "Duplicate shot"),
    (lambda d:d["shots"][0]["source"].update(cell=6), "Cell outside"),
    (lambda d:d["shots"][0]["source"].update(crop=[.8,0,.5,1]), "Crop outside"),
    (lambda d:d["sheets"]["shots"].update(file="../escape.png"), "escapes"),
    (lambda d:d["shots"][0].update(end={"cue":"missing","edge":"end"}), "Unknown audio"),
    (lambda d:d["shots"][0]["camera"].update(zoom=[.5,1]), "minimum"),
    (lambda d:d.update(story_id="../escape"), "does not match"),
])
def test_reject_bad_story(story,change,match):
    mutate(story,change)
    with pytest.raises(ValueError,match=match):
        p.validate(story)


def test_reject_missing_fiction(story):
    (story/"story.md").write_text("No fiction header",encoding="utf-8")
    with pytest.raises(ValueError,match="FICTION"):
        p.validate(story)


def test_reference_registry_reciprocity(story):
    mutate(story,lambda d:d["items"][0].update(appears_in=["missing"]),"references.json")
    with pytest.raises(ValueError,match="unknown shots"):
        p.validate(story)


def test_cell_extraction_geometry():
    sheet = dict(columns=2,rows=3,edge_px=2)
    assert p.cell_box((600,900),sheet,dict(cell=3,crop=[0,0,1,1])) == (302,302,598,598)
    assert p.cell_box((600,900),sheet,dict(cell=0,crop=[.5,0,.5,1])) == (150,2,298,298)
    with pytest.raises(ValueError,match="Empty"):
        p.cell_box((4,6),sheet,dict(cell=0,crop=[0,0,1,1]))


def test_cue_binding_and_frame_quantization(story):
    data,_ = p.validate(story)
    data["shots"][0]["end"] = {"cue":"line","edge":"start"}
    cues = {"line":dict(start=2,end=2.5,reveal=False)}
    assert p.timeline(data,cues)[0]["frames"] == 60
    data["shots"][1]["start"] = 2.1
    with pytest.raises(ValueError,match="contiguous"):
        p.timeline(data,cues)


def test_reveal_audio_guard(story):
    data,_ = p.validate(story)
    with pytest.raises(ValueError,match="before reveal"):
        p.timeline(data,{"answer":dict(start=5,end=5.5,reveal=True)})


@pytest.mark.parametrize("name",["../escape", "C:/private/image.png", "/outside.png", "assets\\image.png", "https://x/image.png"])
def test_local_input_confinement(story,name):
    with pytest.raises(ValueError):
        p.local(story,name)


def test_prompt_injects_every_canonical_reference(story):
    data,refs=p.validate(story)
    payload=p.build_prompt(data,refs,"shots",True)
    for item in refs["items"]:
        assert item["id"] in payload["prompt"]
        assert all(feature in payload["prompt"] for feature in item["invariants"])
        assert f"prompts/references/{item['id']}.png" in payload["reference_images"]
    assert p.build_prompt(data,refs,"reference")["purpose"] == "reference_sheet"
    assert not p.build_prompt(data,refs,"shots")["reference_images"]


def test_image_call_budget_and_status(story,tmp_path,monkeypatch):
    monkeypatch.setattr(p,"OUTPUTS",tmp_path/"outputs")
    p.export_prompts(story,False)
    (story/"result.png").write_bytes(b"synthetic image receipt")
    p.record_image(story,"shots","result.png",False)
    p.record_image(story,"shots","result.png",True)
    rows=p.ledger_rows(p.OUTPUTS/"template")
    assert [r["status"] for r in rows] == ["rejected","accepted"]
    assert all(len(r["prompt_sha256"]) == 64 for r in rows)
    with pytest.raises(ValueError,match="budget exceeded"):
        p.record_image(story,"shots","result.png",True)


def test_output_lock_prevents_collision(tmp_path):
    with p.owned_output(tmp_path):
        with pytest.raises(FileExistsError):
            with p.owned_output(tmp_path):
                pass
    assert not (tmp_path/".running").exists()


def test_cache_environment_is_story_local_and_restored(tmp_path,monkeypatch):
    import os
    monkeypatch.setenv("HF_HOME","original-cache")
    with p.owned_output(tmp_path):
        assert Path(os.environ["HF_HOME"]).is_relative_to(tmp_path)
        assert Path(os.environ["TEMP"]) == tmp_path/"tmp"
    assert os.environ["HF_HOME"] == "original-cache"


def test_reject_nonfinite_json(tmp_path):
    (tmp_path/"bad.json").write_text('{"start":NaN}',encoding="utf-8")
    with pytest.raises(ValueError,match="Non-finite"):
        p.read(tmp_path/"bad.json")


def test_pcm_and_sidecars(tmp_path):
    from array import array
    path=tmp_path/"tone.wav"
    pcm=array("h",[100,-100]*120)
    p.write_pcm(path,pcm)
    assert p.read_pcm(path) == pcm
    cues=[dict(start=.1234,end=.5678,en="A clue.",zh="線索。")]
    assert "00:00:00,123 --> 00:00:00,568" in p.srt(cues,"en")
    assert "線索。" in p.srt(cues,"zh")


def test_camera_is_full_bleed_and_endpoint_based():
    result=p.camera(dict(zoom=[1.015,1.035],**{"from":[0,0],"to":[1,1]}),60)
    assert "on/59" in result and "s=1080x1920:fps=30" in result
    assert "pad" not in result


def test_measured_audio_schedule_and_truncation(story,tmp_path):
    from array import array
    data,_=p.validate(story)
    pcm=array("h",[1200,-1200]*6000)  # Exactly half a second, no TTS dependency.
    p.write_pcm(story/"tone.wav",pcm)
    for line in data["narration"]:
        line["file"]="tone.wav"
    out=tmp_path/"out"
    with p.owned_output(out):
        shots,captions=p.prepare_audio(story,data,out)
        assert captions[0]["start"] == .1 and captions[0]["end"] == .6
        assert captions[1]["start"] == 6 and captions[1]["end"] == 6.5
        assert len(p.read_pcm(out/"mix.wav")) == 8*p.RATE
        assert p.read(out/"timeline.json")["cues"][0]["samples"] == 12000
        data["narration"][1]["not_before"] = 7.8
        with pytest.raises(ValueError,match="outside picture"):
            p.prepare_audio(story,data,out)


def test_sfx_truncation_is_rejected(story,tmp_path):
    from array import array
    data,_=p.validate(story)
    p.write_pcm(story/"tone.wav",array("h",[1200,-1200]*6000))
    for line in data["narration"]:
        line["file"]="tone.wav"
    data["shots"][0]["sfx"]=[dict(file="tone.wav",offset=1.8,gain=1,en="[Sound]",zh="［聲音］")]
    with p.owned_output(tmp_path/"out"):
        with pytest.raises(ValueError,match="crosses"):
            p.prepare_audio(story,data,tmp_path/"out")
