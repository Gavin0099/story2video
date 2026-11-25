"""Freeze original scripts and silent storyboard intent before ImageGen."""
import json
from pathlib import Path
import math
import wave
from array import array

ROOT = Path(__file__).resolve().parent

STORIES = {
 'H02': {
  'title':'The Smallest Mirror',
  'question':['Why is she covering the mirror?', '她為何遮住鏡子？'],
  'rule':'When the lift doors close, the passenger behind the glass can cross through an uncovered reflection. The rule applies to reflections, not just the large wall mirror.',
  'alternative':'A loose white coat seems to be moving over the wall mirror; the plausible threat appears to remain behind that large mirror.',
  'clues':'The same grey fingers press against glass; the phone is present from the first frame but initially lit. Its screen goes black only after the coat covers the large mirror.',
  'evidence':'No photographed lettering. The phone screen is an ordinary blank light screen until shot-05, then black reflective glass.',
  'refs':[
   ('mira','character',['invented adult woman, chin-length straight black bob, no bangs','forest-green ribbed sweater, black trousers','plain white cotton coat worn in shots 01-03, removed and draped on wall mirror in shots 04-06; sweater never changes']),
   ('phone','prop',['plain rectangular black smartphone with rounded corners and small brass wrist loop','screen lit blank pale grey in shots 01-04, black reflective glass in shots 05-06','no logos, no icons or text']),
   ('lift','set',['small brushed-steel lift with one tall oval brass-framed mirror on rear wall','warm amber vertical light on right, closed steel sliding entrance','mirror remains on same rear wall; white coat covers reflective surface from shot 04']),
   ('passenger','character',['tall adult human-shaped grey figure behind glass, indistinct face, no wounds','long narrow grey fingers, charcoal collarless clothing','exists as reflection before payoff; grey fingers cross phone surface only in shot 06'])],
  'lines':[
   ('Mira was alone. The other passenger was behind the mirror.', 'Mira 獨自在電梯裡。另一名乘客卻在鏡子後面。'),
   ('When the doors closed, it could cross through an uncovered reflection.', '門一關，它就能穿過沒有遮住的反射面。'),
   ('She held the doors open and pulled off her coat.', '她按住開門鍵，脫下外套。'),
   ('She covered the glass. Something kept pressing underneath.', '她遮住鏡面。底下仍有東西頂著布。'),
   ('Her phone went dark. She finally let the doors close.', '手機螢幕暗了。她終於鬆手讓門關上。'),
   ('The fingers came through the smallest mirror.', '手指穿過了最小的那面鏡子。')],
  'shots':[
   ('establish','medium',['mira','phone','lift','passenger'],'A lone woman faces a mirror containing an extra grey passenger; her lit phone is already in hand.','Mira in white coat over green sweater inside the canonical lift. Black phone with lit blank screen in left hand at waist, brass wrist loop visible. In oval rear mirror a separate grey figure stands beside her reflection although no such person stands in cabin. Readable bright steel and amber light; show ordinary woman and abnormal reflection together.'),
   ('clue','close_up',['lift','passenger'],'Grey fingers press from behind the wall mirror, identifying glass as the boundary.','Tight portrait close-up of oval brass-framed wall mirror inside canonical lift. Five narrow grey fingertips press against the far side of the glass from the grey passenger; no fingers outside glass. Amber light right. No woman or phone in this insert.'),
   ('reaction','medium',['mira','phone','lift'],'She holds the door button while starting to remove her white coat.','Same Mira, same bob and green sweater, white coat slipping off right shoulder. Right index finger holding a plain unlabelled door-open button near entrance, left hand still holds lit blank phone. Frightened glance toward rear mirror outside crop. Lift entrance held open, no extra people.'),
   ('clue','medium',['mira','phone','lift'],'The white coat hides the large mirror; one raised fold suggests the threat is still there.','Same lift rear wall with white coat draped securely over entire oval mirror reflective area, brass rim peeking around cloth. Small tension fold at centre of cloth, no visible limb or face. Mira in green sweater foreground left holds lit phone, looking at cloth. Steel doors open at edge. No writing.'),
   ('reaction','close_up',['mira','phone','lift'],'A black phone screen reflects a hint of grey fingertips as the lift doors close.','Close-up of Mira green sleeve and hand holding canonical phone with brass loop. Screen now OFF, glossy black, faint reflection of long grey fingertips INSIDE the glass but no protrusion. White coat covering oval mirror softly visible behind, entrance doors now meeting closed. Keep screen in middle of portrait crop, no text.'),
   ('reveal','close_up',['mira','phone','lift','passenger'],'Grey fingers physically emerge from the black phone; the covered mirror is no longer the apparent source.','Unmistakable horror payoff close-up: same black phone held by Mira green-sleeved hand, small brass loop; FIVE narrow grey fingers protrude out through the middle of black screen into cabin, casting real shadows onto phone rim. No wounds, no gore, no shattered glass. In background same white coat still completely covers oval wall mirror and steel doors closed. Fingers occupy central portrait safe area.')]
 },
 'H03': {
  'title':'The Woman with the Hammer',
  'question':['Who is hitting that window?', '誰在敲那扇窗？'],
  'rule':'The opposite window shows this room shortly before events happen. It is a fixed glimpse of the future, not a portal or an attacker who can travel across the shaft.',
  'alternative':'A smoky silhouette raising a hammer looks like an intruder about to enter her room. She blocks the entrance to prevent that future.',
  'clues':'The figure has a white wrap on the left wrist matching Lea; smoke is visible in the opening image, and the hammer is already on her own sill. The payoff changes the hammer from weapon to escape tool.',
  'evidence':'No photographed lettering; matching white wrist wrap is evidence, not an injury image.',
  'refs':[
   ('lea','character',['invented adult woman, dark curly hair in a high round bun','ochre knitted sweater, black trousers','plain white fabric support wrap on LEFT wrist, no wounds; same appearance for future figure']),
   ('hammer','prop',['short hammer with black rubber handle and square silver steel head','rests on interior sill until shot 05; held in RIGHT hand in shots 05-06','no logos']),
   ('room','set',['small cream apartment, tall rectangular two-pane white sash window looking across a narrow dark shaft to an identical window','square grey metal storage trunk near solid cream entrance door, plain horizontal sliding bolt','small rectangular ceiling vent above door; grey smoke increases from shot 04; no visible flames']),
   ('future','set',['opposite white two-pane sash window across narrow shaft duplicates the protagonist room','future figure wears ochre sweater and left white wrist wrap but face initially obscured by grey smoke and glass glare','hammer raised in right hand with square head; no additional attacker'])],
  'lines':[
   ('Across the shaft, a woman raised a hammer inside her room.', '天井對面，一個女人在房裡舉起鐵鎚。'),
   ('That window showed Lea her own room, just before things happened.', '那扇窗會提早映出 Lea 自己房裡將發生的事。'),
   ('She bolted the door and shoved the heavy trunk against it.', '她閂上門，把沉重的箱子推去抵門。'),
   ('Then smoke poured from the vent. The blocked door would not open.', '接著煙從通風口湧出。被堵住的門打不開。'),
   ('Lea grabbed the hammer from her sill. The woman was not breaking in.', 'Lea 抓起窗台上的鐵鎚。那女人不是要闖進來。'),
   ('She was trying to get out.', '她是要逃出去。')],
  'shots':[
   ('establish','medium',['hammer','room','future'],'Across a shaft, a smoky figure raises a hammer at a window; a matching hammer rests on the near sill.','View from inside canonical cream room across narrow dark shaft. Opposite white sash window fills central portrait area; behind it smoky silhouette of woman in ochre raising black-handled silver hammer in RIGHT hand. Face obscured by grey smoke and glare, LEFT wrist white wrap barely visible. Near sill bottom foreground holds identical real hammer. No threatening figure in near room.'),
   ('clue','close_up',['lea','room','future'],'A white wrist wrap on the distant figure matches the observer wrist in foreground.','Close insert across shaft at opposite window: smoky ochre-sleeved LEFT hand with plain white support wrap braced against inside glass. Foreground edge: Lea own left ochre sleeve and identical white wrist wrap rests on near sill. Deliberate match, two hands separated by shaft and two windows, face absent. Grey smoke behind far glass, cream walls and white frames.'),
   ('reaction','medium',['lea','room'],'She barricades her own exit because she reads the figure as an incoming threat.','Inside cream apartment: Lea high dark curly bun, ochre sweater, black trousers, LEFT white wrist wrap, pushes square heavy grey metal storage trunk firmly against cream entrance door with horizontal bolt visibly shut. Strained frightened expression. Window and hammer outside crop, no smoke yet in this near room.'),
   ('reaction','medium',['lea','room'],'Smoke comes from above her blocked doorway; the barricade is now a danger.','Same Lea recoils toward camera as visible grey smoke pours from small ceiling vent above same cream entrance door. Horizontal bolt shut; same square grey metal trunk tight against door. Lea left white wrist wrap clear as she tugs trunk, concern and urgency, no flames or burns. Readable exposure and cream room geometry.'),
   ('reveal','medium',['lea','hammer','room'],'The smoky hammer figure is recognizably Lea, using her own hammer to escape her room.','From exterior shaft looking directly at Lea OWN white sash window. Smoke behind glass. Lea with identical high dark curly bun, ochre sweater and LEFT white wrist wrap clearly recognizable; RIGHT hand raises canonical black-handled silver square hammer against inside of intact glass, matching pose of first shot figure. Fear and need for air, not aggression. This is the SAME room, not another intruder. Central face, wrap, hammer and window readable.'),
   ('reveal','medium',['lea','hammer','room'],'Broken window gives her air; the hammer was an escape tool.','Same exterior view into same white sash window: upper glass now broken open with safe edge fragments, no wounds; Lea ochre sweater, high curly bun and left white wrap leaning face toward fresh air through opening. Right hand lowers same hammer safely inside below chest. Grey smoke stays behind her in room. Relief mixed with fear, fully readable window frame and match to preceding shot, no flames or gore.')]
 },
 'H04': {
  'title':'The Name Underneath',
  'question':['Why did erasing her name fail?', '擦掉名字為何沒用？'],
  'rule':'At midnight the house visitor comes for every name left in the guestbook. Marks copied onto a bound duplicate page are still names in that same book.',
  'alternative':'Eva believes the pencil entry is the only entry and the shape outside is the night porter; erasing the visible name appears sufficient.',
  'clues':'A blue copying sheet corner is visible below the writing page from the first close-up. Pencil pressure leaves a second entry; erasing the surface does not remove it. No warning text explains this before payoff.',
  'evidence':'The ONLY photographed lettering permitted is EVA, written in pencil on top page at first, erased at shot 03, and dark blue intact on underlying duplicate page in shots 05-06. All other pages and surfaces blank.',
  'refs':[
   ('eva','character',['invented adult woman, short dark-brown pixie haircut','burgundy cardigan over plain beige blouse, dark trousers','no jewellery, no wounds']),
   ('book','prop',['large brown cloth-bound guestbook with cream pages and attached blue carbon-copy sheet beneath top writing leaf','the ONLY text is EVA: grey pencil top page initially, erased on top at shot 03, intact dark-blue copy underneath at shots 05-06','same brown spine and cream paper; carbon blue corner visible from first shot; no headings or warning text']),
   ('pencil','prop',['plain yellow hexagonal pencil with pink eraser and silver ferrule','used graphite tip to sign first, pink eraser in shot 03','no logos or printed marks']),
   ('lobby','set',['old apartment lobby with cream plaster, green tiled lower walls, small dark wooden reception desk','wired-glass entrance door behind desk at left; no signage or brands','warm overhead lamp, sufficient readable exposure']),
   ('visitor','character',['tall charcoal overcoat and brimmed dark hat, face a featureless shadow','ordinary adult human outline, long arms, no wounds or gore','only indistinct outside wired glass before payoff, unmistakably inside lobby behind Eva in final shot'])],
  'lines':[
   ('Eva signed in. The night porter had already gone.', 'Eva 簽了名。夜班管理員已經離開。'),
   ('At midnight, the house visitor came for names left in that book.', '午夜，屋裡的訪客會來找名字還留在簿上的人。'),
   ('One minute left. She rubbed out every trace of her name.', '剩下一分鐘。她擦掉名字的每一道痕跡。'),
   ('The shape outside disappeared. Eva closed the book and breathed.', '門外的身影消失了。Eva 合上簿子，鬆了口氣。'),
   ('At the chime, the book fell open to the page underneath.', '鐘響時，簿子掉落，翻開了底下那一頁。'),
   ('Her name was still there. So was her visitor.', '她的名字還在。她的訪客也在。')],
  'shots':[
   ('establish','close_up',['eva','book','pencil','lobby'],'She signs EVA; a blue sheet corner protrudes below the cream page.','Top-down portrait close-up of burgundy-sleeved Eva hand signing exact single word EVA in grey pencil on otherwise blank cream guestbook page. Brown cloth binding, plain yellow pencil pink eraser. Small blue carbon sheet corner peeks under cream writing page at lower right. Warm lamp on dark wooden reception desk. No other text, no copied page visible yet.'),
   ('clue','close_up',['book','lobby','visitor'],'An indistinct person waits beyond wired glass while the signed book remains on the desk.','Close portrait view of same brown guestbook open on dark lobby desk, grey pencil EVA visible, small blue corner beneath top leaf. Behind in soft focus same wired-glass entrance door contains indistinct tall charcoal coat-and-hat silhouette OUTSIDE. Could be a porter. Cream upper walls green tile below. No explanatory text; keep book and doorway visible within portrait crop.'),
   ('reaction','close_up',['eva','book','pencil','lobby'],'The eraser removes the top name but leaves the blue page corner untouched.','Same book and desk, Eva burgundy-sleeved hand using PINK ERASER end of same yellow pencil to finish removing EVA. Top cream page now visually blank except grey eraser dust and faint rubbed area, NO readable letters on surface. Blue carbon corner remains tucked underneath at lower right; do NOT expose underneath page yet. Brown binding same.'),
   ('reaction','medium',['eva','book','lobby'],'She closes the book, believing the empty visible page means safety; doorway is empty.','Eva short dark pixie haircut, burgundy cardigan beige blouse, standing at same dark reception desk, pressing CLOSED brown guestbook cover with both hands, relief in face. Wired-glass entrance door behind left is empty. Green lower tiles cream walls same. No pencil in frame, no visitor inside, no letters on cover.'),
   ('reveal','close_up',['book','lobby'],'The lifted blank writing leaf reveals an untouched blue copy of EVA below.','Unmistakable close-up of same brown cloth guestbook now open after falling onto same dark desk: top cream leaf lifted up and visibly blank rubbed area; blue carbon paper folded back to side; UNDERLYING attached cream duplicate page shows exact word EVA in DARK BLUE at same position. Show physical stacked pages and brown spine clearly. ONLY lettering EVA, large enough to read in centre of portrait crop. No figures, no warning text.'),
   ('reveal','medium',['eva','book','lobby','visitor'],'Her intact name is visible in the book; the visitor now stands directly behind her inside the lobby.','Same lobby, medium portrait: terrified Eva recognizable pixie hair burgundy cardigan beige blouse at wooden desk. Open brown book in lower central foreground with dark-blue EVA on cream duplicate page, blank top leaf flipped back, blue copying sheet folded aside. Tall shadow-faced visitor in charcoal coat and brimmed hat stands INSIDE lobby immediately behind Eva, separated visibly from wired-glass entrance at left. Ordinary long hands at sides, no touch or gore. Face, book and visitor all in central portrait safe area.')]
 }
}

