"""Original illustrated WNL-021 short. Local previews and gated encoding."""

import argparse
import importlib.util
import math
from pathlib import Path
import subprocess
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / 'artifacts/science-shorts/egg-animation'
SCRIPT = HERE / 'script.json'
TOOLS = ROOT / 'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
MODELS = ROOT / 'artifacts/73h-episode02/models'

spec = importlib.util.spec_from_file_location('science_pilot', HERE.parent / 'render.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
shared = pilot.shared()
bindings = pilot.load(ROOT / 'experiments/episode-02-73h/render-manifest.json')
_, _, font = pilot.painter()
W, H, FPS = pilot.W, pilot.H, pilot.FPS
INK, DARK, TEAL, PAPER, WARM = '#193335', '#0d393e', '#006b68', '#fff6df', '#ffcf80'
CORE_TEAL, CORE_GOLD = '#a4eddb', '#ffd797'


def text(draw, x, y, value, size, color=INK, bold=False, anchor='mm'):
    draw.text((x, y), value, font=font(size, bold=bold), fill=color, anchor=anchor)


def background(top, bottom, seed):
    yy, xx = np.ogrid[-1:1:complex(H), -1:1:complex(W)]
    blend = ((yy + 1) * 0.35 + xx ** 2 * 0.13 + yy ** 2 * 0.09)[..., None]
    grain = np.random.default_rng(seed).normal(0, 1.35, (H, W, 1))
    pixels = np.asarray(top) * (1 - blend) + np.asarray(bottom) * blend + grain
    return Image.fromarray(np.uint8(np.clip(pixels, 0, 255)))


def egg_surface(color, marker):
    size = 672
    half = size / 2
    yy, xx = np.ogrid[-1:1:complex(size), -1:1:complex(size)]
    brightness = np.clip(1.22 - 0.30 * (xx + 0.35) ** 2 - 0.20 * (yy + 0.36) ** 2, 0.48, 1.21)
    texture = np.random.default_rng(22).normal(0, 1.65, (size, size, 1))
    rgb = np.asarray(color) * brightness[..., None] + texture
    egg = Image.fromarray(np.uint8(np.clip(rgb, 0, 255))).convert('RGBA')
    mask = Image.new('L', (size, size))
    curve = []
    for degrees in range(0, 360, 2):
        angle = math.radians(degrees)
        curve.append((half + 305 * math.cos(angle), half + (224 - 46 * math.cos(angle)) * math.sin(angle)))
    ImageDraw.Draw(mask).polygon(curve, fill=255)
    egg.putalpha(mask)
    draw = ImageDraw.Draw(egg)
    draw.line(curve + [curve[0]], fill='#986947', width=6, joint='curve')
    draw.ellipse((565, 322, 600, 357), fill=marker, outline=PAPER, width=4)
    return egg


def paste_egg(canvas, surface, center, angle):
    side = surface.width
    egg = surface.rotate(-angle, resample=Image.Resampling.BICUBIC)
    x, y = center
    canvas.paste(egg, (x - side // 2, y - side // 2), egg)


def mark_point(x, y, angle, radius):
    angle = math.radians(angle)
    return x + radius * math.cos(angle), y + radius * math.sin(angle)


def finger(canvas, center, contact, side):
    if contact <= 0:
        return
    x, y = center
    layer = Image.new('RGBA', (W, H))
    draw = ImageDraw.Draw(layer)
    reach = x + side * (68 + 240 * (1 - contact))
    shadow = (60, 38, 24, 75)
    skin = '#d6956c'
    if side > 0:
        draw.rounded_rectangle((reach, y - 27, W + 83, y + 80), 52, fill=shadow)
        draw.rounded_rectangle((reach, y - 47, W + 84, y + 57), 51, fill=skin, outline='#a86845', width=4)
        draw.rounded_rectangle((reach + 18, y - 26, reach + 86, y + 35), 27, fill='#f4bc97')
    else:
        draw.rounded_rectangle((-85, y - 29, reach, y + 74), 49, fill=shadow)
        draw.rounded_rectangle((-85, y - 49, reach, y + 53), 49, fill=skin, outline='#a86845', width=4)
        draw.rounded_rectangle((reach - 86, y - 28, reach - 18, y + 32), 25, fill='#f4bc97')
    canvas.paste(layer, mask=layer.getchannel('A'))


def movement(t, stop, prior_angle=12, speed=140):
    return prior_angle + speed * min(t, stop)


def press(t, stop, release):
    if t < stop:
        return max(0, 1 - (stop - t) / 0.31)
    return max(0, 1 - max(0, t - release) / 0.34)


def damped_distance(t, drag):
    return -math.expm1(-t * drag) / drag


def restarting_distance(t, speed, drag):
    return speed * 0.8 * (damped_distance(t, drag) - damped_distance(t, drag + 3.6))


class Shots:
    """Draw stable per-object positions and explicit shell/liquid angles."""

    first = (440, 648)
    second = (575, 1204)
    focus = (540, 880)
    demo_stop = 1.65
    demo_release = 2.42
    raw_stop = 2.12
    raw_speed = 80
    hold_drag = 0.12
    released_drag = 0.43

    def __init__(self):
        self.boiled = egg_surface((228, 167, 113), '#70412b')
        self.raw = egg_surface((236, 176, 120), TEAL)
        self.table_eggs = tuple(surface.resize((531, 531), Image.Resampling.LANCZOS)
                                for surface in (self.boiled, self.raw))
        self.cutaway_eggs = tuple(surface.resize((706, 706), Image.Resampling.LANCZOS)
                                  for surface in (self.boiled, self.raw))
        self.table = background((245, 229, 197), (211, 181, 142), 21)
        table_shadow = Image.new('RGBA', (W, H))
        shadow = ImageDraw.Draw(table_shadow)
        for x, y in (self.first, self.second):
            shadow.ellipse((x - 245, y - 133, x + 245, y + 183), fill=(78, 47, 27, 60))
        table_shadow = table_shadow.filter(ImageFilter.GaussianBlur(38))
        self.table.paste(table_shadow, mask=table_shadow.getchannel('A'))
        self.cut = background((17, 67, 70), (12, 38, 47), 22)
        guide = ImageDraw.Draw(self.cut)
        x, y = self.focus
        for radius in (340, 357):
            guide.ellipse((x - radius, y - radius, x + radius, y + radius), outline='#35686a', width=2)
        for angle in (0, 90, 180, 270):
            guide.line([mark_point(x, y, angle, 340), mark_point(x, y, angle, 370)], fill='#5d9692', width=3)

    def table_view(self, t, result=False, ending=False):
        im = self.table.copy()
        stop, release = self.demo_stop, self.demo_release
        boil_angle = movement(t, stop)
        raw_angle = boil_angle + restarting_distance(max(0, t - release), 142, 0.7)
        paste_egg(im, self.table_eggs[0], self.first, boil_angle)
        paste_egg(im, self.table_eggs[1], self.second, raw_angle)
        touch = press(t, stop, release)
        finger(im, self.first, touch, 1)
        finger(im, self.second, touch, -1)
        draw = ImageDraw.Draw(im)
        text(draw, 540, 130, 'ANIMATED DEMO', 37, TEAL, True)
        if ending:
            text(draw, 540, 225, 'The moving liquid', 70, bold=True)
            text(draw, 540, 306, 'turns the shell', 70, bold=True)
        else:
            text(draw, 540, 226, 'Why does it', 96, bold=True)
            text(draw, 540, 330, 'spin again?', 96, bold=True)
        if result or ending:
            text(draw, self.first[0], 923, 'Hard-boiled', 46, bold=True)
            text(draw, self.second[0], 1490, 'Raw', 46, TEAL, True)
        elif stop <= t < release:
            text(draw, 540, 393, 'Both shells stop', 47, TEAL, True)
        elif t >= release:
            text(draw, 540, 393, 'Release', 47, TEAL, True)
        return im

    def core(self, draw, angle, liquid, moving):
        x, y = self.focus
        if liquid:
            draw.ellipse((x - 178, y - 178, x + 178, y + 178), fill='#fbc271', outline='#fbdead', width=8)
            draw.ellipse((x - 154, y - 154, x + 154, y + 154), fill=CORE_GOLD)
            for offset, distance, size in ((8, 78, 11), (91, 62, 8), (193, 83, 12), (280, 85, 8)):
                a, b = mark_point(x, y, angle + offset, distance)
                draw.ellipse((a - size, b - size, a + size, b + size), fill='#b55f37')
            if moving:
                radius = 123
                draw.arc((x - radius, y - radius, x + radius, y + radius), angle - 118, angle,
                         fill=TEAL, width=14)
                draw.polygon([mark_point(x, y, angle + 8, 123), mark_point(x, y, angle - 9, 148),
                              mark_point(x, y, angle - 9, 99)], fill=TEAL)
        else:
            draw.ellipse((x - 178, y - 178, x + 178, y + 178), fill='#fff0cc', outline='#fae4b6', width=8)
            draw.ellipse((x - 130, y - 130, x + 130, y + 130), fill='#edb962')
            a, b = mark_point(x, y, angle, 106)
            draw.ellipse((a - 15, b - 15, a + 15, b + 15), fill=INK, outline=PAPER, width=3)

    def cutaway(self, shell_angle, core_angle, liquid, moving, title, state, detail, touch=0, second_try=False):
        im = self.cut.copy()
        x, y = self.focus
        paste_egg(im, self.cutaway_eggs[liquid], self.focus, shell_angle)
        if touch:
            finger(im, (x + 168, y - 123), touch, 1)
        draw = ImageDraw.Draw(im)
        self.core(draw, core_angle, liquid, moving)
        context = 'SECOND TRY  ·  TIMING ENLARGED' if second_try else 'CUTAWAY  ·  TIMING ENLARGED'
        text(draw, 540, 142, context, 36, CORE_TEAL)
        text(draw, 540, 261, title, 90, PAPER, True)
        text(draw, 540, 1264, state, 70, PAPER, True)
        text(draw, 540, 1360, detail, 51, CORE_TEAL if liquid else WARM, True)
        return im

    def frame(self, index, elapsed, cues):
        if index == 0:
            return self.table_view(elapsed)
        if index == 1:
            prior = (cues[0]['end'] - cues[0]['start']) / FPS
            return self.table_view(prior + elapsed, result=True)
        if index == 2:
            stop = 3.85
            angle = movement(elapsed, stop, speed=81)
            state = 'Turn together' if elapsed < stop else 'Stop together'
            touch = press(elapsed, stop, stop + 0.9)
            return self.cutaway(angle, angle, False, False, 'Hard-boiled', state, 'Shell + solid interior', touch)
        if index == 3:
            shell = movement(elapsed, self.raw_stop, speed=self.raw_speed)
            held = max(0, elapsed - self.raw_stop)
            fluid = shell + self.raw_speed * damped_distance(held, self.hold_drag)
            detail = 'Liquid keeps turning' if held else 'Liquid turning inside'
            state = 'Shell stopped' if held else 'Shell turning'
            return self.cutaway(shell, fluid, True, True, 'Raw egg', state, detail,
                                press(elapsed, self.raw_stop, float('inf')))
        hold_time = (cues[3]['end'] - cues[3]['start']) / FPS
        held_angle = movement(hold_time, self.raw_stop, speed=self.raw_speed)
        held_duration = hold_time - self.raw_stop
        release_core = held_angle + self.raw_speed * damped_distance(held_duration, self.hold_drag)
        if index == 4:
            release_speed = self.raw_speed * math.exp(-held_duration * self.hold_drag)
            shell = held_angle + restarting_distance(elapsed, release_speed, self.released_drag)
            fluid = release_core + release_speed * damped_distance(elapsed, self.released_drag)
            return self.cutaway(shell, fluid, True, True, 'Raw egg', 'Released', 'Liquid turns the shell',
                                press(elapsed, 0, 0))
        if elapsed >= 7.05:
            return self.table_view(9, result=True, ending=True)
        long_hold = min(elapsed, 4.9)
        ratio = long_hold / 4.9
        core = held_angle + 255 * (1 - (1 - ratio) ** 2)
        if elapsed < 4.9:
            state, detail = 'Held longer', 'Liquid slows down'
        elif elapsed < 5.85:
            state, detail = 'Held longer', 'Liquid stops'
        else:
            state, detail = 'Released', 'Shell stays still'
        return self.cutaway(held_angle, core, True, elapsed < 4.9, 'Raw egg', state, detail,
                            press(elapsed, 0, 5.85), second_try=True)


def srt_files(cues):
    for lang, name, size in (('en', 'en.srt', 43), ('zh', 'zh-Hant.srt', 47)):
        blocks = []
        divider = ' ' if lang == 'en' else ''
        face = font(size, zh=lang == 'zh')
        for index, cue in enumerate(cues, 1):
            lines = cue[f'captions_{lang}']
            if divider.join(lines) != cue[lang] or max(map(face.getlength, lines)) > 850 or len(lines) > 4:
                raise ValueError(f'Subtitle mismatch or overflow: {lang} {index}')
            start, end = shared.srt_time(cue['start']), shared.srt_time(cue['end'])
            blocks.append(f'{index}\n{start} --> {end}\n' + '\n'.join(lines))
        (OUT / name).write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')


def pending_inputs():
    return {
        'script_sha256': pilot.sha(SCRIPT),
        'renderer_sha256': pilot.sha(Path(__file__)),
        'shared_renderer_sha256': pilot.sha(HERE.parent / 'render.py'),
        'timeline_sha256': pilot.sha(OUT / 'timeline.json'),
        'narration_sha256': pilot.sha(OUT / 'narration.wav'),
        'preview_sha256': pilot.sha(OUT / 'preflight.jpg'),
    }


def previews(shots, cues):
    samples = (
        (0, 0.55), (0, 1.79), (0, 2.27), (0, 3.16), (1, 0.7),
        (2, 1.8), (2, 4.6), (3, 1.3), (3, 2.8), (3, 4.1),
        (4, 0.16), (4, 1.6), (5, 1.0), (5, 4.0), (5, 6.0), (5, 7.55),
    )
    contact = Image.new('RGB', (4 * 270, 4 * 500), '#254343')
    for slot, (cue_index, elapsed) in enumerate(samples):
        image = shots.frame(cue_index, elapsed, cues).resize((270, 480), Image.Resampling.LANCZOS)
        x, y = (slot % 4) * 270, (slot // 4) * 500
        contact.paste(image, (x, y))
        absolute = cues[cue_index]['start'] / FPS + elapsed
        text(ImageDraw.Draw(contact), x + 135, y + 490, f'{absolute:.2f} s', 13, PAPER)
    contact.save(OUT / 'preflight.jpg', quality=92)
    pilot.save(OUT / 'inputs.json', pending_inputs())


def check_gate():
    path = HERE / 'preflight-review.json'
    if not path.is_file():
        raise ValueError('Independent preflight review is missing')
    review = pilot.load(path)
    if review['inputs'] != pending_inputs() or review['fact_visual']['status'] != 'PASS':
        raise ValueError('Fact/visual review does not cover these inputs')
    if review['fact_visual']['critical_defects'] or review['fact_visual']['rights_defects']:
        raise ValueError('Fact/visual or rights review has blocking findings')
    rubric = pilot.load(HERE.parent / 'batch-20261121/gate-policy.json')['rubric']
    readers = review['readers']
    if len(readers) != 2 or len({entry['reviewer'] for entry in readers}) != 2:
        raise ValueError('Both independent readers are required')
    for entry in readers:
        parts = entry['scores']
        if set(parts) != set(rubric) or any(type(parts[key]) is not int or not 0 <= parts[key] <= limit
                                           for key, limit in rubric.items()):
            raise ValueError('Independent script score is outside the rubric')
        if sum(parts.values()) != entry['total'] or entry['total'] < 85 or entry['blockers']:
            raise ValueError('Independent script score is incomplete or below threshold')
    return review


def encode(shots, cues, ffmpeg, review):
    start = time.perf_counter()
    target = OUT / 'wnl-021-original-animation.mp4'
    partial = OUT / 'encoding.mp4'
    args = [
        str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
        '-i', str(OUT / 'narration.wav'), '-i', str(OUT / 'en.srt'), '-i', str(OUT / 'zh-Hant.srt'),
        '-map', '0:v', '-map', '1:a', '-map', '2:s', '-map', '3:s',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-threads', '4', '-pix_fmt', 'yuv420p',
        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-c:a', 'aac', '-ar', '48000', '-b:a', '160k',
        '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-metadata:s:s:1', 'language=zho',
        '-disposition:s:0', '0', '-disposition:s:1', '0', '-movflags', '+faststart',
        '-metadata', 'title=Why Does This Egg Start Spinning Again?', str(partial),
    ]
    with subprocess.Popen(args, stdin=subprocess.PIPE, env=pilot.ENV) as encoder:
        try:
            cursor = 0
            for index, cue in enumerate(cues):
                for frame in range(cursor, cue['end']):
                    elapsed = max(0, frame - cue['start']) / FPS
                    encoder.stdin.write(shots.frame(index, elapsed, cues).tobytes())
                cursor = cue['end']
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError('Encoding failed')
        finally:
            if encoder.poll() is None:
                encoder.kill()
                encoder.wait()
    partial.replace(target)
    pilot.save(OUT / 'render-evidence.json', {
        'inputs': review['inputs'],
        'review_sha256': pilot.sha(HERE / 'preflight-review.json'),
        'video_sha256': pilot.sha(target),
        'seconds': cues[-1]['end'] / FPS,
        'frames': cues[-1]['end'],
        'seconds_encode': round(time.perf_counter() - start, 2),
        'paid_media_calls': 0,
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('preview', 'render'))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ffmpeg = TOOLS / 'ffmpeg.exe'
    shared.verify_file(ffmpeg, **bindings['ffmpeg'])
    for name in ('kokoro-v1.0.int8.onnx', 'voices-v1.0.bin'):
        shared.verify_file(MODELS / name, **bindings['inputs'][f'models/{name}'])
    narration_start = time.perf_counter()
    episode = pilot.load(SCRIPT)
    cues = pilot.synthesize(episode, OUT, MODELS, reuse=True, min_seconds=35)
    srt_files(cues)
    print(f'VOICE/CAPTIONS {time.perf_counter() - narration_start:.2f}s; VIDEO {cues[-1]["end"]/FPS:.2f}s', flush=True)
    if args.mode == 'preview':
        previews(Shots(), cues)
    else:
        review = check_gate()
        encode(Shots(), cues, ffmpeg, review)


if __name__ == '__main__':
    main()
