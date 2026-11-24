"""Puzzle-only adapter: shared implementation, isolated outputs and runtime caches."""
import importlib.util
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUTPUT = REPO / 'artifacts/static-ten-20261124/puzzle'
for name in ('tmp', 'cache'):
    (OUTPUT / name).mkdir(parents=True, exist_ok=True)
os.environ.update(TEMP=str(OUTPUT/'tmp'), TMP=str(OUTPUT/'tmp'),
                  HF_HOME=str(OUTPUT/'cache/huggingface'),
                  XDG_CACHE_HOME=str(OUTPUT/'cache'),
                  NUMBA_CACHE_DIR=str(OUTPUT/'cache/numba'),
                  UV_CACHE_DIR=str(OUTPUT/'cache/uv'),
                  PYTHONDONTWRITEBYTECODE='1')
sys.path.append(str(Path(sys.base_prefix)/'Lib/site-packages'))
spec = importlib.util.spec_from_file_location('static_pipeline', HERE.parent/'pipeline/static_storyboard.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)
pipeline.OUTPUTS = OUTPUT
original_prompt = pipeline.build_prompt
def puzzle_prompt(data, refs, sheet_id, supports_images=False):
    payload = original_prompt(data, refs, sheet_id, supports_images)
    payload['prompt'] += '\nCRITICAL PORTRAIT CROP SAFETY: keep every essential object, face and evidence word entirely inside the CENTRAL 50 PERCENT of each cell width. Outer quarter on each side is expendable setting. Photograph the objects smaller if needed. No letters may be clipped by this central vertical crop.'
    if payload['purpose'] == 'shot_sheet':
        used = {s['source']['cell'] for s in data['shots'] if s['source']['sheet'] == sheet_id}
        sheet = data['sheets'][sheet_id]
        for index in range(sheet['columns']*sheet['rows']):
            if index not in used:
                payload['prompt'] += f'\nCELL {index}: unused atmospheric close-up of the empty tabletop in this same set. No people, lettering or plot props. Do not move any assigned shot into this cell.'
    return payload
pipeline.build_prompt = puzzle_prompt
if __name__ == '__main__':
    pipeline.main()