def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def build():
    for sid,s in STORIES.items():
        dest=ROOT/sid
        (dest/'assets').mkdir(parents=True,exist_ok=True)
        times=[0,5.5,11,17,23,28.5,36]
        shots=[]
        for i,(function,framing,refs,conveys,prompt) in enumerate(s['shots']):
            shot={'id':f'shot-{i+1:02}','function':function,'framing':framing,'start':times[i],'end':times[i+1],
                  'source':{'sheet':'shots-a' if i<3 else 'shots-b','cell':i%3,'crop':[0,0,1,1]},
                  'camera':{'zoom':[1.0,1.035],'from':[.5,.5],'to':[.5,.5]},
                  'required_references':refs,'sfx':[], 'conveys':conveys,
                  'prompt':prompt+' Full-bleed realistic staged fictional photography, readable exposure. Each cell portrait 9:16 with all essential evidence centrally framed. No captions, no added explanatory lettering, no gore, no real brands.'}
            shots.append(shot)
        narration=[{'id':f'line-{i+1:02}','en':en,'zh':zh,'voice':'af_heart','speed':1.08,
                    'reveal':shots[i]['function']=='reveal','not_before':times[i]+.18,'gap_before':.08}
                   for i,(en,zh) in enumerate(s['lines'])]
        sheets={name:{'file':f'assets/{name}.png','columns':(2 if name=='reference' else 3),
                      'rows':(3 if name=='reference' else 1),'edge_px':2}
                for name in ['reference','shots-a','shots-b']}
        save(dest/'shots.json',{'version':1,'story_id':sid.lower()+'-static-v1','fiction':'FICTION — original invented story, not a true-event account. Rights: pending_verification.',
                              'genre':'urban_horror','question':dict(zip(['en','zh'],s['question'])), 'sheets':sheets,'narration':narration,'shots':shots})
        save(dest/'references.json',{'version':1,'items':[{'id':rid,'kind':kind,'invariants':inv,
             'canonical':{'sheet':'reference','cell':i,'crop':[0,0,1,1]},
             'appears_in':[shot['id'] for shot in shots if rid in shot['required_references']]}
             for i,(rid,kind,inv) in enumerate(s['refs'])]})
        lines=[f'# FICTION — {sid}: {s["title"]}','', 'Genre: urban_horror','Rights: pending_verification',
               'Original invented fiction; no real people, events, brands, or source-work recreation. No gore.',
               'Target: 36.0 seconds; English narration, English and Traditional Chinese sidecars.',
               'Opening question only at 1.0–3.5 seconds: '+s['question'][0]+' / '+s['question'][1],
               '', '## World rule',s['rule'],'','## Alternative and fair clues',s['alternative'],s['clues'],
               '', '## In-world evidence text',s['evidence'],'','## Script']
        for i,(en,zh) in enumerate(s['lines']):
            lines += [f'{times[i]:g}–{times[i+1]:g}s: {en}',zh,'']
        lines += ['## Shot list','| Shot | Seconds | Function | Image observation |','|---|---|---|---|']
        lines += [f'| {x["id"]} | {x["start"]}–{x["end"]} | {x["function"]} | {x["conveys"]} |' for x in shots]
        lines += ['','## SILENT STORYBOARD — pre-ImageGen check','Written and frozen before any image call. Read these observations with narration and question removed.']
        lines += [f'{i+1}. {x["conveys"]}' for i,x in enumerate(shots)]
        lines += ['','The visual causal spine is carried by the above changed object states and matching evidence. The supernatural rule requires narration; images alone do not establish its verbal precision. Silent readability is a production intent, not a passed gate.',
                  'Pre-generation revision: use explicit paired before/after object states and the same camera-facing evidence in the payoff. No detached reaction portraits. Each close-up must survive centred 9:16 extraction.',
                  '', '## Gate status','Story Quality Gate PENDING; Storyboard Quality Gate PENDING; Viewer Gate HUMAN_TEST_PENDING. No blind readers this round. Market acceptance NOT_TESTED.']
        (dest/'story.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        # Locally synthesized nonverbal Foley, not a downloaded/licensed recording.
        sounds=[('pulse',.38,85),('click',.16,900),('chime',.9,660)]
        for name,dur,freq in sounds:
            vals=array('h')
            for n in range(round(24000*dur)):
                t=n/24000
                env=min(1,t/.008)*math.exp(-t/(dur*.27))
                v=.22*env*(math.sin(2*math.pi*freq*t)+.25*math.sin(2*math.pi*freq*1.49*t))
                vals.append(round(v*32767))
            with wave.open(str(dest/'assets'/f'{name}.wav'),'wb') as f:
                f.setparams((1,2,24000,0,'NONE','not compressed')); f.writeframes(vals.tobytes())
        data=json.loads((dest/'shots.json').read_text(encoding='utf-8'))
        for idx,name,en,zh in [(1,'pulse','[Low pulse]','[低沉脈衝聲]'),(3,'click','[Dry click]','[喀一聲]'),(4,'chime','[Chime]','[鐘聲]')]:
            data['shots'][idx]['sfx']=[{'file':f'assets/{name}.wav','offset':0,'gain':.5,'en':en,'zh':zh}]
        save(dest/'shots.json',data)

if __name__=='__main__': build()
