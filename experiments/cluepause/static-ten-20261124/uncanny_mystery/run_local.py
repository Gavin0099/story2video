"""Genre-local output routing; shared pipeline remains read-only."""
import importlib.util
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / 'artifacts/static-ten-20261124/uncanny_mystery'
for name in ('TMP', 'TEMP', 'TMPDIR', 'HF_HOME', 'XDG_CACHE_HOME', 'NUMBA_CACHE_DIR', 'UV_CACHE_DIR', 'PYTEST_DEBUG_TEMPROOT'):
    folder = OUT / ('tmp' if name in ('TMP', 'TEMP', 'TMPDIR', 'PYTEST_DEBUG_TEMPROOT') else 'cache') / name.lower()
    folder.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(folder)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
spec = importlib.util.spec_from_file_location('static_storyboard', HERE.parent / 'pipeline/static_storyboard.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)
pipeline.OUTPUTS = OUT
original_prompt = pipeline.build_prompt
def portrait_prompt(*args, **kwargs):
    payload = original_prompt(*args, **kwargs)
    if payload['reference_images']:
        payload['reference_images'] = ['prompts/references/canonical-sheet.png']
    payload['prompt'] += ('\nOUTPUT LAYOUT: portrait canvas aspect 27:32, exactly three columns by two rows of tall 9:16 photographs. '
                          'Six equal tall cells, row-major: 0 top left, 1 top middle, 2 top right, 3 bottom left, 4 bottom middle, 5 bottom right. '
                          'No gutters or divider lines. Every cell must be one complete single shot, not split. '
                          'Input images are canonical reference images for identity, geometry, material and scene only, not edit targets. '
                          'For an unused cell, repeat the last shot, without adding new events.')
    return payload
pipeline.build_prompt = portrait_prompt
original_export = pipeline.export_prompts
def export_with_sheet(story, supports_images):
    original_export(story, supports_images)
    if supports_images:
        data, _ = pipeline.validate(story)
        shutil.copyfile(story/data['sheets']['reference']['file'], pipeline.output_for(data['story_id'])/'prompts/references/canonical-sheet.png')
pipeline.export_prompts = export_with_sheet

if __name__ == '__main__':
    pipeline.main()
