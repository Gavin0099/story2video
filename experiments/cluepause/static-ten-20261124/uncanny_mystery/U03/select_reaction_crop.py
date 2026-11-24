"""Initial plate selection: keep the pre-reveal reaction on face and frosted pane."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'shots.json').read_text(encoding='utf-8'))
shot=data['shots'][6]
old=shot['conveys']
shot['source']['crop']=[0,0,1,.42]
shot['required_references']=['man','kitchen']
shot['conveys']='His concentrated expression turns down toward the counter; part of the soft figure remains behind him, while source objects stay below this initial portrait crop.'
refs=json.loads((HERE/'references.json').read_text(encoding='utf-8'))
for item in refs['items']:
    item['appears_in']=[s['id'] for s in data['shots'] if item['id'] in s['required_references']]
for name,value in [('shots.json',data),('references.json',refs)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text=(HERE/'story.md').read_text(encoding='utf-8').replace(old,shot['conveys'])
text+='\nInitial extraction choice for shot-07: crop [0, 0, 1, 0.42] selects face and pane instead of repeating the complete arrangement before the 26-second reveal. This is the first plate assignment before any encode, not an additional ImageGen correction or a second master. The complete physical relationship remains visible at the reveal.\n'
(HERE/'story.md').write_text(text,encoding='utf-8')
