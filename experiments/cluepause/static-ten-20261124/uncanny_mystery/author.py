"""Portable authored inputs and original local sound effects. No network calls."""
from pathlib import Path
import json
import math
import random
import wave
from array import array

HERE = Path(__file__).resolve().parent

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sound(path, kind):
    rng = random.Random(82)
    length = .36 if kind != 'hum' else 1.25
    values = []
    for i in range(round(length*24000)):
        t = i/24000
        if kind == 'hum':
            v = .08*math.sin(2*math.pi*115*t)*min(1,t*40,(length-t)*40)
        elif kind == 'drop':
            v = .32*math.sin(2*math.pi*(1100*t-650*t*t))*math.exp(-22*t)
        elif kind == 'brush':
            v = .15*rng.uniform(-1,1)*math.sin(math.pi*t/length)**2
        else:
            v = .24*rng.uniform(-1,1)*math.exp(-55*t)
        values.append(round(v*32767))
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,24000,0,'NONE','not compressed'))
        w.writeframes(array('h',values).tobytes())

def story(code, title, question, summary, alternate, refs, frames, lines, duration, notes):
    folder = HERE/code
    (folder/'assets').mkdir(parents=True,exist_ok=True)
    items=[]
    for i,(rid,kind,invariants) in enumerate(refs):
        items.append(dict(id=rid,kind=kind,invariants=invariants,canonical=dict(sheet='reference',cell=i,crop=[0,0,1,1]),appears_in=[]))
    sheets={s:dict(file=f'assets/{s}.png',columns=3,rows=2,edge_px=3) for s in ('reference','setup','resolution')}
    shots=[]
    for i,f in enumerate(frames):
        start,end,function,framing,required,conveys,prompt = f[:7]
        shot=dict(id=f'shot-{i+1:02}',function=function,framing=framing,start=start,end=end,
                  source=dict(sheet='setup' if i<6 else 'resolution',cell=i if i<6 else i-6,crop=[0,0,1,1]),
                  camera=dict(zoom=[1.005,1.025],**{'from':[.5,.5],'to':[.5,.5]}),
                  required_references=required.split(),sfx=[],conveys=conveys,
                  prompt='Use case: photorealistic-natural. '+prompt+' All essential evidence centered inside the middle 85% of this portrait cell. No lettering, no arrows, no diagram, no gore. Freeze one photographed moment; no sequential montage inside a cell.')
        if len(f)>7:
            kind,offset,en,zh=f[7]
            sound(folder/f'assets/{kind}.wav',kind)
            shot['sfx']=[dict(file=f'assets/{kind}.wav',offset=offset,gain=.35,en=en,zh=zh)]
        shots.append(shot)
        for ref in items:
            if ref['id'] in shot['required_references']: ref['appears_in'].append(shot['id'])
    narration=[dict(id=f'line-{i+1:02}',en=en,zh=zh,voice='af_heart',speed=1.08,reveal=reveal,not_before=at,gap_before=.10) for i,(at,en,zh,reveal) in enumerate(lines)]
    data=dict(version=1,story_id=f'uncanny-{code.lower()}-v1',fiction='FICTION — original invented scene; no true-event claim.',genre='uncanny_mystery',question=dict(en=question[0],zh=question[1]),sheets=sheets,narration=narration,shots=shots)
    save(folder/'shots.json',data);save(folder/'references.json',dict(version=1,items=items))
    text=f'# FICTION — {code}: {title}\n\nGenre: uncanny_mystery\n\nOriginal invented story; no real people, brands, news, true-crime or existing-work recreation. Rights: pending_verification. Target: {duration} s, 1080×1920, 30 fps. Opening question only at 1.0–3.5 s; English narration, separate EN/zh-Hant captions.\n\nStory Quality Gate PENDING. Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.\n\n## Story\n\n{summary}\n\nPlausible alternative before the reveal: {alternate}\n\n{notes}\n\n## Script\n\n'
    for at,en,zh,reveal in lines:text+=f'- At or after {at:g} s'+(' (reveal)' if reveal else '')+f': “{en}” / {zh}\n'
    text+='\nNo explanation card or closing repetition. SFX are original locally synthesized illustrative cues, not documentary recordings. No character animation.\n\n## Shot list\n\n| Time | Shot | Function | Visible observation |\n| --- | --- | --- | --- |\n'
    for s in shots:text+=f"| {s['start']:g}–{s['end']:g} | {s['id']} | {s['function']} | {s['conveys']} |\n"
    text+='\n## SILENT STORYBOARD — before ImageGen\n\nThis is authored intent, not an observed viewer result. Each key frame must make the following observation available without speech, captions or the question.\n\n'
    for i,s in enumerate(shots):text+=f"{i+1}. **{s['function']}**: {s['conveys']}\n"
    text+='\nThe core visible change and its physical cause must survive the silent sequence. Recurrence, sole ownership of a key, precise elapsed time and exact spoken hypotheses may still require narration. Compare generated frames against these intentions in record.md; do not claim comprehension from this check. All recurring people, props and sets are registered in references.json.\n'
    (folder/'story.md').write_text(text,encoding='utf-8')
    save(folder/'editorial.json',dict(title=title,summary=summary,rights_status='pending_verification',duration_target=duration,story_quality_gate='PENDING',storyboard_quality_gate='PENDING',viewer_gate='HUMAN_TEST_PENDING'))

