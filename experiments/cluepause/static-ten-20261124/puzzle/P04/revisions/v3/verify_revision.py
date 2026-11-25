"""Offline P04 deliverable integrity checks; no generation, upload or mutation."""
from pathlib import Path
import hashlib
import json
import re

REPO = Path(__file__).resolve().parents[7]
STORY = Path(__file__).resolve().parent
OUTPUT = REPO / 'artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v3'
BASE = REPO / 'artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data = read(STORY / 'shots.json')
    manifest = read(OUTPUT / 'manifest.json')
    timeline = read(OUTPUT / 'timeline.json')
    report = read(OUTPUT / 'qa/report.json')
    assert all(report['checks'].values()) and report['engineering'] == 'PASS'
    master = OUTPUT / (data['story_id'] + '.mp4')
    assert digest(master) == report['master_sha256']
    for name, expected in manifest['inputs'].items():
        assert digest(STORY / name) == expected, name
    original = read(STORY.parents[1] / 'shots.json')
    assert data['question'] == original['question']
    for before, after in zip(original['narration'], data['narration'], strict=True):
        assert {k: v for k, v in after.items() if k != 'file'} == before
        assert digest(STORY / after['file']) == digest(BASE / 'cache/voice' / (after['id'] + '.wav'))
    for shot in (1, 2, 3, 4, 6):
        assert digest(OUTPUT / f'cache/shot-{shot:02}.png') == digest(BASE / f'cache/shot-{shot:02}.png')
    assert digest(OUTPUT / 'cache/shot-07.png') == digest(OUTPUT / 'cache/shot-08.png')
    for language in ('en', 'zh-Hant'):
        assert (OUTPUT / f'{data["story_id"]}.{language}.srt').read_bytes() == (BASE / f'puzzle-p04-static-v1.{language}.srt').read_bytes()
    assert digest(OUTPUT / 'mix.wav') == digest(BASE / 'mix.wav')
    reveal = next(s['start'] for s in timeline['shots'] if s['function'] == 'reveal')
    assert reveal == 27
    assert all(cue['start'] >= reveal for cue in timeline['cues'] if cue['reveal'])
    assert next(c for c in timeline['cues'] if c['id'] == 'line-06')['start'] == 27
    samples = []
    for shot in data['shots']:
        directory = OUTPUT / 'qa' / shot['id']
        schedule = read(directory / 'samples.json')
        assert schedule['minimum_fps'] >= 4
        assert len(schedule['times']) == len(list(directory.glob('*.png')))
        assert max(b-a for a, b in zip(schedule['times'], schedule['times'][1:])) <= .234
        samples += schedule['times']
    rows = [json.loads(line) for line in (OUTPUT / 'images.jsonl').read_text().splitlines()]
    assert len(rows) == 2
    assert [row['attempt'] for row in rows] == [1, 2]
    assert [row['status'] for row in rows] == ['rejected', 'accepted']
    for row in rows:
        assert digest(STORY / row['result_filename']) == row['result_sha256']
        prompt = read(REPO / row['prompt_archive'])
        assert hashlib.sha256(prompt['prompt'].encode()).hexdigest() == row['prompt_sha256']
        for attachment in row['actual_reference_attachments']:
            assert digest(REPO / attachment['path']) == attachment['sha256']
    baseline = read(REPO / 'artifacts/static-ten-20261124/puzzle/p04-fix/protected-before.json')
    changed = [name for name, expected in baseline.items() if (not (REPO / name).is_file() or digest(REPO / name) != expected) and not name.endswith('/P04/record.md')]
    own_changes = [name for name in changed if '/P04/' in name or '/puzzle-p04-static-v1/' in name]
    assert not own_changes, own_changes
    pattern = re.compile(r'(?:[A-Za-z]:[\\/](?:Users|home)[\\/]|/(?:Users|home)/)', re.I)
    extensions = {'.md', '.json', '.jsonl', '.txt', '.srt', '.py', '.sha256'}
    folders = [STORY.parents[1] / 'revisions', OUTPUT, OUTPUT.parent / 'puzzle-p04-static-v2', OUTPUT.parent / 'p04-fix']
    files = [p for folder in folders for p in folder.rglob('*') if p.is_file() and p.suffix in extensions]
    files += [STORY.parents[1] / 'record.md', STORY.parents[2] / 'README.md', STORY.parents[3] / 'README.md']
    hits = [p.relative_to(REPO).as_posix() for p in files if pattern.search(p.read_text(encoding='utf-8'))]
    assert not hits, hits
    whitespace = [p.relative_to(REPO).as_posix() for p in files if any(line.rstrip(' \t') != line for line in p.read_text(encoding='utf-8').splitlines())]
    assert not whitespace, whitespace
    before = read(OUTPUT.parent / 'p04-fix/readmes-before-edit.json')
    for name, text in before.items():
        without_row = lambda text: [line for line in text.splitlines() if not line.startswith('| [P04](')]
        assert without_row((REPO / name).read_text(encoding='utf-8')) == without_row(text), name
    print(json.dumps({'integrity':'PASS', 'master_sha256':digest(master), 'decoded_samples':len(samples), 'sample_fps':report['dense_sampling_fps'], 'unchanged_narration_wavs':7, 'unchanged_v1_plates':[1,2,3,4,6], 'identical_final_rig_plates':True, 'unique_imagegen_calls':2, 'p04_v1_inputs_assets_outputs_unchanged':True, 'readmes_only_p04_rows_changed':True, 'out_of_scope_concurrent_differences':changed, 'personal_path_files_scanned':len(files), 'personal_path_hits':0, 'trailing_whitespace_hits':0}))

if __name__ == '__main__':
    main()
