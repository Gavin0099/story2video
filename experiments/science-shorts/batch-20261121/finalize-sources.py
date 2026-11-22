"""Freeze reachable references; preserve exact reviewed narration and storyboard."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
original=root/'scripts-v1.json'
data=json.loads(original.read_text(encoding='utf-8'))
parent=hashlib.sha256(original.read_bytes()).hexdigest()
assert parent=='80e59d8eac55bb019cae40df840b38b107679cc5f97921798de3631d50db76f7'
def public_payload(value):
    return [{'id':e['id'],'cues':e['cues'],'visual_constraints':e['visual_constraints']} for e in value['episodes']]
public_before=public_payload(data)
space=next(e for e in data['episodes'] if e['id']=='space')
next(c for c in space['claims'] if c['id']=='c2')['source_urls'][0]='https://science.nasa.gov/ems/02_anatomy/'
data['revision']='v1-sources2'
data['parent_sha256']=parent
assert public_before==public_payload(data)
(root/'scripts-sources2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sky=next(e for e in data['episodes'] if e['id']=='sky')
sky['cues'][-1]['pause']=2.1
data['revision']='v1-sources2-timing1'
data['timing_change']='Sky measured 44.73 seconds; final non-speech hold increased 0.8→2.1 seconds. All public words, scene and visual instructions unchanged.'
def words(value):
    return [{'id':e['id'],'cues':[{k:v for k,v in c.items() if k!='pause'} for c in e['cues']],'visual_constraints':e['visual_constraints']} for e in value['episodes']]
assert words(json.loads(original.read_text(encoding='utf-8')))==words(data)
(root/'scripts-final.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Source metadata and final non-speech hold changed; exact public words and diagram instructions unchanged.')
