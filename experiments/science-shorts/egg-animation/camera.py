"""WNL-021 camera revision with original procedural artwork and frozen audio."""

import argparse
import importlib.util
from pathlib import Path
import subprocess
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('egg_master', HERE / 'render.py')
master = importlib.util.module_from_spec(spec)
spec.loader.exec_module(master)

pilot = master.pilot
W, H, FPS = master.W, master.H, master.FPS
OUT = master.OUT / 'camera-revision'
SOURCE = master.OUT / 'wnl-021-original-animation.mp4'
TIMELINE = master.OUT / 'timeline.json'
FFMPEG = master.TOOLS / 'ffmpeg.exe'
REVIEW = HERE / 'camera-review.json'
SOURCE_SHA = '5cc6937b572c3e43375aa629671c6c012afa328d5c8ecfa42313993ccf8d3e27'
TIMELINE_SHA = 'fe705abecbdf331497823c2b5d207504e3b2c9c2eefba9f3ec091f8a405d958c'

WHITE = '#fff3e3'
COOL = '#a8e8da'
GOLD = '#f4ce9a'
PALE = '#c8cedd'
RAW_MARK = '#13776d'
SOLID_MARK = '#a64e28'


def label(draw, x, y, value, size, color=WHITE, bold=False, anchor='mm'):
    master.text(draw, x, y, value, size, color, bold, anchor)


def tabletop():
    yy, xx = np.ogrid[-1:1:complex(H), -1:1:complex(W)]
    rng = np.random.default_rng(21)
    light = np.exp(-((xx + 0.42) ** 2 * 0.67 + (yy + 0.35) ** 2 * 1.6))
    reflected = np.exp(-((xx - 0.71) ** 2 * 1.1 + (yy - 0.18) ** 2 * 1.15))
    texture = rng.normal(0, 0.95, (H, W))
    pores = rng.uniform(-2, 1, (H, W)) * (rng.random((H, W)) > 0.975)
    rgb = (np.array([13, 22, 34]) + light[..., None] * [40, 38, 42]
           + reflected[..., None] * [4, 10, 20] + (texture + pores)[..., None])
    return Image.fromarray(np.uint8(np.clip(rgb, 0, 255)))


def shell(base, marker):
    size = 1000
    yy, xx = np.ogrid[-1:1:complex(size), -1:1:complex(size)]
    taper = 0.64 - xx * 0.147
    normalized_y = yy / taper
    depth = np.sqrt(np.clip(1 - (xx / 0.91) ** 2 - normalized_y ** 2, 0, 1))
    diffuse = np.clip(depth * 0.72 - 0.34 * xx - 0.36 * normalized_y, 0, 1)
    bounce = np.clip(normalized_y * 0.46 + xx * 0.13, 0, 1)
    sheen = np.exp(-((xx + 0.27) ** 2 / 0.10 + (yy + 0.22) ** 2 / 0.023))
    rng = np.random.default_rng(891)
    grain = rng.normal(0, 1.38, (size, size))
    flecks = (rng.random((size, size)) < 0.035) * rng.uniform(0, 22, (size, size))
    rgb = (np.asarray(base) * (0.53 + 0.48 * diffuse[..., None])
           + bounce[..., None] * [24, 24, 25] + sheen[..., None] * [38, 34, 26]
           + (grain - flecks)[..., None])
    im = Image.fromarray(np.uint8(np.clip(rgb, 0, 255))).convert('RGBA')
    points = []
    for degrees in range(0, 360, 2):
        angle = np.deg2rad(degrees)
        x = 0.91 * np.cos(angle)
        y = (0.64 - x * 0.147) * np.sin(angle)
        points.append(((x + 1) * size / 2, (y + 1) * size / 2))
    mask = Image.new('L', (size, size))
    ImageDraw.Draw(mask).polygon(points, fill=255)
    im.putalpha(mask)
    ink = ImageDraw.Draw(im)
    ink.line(points + [points[0]], fill='#b59478', width=3)
    # Both marks stick to the outside. Size and the pale border survive the wide shot.
    ink.ellipse((831, 473, 884, 526), fill=marker, outline='#ffefce', width=5)
    return im


