"""Author-owned original story manifests, synthetic foley and pre-generation checks."""
from pathlib import Path
import json, math, wave, random

ROOT = Path(__file__).resolve().parent
def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

STORIES = {
'P01': dict(title='The Thread Under the Scale', mechanism='object_function / hidden foot force; unchanged P01 v3',
 question=['Why did the weight drop?', '重量為什麼下降？'],
 summary='A buyer cuts the thread loading a dishonest spring scale. A brass calibration weight seems responsible, but merely hides the seller’s toe loop.',
 alternative='The brass cylinder might be a suspended ballast. Both seller hands remain above the counter.',
 refs=[('buyer','character','woman about 30; straight chin-length black bob; olive jacket over cream shirt; brown shoulder bag'),
       ('seller','character','man about 50; short gray hair; clean shaven; burgundy sweater; charcoal trousers; plain black leather lace-up shoes'),
       ('scale','prop','brass mechanical spring scale; cream unnumbered dial with black needle; shallow moving silver pan with dent on front rim; exactly three gold pieces: oval, triangle, rectangle; one black thread knotted to eyelet under moving pan, never housing'),
       ('cylinder','prop','one cylindrical brass calibration weight with empty lifting ring; sits independently on a low wooden shelf; thread passes BEHIND it and is never attached to its ring'),
       ('tools','prop','small silver scissors; brown rectangular clasp purse; intact or severed black thread only as scripted'),
       ('shop','set','warm daylight jeweler shop; dark wooden counter with small thread hole and low shelf; no brands or readable lettering')],
 lines=[(0,'One snip. The gold suddenly weighed less.','剪了一下。金子的讀值突然變輕了。',False),
 (3.5,'Earlier, he charged for the higher reading. Both hands were here.','剪線前，他按較高的讀值收費。兩隻手都在檯面上。',False),
 (7,'She dropped her purse beside the counter.','她的錢包掉在櫃檯旁。',False),
 (11,'Under the scale: a brass weight, right beneath the thread.','秤下面有個黃銅砝碼，就在細線正下方。',False),
 (15,'The needle held steady as he slid her the bill.','他把帳單推給她，指針一直停在高處。',False),
 (23,'Where had the extra weight come from?','多出來的重量，究竟從哪裡來？',False),
 (27,'The brass weight stood on a shelf. His foot pulled the thread.','黃銅砝碼放在架子上。是他的腳在拉線。',True),
 (32,'She cut away his pull, not any gold.','她剪掉的是他的拉力，金子一塊都沒少。',True)],
 shots=[
 (0,.5,'clue','close_up','Scissors and separated thread ends show a snip.','Extreme close-up under counter, silver scissors just CLOSED after cutting black thread. Two separated thread ends clear. No foot loop in frame.',['tools','shop']),
 (.5,3.5,'establish','close_up','Needle is lower, all three gold pieces remain.','POST CUT scale dial needle at lower-left position, all three distinctive gold pieces remain on dented silver moving pan. Readable close view.',['scale','shop']),
 (3.5,7,'establish','medium','Both hands are visible above a high-reading scale.','BEFORE CUT over buyer shoulder: scale needle high upper-right, unchanged three gold pieces on dented pan, seller with BOTH hands clearly above wooden counter, one pointing dial other smoothing blank receipt.',['buyer','seller','scale','shop']),
 (7,11,'clue','close_up','Purse has fallen; thread is tied to moving pan.','Low side view: brown clasp purse on floor foreground. Above it visible eyelet UNDER MOVING PAN with knotted thin black thread descending through counter hole. No toe loop visible.',['tools','scale','shop']),
 (11,15,'clue','close_up','Thread appears to lead behind a brass weight.','Tight low view of brass cylinder top and empty lifting ring beneath descending thread. Thread disappears BEHIND cylinder, never through ring. Bottom of cylinder and support contact OUTSIDE crop.',['cylinder','scale','shop']),
 (15,19,'reaction','medium','Seller offers receipt while high reading persists.','Counter-height profile buyer suspicious, seller sliding blank receipt with one hand, other hand beside scale; BOTH above counter. Needle high, same three gold pieces.',['buyer','seller','scale','shop']),
 (19,23,'clue','medium','Scissors are ready; seller heel is raised.','Low reverse: buyer takes small scissors from brown open bag. Seller black shoe heel slightly raised behind brass cylinder, toe occluded by cylinder; NO visible toe loop yet.',['buyer','seller','tools','cylinder','shop']),
 (23,27,'reaction','close_up','Unchanged gold contradicts the lower reading.','POST CUT close view, same oval triangle rectangle gold on dented pan, needle lower-left; seller hands above counter in background.',['seller','scale','shop']),
 (27,29,'reveal','close_up','Brass weight is supported and its ring is empty.','REVEAL side angle: entire brass cylinder firmly resting on wooden shelf, lifting ring EMPTY, black thread passes behind cylinder. No floating weight.',['cylinder','scale','shop']),
 (29,32,'reveal','close_up','Toe loop is the hidden source of tension.','BEFORE CUT replay low floor view of seller black lace-up shoe, black thread loop around TOE stretched upward behind independently supported brass cylinder to counter hole. Heel raised. Single continuous taut thread.',['seller','scale','cylinder','shop']),
 (32,34,'reveal','close_up','Post-cut lower reading and same gold resolve the opening.','POST CUT matched close view of cream dial lower-left needle and same three gold pieces on dented pan; separated thread end dangling from pan eyelet.',['scale','shop']),
 (34,36,'reaction','medium','Buyer confronts seller with the evidence.','Buyer olive jacket holds silver scissors and looks directly at burgundy seller, both beside same scale and three gold pieces, seller hands still on counter.',['buyer','seller','scale','tools','shop'])]),
'P02': dict(title='The Blackened Message', mechanism='context_reversal / printing negative',
 question=['Why black out her message?', '為什麼把字全塗黑？'],
 summary='A printmaker inks a hand-carved invitation block until its pale lettering disappears. The apparent vandalism is how she prints the invitation.',
 alternative='The woman seems to be censoring a damaged invitation before a visitor arrives.',
 refs=[('maker','character','woman about 40; curly auburn hair tied low; mustard cardigan; indigo canvas apron; no jewelry'),
 ('block','prop','one palm-size rectangular pale maple relief block; raised mirror-reversed word HOME only; one crescent nick in lower right wood edge; ink state goes pale to fully black'),
 ('kit','prop','short black rubber brayer with red wooden handle; shallow black ink tray; cream blank cotton paper; small wooden baren'),
 ('studio','set','sunny small print studio; honey wood table; sage wall; cream envelope with green ribbon, no other readable writing')],
 lines=[(0,'She covered her message in black. Then invited the visitor closer.','她把字全塗黑，還請訪客靠近。',False),
 (5,'The invitation was for tonight. There was no spare block.','邀請是今晚要用的，也沒有備用木板。',False),
 (10,'A chipped corner. Letters facing the wrong way.','角落缺了一塊，字母的方向也反了。',False),
 (15,'Was she hiding a mistake? She kept the clean paper dry.','她是在掩飾錯誤嗎？乾淨的紙一直沒沾墨。',False),
 (21,'Now every letter had vanished into black.','現在，每個字都消失在一片黑裡。',False),
 (27,'She pressed the paper onto the raised letters, then peeled it back.','她把紙壓在凸字上，再揭開。',True),
 (32,'The ruined message was the printing surface. This was her first invitation.','被毀掉的字其實是印面，這才是第一張邀請。',True)],
 shots=[(0,5,'establish','medium','Maker blacks out a wooden message.','Maker holds red-handled brayer over partially inked pale relief block; raised backward HOME partly black; blank paper beside it. Keep black ink readable.',['maker','block','kit','studio']),
 (5,10,'clue','close_up','Envelope and unique nick suggest a one-off invitation.','Close-up cream envelope green ribbon next to pale half-inked maple block with distinctive crescent nick lower right. No printed invitation yet.',['block','studio']),
 (10,15,'clue','close_up','Backwards raised letters are fair evidence of a print matrix.','Raking-light macro raised relief letters mirror-reversed HOME in maple, ink on top surfaces, crescent nick lower right; side relief height visible; NO correct-direction HOME.',['block','studio']),
 (15,21,'reaction','medium','She calmly protects blank paper while ink darkens block.','Maker in mustard cardigan indigo apron holding clean blank cream paper away from black ink tray; half-black relief block and red-handled brayer on table; focused calm expression.',['maker','block','kit','studio']),
 (21,27,'clue','close_up','Fully black surface appears ruined, paper remains blank.','Entire raised block surface uniformly black, lettering difficult to distinguish but embossed relief catches side light; clean blank cream paper alongside, red brayer.',['block','kit','studio']),
 (27,30,'reveal','close_up','Paper contacts the relief.','Maker hands press BLANK BACK of cream paper onto black relief block with wooden baren; red brayer set aside. No finished print yet.',['maker','block','kit','studio']),
 (30,33,'reveal','close_up','Peeling reveals a correct-direction printed word.','Hands peel paper off block; underside facing camera carries crisp black correctly oriented HOME; matching raised backward HOME on black block beneath; same crescent nick.',['maker','block','kit','studio']),
 (33,36,'reveal','medium','Finished invitation differs from apparent destroyed block.','Maker presents cream paper with black HOME above cream envelope green ribbon; black maple printing block with nick and brayer remain below. Bright readable photography.',['maker','block','kit','studio'])]),
'P03': dict(title='The Crack That Crossed the Table', mechanism='other / optical shadow misattribution',
 question=['Why buy the cracked vase?', '為什麼買有裂痕的花瓶？'],
 summary='A buyer chooses a vase with an apparent black crack. The line continues across the table, and blocking light reveals it is a suspended wire’s shadow.',
 alternative='A bargain buyer may tolerate or plan to repair a genuine crack. No repair actually occurs.',
 refs=[('buyer','character','woman about 35; dark brown pixie haircut; navy turtleneck; tan canvas tote'),
 ('potter','character','man about 45; shaved head; short dark beard; light gray shirt; rust apron'),
 ('vase','prop','single matte ivory pear-shaped vase; narrow short neck; small cobalt-blue circular dot near foot; structurally unbroken smooth surface throughout; no handles'),
 ('wire','prop','thin straight black hanging wire belonging to small circular wire mobile above table; strong single side light casts thin diagonal dark shadow across vase and tabletop; no physical black mark on vase'),
 ('shop','set','bright pottery shop; pale oak display table; one square side window upper left; warm cream wall; pottery tools, no signs or brands')],
 lines=[(0,'She chose the vase with a black crack. The potter offered another.','她挑了有黑色裂痕的花瓶，陶匠提議換一個。',False),
 (5,'No discount. No glue. She still wanted this one.','沒有折扣，也沒有膠，她還是要這一個。',False),
 (10,'The thin line ran past the blue dot and across the table.','細線經過藍點，還一路延伸到桌面。',False),
 (16,'Above it hung a wire mobile, turning in the window light.','上方的鐵絲吊飾，在窗光裡轉動。',False),
 (21,'She moved her hand toward the line, without touching the vase.','她把手伸向細線，卻沒碰到花瓶。',False),
 (27,'Her hand blocked the light. The crack disappeared.','她的手擋住光，裂痕消失了。',True),
 (32,'She had bought an unbroken vase, with somebody else’s shadow.','她買的是完整的花瓶，裂痕只是吊飾的影子。',True)],
 shots=[(0,5,'establish','medium','Buyer selects apparently cracked vase.','Navy buyer points to ivory pear vase cobalt dot; thin sharp diagonal BLACK SHADOW resembles crack, crossing vase and table. Rust apron potter offers empty hands, concerned.',['buyer','potter','vase','wire','shop']),
 (5,10,'reaction','medium','Buyer confidently insists without repair.','Buyer tan tote at hip confidently holds out open hand toward selected vase; potter rust apron puzzled, same ivory vase and diagonal shadow on table. NO money text or glue.',['buyer','potter','vase','wire','shop']),
 (10,16,'clue','close_up','Line continues seamlessly off vase onto tabletop.','Close-up lower half unbroken ivory vase with cobalt dot: thin diagonal shadow crosses ceramic and continues across pale oak tabletop, same light direction upper left. Clearly shadow, no physical fracture.',['vase','wire','shop']),
 (16,21,'clue','medium','Wire mobile sits between window and vase.','Vertical composition shows thin black circular wire mobile suspended above pale oak table; bright square side window upper left; its single straight wire casts thin shadow onto ivory vase below.',['vase','wire','shop']),
 (21,27,'reaction','close_up','Hand approaches light beam without touching ceramic.','Navy sleeve buyer hand reaches into sunlight beside vase, fingertips do NOT touch ivory surface; black diagonal shadow still visible across cobalt dot and table; anticipatory.',['buyer','vase','wire','shop']),
 (27,30,'reveal','close_up','Blocking light removes the thin line.','Same vase position and cobalt dot. Navy sleeve open palm between upper-left window and vase casts BROAD soft hand shadow; thin black wire line absent from shaded area, smooth intact ceramic. No touching.',['buyer','vase','wire','shop']),
 (30,33,'reveal','close_up','Smooth vase shows no repair or break.','Close-up buyer hand lifts ivory pear vase into diffuse light away from wire shadow. Smooth perfectly intact surface, same cobalt blue dot, no cracks, no repair.',['buyer','vase','shop']),
 (33,36,'reveal','medium','Shadow remains on empty tabletop while vase leaves.','Navy buyer carries intact ivory vase with cobalt dot at chest; potter smiles; hanging circular wire mobile shadow still on empty pale oak tabletop where vase stood.',['buyer','potter','vase','wire','shop'])]),
'P04': dict(title='The Rope He Refused to Pull', mechanism='causal_reversal / counterweight release',
 question=['Why cut it to raise the flag?', '為什麼剪繩才升旗？'],
 summary='A sailmaker cuts the rope holding a pennant low. A hidden sandbag falls along the opposite side of a simple pulley and raises the pennant; the cut removes a restraint.',
 alternative='A taut line beside a low flag suggests a broken or jammed lifting line. Cutting appears to make raising it impossible.',
 refs=[('maker','character','man about 40; wavy short black hair; teal work shirt sleeves rolled; beige trousers; no hat'),
 ('flag','prop','small triangular RED cloth pennant with WHITE circular patch near broad hoist edge; attached by TWO eyelets to left vertical running rope; first low then high'),
 ('rig','prop','one brass pulley on top of wooden upright; single continuous cream running rope through pulley; left leg holds pennant; right leg tied to tan canvas sandbag; separate thin BLUE restraint ties LEFT running-rope leg downward to bench cleat'),
 ('bag','prop','tan rectangular canvas sandbag with black cross stitching; tied to right cream rope; initially raised behind bench front apron, later on floor; no other weight'),
 ('tools','prop','small orange-handled utility scissors; thin blue restraint intact then cut with two loose ends'),
 ('loft','set','sunlit sail repair loft; whitewashed brick wall; wooden workbench with tall upright and high brass pulley; bench front apron partly occludes raised sandbag; no branding')],
 lines=[(0,'He wanted the flag higher. So he reached for scissors.','他想把旗升高，卻拿起了剪刀。',False),
 (5,'The red pennant hung low. The rope beside it was tight.','紅旗垂在低處，旁邊的繩子卻繃緊了。',False),
 (10,'Perhaps the lifting line was jammed. He never pulled it.','也許升旗繩卡住了，但他從沒拉它。',False),
 (16,'One pale rope crossed the pulley. A blue tie held its left side down.','一條淺色繩穿過滑輪，藍色細繩把左側固定住。',False),
 (22,'He cut only the blue tie.','他只剪斷了藍色細繩。',False),
 (27,'Behind the bench, a sandbag dropped. The other side rose.','工作檯後的沙袋落下，另一側就升起。',True),
 (32,'He had cut the restraint, and let the weight do the lifting.','他剪開的是固定繩，升旗的力來自沙袋。',True)],
 shots=[(0,5,'establish','medium','Maker holds scissors beside a low flag.','Teal maker holds orange scissors beside LOW red triangular pennant white circle at chest height on LEFT cream rope. High brass pulley and bench. Sandbag concealed behind bench apron.',['maker','flag','rig','tools','loft']),
 (5,10,'clue','close_up','Taut rope and low pennant suggest jam.','Close-up LOW red pennant white circle attached by two eyelets to taut LEFT cream rope. Separate thin BLUE restraint tied below flag down to bench cleat. No cut yet.',['flag','rig','tools','loft']),
 (10,16,'reaction','medium','Maker studies rig rather than pulling.','Teal maker studies low red pennant, orange scissors down at side, both hands away from cream lifting rope; brass pulley above, right rope vanishes behind bench.',['maker','flag','rig','tools','loft']),
 (16,22,'clue','close_up','Two rope legs run over pulley, blue restraint differs.','Portrait view brass single pulley high on upright with ONE continuous cream rope draped over, left leg down to low red flag and thin blue restraint cleat, right leg descends behind bench apron. Sandbag not visible yet.',['flag','rig','loft']),
 (22,27,'clue','close_up','Only blue restraint is cut; cream running rope stays intact.','Close-up orange scissors just cut BLUE restraint near bench cleat, two separated BLUE ends. Thick cream running rope INTACT. Low red flag edge above.',['flag','rig','tools','loft']),
 (27,30,'reveal','close_up','Opposite end is weighted by falling bag.','REVEAL low reverse behind bench: tan canvas sandbag black cross stitching now rests on floor, tied to RIGHT cream rope from high pulley; blue severed ends at left bench cleat. No human pulling.',['rig','bag','tools','loft']),
 (30,33,'reveal','medium','Flag has risen as counterweight has fallen.','Wide portrait complete rig: red pennant white circle now HIGH on LEFT leg just below high brass pulley; RIGHT cream rope reaches tan sandbag black cross stitching on floor; both legs single pulley visible, cut blue restraint hangs left cleat.',['flag','rig','bag','tools','loft']),
 (33,36,'reaction','medium','Maker shows empty hands below raised pennant.','Teal maker shows empty open hands smiling below HIGH red pennant white circle; orange scissors set on bench; cream running rope intact, bag on floor right, severed blue tie on cleat.',['maker','flag','rig','bag','tools','loft'])])}

