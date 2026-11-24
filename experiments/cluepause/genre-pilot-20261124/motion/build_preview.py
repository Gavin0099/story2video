"""Build an eleven-second still/motion/still technical montage, not the H01 film."""
import struct
import wave

import hybrid_motion as hm


def main():
    tools = hm.Tools(hm.HERE / "tools.lock.json")
    root = hm.OUTPUTS
    if (root / "hybrid-demo.mp4").exists() or (root / "still-hold.json").exists():
        raise FileExistsError("Preview exists; choose a new version instead of overwriting evidence")
    hm.save(root / "still-hold.json", dict(version=1, frames=30, background="layers/intercom-plate.png", layers=[]))
    hm.render(root / "still-hold.json", root / "still-hold.mp4", tools)
    rate = 48000
    with wave.open(str(root / "click.wav"), "rb") as stream:
        click = struct.unpack("<" + "h"*stream.getnframes(), stream.readframes(stream.getnframes()))
    mix = [0] * (11 * rate)
    at = round((1+3+3+2.3) * rate)
    for i, sample in enumerate(click):
        mix[at+i] = round(sample*.6)
    with wave.open(str(root / "demo-mix.wav"), "wb") as stream:
        stream.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        stream.writeframes(struct.pack("<" + "h"*len(mix), *mix))
    hm.save(root / "hybrid-timeline.json", dict(version=1, audio="demo-mix.wav", shots=[
        dict(clip="still-hold.mp4", frames=30), dict(clip="handle.mp4", frames=90),
        dict(clip="intercom.mp4", frames=90), dict(clip="latch.mp4", frames=90),
        dict(clip="still-hold.mp4", frames=30)]))
    hm.splice(root / "hybrid-timeline.json", root / "hybrid-demo.mp4", tools)


if __name__ == "__main__":
    main()