def finger_sprite():
    width, height = 860, 144
    yy, xx = np.ogrid[0:height, 0:width]
    highlight = np.exp(-((yy - 49) / 36) ** 2) * (0.82 + 0.18 * xx / width)
    pad = np.exp(-((xx - 86) / 100) ** 2)
    rgb = np.array([129, 78, 65]) + highlight[..., None] * [91, 72, 64] + pad[..., None] * [14, 8, 2]
    im = Image.fromarray(np.uint8(np.clip(rgb, 0, 255))).convert('RGBA')
    mask = Image.new('L', (width, height))
    ImageDraw.Draw(mask).rounded_rectangle((1, 8, width + 80, height - 11), 64, fill=255)
    im.putalpha(mask)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((13, 34, 99, 103), 32, fill='#dfaa92', outline='#bf8973', width=3)
    draw.arc((22, 42, 90, 96), 167, 261, fill='#f4c9ac', width=3)
    draw.arc((116, 29, 151, 116), 288, 70, fill='#b9806e', width=2)
    return im


class CameraShots(master.Shots):
    first = (433, 666)
    second = (649, 1220)
    focus = (540, 868)
    close_at = 3.03

    def __init__(self):
        self.scene = tabletop()
        self.diag = self.scene.copy()
        tint = Image.new('RGB', (W, H), '#08141e')
        self.diag = Image.blend(self.diag, tint, 0.24)
        surfaces = (shell((255, 220, 180), SOLID_MARK), shell((255, 231, 199), RAW_MARK))
        self.wide = tuple(im.resize((570, 570), Image.Resampling.LANCZOS) for im in surfaces)
        self.close = tuple(im.resize((950, 950), Image.Resampling.LANCZOS) for im in surfaces)
        self.hand = finger_sprite()
        self.left_hand = self.hand.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.shadows = {side: self.soft_shadow(side) for side in (570, 950)}

    @staticmethod
    def soft_shadow(side):
        mask = Image.new('L', (side, side))
        ImageDraw.Draw(mask).ellipse((side * 0.12, side * 0.28, side * 0.94, side * 0.77), fill=165)
        return mask.filter(ImageFilter.GaussianBlur(side * 0.062))

    def place(self, im, surface, position, angle):
        x, y = position
        side = surface.width
        im.paste((3, 8, 16), (x - side // 2 + 14, y - side // 2 + 27), self.shadows[side])
        master.paste_egg(im, surface, position, angle)

    def fingertip(self, im, position, strength, side, close=False):
        if strength <= 0:
            return
        x, y = position
        reach = round(x + side * ((165 if close else 74) + 650 * (1 - strength)))
        sprite = self.hand if side > 0 else self.left_hand
        left = reach if side > 0 else reach - sprite.width
        im.paste(sprite, (left, y - 72), sprite)

    def table_view(self, t, result=False, ending=False):
        im = self.scene.copy()
        stop, release = self.demo_stop, self.demo_release
        hard = master.movement(t, stop)
        raw = hard + master.restarting_distance(max(0, t - release), 142, 0.7)
        for index, (position, angle) in enumerate(((self.first, hard), (self.second, raw))):
            self.place(im, self.wide[index], position, angle)
        touch = master.press(t, stop, release)
        self.fingertip(im, self.first, touch, 1)
        self.fingertip(im, self.second, touch, -1)
        draw = ImageDraw.Draw(im)
        label(draw, 540, 154, 'ANIMATED DEMO', 32, PALE, True)
        if ending:
            label(draw, 540, 278, 'Liquid turns the shell', 68, bold=True)
        elif result:
            label(draw, 540, 278, 'Same test. Two results.', 66, bold=True)
        else:
            label(draw, 540, 269, 'Why does one', 92, bold=True)
            label(draw, 540, 375, 'spin again?', 92, bold=True)
        if result or ending:
            label(draw, self.first[0], 960, 'Hard-boiled  ·  stopped', 45, GOLD, True)
            label(draw, self.second[0], 1515, 'Raw  ·  restarted', 45, COOL, True)
        elif stop <= t < release:
            label(draw, 540, 1545, 'Both shells stop', 52, bold=True)
        elif t >= release:
            label(draw, 540, 1545, 'Lift both fingers', 52, bold=True)
        return im

    def hero(self, angle, liquid, context='', state='', extra=''):
        im = self.scene.copy()
        self.place(im, self.close[liquid], self.focus, angle)
        draw = ImageDraw.Draw(im)
        label(draw, 540, 164, context, 33, PALE, True)
        label(draw, 540, 1380, state, 74, bold=True)
        if extra:
            label(draw, 540, 1460, extra, 48, COOL if liquid else GOLD, True)
        return im

    def core(self, draw, angle, liquid, moving):
        x, y = self.focus
        draw.ellipse((x - 214, y - 214, x + 214, y + 214),
                     fill='#c9a674' if liquid else '#ead1ae', outline='#fff1d5', width=9)
        draw.ellipse((x - 188, y - 188, x + 188, y + 188),
                     fill='#e9be82' if liquid else '#fff5dc', outline='#6c5846', width=3)
        if not liquid:
            draw.ellipse((x - 141, y - 141, x + 141, y + 141), fill='#e8ad4b')
            dx, dy = master.mark_point(x, y, angle, 106)
            draw.ellipse((dx - 17, dy - 17, dx + 17, dy + 17), fill='#773217', outline=WHITE, width=4)
            return
        ink = '#145851'
        for offset, distance, radius in ((8, 78, 12), (91, 62, 8), (193, 83, 12), (280, 85, 9)):
            dx, dy = master.mark_point(x, y, angle + offset, distance)
            draw.ellipse((dx - radius, dy - radius, dx + radius, dy + radius), fill=ink)
        if moving:
            r = 151
            draw.arc((x - r, y - r, x + r, y + r), angle - 113, angle, fill=ink, width=16)
            draw.polygon([master.mark_point(x, y, angle + 8, r),
                          master.mark_point(x, y, angle - 10, r + 27),
                          master.mark_point(x, y, angle - 10, r - 27)], fill=ink)

    def cutaway(self, shell_angle, core_angle, liquid, moving, title, state, detail, touch=0, second_try=False):
        im = self.diag.copy()
        self.place(im, self.close[liquid], self.focus, shell_angle)
        draw = ImageDraw.Draw(im)
        self.core(draw, core_angle, liquid, moving)
        if touch:
            self.fingertip(im, (self.focus[0] + 136, self.focus[1] - 117), touch, 1, close=True)
        context = 'LONG HOLD  /  TIMING ENLARGED' if second_try else 'CUTAWAY  /  TIMING ENLARGED'
        label(draw, 540, 164, context, 34, PALE, True)
        label(draw, 540, 311, title, 93, bold=True)
        label(draw, 540, 1370, state, 71, bold=True)
        label(draw, 540, 1452, detail, 51, COOL if liquid else GOLD, True)
        return im

    def frame(self, index, elapsed, cues):
        if index == 0 and elapsed >= self.close_at:
            held = master.movement(self.demo_stop, self.demo_stop)
            angle = held + master.restarting_distance(elapsed - self.demo_release, 142, 0.7)
            return self.hero(angle, True, 'AFTER RELEASE', 'It spins again')
        if index == 1:
            prior = (cues[0]['end'] - cues[0]['start']) / FPS
            return self.table_view(prior + elapsed, result=True)
        im = super().frame(index, elapsed, cues)
        if index in (2, 3) and elapsed < 0.64:
            angle = 12 + (81 if index == 2 else self.raw_speed) * elapsed
            exterior = self.hero(angle, index == 3)
            # Match the exterior and cutaway pose on every reveal frame.
            fraction = min(1, elapsed / 0.64)
            return Image.blend(exterior, im, fraction * fraction * (3 - 2 * fraction))
        return im


SAMPLES = (0, 62, 77, 96, 97, 112, 217, 411, 432, 548, 644, 666,
           730, 767, 818, 866, 1002, 1089, 1116, 1161, 1200)


def get_frame(shots, frame, cues):
    index = next(i for i, cue in enumerate(cues) if frame < cue['end'])
    return shots.frame(index, max(0, frame - cues[index]['start']) / FPS, cues)


def encode(shots, cues, target, size, step):
    partial = target.with_name(f'{target.stem}.partial.mp4')
    width, height = size
    args = [str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{width}x{height}', '-r', str(FPS // step),
            '-i', 'pipe:0', '-i', str(SOURCE), '-map', '0:v:0', '-map', '1:a:0', '-map', '1:s',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '4',
            '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-c:s', 'copy', '-movflags', '+faststart',
            str(partial)]
    with subprocess.Popen(args, stdin=subprocess.PIPE, env=pilot.ENV) as encoder:
        try:
            for cue_index, cue in enumerate(cues):
                start = 0 if cue_index == 0 else cue['start']
                start += -start % step
                for frame in range(start, cue['end'], step):
                    im = shots.frame(cue_index, max(0, frame - cue['start']) / FPS, cues)
                    if size != (W, H):
                        im = im.resize(size, Image.Resampling.LANCZOS)
                    encoder.stdin.write(im.tobytes())
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError('Encoding failed')
        finally:
            if encoder.poll() is None:
                encoder.kill()
                encoder.wait()
    partial.replace(target)


def inputs():
    files = (Path(__file__), HERE / 'render.py', HERE.parent / 'render.py',
             Path(master.shared.__file__), HERE / 'script.json', SOURCE, TIMELINE, FFMPEG,
             OUT / 'preview.mp4', OUT / 'shot-contact.jpg')
    return {file.relative_to(master.ROOT).as_posix(): pilot.sha(file) for file in files}


def preview(shots, cues):
    contact = Image.new('RGB', (4 * 208, 6 * 396), '#222b38')
    for slot, frame in enumerate(SAMPLES):
        im = get_frame(shots, frame, cues).resize((208, 370), Image.Resampling.LANCZOS)
        x, y = (slot % 4) * 208, (slot // 4) * 396
        contact.paste(im, (x, y))
        label(ImageDraw.Draw(contact), x + 104, y + 383, f'{frame / FPS:.2f} s', 15, WHITE)
    contact.save(OUT / 'shot-contact.jpg', quality=91)
    encode(shots, cues, OUT / 'preview.mp4', (432, 768), 3)
    pilot.save(OUT / 'inputs.json', inputs())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('preview', 'render'))
    mode = parser.parse_args().mode
    if pilot.sha(SOURCE) != SOURCE_SHA or pilot.sha(TIMELINE) != TIMELINE_SHA:
        raise ValueError('Original video or timeline hash mismatch')
    master.shared.verify_file(FFMPEG, **master.bindings['ffmpeg'])
    OUT.mkdir(parents=True, exist_ok=True)
    cues = pilot.load(TIMELINE)['cues']
    if mode == 'preview':
        preview(CameraShots(), cues)
        return
    if not REVIEW.is_file():
        raise ValueError('Independent camera review is missing')
    receipt = pilot.load(REVIEW)
    if receipt['status'] != 'PASS' or receipt['critical_defects'] or receipt['inputs'] != inputs():
        raise ValueError('Independent camera review has findings or does not cover these files')
    target = OUT / 'wnl-021-camera-revision.mp4'
    started = time.perf_counter()
    encode(CameraShots(), cues, target, (W, H), 1)
    pilot.save(OUT / 'render-evidence.json', {
        'inputs': receipt['inputs'],
        'review_sha256': pilot.sha(REVIEW),
        'video_sha256': pilot.sha(target),
        'frames': cues[-1]['end'],
        'seconds': cues[-1]['end'] / FPS,
        'encode_seconds': round(time.perf_counter() - started, 2),
        'paid_media_calls': 0,
    })


if __name__ == '__main__':
    main()
