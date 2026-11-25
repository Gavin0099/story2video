"""Create isolated revision inputs without changing v1 or other stories."""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
P01 = HERE.parents[1]
REPO = HERE.parents[6]
OUT = REPO / 'artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v2'

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__ == '__main__':
    assert not (HERE/'shots.json').exists()
    assert not OUT.exists()
    (HERE/'assets').mkdir(exist_ok=True)
    OUT.mkdir(parents=True)
    originals = {p.relative_to(P01).as_posix():sha(p) for p in P01.rglob('*') if p.is_file() and 'revisions' not in p.relative_to(P01).parts and p.name != 'record.md'}
    save(OUT/'v1-preservation.json', originals)
    for name in ('reference.png','shots-a-v2.png','shots-b.png','tick.wav'):
        shutil.copyfile(P01/'assets'/name, HERE/'assets'/name)
    data=json.loads((P01/'shots.json').read_text(encoding='utf-8'))
    refs=json.loads((P01/'references.json').read_text(encoding='utf-8'))
    data['story_id']='puzzle-p01-static-v2'
    data['sheets']['mechanism']={'file':'assets/mechanism-reference.png','columns':1,'rows':1,'edge_px':0}
    data['sheets']['fix']={'file':'assets/fix.png','columns':2,'rows':2,'edge_px':2}
    for line in data['narration']:
        name=line['id']+'.wav'
        shutil.copyfile(REPO/'artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/cache/voice'/name, HERE/'assets'/name)
        line['file']='assets/'+name
    replacements={3:0,4:1,8:2,9:2,10:3}
    for i, cell in replacements.items():
        data['shots'][i]['source']={'sheet':'fix','cell':cell,'crop':[0,0,1,1]}
        data['shots'][i]['camera']={'zoom':[1,1.015],'from':[.5,.5],'to':[.5,.5]}
    data['shots'][8]['conveys']='Full loaded route: moving pan knot through sliding counter hole to toe; cylinder independently supported.'
    data['shots'][9]['conveys']='Same full loaded assembly held for inspection; toe tension loads the moving pan.'
    data['shots'][10]['conveys']='Matched cut assembly: thread gap below guide, raised pan, lower needle, same three gold pieces.'
    # Remove erroneous background cylinder from final confrontation by a source crop.
    data['shots'][11]['source']['crop']=[0,0,.68,1]
    for rid in ('scale','cylinder'):
        item=next(r for r in refs['items'] if r['id']==rid)
        item['canonical']={'sheet':'mechanism','cell':0,'crop':[0,0,1,1]}
    for r in refs['items']:
        if r['id']=='cylinder':
            r['invariants']=['one brass cylinder with empty ring independently on low shelf right of thread','no thread connection; vertical thread passes behind in clue perspective; shelf ends before thread corridor']
    refs['items'].append({'id':'thread-route','kind':'prop','invariants':['A knot on MOVING pan underside eyelet -> vertical thread -> G smooth sliding hole in horizontal countertop -> vertical thread -> B toe loop','A and B are only endpoints; G never anchors; no other guides, horizontal runs or edge attachment','loaded: toe down, pan lower, needle upper-right; cut below G: gap, pan raised, needle lower-left; coins unchanged'],'canonical':{'sheet':'mechanism','cell':0,'crop':[0,0,1,1]},'appears_in':['shot-01','shot-03','shot-04','shot-05','shot-06','shot-08','shot-09','shot-10','shot-11']})
    for shot in data['shots']:
        if shot['id'] in refs['items'][-1]['appears_in']:
            shot['required_references'].append('thread-route')
    save(HERE/'shots.json',data)
    save(HERE/'references.json',refs)
    text=(P01/'story.md').read_text(encoding='utf-8')
    text+='\n## v2 mechanism revision\n\nSee mechanism.md, defined before generation. Shots 04/05 use corrected vertical route details; shots 09/10 hold the same full loaded route; shot 11 is the matched post-cut state. Shot 12 removes the incorrect countertop cylinder from view. English and Traditional Chinese narration, question and cue times are unchanged. Existing narration WAVs are reused. No reveal view before 27 s. FIX-CANDIDATE pending independent review, not uploaded; gates remain PENDING / HUMAN_TEST_PENDING.\n'
    (HERE/'story.md').write_text(text,encoding='utf-8')
    print('Created P01 v2 inputs; v1 snapshot saved')
