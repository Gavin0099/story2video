"""U03-only revision evidence; original sources and v1 outputs are read-only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parents[1]
sys.path.insert(0, str(ORIGINAL.parent))
from run_local import OUT, REPO, pipeline as p


def main():
    data, _ = p.validate(HERE)
    out = OUT / data['story_id']
    old_out = OUT / 'uncanny-u03-v1'
    preservation = p.read(HERE / 'v1-preservation.json')
    for name, expected in preservation['source_files'].items():
        actual = HERE / 'record-v1.md' if name == 'record.md' else ORIGINAL / name
        assert p.digest(actual) == expected, name
    for name, expected in preservation['artifact_files'].items():
        assert p.digest(old_out / name) == expected, name
    report, manifest = p.read(out / 'qa/report.json'), p.read(out / 'manifest.json')
    assert all(report['checks'].values())
    assert p.digest(out / (data['story_id'] + '.mp4')) == report['master_sha256']
    for name, expected in manifest['inputs'].items():
        assert p.digest(HERE / name) == expected, name
    old_data = p.read(ORIGINAL / 'shots.json')
    assert data['narration'] == old_data['narration']
    assert data['question'] == old_data['question']
    assert p.digest(HERE / 'references.json') == p.digest(ORIGINAL / 'references.json')
    for name in ('reference.png', 'setup.png', 'resolution.png', 'brush.wav', 'click.wav'):
        assert p.digest(HERE / 'assets' / name) == p.digest(ORIGINAL / 'assets' / name)
    for cue in data['narration']:
        assert p.digest(HERE / cue['file']) == p.digest(ORIGINAL / cue['file'])
    retained_cuts = []
    for old, new in zip(old_data['shots'], data['shots']):
        if new['id'] != 'shot-09':
            assert new == old
            assert p.digest(out / 'cache' / (new['id'] + '.mp4')) == p.digest(old_out / 'cache' / (new['id'] + '.mp4'))
            retained_cuts.append(new['id'])
    assert p.digest(out / 'cache/shot-09.mp4') != p.digest(old_out / 'cache/shot-09.mp4')
    assert p.digest(out / 'cache/question.png') == p.digest(old_out / 'cache/question.png')
    assert p.digest(out / 'mix.wav') == p.digest(old_out / 'mix.wav')
    timeline = p.read(out / 'timeline.json')
    for lang, field in [('en', 'en'), ('zh-Hant', 'zh')]:
        sidecar = out / (data['story_id'] + '.' + lang + '.srt')
        assert sidecar.read_text(encoding='utf-8') == p.srt(timeline['captions'], field)
        assert p.digest(sidecar) == p.digest(old_out / ('uncanny-u03-v1.' + lang + '.srt'))
    # Source reveal declarations and measured cue ids, not ASR.
    revealing_ids = {c['id'] for c in data['narration'] if c['reveal']}
    revealing = [c for c in timeline['cues'] if c['id'] in revealing_ids]
    assert min(c['start'] for c in revealing) == 26
    assert all(c['start'] >= 26 for c in revealing)
    ledger, prompts = p.ledger_rows(out), p.read(HERE / 'image-prompts-used.json')
    assert len(ledger) == len(prompts) == 1
    assert p.read(HERE / 'editorial.json')['viewer_gate'] == 'HUMAN_TEST_PENDING'
    assert (HERE / 'images.jsonl').read_bytes() == (out / 'images.jsonl').read_bytes()
    for receipt, prompt in zip(ledger, prompts):
        assert receipt['status'] == 'accepted' and receipt['attempt'] == 1
        assert receipt['result_sha256'] == p.digest(HERE / receipt['result_filename'])
        assert receipt['prompt_sha256'] == prompt['prompt_sha256'] == hashlib.sha256(prompt['prompt'].encode()).hexdigest()
    samples = [p.read(out / 'qa' / shot['id'] / 'samples.json') for shot in data['shots']]
    assert sum(len(s['times']) for s in samples) == 164
    assert all(s['minimum_fps'] >= 4 for s in samples)
    tools = p.Tools(out)
    audio_hashes = []
    for folder, sid in [(old_out, 'uncanny-u03-v1'), (out, data['story_id'])]:
        audio_hashes.append(tools.run('ffmpeg', p.FF + ['-i', folder / (sid + '.mp4'), '-map', '0:a:0', '-vn', '-c:a', 'pcm_s16le', '-f', 'hash', '-hash', 'sha256', '-']).strip())
    assert audio_hashes[0] == audio_hashes[1]
    summary = {
        **p.read(HERE / 'editorial.json'), 'id': data['story_id'],
        'master': (out / (data['story_id'] + '.mp4')).relative_to(REPO).as_posix(),
        'sha256': report['master_sha256'], 'duration': timeline['shots'][-1]['end'],
        'status': 'FIX-CANDIDATE pending independent review, not uploaded',
        'engineering': report['engineering'], 'imagegen_requests': 1,
        'generated_bitmaps': 1, 'correction_calls': 0, 'new_tts_calls': 0,
        'encode_count': p.read(out / 'cost.json')['encode_count'],
        'render_wall_seconds': p.read(out / 'cost.json')['wall_seconds'],
        'market_acceptance': 'NOT_TESTED',
    }
    p.save(out / 'production-summary.json', summary)
    scanned = []
    candidates = [*HERE.rglob('*'), *out.rglob('*'), ORIGINAL / 'record.md', ORIGINAL.parent / 'README.md', ORIGINAL.parent.parent / 'README.md']
    for path in candidates:
        if not path.is_file() or path.suffix not in ('.py', '.md', '.json', '.jsonl', '.srt', '.txt'):
            continue
        if any(part in ('pytest-temp', 'pytest-cache') for part in path.parts):
            continue
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|[/\\]Users[/\\]', text), path.name
        assert all(not line.endswith((' ', '\t')) for line in text.splitlines()), path.name
        scanned.append(path.relative_to(REPO).as_posix())
    evidence = {
        'at': datetime.now(timezone.utc).isoformat(),
        'base_git_sha': preservation['base_git_sha'],
        'master': (out / (data['story_id'] + '.mp4')).relative_to(REPO).as_posix(),
        'master_sha256': report['master_sha256'], 'duration': timeline['shots'][-1]['end'],
        'v1_source_files_preserved': len(preservation['source_files']),
        'v1_artifact_files_preserved': len(preservation['artifact_files']),
        'unchanged_encoded_cuts': retained_cuts, 'changed_cut': 'shot-09',
        'question_plate': 'IDENTICAL', 'seven_narration_wavs': 'IDENTICAL',
        'mix_wav': 'IDENTICAL', 'decoded_audio_hash': audio_hashes[0],
        'both_sidecars': 'IDENTICAL_TO_V1_AND_EXACT_TIMELINE_MATCH',
        'first_revealing_narration_seconds': 26,
        'imagegen_calls': 1, 'correction_calls': 0, 'imagegen_cost': 'UNKNOWN',
        'dense_decoded_samples': 164, 'dense_strips': 10, 'minimum_fps': 30 / 7,
        'technical_qa': report['engineering'], 'personal_path_grep': 'PASS',
        'text_files_scanned': len(scanned), 'story_quality_gate': 'PENDING',
        'storyboard_quality_gate': 'PENDING', 'viewer_gate': 'HUMAN_TEST_PENDING',
        'independent_review': 'PENDING', 'market_acceptance': 'NOT_TESTED',
    }
    p.save(out / 'verification.json', evidence)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
