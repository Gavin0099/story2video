"""Create the next U01 revision without changing original assets or other jobs."""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__ == '__main__':
    number = 2
    while (HERE / 'revisions' / f'v{number}').exists() or (REPO / 'artifacts/static-ten-20261124/uncanny_mystery' / f'uncanny-u01-v{number}').exists():
        number += 1
    dest = HERE / 'revisions' / f'v{number}'
    (dest / 'assets').mkdir(parents=True)
    files = ['story.md', 'shots.json', 'references.json', 'source-v3.md']
    files += [p.relative_to(HERE).as_posix() for p in (HERE/'assets').iterdir() if p.suffix == '.wav' or p.name in ('reference.png','setup.png','resolution.png')]
    originals = {name: sha(HERE/name) for name in files}
    for name in files:
        shutil.copyfile(HERE/name, dest/name)
    save(dest/'baseline.json', {'original_files': originals, 'v1_master_sha256': 'e075afa52d9e4a6d687076c46f8b0919375785efcca2d57591b37ed61b12fb77', 'original_revision': 'uncanny-u01-v1'})
    data = json.loads((dest/'shots.json').read_text(encoding='utf-8'))
    refs = json.loads((dest/'references.json').read_text(encoding='utf-8'))
    data['story_id'] = f'uncanny-u01-v{number}'
    data['sheets']['mechanism'] = {'file':'assets/mechanism.png','columns':2,'rows':1,'edge_px':3}
    data['sheets']['resolution']['file'] = 'assets/resolution-v2.png'
    data['shots'][5]['source'].update(sheet='mechanism', cell=0)
    paper = ('ONE plain white absorbent rectangular sheet spans the ENTIRE cabinet top from left edge to right edge, under the whole plant saucer; '
             'it reaches BOTH rear corners and folds over the FULL rear edge as a continuous 5 cm white skirt ending ABOVE the horizontal rear vent. '
             'No gaps, cutouts, exposed wood strip or bypass between saucer and rear edge. Reservoir stands on its right portion. '
             'It stays in exactly this position from shot-06 to shot-12, including when the pot and saucer are lifted in shot-11. Paper is always dry.')
    hose = ('One thin black hose enters through the rear vent, connects to the TOP of one short ivory ribbed inline connector, '
            'then a second black hose is firmly attached to its BOTTOM and curves downward then upward into the same rear vent. '
            'Both joints are sealed, no open outlet. The single fine side split is on the connector camera-facing lower-right SIDE WALL halfway along its body, '
            'away from both ends. No visible split/water before reveal; at reveal a fine side jet starts at that wall split while both black hoses stay attached. '
            'Water falls onto inner rear wood and into black shoe tray; it never emerges from a connector end.')
    for r in refs['items']:
        if r['id'] == 'paper':
            r['invariants'] = [paper]
            r['canonical'].update(sheet='mechanism',cell=0)
            r['appears_in'] = ['shot-06','shot-07','shot-08','shot-09','shot-11']
        if r['id'] == 'watering':
            r['appears_in'] = sorted(set(r['appears_in']+['shot-03','shot-12']))
    refs['items'].append({'id':'hose','kind':'prop','invariants':[hose], 'canonical':{'sheet':'mechanism','cell':1,'crop':[0,0,1,1]}, 'appears_in':['shot-02','shot-03','shot-07','shot-10','shot-12']})
    prompts = {
        6: 'Evening. Same rust-sleeved woman finishes laying the canonical full-width white sheet under saucer. Elevated REAR three-quarter camera: show both rear corners, entire uninterrupted white fold across rear edge, 5 cm rear skirt ABOVE vent. Pot/saucer left, reservoir/pump right ON sheet. Hands at side edge, no hand obscures rear fold. Dry sheet. No flowing water.',
        7: 'Evening front three-quarter medium view. Same woman kneels holding dry cloth and brass key, open cabinet; dry grey shoes in dry shallow black tray. Above cabinet ALL of full-width white paper remains beneath saucer and reservoir, rear fold visible in oblique view. Inside identical ivory connector with black hoses visibly attached above AND below, lower hose curves back up to vent. No leak or split visible. Woman looks at tray.',
        8: 'Night. Same woman placing one brass key on bedside table in foreground. Through doorway cabinet is large enough to recognize, CLOSED brass padlock. Plant and reservoir remain on full-width white sheet; its continuous rear-edge fold remains visible as white strip. Keep cabinet and white paper sharply readable. No water flowing. Do not show cabinet interior.',
        9: 'Predawn exterior front three-quarter cabinet view, closed brass padlock. Canonical white sheet covers whole top beneath saucer AND reservoir, full rear-edge fold still visible. Same sheet never moved. Dry top and floor. No active water. No person.',
        10: 'Morning close-up INSIDE cabinet. Large identical ivory ribbed inline connector: black hose firmly attached to TOP and another black hose firmly attached to BOTTOM, lower hose clearly descends and loops back up. Show fine SIDE WALL SPLIT midway along right side of ivory body. Thin side jet emerges sideways from the split, then curves down onto rear wood into shallow tray. NO water at either sealed end. Both hose attachment points entirely visible, not cropped. Grey shoes below have dry white laces; soles in shallow tray water. Small analog clock at bottom, TWO hands, minute hand up and short hour hand down (six). No person. Cabinet top/paper offscreen.',
        11: 'Morning elevated REAR three-quarter close view matching canonical placement: rust-sleeved hands lift whole terracotta pot AND beige saucer together ABOVE paper. Entire white sheet remains flat on top and folded uninterrupted over full rear edge, both rear corners visible. Dry paper under whole former saucer footprint, no translucent wet spots or droplets. Reservoir stays on right portion. Reveal dry underside of beige saucer with white tide ring on inner rim if visible. No bare wood path between footprint and rear edge. Do not remove or shift paper.',
        12: 'Morning lower interior view through open doors. Same grey shoes white dry laces stand in shallow black tray water. Low tray front lip spills a SMALL amount across oak cabinet floor and out bottom seam. Identical ivory connector visible above with BOTH top and bottom black hoses attached, lower hose curves back up, no disconnected end. Pump cycle has ended, residual beads at same connector side wall but no end jet. Cabinet top/paper cropped offscreen. No person. No flood or splashes.'
    }
    for shot in data['shots']:
        n = int(shot['id'].split('-')[1])
        if n in prompts:
            shot['prompt'] = prompts[n] + ' Photorealistic single still. No text, arrows, diagram or extra panels. Keep all evidence inside central 90% portrait-safe framing.'
        shot['required_references'] = [r['id'] for r in refs['items'] if shot['id'] in r['appears_in']]
    save(dest/'shots.json',data)
    save(dest/'references.json',refs)
    with (dest/'story.md').open('a',encoding='utf-8') as f:
        f.write('\n## Revision visual contract\n\nNarration, bilingual lines, timing and causal story are unchanged. Revision '+f'v{number}'+'.\n\n'+paper+'\n\n'+hose+'\n\nShot-06 uses the new mechanism reference cell itself; shots 07-12 are regenerated conditioned on that paper placement and connector reference. Shots 01-05 reuse original setup cells.\n')
    print(dest.relative_to(REPO).as_posix())
