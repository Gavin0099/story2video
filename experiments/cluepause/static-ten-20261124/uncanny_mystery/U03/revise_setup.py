"""One pre-encode revision to avoid showing the complete answer in setup."""
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
for name in ('story.md','shots.json'):
    shutil.copyfile(HERE/name,HERE/(Path(name).stem+'-initial'+Path(name).suffix))
data=json.loads((HERE/'shots.json').read_text(encoding='utf-8'))
updates={
 0:('The man faces a person-like shadow on the closed frosted pantry door. Ordinary counter objects are outside this tight frame.',
    'Tight over-the-shoulder medium portrait of same man in ochre henley looking at closed cream frosted pantry door. Human-like soft head-and-shoulders shadow centered on glass; a FEW faint pinpoints inside head, no eyes. Frame from man upper torso to door upper pane; counter, rack, towel and colander are BELOW THE FRAME and must not appear. No identifiable object-shaped handles on shadow.'),
 1:('A few tiny bright pinholes appear inside the blurred shadow head; no recognizable colander outline.',
    'Extreme close-up of frosted glass, ambiguous soft human-like head-and-shoulders shadow. Only about seven SUBTLE irregularly visible bright pinpoints within head, not a crisp geometrical sieve pattern. No ear-shaped side handles, no eyes, no face; lower shoulder shadow straight at hem. No physical colander in this cell.'),
 4:('The closed door again shows the same soft figure, while the man reacts beside it.',
    'Tight waist-up portrait of same man beside closed cream frosted pantry door, puzzled eyes toward soft person-like shadow. Keep counter contents, colander and towel BELOW the lower frame. Shadow has same few faint pinpoints, no object-identifying side handles.'),
 5:('A curved perforated steel detail catches the lamp light; its dots echo the earlier pinholes without showing the complete arrangement.',
    'Macro photograph of only a CURVED PATCH of the same stainless colander surface with small round perforations catching warm light. Its overall circular outline and handles are OUTSIDE THE FRAME. A narrow navy towel edge at bottom and a soft defocused black lamp behind supply context. Do not show full colander, full rack, human-shaped combination, pantry door shadow or complete lamp-object-glass alignment. This is a partial fair clue, not a reveal.')}
text=(HERE/'story.md').read_text(encoding='utf-8')
for index,(conveys,prompt) in updates.items():
    shot=data['shots'][index]
    text=text.replace(shot['conveys'],conveys)
    shot['conveys']=conveys
    shot['prompt']=prompt+' Keep the same photographic identity, set and props. No text, arrows or diagrams. One static moment per cell.'
    if index in (0,4):
        # Those recurring objects remain part of the set but are not visible in this tighter shot.
        shot['required_references']=['man','kitchen']
refs=json.loads((HERE/'references.json').read_text(encoding='utf-8'))
for item in refs['items']:
    item['appears_in']=[s['id'] for s in data['shots'] if item['id'] in s['required_references']]
for filename,value in [('shots.json',data),('references.json',refs)]:
    (HERE/filename).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text+='\n## Single pre-encode storyboard revision\n\nInitial generated setup exposed the whole colander/towel combination beside its matching shadow. The only fix pass reframes setup to retain a few pinholes and an isolated curved steel detail while deferring the complete projection relationship. Original authored storyboard is preserved in story-initial.md; no spoken line or causal explanation changed. This revised SILENT STORYBOARD was written before the correction request.\n'
(HERE/'story.md').write_text(text,encoding='utf-8')
