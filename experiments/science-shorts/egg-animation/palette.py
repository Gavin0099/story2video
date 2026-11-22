"""Preview and encode color variations from the verified WNL-021 master."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'artifacts/science-shorts/egg-animation/wnl-021-original-animation.mp4'
OUT = SOURCE.parent / 'palette-revision'
FFMPEG = ROOT / 'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin/ffmpeg.exe'
SOURCE_SHA256 = '5cc6937b572c3e43375aa629671c6c012afa328d5c8ecfa42313993ccf8d3e27'
FFMPEG_SHA256 = 'ed8f66cb877087a96f5bbb40a2944f0e764f2ad8870d5cb647360d912e62bc07'

# Each row maps one existing visual role to its ice, sage, and plum colors.
ANCHORS = (
    ('table light',   '#f5e5c5', '#ebf2fa', '#f2f5e5', '#f4eaf4'),
    ('table shade',   '#d3b58e', '#a1b3d6', '#acbf9d', '#bb9fca'),
    ('table shadow',  '#c1a581', '#9caccc', '#99b18f', '#aa8bb9'),
    ('shell light',   '#ffd28f', '#f8e7d8', '#f8e9cf', '#f9e2de'),
    ('shell middle',  '#e8ac76', '#dec6b4', '#dfc8aa', '#dfbdba'),
    ('shell shade',   '#b57e58', '#ad958b', '#ae987a', '#ae9093'),
    ('shell outline', '#986947', '#79655f', '#78654e', '#79616b'),
    ('boiled marker', '#70412b', '#56617b', '#596144', '#644059'),
    ('raw marker',    '#006b68', '#2352ac', '#3c672b', '#7a306d'),
    ('finger',        '#d6956c', '#cb9a92', '#c99579', '#cc92a0'),
    ('finger edge',   '#a86845', '#8a645f', '#8b604a', '#8b5670'),
    ('finger nail',   '#f4bc97', '#f1c2b1', '#efc0a1', '#edb6c7'),
    ('cutaway light', '#114346', '#233565', '#364d31', '#493050'),
    ('cutaway dark',  '#0c262f', '#101a35', '#1c291c', '#261c35'),
    ('guide',         '#35686a', '#435c90', '#587751', '#775681'),
    ('guide tick',    '#5d9692', '#809ad0', '#91a77c', '#ad87ad'),
    ('dark text',     '#193335', '#172644', '#203320', '#38223b'),
    ('light text',    '#fff6df', '#f8fbff', '#fcfff0', '#fff6f6'),
    ('raw label',     '#a4eddb', '#b8d8ff', '#d1efae', '#f3c4e9'),
    ('boiled label',  '#ffcf80', '#f9d49d', '#ffe4a0', '#ffcead'),
    ('raw fluid',     '#ffd797', '#fae9d3', '#faecd2', '#fbe5df'),
    ('fluid edge',    '#fbc271', '#eacfad', '#ebd3a3', '#ecc5bf'),
    ('edge highlight','#fbdead', '#fcf2df', '#fcf0d5', '#fcf0eb'),
    ('fluid marks',   '#b55f37', '#476894', '#5b763a', '#935977'),
    ('boiled white',  '#fff0cc', '#f4f2ec', '#faf4da', '#fff1e6'),
    ('boiled ring',   '#fae4b6', '#d8deed', '#eee4b5', '#ecd5d7'),
    ('boiled yolk',   '#edb962', '#ecb45d', '#e1b95c', '#e6a879'),
)
PALETTES = {'ice': '冰藍 × 深海藍', 'sage': '鼠尾草綠 × 森林綠', 'plum': '霧紫 × 莓果紫'}
SAMPLES = ('2.10', '24.50', '28.30')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def component_values(hex_colors):
    return np.array([ImageColor.getrgb(color) for color in hex_colors]) / 255


def write_cube(name):
    index = list(PALETTES).index(name) + 2
    original = component_values(row[1] for row in ANCHORS)
    target = component_values(row[index] for row in ANCHORS)
    size = 33
    blue, green, red = np.mgrid[0:size, 0:size, 0:size] / (size - 1)
    rgb = np.column_stack([red.ravel(), green.ravel(), blue.ravel()])
    distances = np.square(rgb[:, None, :] - original).sum(axis=2)
    weights = (distances + 0.00055) ** -2.5
    offsets = (weights @ (target - original)) / weights.sum(axis=1, keepdims=True)
    result = np.clip(rgb + offsets, 0, 1)
    path = OUT / f'{name}.cube'
    with path.open('w', encoding='ascii', newline='\n') as file:
        file.write(f'LUT_3D_SIZE {size}\n')
        np.savetxt(file, result, fmt='%.7f')
    return path


def run(*args):
    subprocess.run([str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y', *args],
                   cwd=OUT, check=True)


def grade(name):
    return f'lut3d=file={name}.cube:interp=tetrahedral'


def preview():
    col, shot_w, shot_h = 396, 360, 640
    sheet = Image.new('RGB', (col * len(PALETTES) + 36, 1408), '#f4f5f9')
    title_face = ImageFont.truetype('C:/Windows/Fonts/msjh.ttc', 29)
    draw = ImageDraw.Draw(sheet)
    for column, (name, label) in enumerate(PALETTES.items()):
        write_cube(name)
        x = 36 + column * col
        draw.text((x + shot_w / 2, 48), label, font=title_face, fill='#243148', anchor='mm')
        for index, timecode in enumerate(SAMPLES):
            path = f'{name}-{index + 1}.png'
            run('-ss', timecode, '-i', str(SOURCE), '-frames:v', '1',
                '-vf', f'{grade(name)},scale={shot_w}:{shot_h}:flags=lanczos', path)
            if index < 2:
                with Image.open(OUT / path) as sample:
                    sheet.paste(sample, (x, 87 + index * 663))
    sheet.save(OUT / 'palette-comparison.png')


def render(name):
    lut = write_cube(name)
    partial = OUT / f'{name}-encoding.mp4'
    output = OUT / f'wnl-021-{name}-palette.mp4'
    start = time.perf_counter()
    run('-i', str(SOURCE), '-vf', f'{grade(name)},format=yuv420p',
        '-map', '0:v:0', '-map', '0:a:0', '-map', '0:s',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '4',
        '-c:a', 'copy', '-c:s', 'copy', '-movflags', '+faststart', partial.name)
    partial.replace(output)
    evidence = {
        'source_sha256': SOURCE_SHA256,
        'palette_script_sha256': sha(Path(__file__)),
        'lut_sha256': sha(lut),
        'video_sha256': sha(output),
        'palette': name,
        'seconds_to_encode': round(time.perf_counter() - start, 2),
    }
    (OUT / f'{name}-evidence.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(evidence, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('preview', *PALETTES))
    mode = parser.parse_args().mode
    if sha(SOURCE) != SOURCE_SHA256 or sha(FFMPEG) != FFMPEG_SHA256:
        raise ValueError('Unexpected source or FFmpeg digest')
    OUT.mkdir(parents=True, exist_ok=True)
    if mode == 'preview':
        preview()
    else:
        render(mode)


if __name__ == '__main__':
    main()