if any((ROOT/key/'shots.json').exists() for key in STORIES):
    raise SystemExit('Final story inputs already exist. Preserve them; do not rerun draft authoring over delivery.')

for key, s in STORIES.items():
    folder=ROOT/key; (folder/'assets').mkdir(parents=True,exist_ok=True)
    sheets={name:dict(file=f'assets/{name}.png',columns=2,rows=3,edge_px=2) for name in ('reference','shots-a','shots-b')}
    shots=[]
    for i,(start,end,func,framing,conveys,prompt,refs) in enumerate(s['shots']):
        shots.append(dict(id=f'shot-{i+1:02}',function=func,framing=framing,start=start,end=end,
          source=dict(sheet='shots-a' if i<6 else 'shots-b',cell=i%6,crop=[0,0,1,1]),
          camera=dict(zoom=[1.015,1.045],**{'from':[.5,.5],'to':[.5,.5]}),
          required_references=refs,sfx=[],conveys=conveys,prompt=prompt))
    # Locally synthesized subtle foley; never pretends to be documentary sound.
    random.seed(1729)
    samples=[int(4200*random.uniform(-1,1)*math.exp(-t/500)) for t in range(4800)]
    with wave.open(str(folder/'assets/tick.wav'),'wb') as w:
        import struct
        w.setparams((1,2,24000,0,'NONE','not compressed')); w.writeframes(struct.pack('<'+'h'*len(samples),*samples))
    foley_index=0 if key=='P01' else 5
    shots[foley_index]['sfx']=[dict(file='assets/tick.wav',offset=.1,gain=.45,en='[snip]' if key in ('P01','P04') else '[soft contact]',zh='[剪斷聲]' if key in ('P01','P04') else '[輕碰聲]')]
    data=dict(version=1,story_id=f'puzzle-{key.lower()}-static-v1',fiction='FICTION — original fictional puzzle; rights pending_verification',genre='puzzle',
        question=dict(zip(('en','zh'),s['question'])),sheets=sheets,
        narration=[dict(id=f'line-{i+1:02}',en=en,zh=zh,voice='af_heart',speed=1.08,reveal=reveal,not_before=t,gap_before=.08 if i else 0) for i,(t,en,zh,reveal) in enumerate(s['lines'])],shots=shots)
    refs=dict(version=1,items=[dict(id=rid,kind=kind,invariants=invariants.split('; '),canonical=dict(sheet='reference',cell=i,crop=[0,0,1,1]),appears_in=[sh['id'] for sh in shots if rid in sh['required_references']]) for i,(rid,kind,invariants) in enumerate(s['refs'])])
    save(folder/'shots.json',data); save(folder/'references.json',refs)
    script='\n'.join(f"- {t:g} s: {en}\n  - zh-Hant: {zh}" for t,en,zh,_ in s['lines'])
    table='\n'.join(f"| {sh['id']} | {sh['start']:g}–{sh['end']:g} | {sh['function']} | {sh['conveys']} |" for sh in shots)
    md=f'''# FICTION — {key}: {s['title']}

Genre: puzzle
Rights: pending_verification. Original-fiction candidate; no true-event claim, real people or brands. External originality clearance remains outstanding.
Duration: 36 seconds. Opening question: 1.0–3.5 seconds only. Static photographic states with camera moves; actions are inferred across cuts.
Mechanism: {s['mechanism']}
Story summary: {s['summary']}
Plausible alternative: {s['alternative']}
Story Quality Gate PENDING. Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Script

{script}

## Shot list

| Shot | Seconds | Narrative function | Silent observation |
| --- | --- | --- | --- |
{table}

## SILENT STORYBOARD — BEFORE IMAGEGEN

The ordered observations above are the required silent key frames. The core event must be understood from state changes, not an explanation card. Establish shows the apparent contradiction; clue close-ups preserve the alternative; reaction registers a deliberate choice; reveal exposes the physical relationship and revisits the opening state.

Pre-generation revision: use explicit before/after states rather than asking a still photograph to show movement. Reveal pairs retain the same unique prop markings. No explanatory lettering. P02 permits photographed evidence HOME (mirrored on the block, correct on the proof); all other stories require no readable evidence text. No extra narrative text in images.

Silent limitations: exact motive and temporal order may still need narration. This is an author inspection, not a reader test or a gate pass. If generated evidence fails, record the actual defect with timestamps; at most one fix pass.
'''
    if key=='P01':
        md+='\nP01 source: genre-pilot-v3 branch puzzle-v3.md. All eight source narration lines retained verbatim; no story change. 0–3.5 and 23–27/32–36 are post-cut; 3.5–23 and 27–32 revisit pre-cut evidence. Static states replace continuous snip/needle motion. v3 reader scores 81/80/84 did not meet the existing story gate; not transferred as a pass.\n'
    (folder/'story.md').write_text(md,encoding='utf-8')
print('Prepared four stories and silent checks before generation.')
