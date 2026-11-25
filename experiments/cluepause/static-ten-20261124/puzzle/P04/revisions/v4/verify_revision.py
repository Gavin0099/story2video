"""Offline deliverable audit. Decoded-image landmarks remain manual observations."""
from array import array
import hashlib
import json
from pathlib import Path
import re
import wave

STORY = Path(__file__).resolve().parent
REPO = STORY.parents[6]
OUTPUT = REPO / 'artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v4'
AUDIT = OUTPUT.parent / 'p04-v4-fix'
PREVIOUS = OUTPUT.parent / 'puzzle-p04-static-v3'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pcm(path):
    with wave.open(str(path), 'rb') as stream:
        assert (stream.getframerate(), stream.getnchannels(), stream.getsampwidth()) == (24000, 1, 2)
        return array('h', stream.readframes(stream.getnframes()))


def main():
    data = read(STORY / 'shots.json')
    manifest = read(OUTPUT / 'manifest.json')
    report = read(OUTPUT / 'qa/report.json')
    assert report['engineering'] == 'PASS' and all(report['checks'].values())
    master = OUTPUT / 'puzzle-p04-static-v4.mp4'
    assert digest(master) == report['master_sha256']
    for name, expected in manifest['inputs'].items():
        assert digest(STORY / name) == expected, name
    for cue in data['narration']:
        assert digest(STORY / cue['file']) == digest(PREVIOUS / 'cache/voice' / (cue['id'] + '.wav'))
    timeline = read(OUTPUT / 'timeline.json')
    before = read(PREVIOUS / 'timeline.json')
    assert timeline['cues'] == before['cues']
    sound = next(c for c in timeline['captions'] if c.get('en') == '[snip]')
    assert (sound['start'], sound['end']) == (22, 22.2)
    assert next(s for s in timeline['shots'] if s['sfx'])['id'] == 'shot-05'
    assert all(c['start'] >= 27 for c in timeline['cues'] if c['reveal'])
    oldmix, newmix = pcm(PREVIOUS / 'mix.wav'), pcm(OUTPUT / 'mix.wav')
    assert len(oldmix) == len(newmix) == 39 * 24000
    changed = [i for i, (a, b) in enumerate(zip(oldmix, newmix)) if a != b]
    assert changed
    assert all(22 * 24000 <= i < 22.2 * 24000 or 27.1 * 24000 <= i < 27.3 * 24000 for i in changed)
    assert digest(OUTPUT / 'cache/shot-06.png') == digest(PREVIOUS / 'cache/shot-06.png')
    assert digest(OUTPUT / 'cache/shot-07.png') == digest(OUTPUT / 'cache/shot-08.png')
    samples = 0
    for shot in timeline['shots']:
        folder = OUTPUT / 'qa' / shot['id']
        schedule = read(folder / 'samples.json')
        assert schedule['minimum_fps'] >= 4
        assert len(schedule['times']) == len(list(folder.glob('*.png')))
        assert schedule['times'][0] == shot['start']
        assert abs(schedule['times'][-1] - (shot['end'] - 1/30)) < .00001
        assert max(b-a for a, b in zip(schedule['times'], schedule['times'][1:])) < .234
        samples += len(schedule['times'])
    ledger = [json.loads(line) for line in (STORY / 'images.jsonl').read_text().splitlines()]
    assert [r['attempt'] for r in ledger] == [1, 2]
    assert [r['status'] for r in ledger] == ['rejected', 'accepted']
    assert (STORY / 'images.jsonl').read_bytes() == (OUTPUT / 'images.jsonl').read_bytes()
    for row in ledger:
        assert digest(STORY / row['result_filename']) == row['result_sha256']
        prompt = read(REPO / row['prompt_archive'])
        assert hashlib.sha256(prompt['prompt'].encode()).hexdigest() == row['prompt_sha256']
        for attachment in row['actual_reference_attachments']:
            assert digest(REPO / attachment['path']) == attachment['sha256']
    landmarks = read(AUDIT / 'landmarks.json')
    assert landmarks['within_visual_tolerance'] and landmarks['range'] <= .06
    assert {s['shot'] for s in landmarks['samples']} == {'shot-02', 'shot-04', 'shot-05', 'shot-07', 'shot-08'}
    assert read(AUDIT / 'decoded-frame-schedule.json')['master_sha256'] == digest(master)
    protected = read(AUDIT / 'protected-before.json')
    changed_protected = [name for name, expected in protected.items()
                         if not (REPO / name).is_file() or digest(REPO / name) != expected]
    assert changed_protected == ['experiments/cluepause/static-ten-20261124/puzzle/P04/record.md'], changed_protected
    personal = re.compile(r'(?:[A-Za-z]:[\\/](?:Users|home)[\\/]|/(?:Users|home)/)', re.I)
    extensions = {'.md', '.json', '.jsonl', '.py', '.txt', '.srt', '.sha256'}
    files = [p for folder in (STORY, OUTPUT, AUDIT) for p in folder.rglob('*')
             if p.is_file() and p.suffix in extensions and not any(part.startswith('pytest-') for part in p.parts)]
    files += [STORY.parents[1] / 'record.md']
    hits = [p.relative_to(REPO).as_posix() for p in files if personal.search(p.read_text(encoding='utf-8'))]
    whitespace = [p.relative_to(REPO).as_posix() for p in files
                  if any(line.rstrip(' \t') != line for line in p.read_text(encoding='utf-8').splitlines())]
    assert not hits, hits
    assert not whitespace, whitespace
    provenance = {p.relative_to(REPO).as_posix(): digest(p) for p in [
        STORY / 'render_revision.py', STORY / 'verify_revision.py',
        STORY.parents[3] / 'pipeline/static_storyboard.py',
        STORY.parents[2] / 'run.py', STORY / 'images.jsonl',
        AUDIT / 'landmarks.json', OUTPUT / 'manifest.json']}
    result = {'integrity': 'PASS', 'git_base_sha': manifest['git_sha'],
              'master_sha256': digest(master), 'decoded_samples': samples,
              'minimum_sample_fps': 30/7, 'unchanged_narration_wavs': 7,
              'narration_schedule_unchanged': True,
              'mix_changes_only_in_old_and_new_snip_windows': True,
              'sfx_seconds': [22, 22.2], 'imagegen_calls': 2, 'corrections': 1,
              'protected_files': len(protected), 'protected_changes': changed_protected,
              'v1_v3_and_readmes_unchanged': True,
              'landmark_ratio_range': [landmarks['minimum'], landmarks['maximum']],
              'personal_path_text_files_scanned': len(files), 'personal_path_hits': hits,
              'trailing_whitespace_hits': whitespace, 'provenance': provenance,
              'independent_review': 'PENDING', 'market_acceptance': 'NOT_TESTED'}
    (OUTPUT / 'revision-provenance.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (STORY / 'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
