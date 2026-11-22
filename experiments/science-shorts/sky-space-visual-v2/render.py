"""Reviewed science visuals, version 2: sky and space. Local output only.

Uses frozen ice-v2 typography/compositing helpers, not its frozen render gate.
Each topic has a fresh scientific visual review and immutable input manifest.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import time
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'artifacts/science-shorts/sky-space-visual-v2'
BATCH=HERE.parent/'batch-20261121'
STYLE_PATH=HERE.parent/'ice-visual-v2/render.py'
W,H,FPS=1080,1920,30
ENV={k:v for k,v in os.environ.items() if k.upper() in {'SYSTEMROOT','WINDIR','TEMP','TMP'}}
INK,TEAL,BLUE,RED,GOLD='#163f49','#087d88','#147bd1','#ce503d','#ffca86'
S=None


def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path,obj): Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def verify(path,binding):
    path=Path(path)
    if not path.is_absolute() or path.resolve(strict=True)!=path: raise ValueError('Noncanonical input')
    if path.stat().st_size!=binding['size'] or sha(path)!=binding['sha256']: raise ValueError(f'Frozen input changed: {path.name}')


def inputs(episode,require_review=False):
    manifest_path=HERE/f'{episode}-inputs.json'
    manifest=load(manifest_path)
    for relative,binding in manifest['files'].items(): verify((ROOT/relative).resolve(strict=True),binding)
    binaries=load(ROOT/'experiments/episode-02-73h/render-manifest.json')
    tools=ROOT/'artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin'
    for name in ('ffmpeg','ffprobe'): verify((tools/(name+'.exe')).resolve(strict=True),binaries[name])
    original=ROOT/f'artifacts/science-shorts/batch-20261121/{episode}'
    timed=load(original/'timeline.json')
    if timed['audio_sha256']!=sha(original/'narration.wav'): raise ValueError('Narration changed')
    source=next(e for e in load(BATCH/'scripts-final.json')['episodes'] if e['id']==episode)
    if len(source['cues'])!=len(timed['cues']): raise ValueError('Cue count differs')
    for a,b in zip(source['cues'],timed['cues']):
        if any(a[k]!=b[k] for k in ('en','zh','claim_ids')): raise ValueError('Public script changed')
    original_gate=load(BATCH/'editorial-gate.json')
    if original_gate['status']!='PASS' or original_gate['script_sha256']!=sha(BATCH/'scripts-final.json'): raise ValueError('Original editorial gate not passed')
    if require_review:
        review=load(HERE/f'{episode}-visual-review.json')
        if review.get('status')!='PASS' or review.get('critical_defects'): raise ValueError('New visual review not passed')
        if review.get('renderer_sha256')!=sha(Path(__file__)) or review.get('inputs_sha256')!=sha(manifest_path): raise ValueError('Visual review stale')
    # Verify the shared helper before loading executable Python from it.
    global S
    if S is None:
        spec=importlib.util.spec_from_file_location('frozen_ice_visual_style',STYLE_PATH)
        S=importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
    return timed['cues'],tools,binaries,original


def txt(d,pos,value,size=42,color=INK,zh=False,bold=False,anchor=None):
    S.txt(d,pos,value,size,color,zh,bold,anchor)


def arrow(d,a,b,color=BLUE,width=6,head=15):
    d.line((*a,*b),fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    d.polygon([b,(b[0]-head*math.cos(angle-.48),b[1]-head*math.sin(angle-.48)),(b[0]-head*math.cos(angle+.48),b[1]-head*math.sin(angle+.48))],fill=color)


def pulse(d,a,b,t,color=BLUE,r=9):
    p=t%1
    x,y=a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p
    d.ellipse((x-r,y-r,x+r,y+r),fill=color)


def note(im,ch='科學機制示意；圖像、距離與數量不依比例',dark=False):
    d=ImageDraw.Draw(im)
    col='#b8d9d8' if dark else '#55747a'
    txt(d,(540,1400),ch,26,col,True,anchor='mm')
    txt(d,(540,1440),'SCHEMATIC · NOT TO SCALE',22,col,anchor='mm')


def head(im,i,ch,en,dark=False): S.heading(im,i+1,ch,en,dark)


@lru_cache(maxsize=3)
def raster(name):
    im=Image.open(OUT/'assets'/name).convert('RGB')
    scale=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    x,y=im.width-W,(im.height-H)//2
    return im.crop((x,y,x+W,y+H))


def camera(im,z=1,dx=0,dy=0):
    nw,nh=round(W*z),round(H*z)
    if z<=1: return im.copy()
    x=max(0,min(nw-W,(nw-W)//2+round(dx)))
    y=max(0,min(nh-H,(nh-H)//2+round(dy)))
    return im.resize((nw,nh),Image.Resampling.BICUBIC).crop((x,y,x+W,y+H))


def sun(d,xy,r=48):
    x,y=xy
    d.ellipse((x-r-8,y-r-8,x+r+8,y+r+8),fill='#f5b765')
    d.ellipse((x-r,y-r,x+r,y+r),fill='#ffe3a3')


def eye(d,xy,color=INK):
    x,y=xy
    d.ellipse((x-37,y-20,x+37,y+20),fill='#fff8e8',outline=color,width=4)
    d.ellipse((x-12,y-12,x+12,y+12),fill=color)


def sky_hero(n,index,cue):
    t=n/FPS
    if index==9:
        p=S.ease((n-cue['start'])/45)
        im=Image.blend(raster('sky-day.png'),raster('sky-sunset.png'),p)
        im=camera(im,1.02+0.01*math.sin(t*.4))
        # Warm-sky legibility uses an ivory title plate rather than white text.
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((55,90,1025,410),radius=25,fill='#fff2dc')
        head(im,index,'同一種散射，不同的路徑。','BLUE SKY. RED SUNSET.')
        d.rounded_rectangle((80,990,1000,1170),radius=30,fill='#fff2dc')
        txt(d,(540,1050),'穿過大氣的路徑改變',48,TEAL,True,True,anchor='mm')
        txt(d,(540,1125),'抵達眼睛的光，也就不同',37,INK,True,anchor='mm')
        return im
    im=camera(raster('sky-day.png'),1.015+.012*math.sin(t*.5))
    d=ImageDraw.Draw(im)
    if index==0:
        txt(d,(80,110),'ONE QUESTION / ONE MINUTE',27,'#d8f7f1',bold=True)
        txt(d,(80,205),'陽光是白的，',75,'#fff8e9',True,True)
        txt(d,(80,320),'天空怎麼是藍的？',77,'#fff8e9',True,True)
        txt(d,(85,440),'WHY IS THE SKY BLUE?',32,'#d8f7f1',bold=True)
    else:
        head(im,index,'藍光，從天空來到眼睛。','LOOK AWAY FROM THE SUN.',True)
        sun(d,(950,550),43)
        # Direct sunlight goes down the right edge, away from the gaze.
        arrow(d,(950,605),(1030,1190),'#ffe3a3',4)
        observer=(620,1120)
        for j,start in enumerate(((170,600),(420,690),(790,760))):
            d.ellipse((start[0]-9,start[1]-9,start[0]+9,start[1]+9),fill='#dae3de')
            arrow(d,start,observer,'#9ae8ff',6)
            pulse(d,start,observer,t*.5+j*.27,'#e8feff',8)
        eye(d,observer)
        txt(d,(620,1190),'觀察者眼睛（示意）',30,'#fff8e9',True,True,anchor='mm')
        note(im,'藍光由不同方向進入眼睛；視線避開太陽',True)
    return im


def sky_colors(n,cue):
    im=S.backdrop(True).copy(); d=ImageDraw.Draw(im)
    head(im,1,'白光裡，混合了多種顏色。','MANY COLORS. ONE BEAM.',True)
    sun(d,(150,850),62)
    arrow(d,(222,850),(460,850),'#fff8e9',18)
    colors=['#f47368','#ffb464','#f8dc7e','#7bd797','#69bfff','#ad9fea']
    for i,col in enumerate(colors):
        y=775+i*30
        d.line((465,850,545,y),fill=col,width=8)
        arrow(d,(545,y),(930,y),col,8)
        pulse(d,(545,y),(930,y),n/FPS*.36+i*.05,'#fff6e5',6)
    txt(d,(540,1200),'紅、橙、黃、綠、藍、紫……',43,'#fff2de',True,True,anchor='mm')
    note(im,'分色只為辨識成分，並非陽光在此自行分開',True)
    return im


def earth(im):
    d=ImageDraw.Draw(im)
    d.ellipse((-360,850,1440,2650),fill='#a3d8df',outline='#71b4c5',width=4)
    d.ellipse((-180,1030,1260,2470),fill='#5d9d9d',outline='#2d727d',width=6)
    d.arc((-120,1090,1200,2410),195,345,fill='#8fbda9',width=38)
    eye(d,(540,1000))
    txt(d,(540,1135),'同一位觀察者',30,INK,True,True,anchor='mm')
    txt(d,(875,935),'大氣',31,INK,True,anchor='mm')


def sky_atmosphere(n,index,cue):
    im=S.backdrop().copy(); d=ImageDraw.Draw(im)
    titles={2:('跟著光，進入大氣。','INTO THE ATMOSPHERE.'),6:('太陽，移近地平線。','THE SAME OBSERVER. A NEW ANGLE.'),7:('傍晚，穿過更多大氣。','A LONGER PATH THROUGH AIR.'),8:('藍光散出，直射光更紅。','BLUE SCATTERS OUT. RED CONTINUES.')}
    head(im,index,*titles[index]); earth(im); d=ImageDraw.Draw(im)
    observer=(540,1000)
    if index==2:
        sun(d,(540,540))
        arrow(d,(540,600),observer,'#e9aa54',9)
        pulse(d,(540,600),observer,n/FPS*.45,'#fffaf0',12)
        for xy in ((440,905),(540,890),(625,925),(770,1000),(315,985)):
            d.ellipse((xy[0]-9,xy[1]-9,xy[0]+9,xy[1]+9),fill='#b5bbad')
    elif index==6:
        p=S.ease((n-cue['start'])/(cue['end']-cue['start']))
        angle=-math.pi/2-p*math.pi/2
        pos=(540+490*math.cos(angle),1000+490*math.sin(angle))
        sun(d,pos,45); arrow(d,pos,observer,'#e9aa54',7)
    else:
        sun(d,(55,1000),42)
        arrow(d,(540,850),observer,'#83a39e',4)
        txt(d,(680,735),'較短路徑',33,INK,True,True,anchor='mm')
        txt(d,(285,1190),'較長路徑',36,TEAL,True,True,anchor='mm')
        arrow(d,(110,1000),observer,RED,10)
        pulse(d,(110,1000),observer,n/FPS*.45,'#ffe6b2',11)
        if index==8:
            for j,x in enumerate((155,265,375)):
                start=(x,1000); end=(x+35,750-j*45)
                arrow(d,start,end,BLUE,7)
                pulse(d,start,end,n/FPS*.5+j*.22,'#79d4ff',9)
            txt(d,(790,640),'散射出去的藍光',33,BLUE,True,True,anchor='mm')
        else: pulse(d,(540,850),observer,n/FPS*.8,'#fffaf0',9)
    note(im,'大氣厚度、光路與太陽位置經簡化，並非實際比例')
    return im


def sky_scatter(n,index,cue):
    im=S.backdrop().copy(); d=ImageDraw.Draw(im)
    if index==3:
        head(im,index,'碰到空氣分子，光會散射。','SOME LIGHT CHANGES DIRECTION.')
        sun(d,(120,820),46)
        arrow(d,(180,820),(925,820),'#e9aa54',10)
        center=(460,820)
        for j,end in enumerate(((740,530),(870,1050),(290,1160),(265,510))):
            arrow(d,center,end,BLUE,6); pulse(d,center,end,n/FPS*.5+j*.2,'#55c6ed',9)
        arrow(d,center,(815,1260),RED,4)
        d.ellipse((440,800,480,840),fill='#9aaea8',outline='#fff8e8',width=4)
        txt(d,(460,910),'空氣分子',34,INK,True,True,anchor='mm')
        note(im,'部分光向不同方向散射，仍有光繼續前進')
    else:
        head(im,index,'藍光，比紅光更容易散射。','SAME INPUT. DIFFERENT SCATTERING.')
        for is_blue,top,col in ((True,530,BLUE),(False,975,RED)):
            d.rounded_rectangle((75,top,1005,top+365),radius=32,fill='#e3f3ed' if is_blue else '#ffead9')
            txt(d,(115,top+30),'藍光' if is_blue else '紅光',44,col,True,True)
            for j in range(5):
                y=top+125+j*44; start=(170,y); hit=(505,y)
                d.line((*start,*hit),fill=col,width=6)
                d.ellipse((496,y-9,514,y+9),fill='#a8b5ac')
                end=(875,y-65) if j<(4 if is_blue else 1) else (875,y)
                arrow(d,hit,end,col,6)
                pulse(d,hit,end,n/FPS*.45+j*.11,col,8)
        note(im,'入射光各五條作比較；分支數量只是示意，並非散射比例')
    return im


@lru_cache(maxsize=1)
def astro_source():
    im=Image.open(OUT/'assets/astronaut.png').convert('RGBA')
    if im.getextrema()[3][0]!=0 or im.getextrema()[3][1]<240: raise ValueError('Astronaut needs alpha')
    return im.crop(im.getbbox())


@lru_cache(maxsize=16)
def astro_sprite(width,flipped=False):
    source=astro_source()
    im=source.resize((width,round(width*source.height/source.width)),Image.Resampling.LANCZOS)
    return ImageOps.mirror(im) if flipped else im


def astronaut(im,center,width=430,flipped=False):
    sprite=astro_sprite(width,flipped)
    im.paste(sprite,(round(center[0]-sprite.width/2),round(center[1]-sprite.height/2)),sprite)


@lru_cache(maxsize=1)
def stars():
    rng=np.random.default_rng(2108)
    return list(zip(rng.integers(0,W,85),rng.integers(370,1420,85),rng.integers(1,3,85)))


def space_bg(n):
    im=S.backdrop(True).copy(); d=ImageDraw.Draw(im)
    for i,(x,y,r) in enumerate(stars()):
        xx=(x+int(n*.018*(r+1)))%W
        d.ellipse((xx-r,y-r,xx+r,y+r),fill='#9ab9bd' if i%3 else '#d0dcd6')
    d.ellipse((-600,1430,1850,2950),fill='#3b777c',outline='#7fbeb7',width=7)
    d.ellipse((-600,1460,1850,2980),fill='#234d62')
    return im


def space_pair(n,index,cue):
    t=n/FPS
    im=space_bg(n)
    for x,flip in ((220,False),(860,True)): astronaut(im,(x,990+math.sin(t*.8+(1 if flip else 0))*10),430,flip)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((420,670,660,1180),radius=25,fill='#174651')
    if index==0:
        txt(d,(80,110),'ONE QUESTION / ONE MINUTE',27,'#bce9df',bold=True)
        txt(d,(80,205),'隔著真空，',77,'#fff5e3',True,True)
        txt(d,(80,320),'怎麼還能通話？',79,'#fff5e3',True,True)
        txt(d,(85,440),'CAN SOUND CROSS SPACE?',32,'#bce9df',bold=True)
    else:
        titles={4:('聲音，過不了這段真空。','NO SOUND PATH THROUGH THE GAP.'),5:('送出去的，是無線電。','RADIO = ELECTROMAGNETIC WAVES.'),6:('電磁波，不需要空氣。','RADIO CAN CROSS A VACUUM.'),9:('跨真空靠無線電，耳邊才是聲音。','SAME MESSAGE. DIFFERENT CARRIER.')}
        ch,en=titles[index]
        # Long closing title uses a deliberately smaller size.
        if index==9:
            txt(d,(80,110),'10 / EVERYDAY SCIENCE',27,'#87e5e0',bold=True)
            txt(d,(80,200),'跨真空靠無線電，',65,'#fff5e3',True,True)
            txt(d,(80,292),'耳邊才是聲音。',65,'#fff5e3',True,True)
            txt(d,(83,390),en,29,'#87e5e0')
        else: head(im,index,ch,en,True)
    txt(d,(540,730),'真空',44,'#d8f1e8',True,True,anchor='mm')
    txt(d,(540,790),'VACUUM',24,'#b8d3d0',anchor='mm')
    if index>=5:
        y=1000
        for cx in (320,760):
            d.rounded_rectangle((cx-26,y-40,cx+26,y+40),radius=8,fill='#71d5d2',outline='#d8fff5',width=3)
        points=[]
        for x in range(350,732,4): points.append((x,y+26*math.sin((x-350)*.045-t*4)))
        d.line(points,fill='#7ee3e7',width=7)
        arrow(d,(350,1080),(730,1080),'#7ee3e7',4)
        pulse(d,(350,y),(730,y),t*.32,'#f1ffed',11)
        txt(d,(540,1190),'電磁波',36,'#9aeeec',True,True,anchor='mm')
    elif index==4:
        txt(d,(540,1010),'無傳聲介質',31,'#c5dbd5',True,anchor='mm')
    if index==9:
        d.rounded_rectangle((75,1260,1005,1390),radius=25,fill='#fff3df')
        txt(d,(540,1320),'說話 → 無線電 → 接收 → 喇叭 → 聲音',36,INK,True,True,anchor='mm')
    else: note(im,'真空區無分子接力；背景星點不是傳聲介質',True)
    return im


def space_intuition(n,cue):
    im=space_bg(n)
    astronaut(im,(430,1030),690)
    head(im,1,'喊再大聲，也需要物質。','SOUND NEEDS A MATERIAL MEDIUM.',True)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((550,680,1020,1130),radius=35,fill='#fff2dd')
    txt(d,(785,760),'聲音',61,INK,True,True,anchor='mm')
    txt(d,(785,890),'需要物質',49,TEAL,True,True,anchor='mm')
    txt(d,(785,1000),'空氣只是其中一種介質',26,INK,True,anchor='mm')
    note(im,'聲音是物質中的擾動，並非只有空氣能傳聲',True)
    return im


def speaker(d,x,y,col=GOLD):
    d.rectangle((x-35,y-30,x-10,y+30),fill=col)
    d.polygon([(x-10,y-30),(x+30,y-65),(x+30,y+65),(x-10,y+30)],fill=col)


def air_particles(im,n,x0,x1,y,rows=3):
    t=n/FPS
    for row in range(rows):
        for j in range(10):
            fixed_x=x0+(x1-x0)*j/9
            x=fixed_x+8*math.sin(t*5-j*.7)
            yy=y+row*75
            sprite=S.ball(13,True)
            im.paste(sprite,(round(x-15),round(yy-15)),sprite)


def space_air(n,index,cue):
    im=S.backdrop().copy(); d=ImageDraw.Draw(im)
    if index==2:
        head(im,index,'聲音，是物質傳遞的擾動。','PARTICLES VIBRATE. THE DISTURBANCE TRAVELS.')
        d.rounded_rectangle((215,650,1000,1130),radius=35,fill='#fff0d9',outline='#e1b681',width=3)
        txt(d,(610,710),'空氣中的聲音（獨立示意）',35,TEAL,True,True,anchor='mm')
        speaker(d,135,920,TEAL)
        air_particles(im,n,270,930,825)
        d=ImageDraw.Draw(im)
        p=(n/FPS*.3)%1; x=265+670*p
        d.rounded_rectangle((x-14,790,x+14,1020),radius=12,outline='#ce744b',width=4)
        arrow(d,(280,1210),(930,1210),'#c97d4f',5)
        txt(d,(540,1300),'粒子原地振動，擾動向前傳',40,INK,True,True,anchor='mm')
    else:
        head(im,index,'物質能接力，理想真空不行。','AIR CAN CARRY SOUND. VACUUM CANNOT.')
        d.rounded_rectangle((70,600,525,1200),radius=30,fill='#fff0d9',outline='#e1b681',width=3)
        d.rounded_rectangle((555,600,1010,1200),radius=30,fill='#e7f3ef',outline='#8cb6b3',width=3)
        txt(d,(298,675),'空氣',49,INK,True,True,anchor='mm')
        txt(d,(783,675),'理想真空',49,TEAL,True,True,anchor='mm')
        air_particles(im,n,115,480,840)
        d=ImageDraw.Draw(im)
        compression_x=120+355*((n/FPS*.32)%1)
        d.rounded_rectangle((compression_x-12,800,compression_x+12,1030),radius=10,outline='#bd7544',width=4)
        txt(d,(783,965),'沒有粒子接力',33,TEAL,True,anchor='mm')
        txt(d,(540,1300),'擾動留在有物質的區域',40,INK,True,True,anchor='mm')
    note(im,'每個粒子只在固定位置附近振動；此為獨立空氣示意')
    return im


def receiver(n,index,cue):
    im=space_bg(n)
    head(im,index,'接收後，喇叭把聲音還原。' if index==7 else '耳朵聽見的，最後仍是聲音。','RECEIVER → SPEAKER → AIR → EAR.',True)
    d=ImageDraw.Draw(im)
    # A clearly separate cutaway, rather than adding air to the vacuum gap.
    d.rounded_rectangle((255,590,1000,1320),radius=180,fill='#edf3e5',outline='#a4e2dc',width=9)
    txt(d,(640,665),'頭盔內部（剖面示意）',38,INK,True,True,anchor='mm')
    d.rounded_rectangle((75,760,235,910),radius=22,fill='#6ac5cc',outline='#d5fbef',width=4)
    txt(d,(155,805),'接收機',32,INK,True,True,anchor='mm')
    txt(d,(155,865),'RADIO',22,INK,anchor='mm')
    arrow(d,(238,840),(342,965),'#67d9e5',7)
    speaker(d,365,1000,TEAL)
    # Local air is confined inside the receiver's closed helmet cutaway.
    air_particles(im,n,440,765,925,2)
    d=ImageDraw.Draw(im)
    d.arc((815,900,930,1100),-100,110,fill='#bd7544',width=10)
    d.arc((845,940,910,1050),-100,100,fill='#bd7544',width=7)
    if index==8:
        rr=75+5*math.sin(n/FPS*3)
        d.ellipse((870-rr,1000-rr,870+rr,1000+rr),outline='#ce8a49',width=4)
    txt(d,(365,1160),'喇叭',31,INK,True,True,anchor='mm')
    txt(d,(600,1160),'空氣振動',31,INK,True,True,anchor='mm')
    txt(d,(875,1160),'耳朵',31,INK,True,True,anchor='mm')
    arrow(d,(440,1240),(815,1240),'#bd7544',5)
    note(im,'青色為電訊號；橙色為頭盔內的聲音與空氣振動',True)
    return im


def shot(episode,n,index,cues):
    cue=cues[index]
    if episode=='sky':
        if index in (0,5,9): return sky_hero(n,index,cue)
        if index==1: return sky_colors(n,cue)
        if index in (2,6,7,8): return sky_atmosphere(n,index,cue)
        return sky_scatter(n,index,cue)
    if index in (0,4,5,6,9): return space_pair(n,index,cue)
    if index==1: return space_intuition(n,cue)
    if index in (2,3): return space_air(n,index,cue)
    return receiver(n,index,cue)


def frame(episode,n,cues):
    index=next((i for i,c in enumerate(cues) if c['start']<=n<c['end']),0)
    im=shot(episode,n,index,cues)
    dt=n-cues[index]['start']
    if index>0 and 0<=dt<12:
        previous=shot(episode,cues[index]['start']-1,index-1,cues)
        im=Image.blend(previous,im,S.ease(dt/12))
    S.caption(im,n,cues,'zh')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((80,1830,1000,1835),radius=2,fill='#96b8b2')
    d.rounded_rectangle((80,1830,80+920*(n+1)/cues[-1]['end'],1835),radius=2,fill=TEAL)
    return im


def contact(pictures,path):
    sheet=Image.new('RGB',(810,480*math.ceil(len(pictures)/3)),'#fff0da')
    for i,im in enumerate(pictures): sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i%3)*270,(i//3)*480))
    sheet.save(path)


def preview(episode,cues):
    dest=OUT/episode/'preview'; dest.mkdir(parents=True,exist_ok=True)
    pics=[]
    for i,c in enumerate(cues):
        im=frame(episode,(c['start']+c['end'])//2,cues); im.save(dest/f'shot-{i+1:02}.png'); pics.append(im)
    contact(pics,dest/'contact.png')
    # Direction/oscillation pairs are additional evidence, not only static midpoints.
    for n in ([1040,1046,1070] if episode=='sky' else [380,386,1040,1046,1190,1196]):
        frame(episode,n,cues).save(dest/f'frame-{n:04}.png')


def execute(name,argv,episode,tools,binding,capture=False):
    binary=(tools/(name+'.exe')).resolve(strict=True); verify(binary,binding[name])
    base=['-hide_banner','-loglevel','error','-nostdin','-y'] if name=='ffmpeg' else []
    return subprocess.run([str(binary),*base,*map(str,argv)],cwd=OUT/episode,env=ENV,check=True,capture_output=capture,text=capture,encoding='utf-8' if capture else None)


def render(episode,cues,tools,bindings,original):
    dest=OUT/episode
    start=time.perf_counter(); binary=(tools/'ffmpeg.exe').resolve(strict=True); verify(binary,bindings['ffmpeg'])
    argv=[str(binary),'-hide_banner','-loglevel','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-i',str(original/'narration.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-pix_fmt','yuv420p','-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-ar','48000','-b:a','160k','-movflags','+faststart',f'{episode}-v2-zh.mp4']
    with subprocess.Popen(argv,stdin=subprocess.PIPE,cwd=dest,env=ENV) as proc:
        try:
            for n in range(cues[-1]['end']):
                proc.stdin.write(frame(episode,n,cues).tobytes())
                if n%240==0: print(f'{episode} {n}/{cues[-1]["end"]}',flush=True)
            proc.stdin.close()
            if proc.wait(): raise RuntimeError('FFmpeg failed')
        except BaseException: proc.kill(); proc.wait(); raise
    for lang,name in (('zh','zh-Hant.srt'),('en','en.srt')):
        entries=[f'{i}\n{S.srt_time(c["start"])} --> {S.srt_time(c["end"])}\n{c[lang]}' for i,c in enumerate(cues,1)]
        (dest/name).write_text('\n\n'.join(entries)+'\n',encoding='utf-8')
    execute('ffmpeg',['-i',f'{episode}-v2-zh.mp4','-t','12','-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-c:a','aac','-movflags','+faststart',f'{episode}-v2-preview.mp4'],episode,tools,bindings)
    save(dest/'provenance.json',{'renderer_sha256':sha(Path(__file__)),'inputs_sha256':sha(HERE/f'{episode}-inputs.json'),'review_sha256':sha(HERE/f'{episode}-visual-review.json'),'audio_sha256':sha(original/'narration.wav'),'frames':cues[-1]['end'],'render_seconds':round(time.perf_counter()-start,2),'engine':'Pillow layered composition + FFmpeg, not production Remotion','image_generation':{'mode':'built-in image_gen','batch_calls':3,'metered_api_calls':0,'price':'not reported; subscription/compute/review unpriced'},'human_acceptance':'PENDING','market_acceptance':'PENDING'})


def qa(episode,cues,tools,bindings):
    dest=OUT/episode; samples=dest/'actual-mp4'; samples.mkdir(exist_ok=True)
    reports={}
    for name in (f'{episode}-v2-zh.mp4',f'{episode}-v2-preview.mp4'):
        data=json.loads(execute('ffprobe',['-v','error','-show_streams','-show_format','-of','json',name],episode,tools,bindings,True).stdout)
        video=next(s for s in data['streams'] if s['codec_type']=='video'); audio=next(s for s in data['streams'] if s['codec_type']=='audio')
        expected=cues[-1]['end']/FPS if '-zh.' in name else 12
        assert (video['width'],video['height'],video['avg_frame_rate'],video['pix_fmt'],video['codec_name'],audio['codec_name'])==(W,H,'30/1','yuv420p','h264','aac')
        assert abs(float(data['format']['duration'])-expected)<.11
        execute('ffmpeg',['-v','error','-xerror','-i',name,'-map','0:v','-map','0:a','-f','null','NUL'],episode,tools,bindings)
        analysis=execute('ffmpeg',['-i',name,'-vf','blackdetect=d=0.15:pix_th=0.08','-af','silencedetect=n=-45dB:d=2,ebur128=peak=true','-f','null','NUL','-loglevel','info'],episode,tools,bindings,True).stderr
        (samples/(Path(name).stem+'-analysis.txt')).write_text(analysis,encoding='utf-8')
        assert 'black_start:' not in analysis
        silences=[float(s) for s in re.findall(r'silence_start: ([\d.]+)',analysis)]
        assert not silences or (episode=='sky' and '-zh.' in name and len(silences)==1 and silences[0]>=cues[-1]['speech_end']/FPS-.2)
        integrated=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',analysis)[-1])
        peak=float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',analysis)[-1])
        assert -19<=integrated<=-13 and peak<=0
        reports[name]={'sha256':sha(dest/name),'bytes':(dest/name).stat().st_size,'duration':data['format']['duration'],'probe':data,'decode':'PASS','blackdetect':'PASS','silence_starts':silences,'integrated_lufs':integrated,'true_peak_dbfs':peak}
    pictures=[]
    indices=[(c['start']+c['end'])//2 for c in cues]
    extra=[1040,1046,1070] if episode=='sky' else [380,386,1040,1046,1190,1196]
    for j,n in enumerate(indices+extra+[0,cues[-1]['end']-1]):
        path=samples/(f'shot-{j+1:02}.png' if j<len(cues) else f'frame-{n:04}.png')
        execute('ffmpeg',['-ss',n/FPS,'-i',f'{episode}-v2-zh.mp4','-frames:v','1',str(path)],episode,tools,bindings)
        if j<len(cues):
            with Image.open(path) as im: pictures.append(im.copy())
    contact(pictures,samples/'contact.png')
    for lang in ('zh','en'):
        for c in cues:
            lines,size=S.wrapped(c[lang],lang)
            assert len(lines)*(size+21)<=250
            assert all(S.font(size,lang=='zh').getlength(line)<=850 for line in lines)
    save(dest/'qa.json',{'status':'PASS','renderer_sha256':sha(Path(__file__)),'inputs_sha256':sha(HERE/f'{episode}-inputs.json'),'reports':reports,'caption_bounds':'PASS','human_acceptance':'PENDING','market_acceptance':'PENDING'})
    print(episode+' QA PASS',flush=True)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--episode',choices=['sky','space'],required=True); parser.add_argument('--mode',choices=['preview','render','qa'],required=True)
    args=parser.parse_args()
    cues,tools,bindings,original=inputs(args.episode,args.mode!='preview')
    if args.mode=='preview': preview(args.episode,cues)
    elif args.mode=='render': render(args.episode,cues,tools,bindings,original)
    else: qa(args.episode,cues,tools,bindings)


if __name__=='__main__': main()
