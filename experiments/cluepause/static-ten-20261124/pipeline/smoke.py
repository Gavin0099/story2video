"""Synthetic full-resolution end-to-end proof; no TTS or ImageGen calls."""
from array import array
import argparse
import copy
import math

import static_storyboard as pipeline


def fixture(folder, story_id="synthetic-smoke"):
    from PIL import Image, ImageDraw
    folder.mkdir(parents=True, exist_ok=True)
    (folder/"assets").mkdir(exist_ok=True)
    data = copy.deepcopy(pipeline.read(pipeline.HERE/"template/shots.json"))
    data["story_id"] = story_id
    # Full 8 seconds covers both exact question boundaries and all narrative functions.
    for name in ("shots", "reference"):
        sheet = Image.new("RGB", (480,1284), "black")
        draw = ImageDraw.Draw(sheet)
        for i, color in enumerate(("#9f3c31", "#3d884d", "#335fa0", "#ad8b3c", "#73488b", "#4a9e9e")):
            x,y = (i%2)*240,(i//2)*428
            draw.rectangle((x+2,y+2,x+237,y+425), fill=color)
        sheet.save(folder/f"assets/{name}.png")
    # Non-speech tones deliberately prove measured PCM timing only.
    for i,line in enumerate(data["narration"]):
        line["file"] = f"assets/tone-{i}.wav"
        pcm = array("h", (round(3500*math.sin(2*math.pi*(440+i*220)*n/pipeline.RATE))
                           for n in range(pipeline.RATE//2)))
        pipeline.write_pcm(folder/line["file"],pcm)
    sound = array("h", (round(1800*math.sin(2*math.pi*880*n/pipeline.RATE)) for n in range(2400)))
    pipeline.write_pcm(folder/"assets/click.wav",sound)
    data["shots"][1]["sfx"] = [dict(file="assets/click.wav",offset=.2,gain=.4,en="[Click]",zh="［喀聲］")]
    pipeline.save(folder/"shots.json",data)
    pipeline.save(folder/"references.json",pipeline.read(pipeline.HERE/"template/references.json"))
    (folder/"story.md").write_text((pipeline.HERE/"template/story.md").read_text(encoding="utf-8"),encoding="utf-8")
    return folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id",default="synthetic-smoke")
    args = parser.parse_args()
    # Validate the id before creating anything using it.
    import re
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}",args.id):
        parser.error("Use a portable story id")
    output = pipeline.output_for(args.id)
    story = fixture(output/"input",args.id)
    pipeline.export_prompts(story,True)
    pipeline.run_story(story)
    # Independent decoded-pixel checks for exact question boundaries and cell isolation.
    from PIL import Image
    def pixels(image):
        return image.get_flattened_data() if hasattr(image,"get_flattened_data") else image.getdata()
    tools = pipeline.Tools(output)
    samples = [29,30,104,105]
    expr = "+".join(f"eq(n\\,{n})" for n in samples)
    tools.run("ffmpeg",pipeline.FF+["-i",output/f"{args.id}.mp4","-vf",f"select='{expr}'",
              "-fps_mode","vfr",output/"qa/question-%02d.png"])
    whites = []
    for path in sorted((output/"qa").glob("question-*.png")):
        with Image.open(path) as image:
            whites.append(sum(min(pixel)>210 for pixel in pixels(image.convert("RGB").crop((0,100,1080,350)))))
    assert whites[0] < 100 and whites[1] > 1000 and whites[2] > 1000 and whites[3] < 100
    with Image.open(output/"silent-storyboard.jpg") as image:
        assert sum(min(pixel)>210 for pixel in pixels(image.convert("RGB"))) == 0
    pipeline.save(output/"qa/smoke-assertions.json",dict(question_sample_frames=samples,
                  bright_text_pixels=whites,question_interval="[1.0,3.5)",silent_storyboard_has_no_question=True))
    print(f"PASS artifacts/static-ten-20261124/{args.id}/qa/report.json")
