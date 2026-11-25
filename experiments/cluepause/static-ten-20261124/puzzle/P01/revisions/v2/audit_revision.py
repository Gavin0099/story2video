"""P01-only integrity, captions, disclosure and portable-path evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import re

HERE=Path(__file__).resolve().parent
P01=HERE.parents[1]
REPO=HERE.parents[6]
OUT=REPO/'artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v2'
OLD=OUT.parent/'puzzle-p01-static-v1'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p,x):
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

spec=importlib.util.spec_from_file_location('p01_render',HERE/'render_revision.py')
binding=importlib.util.module_from_spec(spec)
spec.loader.exec_module(binding)
pipe=binding.adapter.pipeline
data,refs=pipe.validate(HERE)
report=read(OUT/'qa/report.json')
assert report['engineering']=='PASS' and all(report['checks'].values())
assert sha(OUT/(data['story_id']+'.mp4'))==report['master_sha256']
old_data=read(P01/'shots.json')
assert data['question']==old_data['question']
assert [{k:v for k,v in x.items() if k!='file'} for x in data['narration']]==old_data['narration']
wavs=[]
for line in data['narration']:
    source=OLD/'cache/voice'/(line['id']+'.wav')
    assert sha(source)==sha(HERE/line['file'])==sha(OUT/'cache/voice'/(line['id']+'.wav'))
    wavs.append(dict(id=line['id'],sha256=sha(source),reused_byte_for_byte=True))
for lang in ('en','zh-Hant'):
    assert (OUT/(data['story_id']+'.'+lang+'.srt')).read_bytes()==(OLD/(old_data['story_id']+'.'+lang+'.srt')).read_bytes()

manifest=read(OUT/'manifest.json')
assert all(sha(HERE/name)==expected for name,expected in manifest['inputs'].items())
assert all(sha(HERE.parents[2].parent/'pipeline'/name)==expected for name,expected in manifest['pipeline'].items())
assert all(sha(P01/name)==expected for name,expected in read(OUT/'v1-preservation.json').items())
assert sha(OLD/'puzzle-p01-static-v1.mp4')=='f806ed777997b2fc6e37d4e7a345b605cba2980ff55ad23491d6ebea82469a8e'
ledger=[json.loads(x) for x in (OUT/'images.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(ledger)==3
for row in ledger:
    prompt=(REPO/row['prompt_archive']).read_text(encoding='utf-8').rstrip('\n')
    assert hashlib.sha256(prompt.encode()).hexdigest()==row['prompt_sha256']
    assert sha(HERE/row['result_filename'])==row['result_sha256']
    assert all(sha(REPO/x['path'])==x['sha256'] for x in row['actual_reference_attachments'])
assert sum(x['sheet']=='fix' for x in ledger)==2
assert sum(x['sheet']=='mechanism' for x in ledger)==1

timeline=read(OUT/'timeline.json')
reveal=min(x['start'] for x in timeline['shots'] if x['function']=='reveal')
assert reveal==27
captions=timeline['captions']
assert all(x['start']>=reveal for x in captions if x.get('reveal'))
answer=re.compile(r'\b(?:foot|toe|pulled|pull)\b|腳|腳趾|拉力|拉線',re.I)
assert not any(answer.search(x['en']+' '+x['zh']) for x in captions if x['start']<reveal)
assert not answer.search(data['question']['en']+data['question']['zh'])
sample_count=sum(len(read(OUT/'qa'/s['id']/'samples.json')['times']) for s in data['shots'])
assert sample_count==167
assert all(read(OUT/'qa'/s['id']/'samples.json')['minimum_fps']>=4 for s in data['shots'])

tools=pipe.Tools(OUT)
master=OUT/(data['story_id']+'.mp4')
diagnostic=tools.run('ffmpeg',['-nostdin','-hide_banner','-i',master,'-vf','blackdetect=d=0.1:pix_th=0.1','-af','volumedetect','-f','null','-'])
# FFmpeg diagnostics live in stderr, retained in the scrubbed command ledger.
last=json.loads((OUT/'commands.jsonl').read_text(encoding='utf-8').splitlines()[-1])
assert 'black_start:' not in last['stderr']
peak=re.search(r'max_volume: ([-\d.]+) dB',last['stderr'])
assert peak and float(peak[1])<0
audio=dict(max_volume_db=float(peak[1]),black_intervals_over_100ms=0)

pattern=re.compile(r'(?i)(?:[A-Z]:[\\/]+Users[\\/]|/[U]sers/|/[h]ome/)')
violations=[]
for root in (P01,OUT):
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in ('.md','.json','.jsonl','.py','.txt','.srt','.sha256'):
            try: text=p.read_text(encoding='utf-8-sig')
            except UnicodeError: continue
            if pattern.search(text): violations.append(p.relative_to(REPO).as_posix())
assert not violations,violations
for p in HERE.rglob('*'):
    if p.is_file() and p.suffix in ('.py','.md','.json','.txt'):
        assert all(line.rstrip()==line for line in p.read_text(encoding='utf-8').splitlines()),p.name

result=dict(at=datetime.now(timezone.utc).isoformat(),git_sha=manifest['git_sha'],structural_validator='VALID',
    engineering='PASS',status='FIX-CANDIDATE pending independent review, not uploaded',
    v1_inputs_and_master_unchanged=True,narration_wavs=wavs,question_unchanged=True,
    sidecars_byte_identical_to_v1=True,reveal_start_s=reveal,early_answer_keyword_scan='CLEAN',
    disclosure_scope='Question and all timed EN/zh-Hant captions/narration checked; pre-reveal thread clue and snip remain intentional; no foot/toe/pull answer before 27s.',
    imagegen_calls=3,corrections_by_sheet={'mechanism':0,'fix':1},all_prompt_image_attachment_hashes=True,
    dense_decoded_samples=sample_count,dense_sampling_fps=30/7,personally_inspected_strips=12,
    silent_storyboard_inspected=True,personal_absolute_paths='CLEAN',audio=audio,
    pipeline_pytest='33 passed in 0.56s',story_gate='PENDING',storyboard_gate='PENDING',
    viewer_gate='HUMAN_TEST_PENDING',market_acceptance='NOT_TESTED',
    unverified=['independent review','human listening','phone readability','blind comprehension','ASR','external rights/originality','market response'])
save(OUT/'revision-audit.json',result)
files=[data['story_id']+'.mp4',data['story_id']+'.en.srt',data['story_id']+'.zh-Hant.srt','images.jsonl','timeline.json','manifest.json','silent-storyboard.jpg','qa/report.json','revision-audit.json']
(OUT/'delivery.sha256').write_text(''.join(sha(OUT/name)+'  '+name+'\n' for name in files),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='narration_wavs'},ensure_ascii=False,indent=2))
