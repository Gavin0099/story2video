"""Add Studio-verified publications to the first-day measurement sheet."""
import csv
import json
from pathlib import Path


BATCH = Path(__file__).resolve().parent
JOURNAL = BATCH.parents[2] / 'artifacts/science-shorts/public-20-20261122/studio-public.jsonl'
CHANNEL = 'UCJpx-XFeS91Vd26QokWAWOw'


def update_sheet():
    path = BATCH / 'd1.csv'
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        episodes = {row['episode_id']: row for row in reader}
    for line in JOURNAL.read_text(encoding='utf-8-sig').splitlines():
        release = json.loads(line)
        if (release['stage'],release['visibility'],release['target_channel_id']) != (
                'verified public','public',CHANNEL):
            continue
        episode = release['episode']
        if episode in episodes:
            if episodes[episode]['video_id'] != release['video_id']:
                raise ValueError(f'Studio ID changed for episode {episode}')
            continue
        episodes[episode] = {
            'episode_id':episode, 'video_id':release['video_id'],
            'public_verified_at_taipei':release['observed_at'],
            'd1_due_taipei':release['d1_due'], 'data_status':'waiting',
        }
    completed = path.with_suffix('.csv.tmp')
    with completed.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(episodes[episode] for episode in sorted(episodes))
    completed.replace(path)
    print(f'{len(episodes)} Studio-verified Shorts in {path.name}')


if __name__ == '__main__':
    update_sheet()
