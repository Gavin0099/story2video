"""Create each input freeze once. Changed inputs require a new revision."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
common=[
 'experiments/science-shorts/batch-20261121/scripts-final.json',
 'experiments/science-shorts/batch-20261121/source-cards.json',
 'experiments/science-shorts/batch-20261121/editorial-gate.json',
 'experiments/science-shorts/batch-20261121/reviews/fact-visual-v1.json',
 'experiments/science-shorts/batch-20261121/reviews/reader-a-v1.json',
 'experiments/science-shorts/batch-20261121/reviews/reader-b-v1.json',
 'experiments/episode-02-73h/render-manifest.json',
 'experiments/science-shorts/ice-visual-v2/render.py',
 'experiments/science-shorts/sky-space-visual-v2/image-prompts.json',
 'experiments/science-shorts/sky-space-visual-v2/visual-plan.md',
]
for episode in ('sky','space'):
 target=HERE/f'{episode}-inputs.json'
 if target.exists(): raise SystemExit(f'{target.name} exists; do not refresh review inputs silently')
 extra=[f'artifacts/science-shorts/batch-20261121/{episode}/'+name for name in ('timeline.json','narration.wav')]
 extra += [f'artifacts/science-shorts/sky-space-visual-v2/assets/{name}' for name in (['sky-day.png','sky-sunset.png'] if episode=='sky' else ['astronaut.png'])]
 records={}
 for relative in common+extra:
  path=ROOT/relative
  with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
  records[relative]={'size':path.stat().st_size,'sha256':digest}
 target.write_text(json.dumps({'revision':episode+'-visual-v2','files':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(episode,'frozen',len(records),'inputs')
