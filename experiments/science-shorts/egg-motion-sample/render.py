"""Render the local WhyNest Lab spinning egg motion sample."""

import importlib.util
import json
import math
from pathlib import Path
import subprocess
import time

from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BATCH = HERE.parent
OUT = ROOT / 'artifacts/science-shorts/egg-motion-sample'
TOOLS = ROOT / 'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
MODELS = ROOT / 'artifacts/73h-episode02/models'
SOURCE = OUT / 'coyau-source.webm'
SOURCE_HASH = 'c2ed2177faf36f77001c56ab6e38557ccd82be26b51e980bf61a5b77decdf8e9'

spec = importlib.util.spec_from_file_location('shared_science', BATCH / 'render.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
shared = pilot.shared()
verify_file = shared.verify_file
bindings = pilot.load(ROOT / 'experiments/episode-02-73h/render-manifest.json')
_, _, font = pilot.painter()

W, H, FPS = pilot.W, pilot.H, pilot.FPS
INK, TEAL, WHITE = '#1c2e2d', '#065e59', '#fffaf0'
CX, CY = 540, 944
CLIP_START, REPLAY_START = 33.48, 33.96
REPLAY_FRAMES = 84

EPISODE = {
    'id': 'WNL-021-motion-sample',
    'cues': [
        {'en': 'Watch this raw egg. It stops, then starts turning again.',
         'en_break_after': 'egg.', 'zh': '看看這顆生蛋。\n它停下後，又開始轉了。', 'pause': 0.55},
        {'en': 'A finger stops the shell. The liquid inside keeps turning.',
         'en_break_after': 'shell.', 'zh': '手指停住蛋殼。\n裡面的液體還在轉。', 'pause': 0.45},
        {'en': 'Let go, and the moving liquid pulls the shell around again.',
         'en_break_after': 'liquid', 'zh': '放開手，\n還在轉的液體又帶動蛋殼。', 'pause': 0.45},
    ],
}


def label(draw, xy, value, size, color=INK, bold=False, anchor='mm'):
    draw.text(xy, value, font=font(size, bold=bold), fill=color, anchor=anchor)


def footage(ffmpeg, start, frames):
    command = [
        str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin',
        '-ss', str(start), '-i', str(SOURCE), '-an',
        '-vf', 'crop=608:1080:820:0,scale=1080:1920:flags=lanczos,fps=30',
        '-frames:v', str(frames), '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1',
    ]
    with subprocess.Popen(command, stdout=subprocess.PIPE, env=pilot.ENV) as decoder:
        try:
            for _ in range(frames):
                pixels = decoder.stdout.read(W * H * 3)
                if len(pixels) != W * H * 3:
                    raise RuntimeError('Incomplete source frame')
                yield Image.frombytes('RGB', (W, H), pixels)
            if decoder.wait():
                raise RuntimeError('Source decode failed')
        finally:
            if decoder.poll() is None:
                decoder.kill()
                decoder.wait()


def live_title(image, frame, replay=False):
    draw = ImageDraw.Draw(image)
    if replay:
        label(draw, (540, 231), 'Watch it turn again.', 76, bold=True)
    else:
        label(draw, (540, 177), 'RAW EGG', 41, TEAL, True)
        label(draw, (540, 281), 'Why does it', 96, bold=True)
        label(draw, (540, 387), 'spin again?', 96, bold=True)
    if not replay and frame >= 45:
        label(draw, (540, 518), 'Turns again after release', 44, TEAL, True)
    label(draw, (540, 1642), 'Footage by Coyau / Wikimedia Commons', 34)
    label(draw, (540, 1690), 'CC BY-SA 3.0  ·  Cropped and excerpted', 31)
    return image


def diagram_background():
    gray = Image.linear_gradient('L').resize((W, H))
    image = ImageOps.colorize(gray, '#fffaf1', '#e4d5c2')
    draw = ImageDraw.Draw(image)
    draw.ellipse((194, 601, 886, 1293), outline='#d8cbbb', width=3)
    for x, y in ((194, CY), (886, CY), (CX, 601), (CX, 1293)):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill='#c3b29d')
    return image


