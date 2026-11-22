"""Recompute the science editorial decision from independent frozen evidence."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def load(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
policy=load('gate-policy.json')
script=load('scripts-final.json')
original=load('scripts-v1.json')
audit=load('reviews/fact-visual-v1.json')
assert audit['script_sha256']==sha(ROOT/'scripts-final.json')
assert audit['renderer_sha256']==sha(ROOT.parent/'render.py')
assert audit['source_cards_sha256']==sha(ROOT/'source-cards.json')
assert audit['gate_policy_sha256']==sha(ROOT/'gate-policy.json')
assert audit['fact_pass'] and audit['visual_plan_pass'] and not audit['critical_defects']
assert script['parent_sha256']==sha(ROOT/'scripts-v1.json')
def public_words(data):
    return [(e['id'],[{k:v for k,v in c.items() if k!='pause'} for c in e['cues']],e['visual_constraints']) for e in data['episodes']]
assert public_words(script)==public_words(original)
for final,initial in zip(script['episodes'],original['episodes']):
    for index,(a,b) in enumerate(zip(final['cues'],initial['cues'])):
        assert a['pause']==(2.1 if final['id']=='sky' and index==len(final['cues'])-1 else b['pause'])
publishers={s['url']:s['publisher'] for s in load('source-cards.json')['sources']}
readers=[load(f'reviews/reader-{r}-v1.json') for r in ['a','b']]
items=[]
for episode in script['episodes']:
    for claim in episode['claims']:
        assert len({publishers[url] for url in claim['source_urls']})>=2
    scores=[]
    for reader in readers:
        record=next(r for r in reader if r['id'].lower()==episode['id'])
        assert set(record['scores'])==set(policy['rubric'])
        assert all(0<=v<=policy['rubric'][k] for k,v in record['scores'].items())
        total=sum(record['scores'].values())
        assert total==record['total'] and total>=policy['minimum_score_each_reader']
        assert not record['critical_defects']
        scores.append(total)
    items.append({'id':episode['id'],'scores':scores,'critical_defects':[]})
files=['fact-visual-v1.json','reader-a-v1.json','reader-b-v1.json','reader-a-protocol.md','reader-b-protocol.md']
gate={'status':'PASS','scope':'local production only; not human/publish/market approval',
      'script_sha256':sha(ROOT/'scripts-final.json'),'reviewed_original_sha256':sha(ROOT/'scripts-v1.json'),
      'renderer_sha256':sha(ROOT.parent/'render.py'),'fact_pass':True,'visual_plan_pass':True,
      'episodes':items,'review_files':[{'path':p,'sha256':sha(ROOT/'reviews'/p)} for p in files]}
(ROOT/'editorial-gate.json').write_text(json.dumps(gate,indent=2)+'\n',encoding='utf-8')
print(json.dumps(items))
