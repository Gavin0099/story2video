"""Owner-authorized local A/B pilot. No hosted APIs; no reference-tree writes.

Run with the read-only render Python using -B. All generated files are in ROOT.
The frozen source Markdown is copied with git show outside this program.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import shutil
import sys
import textwrap
import wave

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO / "artifacts/genre-pilot-20261124/h01-v2.1"
SHARED = ROOT / "shared"
sys.path.insert(0, str(HERE / "motion"))
import hybrid_motion as hm

# Reuse the pinned renderer with this experiment's isolated output boundary.
hm.OUTPUTS = ROOT
RATE = 24000
BASE_SHA = "6270889a9de8cfb056c7009b69ffa01f7e02e474"
SOURCE_SHA = "fe2ce6abd4c3ec1d8537850557077a1abd7c930e"
MODELS = Path("D:/story2video/artifacts/73h-episode02/models")
MODEL_HASHES = {
    "kokoro-v1.0.int8.onnx": "6e742170d309016e5891a994e1ce1559c702a2ccd0075e67ef7157974f6406cb",
    "voices-v1.0.bin": "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}


def save(path, value):
    hm.save(path, value)


def wav(path, values):
    import numpy as np
    with wave.open(str(path), "wb") as out:
        out.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        out.writeframes((np.clip(values, -.99, .99)*32767).astype("<i2").tobytes())


def readwav(path):
    import numpy as np
    with wave.open(str(path), "rb") as stream:
        assert stream.getframerate() == RATE
        return np.frombuffer(stream.readframes(stream.getnframes()), "<i2").astype(float)/32767


def stamp(t):
    ms = round(t*1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def make_audio():
    import numpy as np
    for name, expected in MODEL_HASHES.items():
        if hm.digest(MODELS/name) != expected:
            raise ValueError("Local model digest mismatch")
    from kokoro_onnx import Kokoro
    tts = Kokoro(*(str(MODELS/name) for name in MODEL_HASHES))
    folder = SHARED / "voice"
    folder.mkdir(exist_ok=True)
    if (SHARED/"mix.wav").exists():
        raise FileExistsError("Shared mix already exists; preserve it")
    # Each subtitle is placed using its own measured synthesized PCM boundaries.
    texts = [
        ("call", "Nia?", "Nia？", "af_bella"),
        ("mom_voice", "Mom's voice. But Mom was asleep beside her.", "是媽媽的聲音。可媽媽正睡在她身旁。", "af_heart"),
        ("mouth", "Nia covered her mouth.", "Nia 捂住嘴。", "af_heart"),
        ("untouched", "Nobody had pressed the intercom.", "沒有人按過對講機。", "af_heart"),
        ("rule1", "After midnight, it saved your first reply,", "午夜後，它會存下你的第一句回話，", "af_heart"),
        ("rule2", "but only the final two words.", "卻只留最後兩個英文單字。", "af_heart"),
        ("consent", "An invitation unlocked the door.", "留下的是邀請，門鎖就會打開。", "af_heart"),
        ("dawn", "You couldn't record again until dawn.", "天亮前不能重錄。", "af_heart"),
        ("cough_intro", "Mom coughed.", "媽媽咳了兩聲。", "af_heart"),
        ("copied", "The speaker copied it.", "喇叭照樣學了。", "af_heart"),
        ("harder", "The handle jerked harder.", "門把猛地轉得更用力。", "af_heart"),
        ("slipped", "Nia's hand slipped from her mouth.", "Nia 的手從嘴前滑落。", "af_heart"),
        ("question", "Could she still keep it out?", "她還能把它擋在外面嗎？", "af_heart"),
        ("refusal_prefix", "Mom, don't", "", "af_sarah"),
        ("invitation_tail", "come in.", "", "af_sarah"),
    ]
    pieces, metadata = {}, {}
    for key, en, zh, voice in texts:
        path = folder/(key+".wav")
        if path.exists():
            pcm = readwav(path)
        else:
            pcm, rate = tts.create(en, voice=voice, speed=1.08, lang="en-us")
            assert rate == RATE and np.isfinite(pcm).all()
            active = np.flatnonzero(np.abs(pcm) > max(.003, np.max(np.abs(pcm))*.017))
            pcm = pcm[max(0,active[0]-120):min(len(pcm),active[-1]+121)]
            wav(path, pcm)
            pcm = readwav(path)
        pieces[key] = pcm
        metadata[key] = dict(en=en, zh=zh, voice=voice, speed=1.08,
                             samples=len(pcm), seconds=len(pcm)/RATE, sha256=hm.digest(path))
        print(key, round(len(pcm)/RATE,3), flush=True)
    # Retain target row boundaries unless natural speech needs a longer row.
    groups = [(["call","mom_voice"],3.5),(["mouth","untouched"],3.5),
              (["rule1","rule2"],5),(["consent","dawn"],4),
              (["cough_intro","copied"],4),(["harder","slipped"],4),
              (["question"],2),([],2),(["refusal_prefix","invitation_tail"],3),([],4),([],4)]
    events, rows, cursor = [], [], 0.
    for index,(keys,target) in enumerate(groups):
        start = cursor
        if index == 0:
            call_end = .2+metadata["call"]["seconds"]
            placements = [("call",.2),("mom_voice",max(.8,call_end+.06))]
        elif index == 4:
            intro_end = start+metadata["cough_intro"]["seconds"]
            mom_at = max(start+1.2,intro_end+.08)
            device_at = mom_at+.8
            placements = [("cough_intro",start),("copied",device_at+.7)]
        elif index == 8:
            placements = [("refusal_prefix",start),
                          ("invitation_tail",start+metadata["refusal_prefix"]["seconds"]+.07)]
        else:
            placements, pos = [], start
            for key in keys:
                placements.append((key,pos))
                pos += metadata[key]["seconds"]+.09
        end = max([start+target]+[at+metadata[key]["seconds"]+.08 for key,at in placements])
        if index == 8:
            full_end = placements[-1][1]+metadata["invitation_tail"]["seconds"]
            playback_at = full_end+.16
            playback_end = playback_at+metadata["invitation_tail"]["seconds"]
            latch_at = math.ceil((playback_end+.06)*30)/30
            end = max(end,latch_at+.6)
        end = math.ceil(end*30)/30
        rows.append(dict(index=index,start=start,end=end,target_duration=target))
        for key,at in placements:
            events.append(dict(key=key,start=at,end=at+metadata[key]["seconds"],**metadata[key]))
        cursor = end
    rng = np.random.default_rng(20261124)
    mix = np.convolve(rng.normal(0,1,round(cursor*RATE)),np.ones(31)/31,mode="same")*.007
    def add(at,pcm,gain=1):
        n=round(at*RATE)
        mix[n:n+len(pcm)] += pcm[:len(mix)-n]*gain
    for event in events:
        add(event["start"],pieces[event["key"]],.82)
    tail = pieces["invitation_tail"]
    add(playback_at,tail,.82)
    replay_at = rows[10]["start"]+1.1
    add(replay_at,tail,.50)
    # Procedural two-part cough: glottal burst plus band-limited breath, not stock audio.
    def noise_burst(length,seed,frequency=170):
        rr=np.random.default_rng(seed); t=np.arange(round(length*RATE))/RATE
        spectrum=np.fft.rfft(rr.normal(0,1,len(t)))
        freqs=np.fft.rfftfreq(len(t),1/RATE)
        spectrum[(freqs<240)|(freqs>3400)]=0
        noise=np.fft.irfft(spectrum,n=len(t))
        return (noise*.12+np.sin(2*np.pi*frequency*t)*.06)*np.minimum(t*100,1)*np.exp(-t*13)
    cough=np.zeros(round(.62*RATE))
    for at,seed in ((0,9),(.29,10)):
        burst=noise_burst(.27,seed)
        cough[round(at*RATE):round(at*RATE)+len(burst)] += burst
    wav(SHARED/"cough.wav",cough)
    add(mom_at,cough); add(device_at,cough)
    sounds=[dict(key="mom_cough",start=mom_at,end=mom_at+.62,en="[Mom coughs.]",zh="［媽媽咳嗽］"),
            dict(key="device_cough",start=device_at,end=device_at+.62,en="[The intercom repeats the cough.]",zh="［對講機重複同樣的咳聲］")]
    add(.35,noise_burst(.25,11,420),.6)
    add(rows[5]["start"]+.15,noise_burst(.5,12,370),.7)
    add(latch_at,noise_burst(.10,13,1370),.7)
    for at,seed in ((rows[9]["start"]+.1,14),(rows[9]["start"]+.7,15),
                    (rows[9]["start"]+1.0,16),(rows[10]["start"]+.15,17),(rows[10]["start"]+2.4,18)):
        add(at,noise_burst(.7,seed,90),.8)
    sounds += [dict(key="door_scrape",start=rows[9]["start"]+.1,end=rows[9]["start"]+.7,en="[Door scrapes. Nia gasps.]",zh="［門邊摩擦，Nia 喘息］"),
               dict(key="shoe_scrape",start=rows[10]["start"]+.15,end=rows[10]["start"]+.85,en="[Shoe scrapes. Door creaks.]",zh="［鞋底摩擦，門受壓作響］")]
    # Preserve the actual prefix and tail samples as one complete recorded utterance.
    refusal=np.concatenate([pieces["refusal_prefix"],np.zeros(round(.07*RATE)),tail])
    wav(SHARED/"nia-full-reply.wav",refusal)
    wav(SHARED/"nia-saved-two-words.wav",tail)
    wav(SHARED/"mix.wav",mix)
    cues=[e.copy() for e in events if e["key"] not in {"refusal_prefix","invitation_tail"}]
    cues += [dict(key="refusal",start=rows[8]["start"],end=full_end,en="Mom, don't come in.",zh="媽，別進來。（Mom, don't come in.）"),
             dict(key="playback",start=playback_at,end=playback_end,en="[Intercom, Nia's voice] Come in.",zh="［對講機，Nia 的聲音］進來。（Come in.）"),
             dict(key="final_playback",start=replay_at,end=replay_at+len(tail)/RATE,en="[Intercom] Come in.",zh="［對講機］進來。（Come in.）")]+sounds
    cues.sort(key=lambda e:e["start"])
    for lang,field in (("en","en"),("zh-Hant","zh")):
        blocks=[]
        for i,c in enumerate(cues,1):
            content="\n".join(textwrap.wrap(c[field],42 if lang=="en" else 30,break_long_words=False))
            blocks.append(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{content}\n")
        (SHARED/f"h01-v2.1.{lang}.srt").write_text("\n".join(blocks),encoding="utf-8")
    save(SHARED/"timeline.json",dict(base_git_sha=BASE_SHA,source_branch_sha=SOURCE_SHA,
         script_sha256=hm.digest(SHARED/"urban_horror-v2.1.md"),frames=round(cursor*30),seconds=cursor,
         rate=RATE,rows=rows,events=events,cues=cues,mom_cough=mom_at,device_cough=device_at,
         playback_at=playback_at,playback_end=playback_end,latch_at=latch_at,
         replay_at=replay_at,model_hashes=MODEL_HASHES,peak_dbfs=20*np.log10(np.max(np.abs(mix))),
         reply_assembly="Two naturally synthesized clauses in the same voice joined by 70 ms; final two-word PCM is reused without regeneration or time stretching.",
         human_listened=False,market_acceptance="NOT_TESTED"))
    print("AUDIO",cursor,"seconds",flush=True)


def stage():
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    dest=SHARED/"plates"
    dest.mkdir(exist_ok=True)
    names=[["mother-nearby","covered","lips","uncovered"],
           ["mother-close","door-check","brace","foot"]]
    provenance={}
    for sheet_name,shot_names in zip(("actors-selected.png","action-selected.png"),names):
        path=SHARED/sheet_name
        with Image.open(path) as source:
            for i,name in enumerate(shot_names):
                # Extract cells individually; trim the seam and cover each 9:16 canvas.
                w,h=source.size; x=i%2; y=i//2
                box=(round(x*w/2)+2,round(y*h/2)+2,round((x+1)*w/2)-2,round((y+1)*h/2)-2)
                image=ImageOps.fit(source.crop(box).convert("RGB"),(1080,1920),Image.Resampling.LANCZOS)
                image.save(dest/(name+".png"))
                provenance[name]=dict(sheet=sheet_name,source_sha256=hm.digest(path),crop=box)
    demo=REPO/"artifacts/genre-pilot-20261124/motion"
    for name in ("handle-plate","handle-element","intercom-plate","screen-element",
                 "indicator-element","latch-plate","latch-element","latch-occluder"):
        shutil.copyfile(demo/"layers"/(name+".png"),dest/(name+".png"))
    for name,lines in {
        "neutral":[],
        "rules":["NIGHT MODE","FIRST REPLY: WAITING","RETENTION: LAST 2 WORDS"],
        "consent":["LATCH: SAVED CONSENT","REPLACE: AT DAWN"],
        "cough":["[cough] [cough]"],
        "input":["INPUT:","Mom, don't come in."],
        "input-wait":["INPUT:"],
        "input-prefix":["INPUT:","Mom, don't"],
        "input-full":["INPUT:","Mom, don't come in."],
        "saved":["SAVED: Come in."],
    }.items():
        im=Image.new("RGBA",(550,390),(7,28,30,255)); d=ImageDraw.Draw(im)
        font=ImageFont.truetype("C:/Windows/Fonts/consola.ttf",35)
        for n,line in enumerate(lines):
            d.text((275,195+(n-(len(lines)-1)/2)*76),line,font=font,anchor="mm",fill=(192,244,226,255))
        alpha=Image.new("L",im.size,0)
        ImageDraw.Draw(alpha).rounded_rectangle((0,0,549,389),radius=7,fill=255)
        im.putalpha(alpha)
        im.save(dest/("screen-"+name+".png"))
    # The opening question is the only editorial lettering in the picture.
    im=Image.new("RGBA",(1080,1920)); d=ImageDraw.Draw(im)
    for text,y,size in (("Can She Keep It Out?",145,62),("她擋得住嗎？",227,58)):
        font=ImageFont.truetype("C:/Windows/Fonts/msjhbd.ttc",size)
        d.text((540,y),text,font=font,anchor="mm",fill="white",stroke_width=4,stroke_fill=(0,0,0,220))
    im.save(dest/"question.png")
    # A uses these identical physical screen observations as still/cut states.
    for name in ("neutral","rules","consent","cough","input","input-wait","input-prefix","input-full","saved"):
        im=Image.open(dest/"intercom-plate.png").convert("RGBA")
        im.alpha_composite(Image.open(dest/("screen-"+name+".png")),(260,443))
        led=Image.open(dest/"indicator-element.png").resize((45,46),Image.Resampling.LANCZOS)
        im.alpha_composite(led,(514,882))
        im.convert("RGB").save(dest/("device-"+name+".png"))
    im=Image.open(dest/"uncovered.png").convert("RGBA")
    # Small in-world live-input readout in the reaction framing; cut closer at 28.3 s.
    # Project onto the physical glass quadrilateral; no floating rectangle.
    import numpy as np
    display=Image.open(dest/"screen-input-wait.png")
    points=[(904,536),(1030,501),(1030,696),(904,718)]
    matrix=[];values=[]
    for (x,y),(u,v) in zip(points,[(0,0),(550,0),(550,390),(0,390)]):
        matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
        values.extend([u,v])
    coeff=np.linalg.solve(np.array(matrix,float),np.array(values,float))
    projected=display.transform(im.size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)
    im.alpha_composite(projected)
    im.convert("RGB").save(dest/"nia-input.png")
    save(SHARED/"assets.json",dict(extracted=provenance,
         source_assets={p.name:hm.digest(p) for p in dest.glob("*.png")},
         processing="Individual cover crops, alpha prop registration, code-native in-world device display and opening question. No generated diagram or caption overlay."))
    print("STAGED",flush=True)


def camera(frames):
    return f"zoompan=z='1.015+0.020*on/{max(1,frames-1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,setsar=1"


def encode_still(path,out,frames,tools,question=False,after=None,cut=0):
    args=hm.ffargs()+["-loop","1","-framerate","30","-i",path]
    if question:
        args += ["-loop","1","-framerate","30","-i",SHARED/"plates/question.png"]
    zoom=camera(frames)
    if question:
        args += ["-filter_complex",f"[0:v]{zoom}[z];[z][1:v]overlay=enable='gte(t,0.3)*lt(t,2.8)'[v]","-map","[v]"]
    elif after:
        args += ["-loop","1","-framerate","30","-i",after,"-filter_complex",
                 f"[0:v][1:v]overlay=enable='gte(n,{cut})'[s];[s]{zoom}[v]","-map","[v]"]
    else:
        args += ["-vf",zoom]
    tools.run("ffmpeg",args+["-an","-frames:v",frames,*hm.encode_args(),out],out.parent)


def motion_spec(name,frames,plate,layers):
    p=SHARED/"plates"
    def prop(id,image,size,pivot,anchor,motions,**kw):
        return dict(id=id,image=str(p/(image+".png")),size=size,pivot=pivot,anchor=anchor,motions=motions,**kw)
    def move(kind,start,end,**kw):
        return dict(type=kind,start_s=start,end_s=end,easing="smoothstep",**kw)
    result=[]
    if name in {"opening-handle","harder-handle"}:
        end=.65 if name=="opening-handle" else .65
        motions=[move("rotate",.35 if name=="opening-handle" else .08,end,**{"from":0,"to":18 if name=="opening-handle" else 28})]
        if name=="harder-handle":
            motions.append(dict(type="shake",start_s=.1,end_s=1.25,easing="linear",amplitude=[3,5],cycles=4))
        result=[prop("lever","handle-element",[440,119],[57,60],[368,921],motions)]
    elif name=="latch-retract":
        # The local shot starts at the already measured click/retraction boundary.
        result=[prop("bolt","latch-element",[440,56],[0,28],[480,978],
                     [move("translate",0,min(.36,(frames-1)/30),path=[[0,0],[-405,0]])]),
                prop("occluder","latch-occluder",[1080,1920],[540,960],[540,960],[])]
    elif name=="latch-hold":
        result=[prop("bolt","latch-element",[440,56],[0,28],[480,978],[]),
                prop("occluder","latch-occluder",[1080,1920],[540,960],[540,960],[])]
    elif name.startswith("device-"):
        mode=name.removeprefix("device-")
        result=[prop("physical-readout","screen-"+mode,[550,390],[275,195],[535,638],[])]
        if mode=="cough":
            # Two independent copies of one light bitmap: each has its own brief pulse.
            for i,at in enumerate((.1,.39)):
                result.append(prop("pulse-"+str(i),"indicator-element",[45,46],[22.5,23],[536,905],
                    [dict(type="shake",start_s=at,end_s=at+.18,easing="linear",amplitude=[0,0],cycles=1),
                     move("fade",at,at+.04,**{"from":0,"to":1})],opacity=.7))
            # Pulse off is handled by the frame compositor below rather than a second fade primitive.
        else:
            result.append(prop("listening","indicator-element",[45,46],[22.5,23],[536,905],
                               [move("glow",0,min(.3,(frames-1)/30),**{"from":.65,"to":1})],glow_radius=3))
    return dict(version=1,id=name,frames=frames,background=str(SHARED/"plates"/(plate+".png")),layers=result)


def encode_mesh(path,out,frames,kind,tools,offset):
    """Bounded photographic mesh displacement; no generated intermediate identities."""
    from PIL import Image
    folder=out.parent/(out.stem+"-frames")
    folder.mkdir(exist_ok=True)
    source=Image.open(path).convert("RGB")
    for n in range(frames):
        t=n/30; global_t=t+offset
        if kind=="cough":
            # Two visible local shoulder hitches, timed to the two audible bursts.
            amplitude=sum(23*math.sin(math.pi*(global_t-at)/.20) if at<=global_t<=at+.20 else 0 for at in (17.2,17.49))
            center=(520,1420); sx,sy=470,430; dx,dy=0,amplitude
        elif kind=="flinch":
            amplitude=math.sin(math.pi*min(1,t/.40))*15 if t<.4 else 0
            center=(560,800);sx,sy=490,700;dx,dy=amplitude,amplitude*.4
        else:
            amplitude=(math.sin(t*math.pi*.9)*.5+.5)*24
            if kind=="brace":
                amplitude=30*min(1,t/.45)-20*min(1,max(0,t-.7)/.5)+4*math.sin(t*8)
            center=(860,1000);sx,sy=400,1100;dx,dy=amplitude,0
        def sample(x,y):
            weight=math.exp(-((x-center[0])/sx)**2-((y-center[1])/sy)**2)
            return x-dx*weight,y-dy*weight
        mesh=[]
        for y in range(0,1920,120):
            for x in range(0,1080,120):
                box=(x,y,min(x+120,1080),min(y+120,1920)); l,top,r,b=box
                quad=(*sample(l,top),*sample(l,b),*sample(r,b),*sample(r,top))
                mesh.append((box,quad))
        frame=source.transform(source.size,Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)
        # The same slow cover zoom as its A counterpart removes transformed outer edges.
        z=1.015+.020*n/max(1,frames-1)
        w,h=1080/z,1920/z
        frame=frame.crop((round((1080-w)/2),round((1920-h)/2),round((1080+w)/2),round((1920+h)/2))).resize((1080,1920),Image.Resampling.LANCZOS)
        frame.save(folder/f"{n:04}.jpg",quality=96,subsampling=0)
    tools.run("ffmpeg",hm.ffargs()+["-framerate","30","-i",folder/"%04d.jpg","-vf","scale=in_range=pc:out_range=tv,format=yuv420p,setsar=1", "-color_range","tv","-an","-frames:v",frames,*hm.encode_args(),out],out.parent)


def render():
    from PIL import Image
    timeline=hm.read(SHARED/"timeline.json")
    playback=math.ceil(timeline["playback_at"]*30)/30
    latch=timeline["latch_at"]
    prefix_end=math.ceil(next(e["end"] for e in timeline["events"] if e["key"]=="refusal_prefix")*30)/30
    full_end=math.ceil(next(e["end"] for e in timeline["events"] if e["key"]=="invitation_tail")*30)/30
    # Identical cuts and durations in both versions. Only listed key shots differ.
    definitions=[
        (0,.7,"opening-handle","handle-plate","prop"),
        (.7,3.5,"mother-nearby","mother-nearby",None),
        (3.5,7,"covered","covered",None),
        (7,8,"lips","lips",None),
        (8,11,"device-rules","intercom-plate","prop"),
        (11,12,"eyes","lips",None),
        (12,14,"device-consent","intercom-plate","prop"),
        (14,15,"door-check","door-check",None),
        (15,16,"latch-hold","latch-plate",None),
        (16,17.9,"mother-cough","mother-close","cough"),
        (17.9,18,"device-neutral","intercom-plate",None),
        (18,20,"device-cough","intercom-plate","pulse"),
        (20,21.6,"harder-handle","handle-plate","prop"),
        (21.6,22,"flinch","covered","flinch"),
        (22,24,"hand-slipped","uncovered",None),
        (24,26,"question-reaction","uncovered",None),
        (26,28,"listening-hold","uncovered",None),
        (28,28.3,"nia-reply","nia-input",None),
        (28.3,prefix_end,"device-input-wait","intercom-plate","prop"),
        (prefix_end,full_end,"device-input-prefix","intercom-plate","prop"),
        (full_end,playback,"device-input-full","intercom-plate","prop"),
        (playback,latch,"device-saved","intercom-plate","prop"),
        (latch,31,"latch-retract","latch-plate","prop"),
        (31,35,"brace","brace","brace"),
        (35,37,"foot","foot","pressure"),
        (37,39,"final-brace","brace","pressure"),
    ]
    shots=[]
    tools=hm.Tools(HERE/"motion/tools.lock.json")
    for version in ("A","B"):
        (ROOT/version/"cuts").mkdir(parents=True,exist_ok=True)
    for i,(start,end,name,plate,kind) in enumerate(definitions):
        frames=round(end*30)-round(start*30)
        a=ROOT/"A/cuts"/f"{i:02}-{name}.mp4"
        b=ROOT/"B/cuts"/a.name
        p=SHARED/"plates"
        after=None;cut=0
        print("SHOT",i,name,frames,flush=True)
        if name in {"opening-handle","harder-handle","latch-hold","latch-retract"}:
            # A: ordered static photographic states from the exact same layered prop.
            spec=motion_spec(name,frames,plate,[])
            state=hm.parse_spec(spec,SHARED)
            # Native static compositor uses precisely the same prop geometry.
            image=Image.open(p/(plate+".png")).convert("RGBA")
            if "handle" in name:
                lever=Image.open(p/"handle-element.png").resize((440,119),Image.Resampling.LANCZOS)
                image.alpha_composite(lever,(368-57,921-60))
                padded=Image.new("RGBA",(1001,1001));padded.alpha_composite(lever,(500-57,500-60))
                rotated=padded.rotate(-28 if name=="harder-handle" else -18,Image.Resampling.BICUBIC)
                state_after=Image.open(p/(plate+".png")).convert("RGBA")
                state_after.alpha_composite(rotated,(368-500,921-500))
                after=p/(name+"-after.png");state_after.convert("RGB").save(after)
                cut=5 if name=="harder-handle" else 11
            else:
                bolt=Image.open(p/"latch-element.png").resize((440,56),Image.Resampling.LANCZOS)
                image.alpha_composite(bolt,(480-(405 if name=="latch-retract" else 0),950))
                image.alpha_composite(Image.open(p/"latch-occluder.png").convert("RGBA"))
            still=p/(name+"-static.png");image.convert("RGB").save(still)
        elif name.startswith("device-"):
            still=p/(name+".png")
        else:
            still=p/(plate+".png")
        if not a.exists():
            encode_still(still,a,frames,tools,question=name=="mother-nearby",after=after,cut=cut)
        if not b.exists():
            if kind=="prop":
                spec=motion_spec(name,frames,plate,[])
                spec_path=SHARED/(name+".json");save(spec_path,spec)
                raw=SHARED/(name+"-motion-raw.mp4")
                if not raw.exists():
                    hm.render(spec_path,raw,tools)
                tools.run("ffmpeg",hm.ffargs()+["-i",raw,"-vf",camera(frames),"-an","-frames:v",frames,*hm.encode_args(),b],b.parent)
            elif kind in {"cough","flinch","brace","pressure"}:
                encode_mesh(still,b,frames,kind,tools,start)
            elif kind=="pulse":
                encode_pulse(still,b,frames,tools,start)
            else:
                shutil.copyfile(a,b)
        shots.append(dict(index=i,name=name,start=start,end=end,frames=frames,key=bool(kind),
                          A=str(a.relative_to(ROOT)),B=str(b.relative_to(ROOT)),motion=kind,
                          a_sha256=hm.digest(a),b_sha256=hm.digest(b)))
        save(SHARED/"shots.json",shots)
    # Encode one AAC file; copy that same bitstream into both masters.
    aac=SHARED/"mix.m4a"
    if not aac.exists():
        tools.run("ffmpeg",hm.ffargs()+["-i",SHARED/"mix.wav","-c:a","aac","-b:a","192k","-ar","48000","-ac","2",aac],SHARED)
    for version in ("A","B"):
        out=ROOT/version
        manifest=out/"concat.txt"
        manifest.write_text("".join(f"file '{(ROOT/s[version]).as_posix()}'\n" for s in shots),encoding="utf-8")
        master=out/"h01-v2.1.mp4"
        if not master.exists():
            tools.run("ffmpeg",hm.ffargs()+["-f","concat","-safe","0","-i",manifest,"-i",aac,
                      "-map","0:v:0","-map","1:a:0","-c","copy","-bsf:v",
                      "h264_metadata=video_full_range_flag=0:colour_primaries=2:transfer_characteristics=2:matrix_coefficients=2:chroma_sample_loc_type=0",
                      "-map_metadata","-1","-movflags","+faststart",master],out)
        for lang in ("en","zh-Hant"):
            shutil.copyfile(SHARED/f"h01-v2.1.{lang}.srt",out/f"h01-v2.1.{lang}.srt")
    print("RENDER COMPLETE",flush=True)


def encode_pulse(path,out,frames,tools,start):
    from PIL import Image, ImageDraw
    folder=out.parent/(out.stem+"-frames");folder.mkdir(exist_ok=True)
    for n in range(frames):
        t=start+n/30
        im=Image.open(path).convert("RGB");d=ImageDraw.Draw(im)
        pulse=any(at<=t<at+.18 for at in (18.,18.29))
        d.ellipse((518,886,554,924),fill=(90,255,203) if pulse else (7,45,35))
        im.save(folder/f"{n:04}.jpg",quality=96,subsampling=0)
    tools.run("ffmpeg",hm.ffargs()+["-framerate","30","-i",folder/"%04d.jpg","-vf","scale=in_range=pc:out_range=tv,format=yuv420p,"+camera(frames),"-color_range","tv","-an","-frames:v",frames,*hm.encode_args(),out],out.parent)


def qa():
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import re
    tools=hm.Tools(HERE/"motion/tools.lock.json")
    timeline=hm.read(SHARED/"timeline.json");shots=hm.read(SHARED/"shots.json")
    assert sum(s["frames"] for s in shots)==1170
    assert len(shots)==26
    reports={};hashes={};audio_hashes={}
    for version in ("A","B"):
        folder=ROOT/version; q=folder/"qa";q.mkdir(exist_ok=True)
        clip=folder/"h01-v2.1.mp4"
        probe=hm.inspect(tools,clip,q,1170)
        audio=next(s for s in probe["streams"] if s["codec_type"]=="audio")
        assert (audio["codec_name"],audio["sample_rate"],audio["channels"])==("aac","48000",2)
        assert abs(float(probe["format"]["duration"])-39)<1/30
        save(q/"ffprobe.json",probe)
        frame_info=json.loads(tools.run("ffprobe",["-v","error","-select_streams","v:0","-show_frames",
            "-show_entries","frame=best_effort_timestamp_time,pix_fmt,color_range,color_space,chroma_location,sample_aspect_ratio",
            "-of","json",clip],q))["frames"]
        assert len(frame_info)==1170
        assert all(f["pix_fmt"]=="yuv420p" and f.get("color_range")=="tv" for f in frame_info)
        assert all(f.get("chroma_location")=="left" for f in frame_info)
        assert all(abs(float(f["best_effort_timestamp_time"])-n/30)<.00001 for n,f in enumerate(frame_info))
        save(q/"frame-timestamps.json",frame_info)
        audio_hashes[version]=tools.run("ffmpeg",["-nostdin","-v","error","-i",clip,"-map","0:a:0","-c:a","copy","-f","hash","-hash","sha256","-"],q).strip()
        tools.run("ffmpeg",hm.ffargs()+["-i",clip,"-an","-f","framemd5",q/"video.framemd5"],q)
        hashes[version]=[line.split(",")[-1].strip() for line in (q/"video.framemd5").read_text().splitlines() if not line.startswith("#")]
        assert len(hashes[version])==1170
        subtitle=[]
        for lang,field in (("en","en"),("zh-Hant","zh")):
            path=folder/f"h01-v2.1.{lang}.srt"
            assert hm.digest(path)==hm.digest(SHARED/path.name)
            blocks=path.read_text(encoding="utf-8").strip().split("\n\n")
            assert len(blocks)==len(timeline["cues"])
            previous=0
            for block,cue in zip(blocks,timeline["cues"]):
                lines=block.splitlines()
                assert lines[1]==f"{stamp(cue['start'])} --> {stamp(cue['end'])}"
                assert " ".join(" ".join(lines[2:]).split())==" ".join(cue[field].split())
                assert 0<=cue["start"]<cue["end"]<=39 and cue["start"]>=previous-.001
                assert len(lines[2:])<=2
                previous=cue["end"]
                if re.search(r"come in",cue[field],re.I):
                    assert cue["start"]>=28
            subtitle.append(dict(language=lang,cues=len(blocks),sha256=hm.digest(path),
                pcm_boundaries=True,overlap=False,beyond_duration=False,max_lines=2,
                translation_semantics="Agent inspection only; no human localization check"))
        # All boundary samples come from the encoded delivery master.
        samples=set([0,10,11,15,20,29,30,104,105,239,240,329,330,359,360,419,420,
                     479,480,515,516,519,524,525,536,537,539,540,543,549,554,599,600,605,620,
                     647,648,654,659,660,719,720,779,780,839,840,848,849,862,863,880,881,884,
                     885,886,900,904,905,910,929,930,944,960,989,1020,1049,1050,1080,1109,1110,1140,1169])
        for s in shots:
            samples.update([round(s["start"]*30),round(s["start"]*30)+s["frames"]//2,round(s["end"]*30)-1])
        samples=sorted(f for f in samples if 0<=f<1170)
        frames=q/"frames";frames.mkdir(exist_ok=True)
        expr="+".join(f"eq(n\\,{f})" for f in samples)
        tools.run("ffmpeg",hm.ffargs()+["-i",clip,"-vf","select='"+expr+"'","-fps_mode","vfr",frames/"%03d.png"],q)
        decoded={f:frames/f"{i+1:03d}.png" for i,f in enumerate(samples)}
        assert all(p.exists() for p in decoded.values())
        save(q/"decoded-samples.json",{str(f):p.name for f,p in decoded.items()})
        font=ImageFont.truetype("C:/Windows/Fonts/consola.ttf",18)
        def contact(name,groups,columns=4):
            result=Image.new("RGB",(270*columns,505*math.ceil(len(groups)/columns)),(18,18,18))
            d=ImageDraw.Draw(result)
            for i,(frame,label) in enumerate(groups):
                thumb=Image.open(decoded[frame]).resize((270,480),Image.Resampling.LANCZOS)
                x=i%columns*270;y=i//columns*505
                result.paste(thumb,(x,y));d.text((x+5,y+482),f"{frame/30:.3f}s {label}",font=font,fill="white")
            result.save(q/name,quality=94)
        contact("contact-sheet.jpg",[(round(s["start"]*30)+s["frames"]//2,s["name"]) for s in shots])
        contact("hardware-actions.jpg",[(f,label) for f,label in [(0,"handle start"),(11,"handle action"),(15,"handle mid"),(20,"handle end"),
                (240,"rule visible"),(540,"cough readout"),(543,"pulse 1"),(549,"pulse 2"),
                (840,"live input"),(863,"prefix visible"),(881,"full reply"),(900,"saved playback"),
                (905,"latch start"),(910,"latch moving"),(929,"latch end"),(930,"door pressure")]])
        contact("actor-actions.jpg",[(f,label) for f,label in [(480,"mother start"),(516,"cough 1"),(519,"hitch 1"),(525,"hitch 2"),
                (648,"flinch start"),(654,"flinch"),(660,"hand below"),(779,"question end"),
                (930,"door start"),(944,"push"),(960,"brace"),(1049,"brace end"),
                (1050,"foot planted"),(1080,"pressure"),(1110,"final brace"),(1169,"end")]])
        # Actual encoded pixels: fit the lever's bright low-chroma ridge at each opening sample.
        angles=[]
        for f in (0,10,11,15,20):
            im=np.array(Image.open(decoded[f]).convert("RGB"),dtype=float)
            roi=im[885:1120,435:790]
            mask=(roi.max(2)-roi.min(2)<45)&(roi.mean(2)>110)
            yy,xx=np.where(mask)
            slope=np.polyfit(xx,yy,1)[0]
            angles.append(dict(frame=f,time_s=f/30,angle_deg=float(np.degrees(np.arctan(slope))),pixels=len(xx)))
        # Verify opening question is present only within the requested interval at its two boundaries.
        question_counts={}
        for f in (29,30,104,105):
            im=np.array(Image.open(decoded[f]).convert("RGB"))[:300]
            count=int(((im.min(2)>215)&((im.max(2)-im.min(2))<28)).sum())
            question_counts[str(f)]=count
        assert question_counts["30"]>question_counts["29"]+1000
        assert question_counts["104"]>question_counts["105"]+1000
        # Actual final PCM and subtitle evidence stay bound to the input; no ASR/listening claim.
        tools.run("ffmpeg",["-nostdin","-v","info","-i",clip,"-af","ebur128=peak=true","-f","null","-"],q)
        meter=json.loads((q/"commands.jsonl").read_text(encoding="utf-8").splitlines()[-1])["stderr"].rsplit("Summary:",1)[-1].strip()
        (q/"audio-loudness.txt").write_text(meter+"\n",encoding="utf-8")
        edge_check={}
        for f,path in decoded.items():
            arr=np.asarray(Image.open(path).convert("RGB"),dtype=float)
            edges=[arr[0].mean(),arr[-1].mean(),arr[:,0].mean(),arr[:,-1].mean()]
            edge_check[str(f)]=[round(float(v),2) for v in edges]
        report=dict(version=version,base_git_sha=BASE_SHA,script_sha256=timeline["script_sha256"],
            master_sha256=hm.digest(clip),frames=1170,duration_s=float(probe["format"]["duration"]),
            full_decode="PASS",format="1080x1920 30fps H.264 yuv420p SAR1:1 AAC48k stereo",
            all_frame_timestamps="PASS: every PTS equals n/30",all_frame_pixel_format="yuv420p limited range, no midstream switches",
            all_frame_chroma_location="left",audio_loudness_summary=meter,
            embedded_subtitles=False,subtitles=subtitle,audio_packet_sha256=audio_hashes[version],
            question_boundary_white_pixel_counts=question_counts,decoded_opening_lever_angles=angles,
            edge_luminance_samples=edge_check,black_border_detection="Sampled edge statistics and agent image inspection; dark in-world hallway edges are intentional",
            timestamps=dict(anomaly_voice=.2,handle_target=.35,first_handle_state_frame=11,question_in=1.,question_out=3.5,
                mother_asleep=.7,retention_status=8.,consent_status=12.,mom_cough=timeline["mom_cough"],
                repeated_cough=timeline["device_cough"],pressure_handle=20.,think_hold=[26,28],reply=28.,
                input_prefix=math.ceil(next(e["end"] for e in timeline["events"] if e["key"]=="refusal_prefix")*30)/30,
                input_full=math.ceil(next(e["end"] for e in timeline["events"] if e["key"]=="invitation_tail")*30)/30,
                saved_readout=math.ceil(timeline["playback_at"]*30)/30,recorded_playback=timeline["playback_at"],
                playback_end=timeline["playback_end"],latch_shot=timeline["latch_at"],door_gap=31.,final_pressure=35.),
            timestamp_method="Actual PCM sample offsets, master-frame extracts at cut/text boundaries, lever pixel-angle samples; not inferred audience recognition or OCR",
            market_acceptance="NOT_TESTED",human_status="HUMAN_TEST_PENDING",human_listened=False,
            phone_readability="NOT_VERIFIED",continuous_human_playback="NOT_VERIFIED")
        save(q/"media-qa.json",report);reports[version]=report
        (folder/"sha256.txt").write_text("".join(f"{hm.digest(p)}  {p.name}\n" for p in [clip,*folder.glob("*.srt")]),encoding="utf-8")
    assert audio_hashes["A"]==audio_hashes["B"]
    comparisons=[]
    for s in shots:
        lo=round(s["start"]*30);hi=round(s["end"]*30)
        equal=sum(a==b for a,b in zip(hashes["A"][lo:hi],hashes["B"][lo:hi]))
        if not s["key"]:
            assert s["a_sha256"]==s["b_sha256"] and equal==s["frames"]
        comparisons.append(dict(name=s["name"],key=s["key"],frames=s["frames"],identical_decoded_frames=equal))
    # Check PCM identity of two-word repeats and coughs, independently of SRT strings.
    mix=readwav(SHARED/"mix.wav");tail=readwav(SHARED/"nia-saved-two-words.wav")
    exact_source=readwav(SHARED/"nia-full-reply.wav")[-len(tail):]
    assert np.array_equal(tail,exact_source)
    pcm_checks=[]
    for key,at,source,gain in [
        ("nia_two_words",next(e["start"] for e in timeline["events"] if e["key"]=="invitation_tail"),tail,.82),
        ("saved_playback",timeline["playback_at"],tail,.82),
        ("final_playback",timeline["replay_at"],tail,.50),
        ("mother_cough",timeline["mom_cough"],readwav(SHARED/"cough.wav"),1),
        ("device_cough",timeline["device_cough"],readwav(SHARED/"cough.wav"),1)]:
        n=round(at*RATE);target=mix[n:n+len(source)]
        correlation=float(np.corrcoef(target,source)[0,1]);assert correlation>.98
        pcm_checks.append(dict(key=key,at_sample=n,at_s=n/RATE,source_correlation=correlation,gain=gain))
    save(SHARED/"ab-comparison.json",dict(non_key_frames_identical=True,audio_packets_identical=True,
        shared_audio_sha256=hm.digest(SHARED/"mix.wav"),two_words_are_exact_source_suffix=True,
        pcm_checks=pcm_checks,shots=comparisons,not_claimed=["human results","market results","rights clearance","lip sync","physical realism","phone readability"]))
    print("QA PASS: full decode, master format, 26 shared-timing shots, identical non-key decoded frames/audio, subtitle and source-PCM checks",flush=True)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=["audio","stage","render","qa"])
    args=parser.parse_args()
    tools=hm.Tools(HERE/"motion/tools.lock.json")
    SHARED.mkdir(parents=True,exist_ok=True)
    if args.mode=="audio":
        make_audio()
    elif args.mode=="stage":
        stage()
    elif args.mode=="render":
        render()
    elif args.mode=="qa":
        qa()