def shell_texture():
    size = 660
    shade = Image.linear_gradient('L').resize((size, size))
    shell = ImageOps.colorize(shade, '#ffd7a7', '#a35334').convert('RGBA')
    alpha = Image.new('L', (size, size))
    ImageDraw.Draw(alpha).ellipse((16, 95, 644, 565), fill=255)
    shell.putalpha(alpha)
    draw = ImageDraw.Draw(shell)
    draw.ellipse((16, 95, 644, 565), outline='#81442d', width=7)
    draw.ellipse((49, 128, 611, 532), outline='#ffe5bb', width=7)
    draw.ellipse((603, 310, 634, 350), fill=INK, outline=WHITE, width=4)
    return shell


def point(angle, radius):
    theta = math.radians(angle)
    return CX + radius * math.cos(theta), CY + radius * math.sin(theta)


def cutaway(background, shell, elapsed, release):
    hold_start = 0.45
    held = hold_start <= elapsed < release
    since_release = max(0, elapsed - release)
    shell_angle = -18 + 72 * min(elapsed, hold_start) + 47 * since_release ** 1.18
    liquid_angle = 72 * elapsed
    im = background.copy()
    rotated = shell.rotate(-shell_angle, resample=Image.Resampling.BICUBIC)
    im.paste(rotated, (CX - 330, CY - 330), rotated)
    draw = ImageDraw.Draw(im)
    for radius, color in ((178, '#b66942'), (168, '#f5bd6d'), (148, '#ffd697'), (106, '#ffe1a0')):
        draw.ellipse((CX - radius, CY - radius, CX + radius, CY + radius), fill=color)
    for offset, radius, size in ((10, 82, 12), (101, 61, 9), (200, 86, 13), (291, 70, 7)):
        x, y = point(liquid_angle + offset, radius)
        draw.ellipse((x - size, y - size, x + size, y + size), fill='#cf8642')
    draw.arc((CX - 125, CY - 125, CX + 125, CY + 125),
             liquid_angle - 112, liquid_angle, fill=TEAL, width=14)
    tip = point(liquid_angle + 8, 125)
    draw.polygon([tip, point(liquid_angle - 9, 151), point(liquid_angle - 10, 99)], fill=TEAL)
    label(draw, (540, 227), 'INSIDE A RAW EGG', 65, bold=True)
    label(draw, (540, 315), 'Schematic  ·  timing exaggerated', 39)
    if held:
        label(draw, (540, 1420), 'Shell stopped', 66, bold=True)
        label(draw, (540, 1511), 'Liquid still turning', 62, TEAL, True)
    elif elapsed >= release:
        label(draw, (540, 1420), 'Released', 66, bold=True)
        label(draw, (540, 1511), 'Liquid moves the shell', 56, TEAL, True)
    return im


def frames(ffmpeg, cues):
    diagram_start, release = cues[1]['start'], cues[2]['start']
    replay = cues[-1]['end'] - REPLAY_FRAMES
    if not release + 15 < replay:
        raise ValueError('The explanation needs a visible release before replay')
    for n, image in enumerate(footage(ffmpeg, CLIP_START, diagram_start)):
        yield live_title(image, n)
    background, shell = diagram_background(), shell_texture()
    for n in range(diagram_start, replay):
        yield cutaway(background, shell, (n - diagram_start) / FPS, (release - diagram_start) / FPS)
    for n, image in enumerate(footage(ffmpeg, REPLAY_START, REPLAY_FRAMES)):
        yield live_title(image, n, replay=True)


