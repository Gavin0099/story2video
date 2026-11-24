"""Stage the seven original built-in ImageGen outputs; never call a media service."""
import argparse
import json
from pathlib import Path
import shutil
import wave
import math
import struct

from PIL import Image, ImageDraw, ImageOps

import hybrid_motion as hm

GENERATED = {
    "handle-plate": "exec-ee10a9d5-f27e-401a-9938-fd22658f749f.png",
    "handle-element": "exec-312e1c2a-9f37-4f3d-bbcc-d5667a6365cc.png",
    "intercom-plate": "exec-bcd15f90-c3f5-4597-9e35-fe4f9d10861a.png",
    "screen-element": "exec-c97d5288-6035-4680-a8f6-a85cd495fd0f.png",
    "indicator-element": "exec-aa6188c1-f85e-4f32-bbeb-4c7022fa4b7c.png",
    "latch-plate": "exec-2958a363-99d0-4ed6-960b-15e721abe58d.png",
    "latch-element": "exec-7a40b7c1-619f-4f09-9305-a8f1ec07d4c4.png",
}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("generated_directory", type=Path)
    args = cli.parse_args()
    hm.Tools(hm.HERE / "tools.lock.json")  # Bind before output roots.
    root = hm.OUTPUTS
    if (root / "assets.json").exists():
        raise FileExistsError("Demo already staged; do not overwrite reviewed inputs")
    (root / "raw").mkdir(parents=True, exist_ok=True)
    (root / "layers").mkdir(exist_ok=True)
    records = {}
    for name, filename in GENERATED.items():
        source = (args.generated_directory / filename).resolve(strict=True)
        target = root / "raw" / (name + ".png")
        shutil.copyfile(source, target)
        with Image.open(target) as image:
            entry = {"original": str(source), "sha256": hm.digest(target), "size": image.size,
                     "mode": image.mode, "builtin_request": True}
            if "plate" in name:
                cooked = ImageOps.fit(image.convert("RGB"), (1080, 1920), Image.Resampling.LANCZOS)
                box = None
            else:
                alpha = image.getchannel("A")
                # Ignore almost invisible alpha debris when finding the asset's bounds.
                # Keep the original alpha values within the crop; no chroma key/repainting.
                box = alpha.point(lambda a: 255 if a >= 16 else 0).getbbox()
                box = (max(0, box[0]-8), max(0, box[1]-8), min(image.width, box[2]+8), min(image.height, box[3]+8))
                cooked = image.crop(box)
                entry["alpha_extrema"] = alpha.getextrema()
            cooked.save(root / "layers" / (name + ".png"))
            entry["crop"] = box
            entry["staged_sha256"] = hm.digest(root / "layers" / (name + ".png"))
            records[name] = entry
    # Foreground occlusion: copy pixels from the same plate, never invent a second housing.
    with Image.open(root / "layers/latch-plate.png") as image:
        foreground = image.convert("RGBA")
        mask = Image.new("L", foreground.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((0, 0, 546, 1919), fill=255)
        draw.rectangle((918, 0, 1079, 1919), fill=255)
        foreground.putalpha(mask)
        foreground.save(root / "layers/latch-occluder.png")
    # Local synthetic click only; no voice generation or copied narration.
    rate = 48000
    samples = [int(32767 * .14 * math.sin(2*math.pi*1370*n/rate) * math.exp(-70*n/rate)) for n in range(4800)]
    with wave.open(str(root / "click.wav"), "wb") as stream:
        stream.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        stream.writeframes(struct.pack("<" + "h"*len(samples), *samples))

    def layer(name, image, size, pivot, anchor, motions, **extra):
        return dict(id=name, image="layers/"+image+".png", size=size, pivot=pivot, anchor=anchor, motions=motions, **extra)

    def move(kind, start, end, **extra):
        return dict(type=kind, start_s=start, end_s=end, easing="smoothstep", **extra)

    specs = {
        "handle": dict(version=1, id="H01-handle-motion-demo", frames=90, background="layers/handle-plate.png",
            notes="Local macro study. Hand stays clear. Closed plate; no early latch release. Not the final 0-.7 s edit.",
            layers=[layer("lever", "handle-element", [440, 119], [57, 60], [368, 921],
                          [move("rotate", .35, 1.0, **{"from": 0, "to": 18})])]),
        "intercom": dict(version=1, id="H01-intercom-power-demo", frames=90, background="layers/intercom-plate.png",
            notes="Blank screen/light power-on only. Production in-world status text and cough pulses are not implemented.",
            layers=[layer("glass", "screen-element", [550, 390], [275, 195], [535, 638],
                          [move("fade", .4, 1.2, **{"from": 0, "to": .8})]),
                    layer("listening-led", "indicator-element", [45, 46], [22.5, 23], [536, 905],
                          [move("glow", .4, 1.2, **{"from": 0, "to": 1})], glow_radius=3)]),
        "latch": dict(version=1, id="H01-latch-retract-demo", frames=90, background="layers/latch-plate.png",
            notes="Local reveal-only bolt study. Motion starts at local 1.5 s. No actual invitation audio; not approved for pre-reveal use.",
            layers=[layer("bolt", "latch-element", [440, 56], [0, 28], [480, 978],
                          [move("translate", 1.5, 2.3, path=[[0, 0], [-405, 0]])]),
                    layer("housing-occlusion", "latch-occluder", [1080, 1920], [540, 960], [540, 960], [])],
            sound_cues=[dict(file="click.wav", time_s=2.3, gain=.6)]),
    }
    for name, spec in specs.items():
        hm.save(root / (name + ".json"), spec)
    hm.save(root / "assets.json", {"imagegen_requests": 7, "correction_requests": 0, "assets": records,
        "story_reference_sha256": hm.digest(hm.HERE.parent / "urban_horror-v2.md"),
        "source_generation_directory": str(args.generated_directory.resolve()),
        "processing": "original alpha-preserving crop/resize, full-cover plate crop, same-plate housing occlusion"})
    hm.save(root / "demo-timeline.json", {"version": 1, "shots": [{"clip": name+".mp4", "frames": 90} for name in specs]})
    print(json.dumps({"staged": str(root), "requests": 7}))


if __name__ == "__main__":
    main()
