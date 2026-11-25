"""P04 v4 only: contain narrow generated cells; reuse shared audio/render/QA."""
from pathlib import Path
import runpy
import shutil

from PIL import Image, ImageOps

STORY = Path(__file__).resolve().parent
ADAPTER = STORY.parents[2] / 'run.py'
pipeline = runpy.run_path(str(ADAPTER))['pipeline']
original_extract = pipeline.extract


def extract(story, data, source, output):
    if source['sheet'] != 'shots-b-v4':
        return original_extract(story, data, source, output)
    sheet = data['sheets'][source['sheet']]
    path = pipeline.local(story, sheet['file'])
    with Image.open(path) as image:
        box = pipeline.cell_box(image.size, sheet, source)
        cell = image.crop(box).convert('RGB')
        plate = ImageOps.pad(cell, (1080, 1920), Image.Resampling.LANCZOS,
                             color='#181818', centering=(.5, .5))
        plate.save(output)
    return {'sheet': source['sheet'], 'cell': source['cell'], 'pixel_crop': box,
            'sheet_sha256': pipeline.digest(path),
            'plate_sha256': pipeline.digest(output),
            'fit': 'contain with neutral side matte, no content retouch'}


if __name__ == '__main__':
    pipeline.extract = extract
    pipeline.validate(STORY)
    out = pipeline.output_for('puzzle-p04-static-v4')
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STORY / 'images.jsonl', out / 'images.jsonl')
    pipeline.run_story(STORY)
    print(out.relative_to(pipeline.REPO).as_posix())