def main():
    story('U01','The Shoes That Stayed Wet',('Why Wet Inside?','鎖著怎麼還會濕？'),
      'Retains U01 v3 without changing its story: shoes stored dry become wet inside a locked cabinet. A chalky plant saucer and old exterior streak suggest overflow. Paper beneath the saucer stays dry; the timed watering hose connector leaks inside the cabinet, filling the shallow tray and escaping through its bottom seam.',
      'The plant saucer overflows from above; its mineral ring and the old exterior streak support this route. The paper tests that route, and stays dry after the next pump cycle.',
      [('woman','character',['invented woman age 32, straight chin-length black bob, oval face','rust-orange long-sleeve pullover, dark navy trousers, no jewelry']),
       ('cabinet','set',['small pale oak shoe cabinet with two doors, broad rear horizontal vent','single brass padlock centered on front hasp; light grey tiled hallway; cream wall; open bedroom doorway nearby','inside: black shallow rectangular shoe tray with low front lip on bottom shelf']),
       ('shoes','prop',['one pair light grey canvas low-top shoes, white dry laces, dark grey rubber soles','uppers and laces stay dry; only soles contact tray water; never worn outdoors in this story']),
       ('watering','prop',['terracotta plant pot on beige round saucer with white mineral tide ring, green oval leaves','clear rectangular reservoir and compact black timer pump beside pot on cabinet top','one black thin hose loops down through rear vent and back up; same ivory short ribbed cylindrical inline connector on inner rear wall above tray; no drip before reveal']),
       ('paper','prop',['single plain white rectangular sheet, no text','introduced only in evening; covers entire saucer footprint and rear top-edge route; remains dry']),
       ('key','prop',['one small brass padlock key with round bow, no keyring'])],
      [(0,3.5,'establish','close_up','cabinet','Water beads beneath the closed padlocked cabinet while the surrounding tile is dry.','Floor-level view of pale oak cabinet, brass padlock above centered bottom seam, one hanging water droplet and small puddle, dry surrounding grey tiles.',('drop',.3,'[water drop]','[滴水聲]')),
       (3.5,7,'clue','medium','woman cabinet shoes watering key','She opens the lock and lifts the shoes; the pale connector is already present in the rear hose loop.','Woman holding brass key beside unlocked padlock and opening cabinet. Grey canvas shoes in shallow black tray; ivory ribbed inline connector on black hose against inner rear wall below broad vent. Connector dry, no active stream.'),
       (7,10,'clue','close_up','woman cabinet shoes','Water clings to the rubber sole, while canvas and laces are dry.','Close side profile of woman tilting one grey canvas shoe above shallow black tray; clear beads below dark rubber sole; dry pale canvas and white laces. Water pooled just below tray low front lip.',('drop',.4,'[water drop]','[滴水聲]')),
       (10,14,'clue','close_up','cabinet watering','The plant saucer has a white tide ring; watering equipment sits beside it.','Cabinet top, terracotta plant in beige saucer with unmistakable white mineral ring along inner rim; clear reservoir and black pump beside it; thin black hose disappears behind pot. No water flowing.'),
       (14,18,'clue','medium','woman cabinet watering','A dry exterior streak leads down the cabinet back; the hallway remains dry except near its base.','Oblique side view of same woman touching a chalky dried exterior streak below top rear corner of oak cabinet; plant and pump atop it, dry grey hallway beside small base puddle. Do not show active exterior water.'),
       (18,22,'clue','medium','woman cabinet watering paper','She places a white sheet beneath the entire saucer and rear top edge.','Evening warm light, woman placing a clean plain white rectangular sheet under entire plant saucer footprint, paper extending fully over rear top edge beneath the possible overflow route. Same reservoir pump beside it, no drip.',('brush',.3,'[paper rustles]','[紙張窸窣]')),
       (22,25,'transition','medium','woman cabinet shoes watering paper key','The tray and shoes are dry before the cabinet is closed for the night.','Evening woman holds dry cloth beside open cabinet after wiping tray dry. Dry grey shoes back in dry black shallow tray. Same dry pale ribbed connector on rear hose loop above shoes; white paper beneath plant on cabinet top. Brass padlock and key in her other hand.'),
       (25,27,'reaction','medium','woman cabinet watering paper key','She leaves the key beside her bed; the closed locked cabinet remains visible.','Woman in rust pullover placing small brass key on bedside table, concerned profile; through open bedroom doorway same oak cabinet closed and brass padlocked, plant saucer on white sheet on top.'),
       (27,29,'transition','medium','cabinet watering paper','The planted white paper and closed padlock remain undisturbed before morning.','Quiet close portrait view down oak cabinet: plant saucer on white sheet at top, brass padlock closed below. Muted pre-dawn light. Paper flat and dry, hose route behind pot. No flowing water.'),
       (29,33.5,'reveal','close_up','cabinet watering shoes','The same pale ribbed connector now leaks down the inside wall into the shoe tray.','Morning inside now-open cabinet, close-up of identical ivory short ribbed connector on black hose below broad rear vent. A bead and thin trickle emerge from hairline split on connector underside, run visibly down inner rear oak wall into shallow tray beneath grey shoes. Dry white laces. Small unnumbered analog clock at edge points to six.',('hum',.1,'[pump clicks and hums]','[水泵啟動低鳴]')),
       (33.5,35.5,'reveal','close_up','woman cabinet watering paper','Lifting the plant saucer exposes completely dry paper across the tested route.','Morning close-up of rust-sleeved hands lifting beige saucer and terracotta pot above entire plain white sheet, sheet visibly pristine dry and flat across saucer footprint and over rear edge. Reservoir pump beside it.'),
       (35.5,38,'reveal','close_up','cabinet shoes','After the cycle, water crosses the low tray lip and cabinet floor to the same bottom seam; the laces stay dry.','Low cutaway view through open cabinet: grey canvas shoes with dry white laces stand in shallow water in black tray; water overtops LOW FRONT LIP, visibly crosses oak cabinet floor and escapes same bottom seam onto grey tile. This is after a full pump cycle, not one instantaneous drop.',('drop',.3,'[water drop]','[滴水聲]'))],
      [(0.10,'The locked cabinet dripped. Her shoes were wet again.','鎖著的鞋櫃滴下水。她的鞋又濕了。',False),
       (3.5,"She'd put them away dry. Only she had the key.",'她放進去時鞋是乾的。只有她有鑰匙。',False),
       (7,'Dry laces. Wet soles.','鞋帶乾的，鞋底卻濕了。',False),
       (10,'A white tide mark ringed the plant saucer.','花盆底盤內緣，留著一圈白色水痕。',False),
       (14,'A streak ran down the back. The hallway was dry.','櫃背有一道水漬。走道是乾的。',False),
       (18,'That evening, she put paper under the pot and dried the tray.','當晚，她在花盆下墊紙，再把鞋盤擦乾。',False),
       (25,'Where was the water getting in?','水究竟從哪裡進去？',False),
       (29,'At six, the pump started. That connector leaked inside the cabinet.','六點，水泵啟動。那個接頭在鞋櫃裡漏水。',True),
       (33.5,'The paper stayed dry. The leak was already inside.','紙一直是乾的。漏水處早就在櫃子裡。',True)],38,
      'Source: U01 v3 read using git show from codex/cluepause-genre-pilot-v3-20261124. Spoken English and Traditional Chinese lines retained verbatim. Timing and static shot division adapted to 38 seconds; exact six-o’clock observation retained in reveal. No active connector leak before 29 s. The dry exterior streak is old history, not the current route. Existing v3 reader scores 77/72/78 do not qualify this film or transfer to this round.')

    story('U02','The Chair That Came to Breakfast',('Who Moved This Chair?','誰把椅子移過來？'),
      'Each morning, a mustard-apron-draped rolling kitchen stool has left its place and arrived at the doorway. A tilted floor and rolling marble suggest gravity. Yet a strip of rug is crossed uphill. A robot vacuum winds the apron tie into its brush and tows the stool; the curved floor marks were the route of its wheels.',
      'A slightly sloping floor rolls the freely wheeled stool toward the doorway. A marble rolling in that direction makes this credible; the rug ridge and curved scuff path challenge it.',
      [('woman','character',['invented woman age 40, shoulder-length wavy dark brown hair, broad face','sage green cardigan over plain cream shirt, black trousers']),
       ('kitchen','set',['small ordinary kitchen, warm white cabinets, pale wooden floor, dark open doorway','narrow charcoal rug with raised edge at threshold, low grey robot charging dock under cabinet at rear']),
       ('stool','prop',['one light grey backless swivel stool, round padded seat, chrome central stem, five black caster wheels','mustard yellow apron draped over seat, two long matching waist ties; one tie hangs to floor before reveal; apron never worn']),
       ('robot','prop',['one unbranded low round charcoal robot vacuum with pale grey circular top and black bumper','underside has horizontal black brush roller; no text, no extra robot']),
       ('marble','prop',['one small translucent blue glass marble, no other balls']),
       ('scuff','prop',['thin paired curved grey caster scuffs across pale floor, leading from stool position toward doorway'])],
      [(0,4,'establish','wide','woman kitchen stool scuff','A rolling stool with an apron blocks the doorway; its place at the breakfast counter is empty.','Morning woman facing mustard-apron-draped grey rolling stool centered in kitchen doorway beyond charcoal rug; empty counter place visible behind, subtle curved paired scuffs on pale floor.'),
       (4,7,'clue','close_up','kitchen stool scuff','The stool has free caster wheels and paired curved scuffs end beside them.','Low close-up of five black caster wheels below grey stool, mustard apron tie hanging from seat to pale wooden floor; thin paired grey curved scuffs end at wheels. No robot pulling yet.'),
       (7,10,'clue','medium','woman kitchen marble','A blue marble is set on the floor toward the doorway, suggesting a slope.','Woman crouched in sage cardigan, blue marble on pale floor near her fingertips, doorway downframe. Grey low charging dock visible under rear kitchen cabinet, no robot prominent.'),
       (10,13,'clue','close_up','kitchen marble','The same marble now rests against the doorway side of the rug.','Blue glass marble resting just before raised edge of charcoal threshold rug, pale floor slopes slightly toward it. Tight composition of marble and rug, no stool or robot.'),
       (13,17,'clue','close_up','kitchen stool scuff','The stool’s curved wheel trail continues over the raised rug ridge.','Close low oblique view of grey stool caster on far side of charcoal raised rug edge; thin paired curved grey scuff path on exposed wood before and after rug; mustard apron tie trails back across ridge. Evidence of crossing, not a floating chair.'),
       (17,21,'reaction','medium','woman kitchen stool robot','She resets the stool at the counter; the hanging tie and docked vacuum share the floor.','Evening woman pushing same grey stool and mustard apron back against counter; one long mustard waist tie hangs to floor near docked charcoal round robot. Woman puzzled, not smiling. No tie wound around robot yet.'),
       (21,25,'clue','close_up','kitchen stool robot','The loose yellow tie lies across the path from the vacuum dock.','Floor-level nighttime view of mustard apron waist tie hanging from stool seat with loose end across route directly in front of charcoal round vacuum dock. Robot is leaving dock but tie not visibly caught yet.',('hum',.2,'[vacuum motor]','[掃地機馬達聲]')),
       (25,30,'reveal','close_up','kitchen stool robot','The apron tie is taut between the stool and the vacuum’s brush intake.','Strong centered floor-level close view: mustard apron on grey caster stool at left, its single long mustard waist tie stretched TAUT diagonally into underside front brush intake of same round charcoal vacuum moving away to right. Both endpoints visible. Stool caster turned toward robot.'),
       (30,33,'reveal','close_up','woman kitchen stool robot','Lifting the vacuum reveals the same yellow tie wound around its black brush roller.','Sage-sleeved hands tilt same charcoal robot vacuum onto side; underside horizontal black brush roller has several unmistakable mustard yellow apron tie loops wound around it, unbroken tie extends back to mustard apron on grey stool. No extra rope.',('click',.3,'[motor stops]','[馬達停止]')),
       (33,36,'reveal','wide','woman kitchen stool robot scuff','The freed stool stays at the counter while the vacuum sits alone at the rug crossing.','Morning woman holding freed mustard apron tie up off floor beside stool at counter, relieved expression; same charcoal robot beyond rug at doorway, curved paired scuffs connect prior route across pale floor. Do not put apron on woman.')],
      [(0.1,'Every morning, her kitchen chair waited in the doorway.','每天早上，她的廚房椅都等在門口。',False),
       (4,'Nobody else had a key. The wheels left curved marks.','別人沒有鑰匙。輪子留下彎曲的痕跡。',False),
       (8,'A marble rolled toward the door. A sloping floor?','彈珠滾向門口。是地板傾斜嗎？',False),
       (13,'But the chair had crossed the raised rug.','可是椅子還越過了隆起的地毯。',False),
       (17,'She put it back, with her apron still on the seat.','她把椅子推回去，圍裙仍搭在椅面。',False),
       (22,'That night, she watched the floor.','當晚，她盯著地板。',False),
       (25,'The vacuum caught the apron tie and wound it around its brush.','掃地機捲住圍裙帶，纏上滾刷。',True),
       (30.5,'Those curves were a towing route.','那些彎痕，是拖行的路線。',True)],36,
      'Original author draft for this round. Mechanical cause differs from U01 water leakage and U03 optical projection. Keep the rolling stool lightweight and on casters; show a taut continuous tie in the reveal, never teleport it. The marble is a plausible inference, not proof. Silent sequence must show the tie connecting apron, brush and movable stool. Exact nightly recurrence is spoken context.')

    story('U03','The Man in the Pantry Door',('Who Is Behind the Glass?','玻璃後面是誰？'),
      'A head-and-shoulders silhouette stands in a closed frosted pantry door each evening. An empty coat hanger inside suggests a hanging coat. But the pantry is empty when opened, and its interior lamp does not make the figure. A small counter lamp projects the combined shadow of a round perforated colander and a navy tea towel on the dish rack onto the outside of the glass. Moving the colander breaks the head away from the shoulders.',
      'A coat on the pantry’s wall hook makes a person-shaped silhouette. The visible hanger gives this a physical basis; opening the door reveals an empty hanger, and the shadow can be separated by moving objects outside the pantry.',
      [('man','character',['invented man age 35, short tightly curled black hair, light stubble, rectangular face','plain ochre long-sleeve henley shirt, charcoal trousers, no glasses']),
       ('kitchen','set',['compact kitchen, pale mint wall, cream pantry door with one tall frosted glass pane, plain round brass knob','counter opposite pantry door, small black directional task lamp aimed across counter toward frosted pane','inside pantry: pale shelves and one bare wooden hanger on back hook; no person or coat inside']),
       ('rack','prop',['small upright unbranded chrome dish drying rack on counter opposite door','navy blue tea towel draped over rack in shoulder-like triangular shape; stays in place until final shot']),
       ('colander','prop',['one round small stainless steel perforated colander with two short side handles','stored upright on dish rack above navy towel, round silhouette resembles head; hole constellation must match shadow']),
       ('lamp','prop',['small matte black directional task lamp with warm exposed inner shade','stands on same counter BEHIND rack, aimed THROUGH colander and towel toward frosted door; never located inside pantry']),
       ('hanger','prop',['one plain bare triangular wooden clothes hanger on hook inside pantry, no clothing'])],
      [(0,4,'establish','wide','man kitchen rack colander lamp','A person-like silhouette appears on a frosted pantry door in an otherwise ordinary kitchen.','Evening man in ochre henley facing closed mint-wall cream pantry door. Tall frosted pane shows dark head-and-shoulders silhouette, not a real person. In foreground on opposite counter small black task lamp behind upright chrome rack with navy tea towel and round metal colander; objects natural background, not highlighted.'),
       (4,7,'clue','close_up','kitchen','The apparent head has tiny bright pinholes, and its shoulders have a straight lower edge.','Tight portrait of frosted pantry glass with ambiguous human head-and-shoulders shadow. Round head has tiny constellation of bright pinholes, soft side projections from colander handles. Shoulder shadow from navy towel ends in straight horizontal edge. No eyes, face, hands or actual person.'),
       (7,11,'clue','medium','man kitchen hanger','Opening the door reveals empty shelves and a bare hanger.','Man in ochre henley holding cream frosted pantry door open, empty pantry shelves plainly visible and bare triangular wooden hanger on back hook. Warm kitchen, nobody inside pantry.',('click',.2,'[door latch]','[門閂聲]')),
       (11,14,'reaction','medium','man kitchen hanger','He checks the bare hanger, puzzled that there is no coat.','Man looking directly at one bare wooden hanger on pantry back hook, empty shelves behind. Puzzled raised eyebrows. Ochre henley, same short curls and stubble.'),
       (14,18,'clue','medium','man kitchen rack colander lamp','With the door closed, the silhouette returns while all objects remain in place outside.','Man standing next to closed cream frosted pantry door, head-and-shoulders shadow again visible. Foreground black lamp behind chrome rack, navy towel and upright round metal colander visible, identical arrangement. No ghost body.'),
       (18,22,'clue','close_up','kitchen colander rack lamp','The colander’s perforations echo the pinholes in the shadow; its relationship to the lamp is visible.','Shallow oblique close-up across counter: warm black directional task lamp BEHIND round perforated stainless colander upright over navy towel on chrome rack, frosted pantry door at far end of light path. Hole pattern easy to see. Do not show explanatory beam graphics or arrows.'),
       (22,26,'reaction','medium','man kitchen lamp rack colander','He reaches toward the colander, looking from it to the silhouette.','Man in ochre henley looking from round colander to shadow on closed frosted door, his hand approaching colander handle without moving it yet. Lamp behind rack keeps shadow intact; no answer lettering.'),
       (26,30,'reveal','medium','man kitchen rack colander lamp','Lifting the colander away separates the shadow’s head from its towel-shaped shoulders.','Decisive single photographic reveal: man lifting round stainless perforated colander sideways away from chrome rack; on frosted pantry pane its ROUND HEAD SHADOW visibly displaced sideways away from still shoulder-shaped navy towel shadow. Lamp remains on counter behind rack. Show lifted object and matching detached shadow in same composition.'),
       (30,33,'reveal','close_up','kitchen rack colander lamp','The physical line from lamp through colander and towel to the matching shadows is visible.','Oblique portrait looking along counter toward frosted door: black lamp behind rack shines past lifted colander at side and navy towel on rack; detached round perforated head shadow to side of triangular shoulder shadow on pane. All clear, photographic light, no diagram.'),
       (33,36,'reveal','medium','man kitchen rack lamp','Removing the towel leaves a bare rack and no human-shaped silhouette.','Man in ochre shirt holds navy towel away from now-bare chrome dish rack; black task lamp still on, closed frosted pantry glass now has only thin rack shadows and NO HUMAN SILHOUETTE. Relieved small smile, readable exposure.',('brush',.2,'[cloth rustles]','[布料窸窣]'))],
      [(0.1,'Every evening, someone seemed to stand behind his pantry door.','每天傍晚，儲藏室門後好像都站著人。',False),
       (4,'There were tiny bright holes in the head.','那顆頭裡，有幾個細小亮點。',False),
       (7.5,'Inside: empty shelves, and a hanger. No coat.','裡面只有空架和衣架，沒有外套。',False),
       (14,'He closed the door. The figure came back.','他關上門。人影又回來了。',False),
       (19,'Then he looked at what stood in front of the glass.','接著，他看向玻璃前方的東西。',False),
       (26,'He lifted the colander. The head moved away from the shoulders.','他拿起濾盆，頭就離開了肩膀。',True),
       (30.2,'The lamp had joined two ordinary shadows into one visitor.','燈光把兩個普通影子，拼成了一位訪客。',True)],36,
      'Original author draft. Optical projection differs from water and mechanical towing. The entire shadow source stays OUTSIDE the pantry throughout: lamp, rack/towel, colander, then frosted pane in that order. No impossible person or actual translucent ghost. The setup allows the coat/hanger hypothesis without inventing an intruder. Tiny shadow perforations are the fair clue. The reveal must visibly break one apparent body into two independently moved ordinary objects. No text evidence is used.')

if __name__=='__main__': main()