def write_captions(cues):
    for lang, file in (('en', 'en.srt'), ('zh', 'zh-Hant.srt')):
        blocks = []
        for number, cue in enumerate(cues, 1):
            text = cue[lang]
            if lang == 'en':
                boundary = cue['en_break_after']
                text = text.replace(f'{boundary} ', f'{boundary}\n', 1)
            face = font(47 if lang == 'zh' else 43, zh=lang == 'zh')
            lines = text.splitlines()
            if len(lines) != 2 or max(map(face.getlength, lines)) > 830:
                raise ValueError(f'Caption needs a readable two-line layout: {lang} {number}')
            start, end = shared.srt_time(cue['start']), shared.srt_time(cue['end'])
            blocks.append(f'{number}\n{start} --> {end}\n{text}')
        (OUT / file).write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')


def main():
    media_start = time.perf_counter()
    ffmpeg = TOOLS / 'ffmpeg.exe'
    verify_file(ffmpeg, **bindings['ffmpeg'])
    if pilot.sha(SOURCE) != SOURCE_HASH:
        raise ValueError('Unexpected footage digest')
    for name in ('kokoro-v1.0.int8.onnx', 'voices-v1.0.bin'):
        verify_file(MODELS / name, **bindings['inputs'][f'models/{name}'])
    tts_start = time.perf_counter()
    cues = pilot.synthesize(EPISODE, OUT, MODELS, reuse=True, min_seconds=9)
    write_captions(cues)
    tts_seconds = time.perf_counter() - tts_start

    path = OUT / 'wnl-021-motion-preview.mp4'
    partial = OUT / 'wnl-021-motion-preview.in-progress.mp4'
    command = [
        str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
        '-i', 'pipe:0', '-i', str(OUT / 'narration.wav'), '-i', str(OUT / 'en.srt'),
        '-i', str(OUT / 'zh-Hant.srt'), '-map', '0:v', '-map', '1:a', '-map', '2:s', '-map', '3:s',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-threads', '4', '-pix_fmt', 'yuv420p',
        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-c:a', 'aac', '-ar', '48000', '-b:a', '160k',
        '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-metadata:s:s:1', 'language=zho',
        '-disposition:s:0', '0', '-disposition:s:1', '0', '-movflags', '+faststart',
        '-metadata', 'title=Why does this raw egg spin again?',
        '-metadata', 'comment=Footage by Coyau / Wikimedia Commons, CC BY-SA 3.0. Cropped and excerpted.',
        '-metadata', 'copyright=https://creativecommons.org/licenses/by-sa/3.0/',
        '-metadata', 'description=https://commons.wikimedia.org/wiki/File:Spinning_hardboiled_and_raw_eggs_01.ogv',
        str(partial),
    ]
    render_start = time.perf_counter()
    with subprocess.Popen(command, stdin=subprocess.PIPE, env=pilot.ENV) as encoder:
        try:
            for image in frames(ffmpeg, cues):
                encoder.stdin.write(image.tobytes())
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError('Output encode failed')
        finally:
            if encoder.poll() is None:
                encoder.kill()
                encoder.wait()
    partial.replace(path)
    evidence = {
        'source_sha256': SOURCE_HASH,
        'renderer_sha256': pilot.sha(Path(__file__)),
        'shared_renderer_sha256': pilot.sha(BATCH / 'render.py'),
        'audio_sha256': pilot.sha(OUT / 'narration.wav'),
        'preview_sha256': pilot.sha(path),
        'seconds': cues[-1]['end'] / FPS,
        'frames': cues[-1]['end'],
        'diagram_start': cues[1]['start'] / FPS,
        'diagram_release': cues[2]['start'] / FPS,
        'replay_start': (cues[-1]['end'] - REPLAY_FRAMES) / FPS,
        'tts_seconds': round(tts_seconds, 2),
        'composition_and_encode_seconds': round(time.perf_counter() - render_start, 2),
        'machine_seconds': round(time.perf_counter() - media_start, 2),
        'paid_media_calls': 0,
    }
    pilot.save(OUT / 'render-evidence.json', evidence)
    print(json.dumps(evidence, indent=2))


if __name__ == '__main__':
    main()
