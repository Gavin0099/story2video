"""Freeze local pilot inputs once; never silently refresh an existing manifest."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
target=HERE/'inputs.json'
if target.exists():
    raise SystemExit('inputs.json already exists; create a new revision for changed inputs')
files=[
    'experiments/science-shorts/batch-20261121/scripts-final.json',
    'experiments/science-shorts/batch-20261121/source-cards.json',
    'experiments/science-shorts/batch-20261121/editorial-gate.json',
    'experiments/science-shorts/batch-20261121/reviews/fact-visual-v1.json',
    'experiments/science-shorts/batch-20261121/reviews/reader-a-v1.json',
    'experiments/science-shorts/batch-20261121/reviews/reader-b-v1.json',
    'experiments/episode-02-73h/render-manifest.json',
    'artifacts/science-shorts/batch-20261121/ice/timeline.json',
    'artifacts/science-shorts/batch-20261121/ice/narration.wav',
    'artifacts/science-shorts/ice-visual-v2/assets/glass.png',
    'artifacts/science-shorts/ice-visual-v2/assets/ice.png',
]
records={}
for relative in files:
    path=ROOT/relative
    with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    records[relative]={'size':path.stat().st_size,'sha256':digest}
target.write_text(json.dumps({'revision':'ice-visual-v2','files':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Frozen',len(records),'inputs')
