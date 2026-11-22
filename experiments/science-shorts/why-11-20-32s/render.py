"""Build local review cuts for WhyNest Lab #11–20 from the frozen production inputs."""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "artifacts/science-shorts/public-20-20261122"
OUTPUT = ROOT / "artifacts/science-shorts/why-11-20-32s"
FF = ROOT / "artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin/ffmpeg.exe"
FF_HASH = "ed8f66cb877087a96f5bbb40a2944f0e764f2ad8870d5cb647360d912e62bc07"
FFPROBE = FF.with_name("ffprobe.exe")
FPS, RATE, W, H = 30, 24000, 720, 1280
COLORS = {
    11: ("#dc9160", "#95ddd4"), 12: ("#edbc7d", "#7bcfea"), 13: ("#f2a186", "#afd5c2"),
    14: ("#e8b582", "#8debd9"), 15: ("#f19d83", "#9cdcf6"), 16: ("#f2b575", "#9ed7df"),
    17: ("#f4ac72", "#9ddfde"), 18: ("#f6a581", "#9bdce7"), 19: ("#e6a68c", "#9fdbed"),
    20: ("#e1c79d", "#88e0ed"),
}
SCENE_ORDER = {
    11: (0, 1, 2, 3, 4, 5, 6), 12: (0, 1, 2, 3, 4, 5, 6),
    13: (0, 2, 3, 4, 5, 6, 7), 14: (0, 1, 2, 3, 4, 5, 6, 7),
    15: (0, 1, 2, 3, 4, 6, 7), 16: (0, 1, 3, 4, 5, 6, 7),
    17: (0, 1, 2, 3, 4, 5, 7), 18: (0, 1, 2, 3, 5, 6, 7),
    19: (0, 1, 2, 3, 4, 5, 7), 20: (0, 1, 2, 3, 4, 6, 7),
}
QUESTIONS = {
    11: "Did it leak?", 12: "Same push. Why turn more?", 13: "Which dries first?",
    14: "Why won't it lift?", 15: "Why does the book stop?", 16: "Why leave a gap?",
    17: "Same string. Higher note?", 18: "Why does timing matter?",
    19: "Why do you lean forward?", 20: "Why does water climb?",
}
RESULTS = {
    11: "Water from the air", 12: "Same push. More torque.", 13: "Moving air carries vapor away",
    14: "Break the seal", 15: "A push, a slide, a stop", 16: "The deck needs room to move",
    17: "Tighter string. Faster cycles.", 18: "Push with the swing's motion",
    19: "The belt helps you slow down", 20: "Water follows connected pores",
}
HOT = "#efad73"
PAPER = "#f7ead7"
TYPE = "#dbdddb"
FONT_ROOT = Path("C:/Windows/Fonts")
TITLE = ImageFont.truetype(str(FONT_ROOT / "georgiab.ttf"), 54)
MODEL = ImageFont.truetype(str(FONT_ROOT / "bahnschrift.ttf"), 23)
SMALL = ImageFont.truetype(str(FONT_ROOT / "bahnschrift.ttf"), 19)
ZH = ImageFont.truetype(str(FONT_ROOT / "msjhbd.ttc"), 30)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_frozen(path, expected):
    if digest(path) != expected.lower():
        raise RuntimeError(f"Frozen input mismatch: {path.name}")


