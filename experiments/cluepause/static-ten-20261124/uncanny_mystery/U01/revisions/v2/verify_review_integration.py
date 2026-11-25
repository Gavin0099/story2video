"""Verify U01 review records, derivative provenance and the full proposed text set."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess

ROOT = Path.cwd()
BATCH = Path('experiments/cluepause/static-ten-20261124')
U01 = BATCH / 'uncanny_mystery/U01'
V2 = U01 / 'revisions/v2'
OUT = Path('artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2')
STATUS = 'REVIEWED: UPLOAD-OK private review copy, not uploaded yet'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def git(*args):
    return subprocess.run(['git', '-c', 'core.excludesFile=NUL', *args],
                          capture_output=True, text=True, encoding='utf-8')


assert git('branch', '--show-current').stdout.strip() == 'codex/cluepause-static-ten-20261124'
baseline = read_json(V2 / 'review-integration-baseline.json')
allowed_changes = {
    (U01 / 'record.md').as_posix(),
    *((V2 / name).as_posix() for name in
      ['record.md', 'mechanism.md', 'inspection.json', 'pipeline-pytest.txt']),
    (BATCH / 'uncanny_mystery/README.md').as_posix(),
    (BATCH / 'README.md').as_posix(),
}
changed = []
for name, digest in baseline.items():
    path = Path(name)
    assert path.is_file(), f'Removed baseline file: {name}'
    if sha(path) != digest:
        changed.append(name)
assert set(changed) == allowed_changes, changed
for path in [p for p in BATCH.rglob('*') if p.is_file()]:
    if path.as_posix() not in baseline:
        assert path.is_relative_to(U01), path.as_posix()
for path in [p for p in OUT.rglob('*') if p.is_file()]:
    if path.as_posix() not in baseline:
        assert path.is_relative_to(OUT / 'upload-copy-checks') or path.name in {
            'uncanny-u01-v2-upload.mp4', 'upload-copy.md'}, path.as_posix()

# Verify each README differs from HEAD only in its U01 row.
for path, prefix in [(BATCH / 'README.md', '| [U01]'),
                     (BATCH / 'uncanny_mystery/README.md', '| U01 |')]:
    before = git('show', f'HEAD:{path.as_posix()}')
    assert before.returncode == 0
    old = before.stdout.splitlines()
    new = path.read_text(encoding='utf-8').splitlines()
    assert len(old) == len(new)
    differences = [(a, b) for a, b in zip(old, new) if a != b]
    assert len(differences) == 1
    assert all(line.startswith(prefix) for line in differences[0])
    assert STATUS in differences[0][1]

metadata = read_json(U01 / 'upload-metadata-draft.json')
assert metadata['id'] == 'U01' and metadata['status'] == STATUS
assert len(metadata['title']) <= 70 and metadata['title'].endswith(' | CluePause')
assert metadata['title_zh_Hant'] == '她的鞋一直濕，卻看不見有水滴在鞋上｜謎底之前'
assert metadata['description_zh_Hant'].startswith(
    '她的鞋放在鎖著的鞋櫃裡卻一再變濕，看起來也沒有水滴在鞋上。水究竟從哪裡來？\n\n')
reference = next(x for x in read_json(BATCH / 'upload-metadata.json')['videos'] if x['id'] == 'P01')
for field in ['description', 'description_zh_Hant']:
    hook, disclosure = metadata[field].split('\n\n')
    assert disclosure == reference[field].split('\n\n')[1]
    assert hook.endswith('?' if field == 'description' else '？')
    assert len(re.findall(r'[.!?]' if field == 'description' else r'[。！？]', hook)) == 2
text = '\n'.join(metadata[k] for k in ['title', 'title_zh_Hant', 'description', 'description_zh_Hant'])
assert not re.search(r'\b(hose|split|tray|paper|pump|connector|leak|overflow)\b', text, re.I)
assert not any(word in text for word in ['水管', '裂縫', '溢出', '鞋盤', '墊紙', '水泵', '接頭'])
assert not re.search(r'\b(he|his|him)\b', metadata['description'], re.I)
assert 'video_id' not in metadata
result = read_json(OUT / 'upload-copy-checks/results.json')
for field, expected in [('mp4_path', result['master']['path']),
                        ('mp4_sha256', result['master']['sha256']),
                        ('uploaded_file_path', result['upload']['path']),
                        ('uploaded_file_sha256', result['upload']['sha256']),
                        ('uploaded_file_bytes', result['upload']['bytes'])]:
    assert metadata[field] == expected
for prefix in ['mp4', 'uploaded_file']:
    path = Path(metadata[prefix + '_path'])
    assert sha(path) == metadata[prefix + '_sha256']
assert Path(metadata['uploaded_file_path']).stat().st_size == metadata['uploaded_file_bytes'] < 9500000
assert metadata['uploaded_file_ssim_vs_master'] == {k: result['ssim'][k] for k in ['mean', 'min']}
assert {k for k in metadata if k.startswith('uploaded_file_')} == {
    k for k in reference if k.startswith('uploaded_file_')}
tracks = metadata['captions']['tracks']
assert {x['language_code'] for x in tracks} == {'en', 'zh-Hant'}
for track in tracks:
    assert sha(Path(track['srt_path'])) == track['srt_sha256']
    assert track['youtube_language'] == ('英文' if track['language_code'] == 'en' else '中文（繁體）')
    assert track['upload_option'] == 'with timing' and track.get('status') != 'published'

source = read_json(OUT / 'upload-copy-checks/source-probe.json')
upload = read_json(OUT / 'upload-copy-checks/upload-probe.json')
assert source['format']['duration'] == upload['format']['duration'] == '38.000000'
for left, right in zip(source['streams'], upload['streams']):
    for field in ['codec_type', 'codec_name', 'profile', 'pix_fmt', 'width', 'height',
                  'r_frame_rate', 'avg_frame_rate', 'nb_read_frames', 'duration',
                  'sample_rate', 'channels']:
        assert left.get(field) == right.get(field), field
assert all(c['exit_code'] == 0 for c in read_json(OUT / 'upload-copy-checks/commands.json'))
assert result['ssim']['frames'] == 1140 and result['full_decode'] == 'PASS' and result['faststart']

for path in [U01 / 'record.md', V2 / 'record.md', V2 / 'mechanism.md']:
    text = path.read_text(encoding='utf-8').split('## Archived v1 findings', 1)[0]
    assert STATUS in text and 'clock' in text.lower()
    assert 'mineral' in text and 'streak' in text
    for target in re.findall(r'\]\(([^)]+)\)', text):
        assert (path.parent / target).is_file(), (path.as_posix(), target)
assert '[mechanism.md](mechanism.md)' in (V2 / 'record.md').read_text(encoding='utf-8')
assert 'clock_independent_review' in read_json(V2 / 'inspection.json')['observations']

# Full filesystem scan includes proposed untracked U01 records and scripts.
text_files = []
for path in sorted(set(U01.rglob('*')) | set((OUT / 'upload-copy-checks').glob('*.json')) |
                   {OUT / 'upload-copy.md', BATCH / 'README.md', BATCH / 'uncanny_mystery/README.md'}):
    if not path.is_file():
        continue
    raw = path.read_bytes()
    if b'\0' in raw:
        continue
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        continue
    text_files.append(path)
    assert b'\r' not in raw.replace(b'\r\n', b'\n'), f'Invalid CR: {path}'
    assert not text or text.endswith('\n'), f'Missing final newline: {path}'
    assert not text.endswith(('\n\n', '\r\n\r\n')), f'Blank EOF: {path}'
    for number, line in enumerate(text.splitlines(), 1):
        assert line == line.rstrip(' \t'), (path.as_posix(), number, 'trailing whitespace')
        assert not re.match(r'^ +\t', line), (path.as_posix(), number, 'space before tab')
        assert not re.match(r'^(<{7}|={7}|>{7})(?: |$)', line), (path.as_posix(), number, 'conflict')
    assert not re.search(r'(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]|/(?:Users|home)/)', text), path.as_posix()
    if path.suffix == '.py':
        ast.parse(text)

untracked = git('ls-files', '--others', '--exclude-standard', '--', U01.as_posix())
assert untracked.returncode == 0
untracked_names = set(untracked.stdout.splitlines())
no_index_count = 0
for path in text_files:
    if path.as_posix() in untracked_names:
        check = git('-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false',
                    'diff', '--no-index', '--check', '--', 'NUL', path.as_posix())
        assert check.returncode in [0, 1] and not check.stdout and not check.stderr, (
            path.as_posix(), check.returncode, check.stdout, check.stderr)
        no_index_count += 1
diff = git('diff', '--check')
assert diff.returncode == 0 and not diff.stdout, diff.stdout
report = {'base_git_sha': git('rev-parse', 'HEAD').stdout.strip(),
          'baseline_files_checked': len(baseline), 'changed_baseline_files': changed,
          'full_text_files_checked': len(text_files),
          'untracked_u01_no_index_checks': no_index_count,
          'git_diff_check': 'PASS', 'whitespace_path_syntax_checks': 'PASS',
          'metadata_hash_style_spoiler_checks': 'PASS',
          'unchanged_other_inputs_masters_sidecars_and_metadata': 'PASS',
          'readme_u01_rows_only': 'PASS', 'derivative_provenance_format_duration': 'PASS',
          'market_acceptance': 'NOT_TESTED'}
(V2 / 'review-integration-checks.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
