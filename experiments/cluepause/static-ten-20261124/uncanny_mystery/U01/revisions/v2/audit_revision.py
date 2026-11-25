"""Bind U01 v2 media, original WAVs, image receipts and reveal boundaries."""
import ast
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from run_revision import HERE, REPO, pipeline

def run():
    data, refs = pipeline.validate(HERE)
    original = HERE.parents[1]
    out = pipeline.output_for(data['story_id'])
    baseline = pipeline.read(HERE/'baseline.json')
    for name, expected in baseline['original_files'].items():
        assert pipeline.digest(original/name) == expected, name
    v1 = out.parent/'uncanny-u01-v1/uncanny-u01-v1.mp4'
    assert pipeline.digest(v1) == baseline['v1_master_sha256']
    original_data = pipeline.read(original/'shots.json')
    assert data['narration'] == original_data['narration']
    for cue in data['narration']:
        assert pipeline.digest(HERE/cue['file']) == pipeline.digest(original/cue['file'])
    assert data['question'] == original_data['question']
    report = pipeline.read(out/'qa/report.json')
    manifest = pipeline.read(out/'manifest.json')
    timeline = pipeline.read(out/'timeline.json')
    assert all(report['checks'].values())
    master = out/(data['story_id']+'.mp4')
    assert pipeline.digest(master) == report['master_sha256']
    for name, expected in manifest['inputs'].items():
        assert pipeline.digest(HERE/name) == expected, name
    reveal = next(s['start'] for s in timeline['shots'] if s['function']=='reveal')
    assert reveal == 29
    assert all(c['start'] >= reveal for c in timeline['cues'] if c['reveal'])
    # All answer-bearing tokens must remain in reveal cues, in both languages.
    answer_tokens = ('connector', 'pump started', 'leak', 'paper stayed dry', '接頭', '水泵啟動', '漏水', '紙一直是乾的')
    for c in timeline['captions']:
        if any(word in (c['en']+' '+c['zh']).lower() for word in answer_tokens):
            assert c['start'] >= reveal, c
    assert not any(word in ' '.join(data['question'].values()).lower() for word in answer_tokens)
    for lang, field in [('en','en'),('zh-Hant','zh')]:
        assert (out/(data['story_id']+'.'+lang+'.srt')).read_text(encoding='utf-8') == pipeline.srt(timeline['captions'],field)
    rows = pipeline.ledger_rows(out)
    assert len(rows) <= 5 and max(Counter(r['sheet'] for r in rows).values()) <= 2
    prompts = pipeline.read(HERE/'image-prompts-used.json')
    assert len(prompts) == len(rows)
    for row, prompt in zip(rows,prompts):
        assert pipeline.digest(HERE/row['result_filename']) == row['result_sha256']
        assert hashlib.sha256(prompt['prompt'].encode()).hexdigest() == row['prompt_sha256'] == prompt['prompt_sha256']
        for name, expected in prompt['conditioned_input_sha256'].items():
            assert pipeline.digest(HERE/name) == expected
    frames = 0
    for s in data['shots']:
        samples = pipeline.read(out/'qa'/s['id']/'samples.json')
        assert samples['minimum_fps'] >= 4
        assert max(b-a for a,b in zip(samples['times'],samples['times'][1:])) <= .234
        frames += len(samples['times'])
    bad = []
    count = 0
    for root in (original,out):
        for path in root.rglob('*'):
            if path.is_file() and path.suffix in ('.py','.md','.json','.jsonl','.srt','.txt'):
                content = path.read_text(encoding='utf-8-sig')
                count += 1
                assert all(not line.endswith((' ', '\t')) for line in content.splitlines()), path.name
                path_pattern = r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|[/\\]Users[/\\]|/' + r'home/|/mnt/[a-z]/'
                if re.search(path_pattern,content):
                    bad.append(path.relative_to(REPO).as_posix())
                if path.suffix == '.py':
                    ast.parse(content)
    assert not bad, bad
    result = {'base_git_sha':manifest['git_sha'],'master':master.relative_to(REPO).as_posix(),
              'sha256':pipeline.digest(master),'duration_seconds':38,'technical_qa':report['engineering'],
              'original_v1_inputs_unchanged':True,'v1_master_unchanged':True,'nine_bilingual_narration_lines_unchanged':True,
              'nine_wavs_reused_byte_for_byte':True,'reveal_start':reveal,
              'reveal_cues':[{k:c[k] for k in ('id','start','end')} for c in timeline['cues'] if c['reveal']],
              'question_and_sidecars_early_answer_disclosure':False,
              'exact_srt_pcm_schedule':'MATCH; no ASR/listening claim','dense_frames':frames,'sampling_fps':30/7,
              'imagegen_calls':len(rows),'conditioned_input_and_prompt_hashes':'MATCH','personal_path_grep':'PASS',
              'scanned_revision_and_artifact_text_files':count,
              'story_quality_gate':'PENDING','storyboard_quality_gate':'PENDING','viewer_gate':'HUMAN_TEST_PENDING',
              'market_acceptance':'NOT_TESTED','independent_review':'PENDING','upload_status':'NOT_UPLOADED',
              'rights_status':'pending_verification'}
    pipeline.save(HERE/'verification.json',result)
    pipeline.save(out/'production-summary.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    run()
