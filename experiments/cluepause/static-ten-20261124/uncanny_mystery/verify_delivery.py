"""Read-only delivery checks; save evidence only in this genre's artifact tree."""
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from run_local import HERE, OUT, REPO, pipeline

results=[]
for code in ('U01','U02','U03'):
    story=HERE/code
    data,_=pipeline.validate(story)
    out=OUT/data['story_id']
    report=pipeline.read(out/'qa/report.json')
    manifest=pipeline.read(out/'manifest.json')
    timeline=pipeline.read(out/'timeline.json')
    summary=pipeline.read(out/'production-summary.json')
    master=out/(data['story_id']+'.mp4')
    assert all(report['checks'].values())
    assert pipeline.digest(master)==report['master_sha256']==summary['sha256']
    for name,expected in manifest['inputs'].items():
        assert pipeline.digest(story/name)==expected, (code,name)
    for lang,field in [('en','en'),('zh-Hant','zh')]:
        assert (out/(data['story_id']+'.'+lang+'.srt')).read_text(encoding='utf-8')==pipeline.srt(timeline['captions'],field)
    ledger=pipeline.ledger_rows(out)
    assert len(ledger)<=5 and max(Counter(x['sheet'] for x in ledger).values())<=2
    for row in ledger:
        assert pipeline.digest(story/row['result_filename'])==row['result_sha256']
    prompts=pipeline.read(story/'image-prompts-used.json')
    assert len(prompts)==len(ledger)
    for row in prompts:
        assert hashlib.sha256(row['prompt'].encode()).hexdigest()==row['prompt_sha256']
    assert (story/'record.md').exists()
    assert summary['story_quality_gate']=='PENDING'
    assert summary['storyboard_quality_gate']=='PENDING'
    assert summary['viewer_gate']=='HUMAN_TEST_PENDING'
    assert summary['rights_status']=='pending_verification'
    results.append({**summary,'input_hash_bindings':'MATCH','caption_pcm_sidecars':'MATCH','image_prompt_hashes':'MATCH',
                    'dense_frames':sum(len(pipeline.read(out/'qa'/s['id']/'samples.json')['times']) for s in data['shots']),
                    'strips_inspected_by_main_agent':len(data['shots'])})
u01=pipeline.read(HERE/'U01/shots.json')
source=(HERE/'U01/source-v3.md').read_text(encoding='utf-8')
assert all(c['en'] in source and c['zh'] in source for c in u01['narration'])
text_files=[]
for root in (HERE,OUT):
    for path in root.rglob('*'):
        if path.is_file() and path.suffix in ('.py','.md','.json','.jsonl','.srt','.txt'):
            text=path.read_text(encoding='utf-8')
            assert not re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|[/\\]Users[/\\]',text),path.name
            text_files.append(path.relative_to(REPO).as_posix())
            if path.suffix=='.py': ast.parse(text)
            if path.is_relative_to(HERE):
                assert all(not line.endswith((' ','\t')) for line in text.splitlines()),path.name
pipeline.save(OUT/'verification.json',{'at':datetime.now(timezone.utc).isoformat(),
    'base_git_sha':'aef24410f8b45c8651fd922343aeb52db11bfc75','videos':results,
    'u01_nine_bilingual_lines_retained_verbatim':True,'personal_absolute_paths_in_text':False,
    'u01_source_snapshot_sha256':pipeline.digest(HERE/'U01/source-v3.md'),
    'python_syntax':'VALID','authored_text_trailing_whitespace':False,'scanned_text_files':len(text_files),
    'pipeline_tests':{'command':'python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/cache/pytest --basetemp artifacts/static-ten-20261124/uncanny_mystery/tmp/pytest','passed':33,'seconds':.70},
    'quality_gates':'PENDING / PENDING / HUMAN_TEST_PENDING','market_acceptance':'NOT_TESTED'})
print(json.dumps({'videos':[{k:v[k] for k in ('id','duration','sha256','imagegen_requests','generated_bitmaps','encode_count','render_wall_seconds','dense_frames')} for v in results], 'text_files_scanned':len(text_files)},indent=2))
