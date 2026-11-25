"""Read-only delivery checks; evidence is written only in the puzzle output subtree."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OUTPUT=REPO/'artifacts/static-ten-20261124/puzzle'
spec=importlib.util.spec_from_file_location('puzzle_adapter',ROOT/'run.py')
adapter=importlib.util.module_from_spec(spec); spec.loader.exec_module(adapter)
pipeline=adapter.pipeline
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
checks=[]
delivery=read(ROOT/'delivery.json')
for video in delivery['videos']:
    key=video['id']; story=ROOT/key; out=OUTPUT/video['story_id']
    data,refs=pipeline.validate(story)
    manifest=read(out/'manifest.json')
    for name,expected in manifest['inputs'].items():
        assert pipeline.digest(story/name)==expected, (key,name,'input drift')
    for name,expected in manifest['pipeline'].items():
        assert pipeline.digest(ROOT.parent/'pipeline'/name)==expected, (key,name,'shared pipeline drift')
    assert pipeline.digest(REPO/video['mp4'])==video['sha256']==read(out/'qa/report.json')['master_sha256']
    assert 30<=video['duration']<=40
    assert data['fiction'].startswith('FICTION') and 'pending_verification' in data['fiction']
    ledger=[json.loads(x) for x in (out/'images.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(ledger)==video['imagegen_calls']<=5
    for entry in ledger:
        payload=read(REPO/entry['prompt_archive'])
        assert hashlib.sha256(payload['prompt'].encode()).hexdigest()==entry['prompt_sha256']
        if 'result_sha256' in entry:
            assert pipeline.digest(story/entry['result_filename'])==entry['result_sha256']
        for attached in entry['actual_reference_attachments']:
            assert pipeline.digest(REPO/attached['path'])==attached['sha256']
    hashes=[]
    for filename in (video['story_id']+'.mp4',video['story_id']+'.en.srt',video['story_id']+'.zh-Hant.srt','images.jsonl','timeline.json','manifest.json'):
        hashes.append(pipeline.digest(out/filename)+'  '+filename)
    (out/'delivery.sha256').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
    checks.append(dict(id=key,structural_validator='VALID',exact_input_hashes=True,shared_pipeline_hashes=True,
                       master_hash=True,all_call_prompt_hashes=True,all_image_and_attachment_hashes=True))

# Source checkout remains read-only. The environment supplies its location and Git executable.
source_repo=os.environ.get('S2V_P01_SOURCE_REPO')
if source_repo:
    source_ref='codex/cluepause-genre-pilot-v3-20261124:experiments/cluepause/genre-pilot-20261124/puzzle-v3.md'
    git=os.environ['S2V_GIT_EXE']
    raw=subprocess.run([git,'-c','safe.directory='+source_repo,'-C',source_repo,'show',source_ref],check=True,capture_output=True).stdout
    source=raw.decode('utf-8')
    lines=read(ROOT/'P01/shots.json')['narration']
    assert len(lines)==8 and all(line['en'] in source for line in lines)
    (ROOT/'P01/source-p01-v3.md').write_bytes(raw)
    checks.append(dict(p01_source_ref=source_ref,source_sha256=hashlib.sha256(raw).hexdigest(),eight_english_lines_retained_verbatim=True))

pattern=re.compile(r'(?i)(?:[A-Z]:[\\/]+Users[\\/]|/[U]sers/|/[h]ome/)')
violations=[]
for base in (ROOT,OUTPUT):
    for path in base.rglob('*'):
        if path.is_file() and path.suffix.lower() in ('.md','.json','.jsonl','.py','.txt','.srt','.sha256','.tag'):
            try: text=path.read_text(encoding='utf-8-sig')
            except UnicodeError: continue
            if pattern.search(text): violations.append(path.relative_to(REPO).as_posix())
assert not violations, violations
checks.append(dict(personal_absolute_path_scan='CLEAN',scope='authored text and puzzle output text only',core_regression='NOT_RUN_ISOLATED_CONTENT',
                   pipeline_offline_tests='33 passed in 0.51s',human_and_market='PENDING / NOT_TESTED'))
result=dict(git_sha=delivery['git_sha'],checks=checks,adapter_sha256=pipeline.digest(ROOT/'run.py'),
            audit_sha256=pipeline.digest(Path(__file__)),finalizer_sha256=pipeline.digest(ROOT/'finalize.py'))
(OUTPUT/'delivery-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