def frozen(id):
    source = OLD / str(id)
    inputs = read(source / "inputs.json")
    timeline = read(source / "timeline.json")
    receipt = read(source / "encoded-review.json")
    release = read(source / "release-package.json")
    codes = inputs["scores"]
    if receipt["status"] != "PASS" or len(codes) != 2 or min(codes) < 85 or codes != release["scores"]:
        raise RuntimeError(f"Missing original approval: {id}")
    assert_frozen(source / "scene-source.py", inputs["scenes_sha256"])
    assert_frozen(source / "narration.wav", timeline["audio_sha256"])
    assert_frozen(source / "master.mp4", receipt["mp4_sha256"])
    for name in ("opening-art.png", "timeline.json"):
        record = next((x for x in inputs["inputs"] if Path(x["path"]).name == name), None)
        if record:
            assert_frozen(source / name, record["sha256"])
    spec = importlib.util.spec_from_file_location(f"scene_{id}", source / "scene-source.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return source, module, timeline["cues"], release, receipt


def stamps(frame):
    ms = round(frame * 1000 / FPS)
    seconds, part = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"00:{minutes:02}:{seconds:02},{part:03}"


def synth_notes(signal):
    # Demonstration tones only. Frequency is higher for the tighter string.
    for start, hz in ((.10, 196.0), (.48, 293.66)):
        at = round(start * RATE)
        tt = np.arange(round(.40 * RATE)) / RATE
        env = np.minimum(1, tt / .007) * np.exp(-7.8 * tt)
        note = sum(np.sin(2 * np.pi * hz * harmonic * tt) / harmonic**1.5 for harmonic in (1, 2, 3))
        signal[at:at + tt.size] += .073 * note * env


def audio_plan(id, source, timeline, out):
    order = SCENE_ORDER[id]
    frame_total = sum(timeline[k]["end"] - timeline[k]["start"] for k in order)
    tempo = min(1.15, max(1.02, frame_total / FPS / 35.5))
    with wave.open(str(source / "narration.wav"), "rb") as old:
        assert (old.getnchannels(), old.getsampwidth(), old.getframerate()) == (1, 2, RATE)
        old_pcm = old.readframes(old.getnframes())
    bytes_per_frame = RATE // FPS * 2
    audio = [bytes(bytes_per_frame * (27 if id == 17 else 6))]
    position = len(audio[0]) // bytes_per_frame
    records = []
    for k in order:
        cue = timeline[k]
        section = old_pcm[cue["start"]*bytes_per_frame:cue["speech_end"]*bytes_per_frame]
        adjusted = subprocess.run(
            [str(FF), "-hide_banner", "-v", "error", "-f", "s16le", "-ar", str(RATE), "-ac", "1",
             "-i", "pipe:0", "-af", f"atempo={tempo:.6f}", "-f", "s16le", "pipe:1"],
            input=section, stdout=subprocess.PIPE, check=True,
        ).stdout
        exact = math.ceil(len(adjusted) / bytes_per_frame)
        gap = 32 if k == order[-1] else 7
        next_position = position + exact + gap
        audio.append(adjusted + bytes((exact + gap)*bytes_per_frame - len(adjusted)))
        records.append({**cue, "original_cue": k, "start": position, "speech_end": position+exact, "end": next_position})
        position = next_position
    if not 30 <= position/FPS <= 41:
        raise ValueError(f"{id} duration outside the preview target: {position / FPS:.2f}")
    signal = np.frombuffer(b"".join(audio), dtype="<i2").astype(np.float32) / 32768
    if id == 17:
        synth_notes(signal)
    dest = out / "audio.wav"
    with wave.open(str(dest), "wb") as file:
        file.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        file.writeframes(np.int16(np.clip(signal, -.999, .999)*32767).tobytes())
    for code, key in (("en", "en"), ("zh-Hant", "zh")):
        captions = []
        for i, cue in enumerate(records, 1):
            text = cue[key]
            if code == "zh-Hant":
                text = "\n".join(wrap_zh(text, 560))
            captions.append(f"{i}\n{stamps(cue['start'])} --> {stamps(cue['end'])}\n{text}")
        (out / f"{code}.srt").write_text("\n\n".join(captions) + "\n", encoding="utf-8")
    save(out / "timing.json", {"tempo": tempo, "cues": records})
    return dest, records


def ease(p):
    p = max(0, min(1, p))
    return p*p*(3-2*p)


def photo_context(illustration, id):
    # Keep both compared objects in view even when the generated base plate is square.
    photo = ImageOps.fit(illustration, (W, 550), Image.Resampling.LANCZOS, centering=(.5,.60))
    if id == 13:
        # Place the billowing shirt above the moving-air side of the diagram.
        photo = ImageOps.mirror(photo)
    base = Image.new("RGB", (W, H), "#10202b")
    base.paste(photo, (0,0))
    return blend_gradient(base, 198, 529, "#10202b")


def blend_gradient(image, start, end, color):
    row = Image.new("L", (1, H))
    row.putdata([round(255 * ease((y-start)/(end-start))) for y in range(H)])
    return Image.composite(Image.new("RGB", (W, H), color), image, row.resize((W, H)))


def studio_base(id):
    a, b = COLORS[id]
    blur = Image.new("RGB", (W, H), "#101c27")
    d = ImageDraw.Draw(blur)
    d.ellipse((-590,-115,615,980), fill=ImageColor(a, 0.21))
    d.ellipse((278,372,1096,1399), fill=ImageColor(b, 0.16))
    return blur.filter(ImageFilter.GaussianBlur(162))


def ImageColor(color, strength):
    values = [int(color[p:p+2],16) for p in (1,3,5)]
    return tuple(round(c * strength) for c in values)


def title(draw, text, color=PAPER, y=202):
    words = text.split()
    chunks = [""]
    for word in words:
        trial = " ".join(filter(None, (chunks[-1], word)))
        if TITLE.getlength(trial) > 598 and chunks[-1]:
            chunks.append(word)
        else:
            chunks[-1] = trial
    for i, chunk in enumerate(chunks):
        draw.text((55,y+i*62), chunk, font=TITLE, fill=color, anchor="lt")


def wrap_zh(text, limit):
    rows = [""]
    for ch in text:
        if ZH.getlength(rows[-1] + ch) > limit and ch not in "。，！？；、":
            rows.append("")
        rows[-1] += ch
    if any(ZH.getlength(row) > 602 for row in rows):
        raise ValueError("Subtitle exceeded the mobile safe width")
    return rows


def caption(draw, text):
    rows = wrap_zh(text, 560)
    y = 1160 - len(rows)*39
    draw.rounded_rectangle((45,y-11,675,1168), radius=15, fill="#08121c")
    for index, row in enumerate(rows):
        draw.text((360,y+index*39), row, font=ZH, fill="#f4f5f2", anchor="mt")



def macro_art(illustration, id):
    picture = ImageOps.fit(illustration, (W,H), Image.Resampling.LANCZOS)
    if id == 11:
        # Tame the existing fine beads to make the large clear drops legible on a phone.
        return picture.filter(ImageFilter.SMOOTH), None
    if id == 20:
        values = np.array(picture, dtype=np.float32)
        yy, xx = np.mgrid[:H, :W]
        r,g,b = values.transpose(2,0,1)
        colored = np.clip(np.minimum(b-r-18,g-r-10)/22,0,1)
        colored *= (yy > 430)&(yy < 855)&(xx>104)&(xx<612)
        made_dry = np.clip(np.stack((b*1.03+29,b*.95+22,b*.87+16),axis=-1),0,255)
        return picture, (made_dry, values, colored, yy, xx)
    return None, None


def draw_macro(photo, macro, id, seconds):
    if id == 11:
        image = photo.copy()
        draw = ImageDraw.Draw(image, "RGBA")
        phase = ease((seconds-.09)/1.62)
        for index,(x,y,r) in enumerate(((107,546,15),(121,668,19),(579,567,13),(630,740,18))):
            power = ease((phase - index*.09)/.71)
            if power <= 0:
                continue
            center_y = y + 54*ease((seconds-.8-index*.10)/1.55)
            radius = 2+r*power
            draw.ellipse((x-radius,center_y-radius*1.25,x+radius,center_y+radius*1.23),
                         fill=(21,14,10,93),outline=(236,238,220,123),width=2)
            draw.arc((x-radius+2,center_y-radius*1.21,x+radius-2,center_y+radius*1.15),
                     207,300,fill=(255,242,214,224),width=3)
            draw.ellipse((x-radius*.65,center_y-radius*.74,x-radius*.25,center_y-radius*.45),
                         fill=(255,238,188,184))
        return image
    dry, wet, mask, yy, xx = macro
    height = 860-425*ease(seconds/1.66)
    edge = height + 20*np.sin(xx/54) + 11*np.sin(xx/12)
    opacity = mask*np.clip((edge-yy)/18,0,1)
    repaint = dry*opacity[:,:,None]+wet*(1-opacity[:,:,None])
    return Image.fromarray(np.uint8(repaint))


def hook_scene(id, k, p):
    if id == 11:
        return 0, .18 + .82 * ease(p*1.9)
    if id == 12:
        return 4, min(1, .10+p*1.78)
    if id == 13:
        return 5, min(1, .04+p*1.48)
    if id == 14:
        return (0, p) if p < .53 else (6, .39+.61*ease((p-.53)/.34))
    if id == 15:
        return 0, min(5, .12 + p * 7.5)
    if id == 16:
        return 4, .06+.94*ease(p*2.0)
    if id == 17:
        return 4, min(1, .015+p*1.48)
    if id == 18:
        return 0, .06+.94*ease(p*1.04)
    if id == 19:
        return 2, .08+.92*ease(p*1.69)
    if id == 20:
        return 0, .04+.96*ease(p*1.59)
    return k,p


END_SCENE = {11:5, 12:4, 13:5, 14:6, 15:0, 16:7, 17:6, 18:0, 19:7, 20:0}


def hero_model(im, diagram, id, k, prog, mode):
    layer = Image.new("RGBA", (W,H))
    ink = ImageDraw.Draw(layer)
    diagram(ink, k, prog)
    # Moving air, braces and explanatory labels stay in the model safe area.
    cropped = layer.crop((17, 345, 704, 1050))
    if mode in ("opening", "return"):
        x,y = 27, 374
        area = (666, 681)
    else:
        x,y = 30, 352
        area = (660, 682)
    cropped = cropped.resize(area, Image.Resampling.BICUBIC)
    im.paste(cropped, (x,y), cropped)
    if mode == "opening" and id == 14 and k == 0:
        # Mark the attempted movement, while the sealed cup stays stationary.
        d = ImageDraw.Draw(im)
        length = 46+int(21*math.sin(14*prog)**2)
        d.line((382, 515, 382, 515-length), fill=PAPER, width=5)
    if mode == "opening" and id in (13, 17):
        labels = {13:"TIME COMPRESSED", 17:"SLOWED MOTION • SIMULATED NOTES"}
        draw = ImageDraw.Draw(im)
        draw.text((55,1071), labels[id], font=SMALL, fill=PAPER, anchor="ls")


def make_frame(info, frame, preview_zh=False):
    id, cues, diagram, photo, macro, context, background = info
    cue = next(cue for cue in cues if frame < cue["end"])
    index = cue["original_cue"]
    p = max(0, (frame-cue["start"])/max(1, cue["end"]-cue["start"]-1))
    hook = index == 0
    ending = cue is cues[-1]
    color, tint = COLORS[id]


    if hook and photo is not None and frame < 83:
        im = draw_macro(photo, macro, id, frame/FPS)
        d = ImageDraw.Draw(im)
        if frame >= 8:
            d.rounded_rectangle((41,62,374,101),radius=11,fill="#121b23")
            d.text((54,81),"ILLUSTRATED · TIME COMPRESSED",font=SMALL,fill=PAPER,anchor="lm")
        if preview_zh and frame >= cue["start"]:
            caption(d, cue["zh"])
        return im


    if hook or ending:
        im = context.copy()
        if hook:
            k,v = hook_scene(id,index,p)
        else:
            k = END_SCENE[id]
            v = (min(5,p*7.2) if id == 15 else .55+.45*p if id in (11,12,13) else
                 min(1,.36+p) if id == 14 else p)
        hero_model(im, diagram, id, k, v, "opening" if hook else "return")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((41,62,256,101),radius=11,fill="#121b23")
        d.text((54,81),"ILLUSTRATED MODEL",font=SMALL,fill=PAPER,anchor="lm")
        if frame >= 65 or ending:
            title(d, QUESTIONS[id] if hook else RESULTS[id], PAPER, y=253)
    else:
        im = background.copy()
        hero_model(im, diagram, id, index, p, "explanation")
        d = ImageDraw.Draw(im)
        d.text((53,72),"WHYNEST LAB",font=MODEL,fill=tint,anchor="ls")
        d.line((53,99,666,99),fill=ImageColor(tint,.49),width=2)
        heading = cue["overlay_en"]
        if isinstance(heading, list):
            heading = " / ".join(heading)
        title(d, heading.replace("→","to"), y=186)
        d.text((53,1081),"SCHEMATIC",font=SMALL,fill=color,anchor="ls")
    if preview_zh and frame >= cue["start"]:
        caption(d, cue["zh"])
    return im


def entry(id):
    source, scene, timeline, release, receipt = frozen(id)
    out = OUTPUT / str(id)
    out.mkdir(parents=True, exist_ok=True)
    wav, cues = audio_plan(id, source, timeline, out)
    with Image.open(source / "opening-art.png") as file:
        illustrated = file.convert("RGB")
    context = photo_context(illustrated,id)
    background = studio_base(id)
    photo, macro = macro_art(illustrated, id)
    info = id, cues, scene.SCENES[str(id)], photo, macro, context, background

    frame_count = cues[-1]["end"]
    samples = [0, 29, 73] + [math.floor((c["start"]+c["end"])/2) for c in cues[1:]] + [frame_count-10]
    strip = Image.new("RGB",(220*4,418*math.ceil(len(samples)/4)),"#121a20")
    draw = ImageDraw.Draw(strip)
    for i,n in enumerate(samples):
        x,y = i%4*220,i//4*418
        frame = make_frame(info,n,True)
        strip.paste(frame.resize((212,377),Image.Resampling.LANCZOS),(x+4,y+28))
        draw.text((x+9,y+7),f"{id} · {n/FPS:.2f}s",font=SMALL,fill=PAPER)
    strip.save(out / "captioned-frames.jpg",quality=91)

    preview = out / "review.mp4"
    temp = out / "encoding.mp4"
    args = [str(FF), "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-i", str(wav), "-i", str(out/"en.srt"), "-i", str(out/"zh-Hant.srt"),
            "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map", "3:s",
            "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-threads", "3", "-preset", "fast",
            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-b:a", "160k",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=7",
            "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-metadata:s:s:1", "language=zho",
            "-disposition:s:0", "0", "-disposition:s:1", "0", "-movflags", "+faststart", str(temp)]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as process:
        for n in range(frame_count):
            process.stdin.write(make_frame(info,n).tobytes())
        process.stdin.close()
        if process.wait():
            raise RuntimeError(f"FFmpeg rendering failed: {id}")
    temp.replace(preview)

    probe = json.loads(subprocess.check_output(
        [str(FFPROBE), "-v", "error", "-show_format", "-show_streams", "-of", "json", str(preview)]
    ))
    stream = probe["streams"]
    actual_duration = float(probe["format"]["duration"])
    if stream[0]["width"] != 1080 or stream[0]["height"] != 1920 or stream[0]["r_frame_rate"] != "30/1":
        raise ValueError(f"{id} video format unexpected")
    if [row["codec_name"] for row in stream] != ["h264", "aac", "mov_text", "mov_text"]:
        raise ValueError(f"{id} subtitle or stream codec mismatch")
    if abs(actual_duration-frame_count/FPS) > .11:
        raise ValueError(f"{id} video duration drift")

    analysis = subprocess.run([str(FF), "-hide_banner", "-nostats", "-xerror", "-i", str(preview),
        "-map", "0:v", "-map", "0:a", "-vf", "blackdetect=d=0.15:pix_th=0.06:pic_th=0.98",
        "-af", "silencedetect=noise=-45dB:d=1.40,ebur128=peak=true", "-f", "null", "NUL"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=True
    ).stderr
    (out / "ffmpeg-qa.txt").write_text(analysis, encoding="utf-8")
    if "black_start:" in analysis or "silence_start:" in analysis:
        raise ValueError(f"{id} black video or long silence")
    manifest = {
        "episode": id, "scope": "local review",
        "candidate_sha256": digest(preview), "duration": actual_duration,
        "old_sha256": receipt["mp4_sha256"], "original_script_scores": release["scores"],
        "included_original_cues": [c["original_cue"] for c in cues],
        "renderer_sha256": digest(Path(__file__)),
        "original_scene_sha256": digest(source / "scene-source.py"),
        "original_illustration_sha256": digest(source / "opening-art.png"),
        "timing_sha256": digest(out / "timing.json"),
        "subtitle_sha256": {lang:digest(out/f"{lang}.srt") for lang in ("en","zh-Hant")},
        "qa_pass": True,
    }
    save(out / "technical-review.json", manifest)
    print(f"{id}: {actual_duration:.2f}s, {manifest['candidate_sha256'][:12]}",flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("episodes", type=int, nargs="+", choices=range(11,21))
    args = parser.parse_args()
    assert_frozen(FF, FF_HASH)
    for episode in args.episodes:
        entry(episode)

