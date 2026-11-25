"""Recover exact historical prompt payloads by matching already-recorded hashes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
spec=importlib.util.spec_from_file_location('puzzle_adapter',ROOT/'run.py')
adapter=importlib.util.module_from_spec(spec); spec.loader.exec_module(adapter)
engine=adapter.pipeline

for key in ('P01','P02','P03','P04'):
    story=ROOT/key
    data=json.loads((story/'shots.json').read_text(encoding='utf-8'))
    refs=json.loads((story/'references.json').read_text(encoding='utf-8'))
    out=engine.output_for(data['story_id'])
    ledger_path=out/'images.jsonl'
    rows=[json.loads(x) for x in ledger_path.read_text(encoding='utf-8-sig').splitlines()]
    (out/'call-prompts').mkdir(exist_ok=True)
    for i,row in enumerate(rows):
        sheet=row['sheet']
        if row['status']=='input_rejected':
            sheet='shots-a'
            row['prompt_sha256']=rows[i+1]['prompt_sha256']
        candidates=[]
        for old_refs in (False,True):
            r=copy.deepcopy(refs)
            if old_refs and key=='P03':
                for item in r['items']:
                    if item['id']=='wire': item['invariants']=[v for v in item['invariants'] if not v.startswith('canonical mobile')]
            if old_refs and key=='P04':
                for n,item in enumerate(r['items']):
                    item['canonical'].update(cell=n,crop=[0,0,1,1])
                    if item['id']=='bag': item['invariants']=[v for v in item['invariants'] if not v.startswith('before cut freely')]
            for old_shots in (False,True):
                d=copy.deepcopy(data)
                if old_shots and key=='P01':
                    for shot in d['shots']: shot['prompt']=shot['prompt'].split(' CRITICAL:')[0]
                if old_shots and key=='P02':
                    d['shots'][6]['prompt']=d['shots'][6]['prompt'].split(' Match fully blackened')[0]
                    d['shots'][7]['prompt']=d['shots'][7]['prompt'].split(' The printing block remains')[0]
                if old_shots and key=='P04':
                    d['shots'][5]['prompt']='REVEAL low reverse behind bench: tan canvas sandbag black cross stitching now rests on floor, tied to RIGHT cream rope from high pulley; blue severed ends at left bench cleat. No human pulling.'
                for builder in (adapter.original_prompt,adapter.puzzle_prompt):
                    payload=builder(d,r,sheet,sheet!='reference')
                    payload['prompt_sha256']=hashlib.sha256(payload['prompt'].encode()).hexdigest()
                    candidates.append(payload)
        matches=[p for p in candidates if p['prompt_sha256']==row['prompt_sha256']]
        if not matches:
            raise ValueError(f'{key} call {i+1}: exact historical prompt not recovered')
        payload=matches[0]
        if sheet=='reference':
            attached=[]
        elif row['status']=='input_rejected':
            attached=[out/p for p in payload['reference_images']]
        elif key in ('P01','P04'):
            attached=[story/'assets/reference.png']
        elif key=='P02' and row['result_filename']=='assets/shots-b-v2.png':
            attached=[story/'assets/reference.png',story/'assets/shots-a.png']
        else:
            attached=[out/p for p in payload['reference_images']]
        receipt=[dict(path=p.relative_to(REPO).as_posix(),sha256=engine.digest(p)) for p in attached]
        payload['actual_reference_attachments']=receipt
        archive=out/'call-prompts'/f'{i+1:02}-{sheet}.json'
        engine.save(archive,payload)
        row['prompt_archive']=archive.relative_to(REPO).as_posix()
        row['actual_reference_attachments']=receipt
        row['tool']='image_gen.imagegen'
        row['acceptance_scope']='selected for rendering; not story/storyboard quality approval' if row['status']=='accepted' else 'not selected for rendering'
    ledger_path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
    print(f'{key}: {len(rows)} exact prompt hashes recovered and attachments recorded')
