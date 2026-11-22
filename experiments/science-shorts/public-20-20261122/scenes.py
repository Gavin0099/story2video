"""Animated English diagrams for WhyNest Lab. Coordinates use a 720x1280 canvas."""
from functools import lru_cache
import math
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 720, 1280
ART = Path(__file__).resolve().parents[3] / 'artifacts/science-shorts/public-20-20261122'
INK, PAPER = '#171e3a', '#fff1d7'
BLUE, CYAN, ORANGE, GOLD, MUTE = '#2869b9', '#65e2df', '#fa7959', '#ffcd78', '#b8c9dd'


@lru_cache(maxsize=32)
def font(size, serif=False):
    name = 'georgiab.ttf' if serif else 'seguisb.ttf'
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), size)


def txt(d, xy, s, size=26, fill=PAPER, anchor='mm', serif=False):
    d.text(xy, s, font=font(size, serif), fill=fill, anchor=anchor)


def split_text(s, size, limit):
    words = s.split()
    lines, line = [], ''
    for word in words:
        trial = (' '.join((line, word))).strip()
        if line and font(size, True).getlength(trial) > limit:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def arrow(d, a, b, color=ORANGE, width=6):
    ax, ay = a
    x, y = b
    angle = math.atan2(y-ay, x-ax)
    d.line((*a, *b), fill=color, width=width)
    d.polygon([b,(x-17*math.cos(angle-.5),y-17*math.sin(angle-.5)),
                 (x-17*math.cos(angle+.5),y-17*math.sin(angle+.5))], fill=color)


def disk(d, x, y, r, color, outline=None, width=1):
    d.ellipse((x-r,y-r,x+r,y+r), fill=color, outline=outline, width=width)


def ease(p):
    p = min(1, max(0, p))
    return p*p*(3-2*p)


@lru_cache(maxsize=20)
def background(i, bright):
    palette = (('#102347','#163559'),('#281d39','#442b56'),('#103a44','#16505b'),('#20284c','#292f65'))
    low, high = palette[i % len(palette)]
    if bright:
        low, high = high, low
    im = Image.new('RGB',(W,H),low)
    d=ImageDraw.Draw(im)
    d.ellipse((-530,265,1140,1330),fill=high)
    d.arc((-550,239,1162,1370),198,345,fill='#526b83',width=2)
    d.arc((-554,260,1150,1320),12,124,fill='#49667b',width=2)
    jitter=random.Random(i*431+4)
    for _ in range(950):
        x,y=jitter.randrange(W),jitter.randrange(H)
        d.point((x,y),fill=('#43738c' if i%2==0 else '#61506d'))
    return im


def straw(d,k,p):
    top=426; surface=668; rise=(122*ease(p*1.7) if k in (0,4) else 125 if k==5 else 125*(1-ease(p)) if k==6 else 0)
    d.rounded_rectangle((195,575,512,905),radius=35,fill='#22385d',outline=MUTE,width=5)
    d.rounded_rectangle((202,surface,505,894),radius=21,fill=BLUE)
    d.line((204,surface,503,surface),fill=CYAN,width=5)
    d.rectangle((344,top,379,838),fill='#112645',outline=PAPER,width=4)
    d.rectangle((350,surface-rise,373,834),fill=CYAN)
    d.line((351,surface-rise,371,surface-rise),fill='#c8ffff',width=4)
    d.line((194,574,514,574),fill=PAPER,width=5)
    if k>=2 and k<=5:
        d.arc((301,356,423,455),190,338,fill=ORANGE,width=8)
        for j in range(3):
            dot_y=498-(p*95+j*27)%95
            disk(d,361,dot_y,4,MUTE)
    if k in (1,3,4,5):
        for x in (233,280,439,479): arrow(d,(x,588),(x,646),GOLD,5)
        if k == 1: arrow(d,(361,584),(361,649),GOLD,5)
        txt(d,(353,958),'ROOM AIR PUSHES ON THE DRINK',21,GOLD)
    if k==6: arrow(d,(397,398),(371,426),GOLD,4)


def coin(d,k,p):
    # The bent ray crosses an air–water boundary before clearing the rim.
    rim=(486,610); eye=(622,455); source=(302,823); water=680 if k>=3 else 838
    d.polygon([(165,610),rim,(463,883),(198,883)],fill='#253c62',outline=MUTE,width=5)
    if k>=3:
        d.polygon([(174,water),(479,water),(463,879),(198,879)],fill=BLUE)
        d.line((177,water,478,water),fill=CYAN,width=5)
    d.ellipse((source[0]-33,source[1]-12,source[0]+33,source[1]+12),fill=GOLD,outline=ORANGE,width=3)
    d.ellipse((eye[0]-25,eye[1]-13,eye[0]+25,eye[1]+13),fill=PAPER)
    disk(d,*eye,8,INK)
    if k in (0,2):
        d.line((*source,490,606),fill=ORANGE,width=5)
        d.line((480,596,500,616),fill=ORANGE,width=5)
        d.line((500,596,480,616),fill=ORANGE,width=5)
    if k>=3:
        turn=(395,water)
        d.line((*source,*turn,*eye),fill=GOLD,width=5)
        if k in (3,4):
            for y in range(600,771,20): d.line((turn[0],y,turn[0],y+11),fill=MUTE,width=2)
        x,y=(source,turn) if p < .5 else (turn,eye)
        t=p*2 if p < .5 else p*2-1
        disk(d,x[0]+(y[0]-x[0])*t,x[1]+(y[1]-x[1])*t,8,PAPER)
    d.line((165,610,*rim),fill=PAPER,width=6)
    txt(d,(312,924),'CUP CUTAWAY',20,MUTE)


def metal(d,k,p):
    for x,name,col in ((92,'METAL','#95b6d7'),(388,'WOOD','#af6e4c')):
        d.rounded_rectangle((x,665,x+240,858),radius=25,fill=col,outline=PAPER,width=3)
        if name=='WOOD':
            for yi in range(695,842,29): d.arc((x+14,yi-15,x+222,yi+28),200,342,fill='#7e453c',width=3)
        else:
            for yi in range(695,842,29): d.line((x+20,yi,x+217,yi),fill='#c6dceb',width=2)
        finger_y=594+22*ease(p) if k==0 else 628
        d.rounded_rectangle((x+80,finger_y-121,x+158,finger_y+35),radius=39,fill='#ffb587',outline=ORANGE,width=4)
        txt(d,(x+120,909),name,24)
        if k==1: txt(d,(x+120,754),'22 °C',39,INK if name=='METAL' else PAPER)
        if 2<=k<=5:
            length=(110 if name=='METAL' else 55)*(.65+.35*ease(p))
            arrow(d,(x+120,651),(x+120,651+length),GOLD,7)
            if k>=3 and name=='METAL':
                arrow(d,(x+115,765),(x+45,790),GOLD,5); arrow(d,(x+124,765),(x+200,790),GOLD,5)


def bubble(d,k,p):
    if k in (1,2):
        disk(d,360,663,188,'#1e5370',CYAN,5)
        d.arc((177,477,543,849),192,309,fill=PAPER,width=5)
        d.arc((187,487,533,839),207,291,fill=ORANGE,width=6)
        arrow(d,(562,486),(480,535),GOLD,4); txt(d,(574,456),'THIN FILM',20)
        txt(d,(349,669),'AIR',29,CYAN)
        if k==2:
            arrow(d,(341,471),(270,471),CYAN,5)
            arrow(d,(379,471),(450,471),CYAN,5)
            txt(d,(360,422),'TENSION ALONG THE FILM',20,CYAN)
    elif k in (3,4):
        d.ellipse((83,555,323,795),fill='#1e5370',outline=CYAN,width=5)
        r_y=173
        r_x=math.sqrt(120**3/r_y)
        d.ellipse((512-r_x,675-r_y,512+r_x,675+r_y),fill='#244d6a',outline=ORANGE,width=5)
        d.arc((83,643,323,706),0,180,fill=CYAN,width=2)
        d.arc((512-r_x,643,512+r_x,706),0,180,fill=ORANGE,width=2)
        txt(d,(200,881),'SPHERE',21,CYAN); txt(d,(515,881),'STRETCHED',21,ORANGE)
        txt(d,(360,934),'SAME ENCLOSED VOLUME · SCHEMATIC',18,MUTE)
        if k==4:
            txt(d,(200,845),'LESS FILM',19,CYAN)
            txt(d,(515,456),'MORE FILM',19,ORANGE)
    else:
        if k==0 or k==6:
            d.line((164,572,109,782),fill=ORANGE,width=19)
            d.ellipse((88,498,240,623),outline=GOLD,width=10)
        shift=55*ease(p); r=158; extension=1+.39*(1-ease(p)) if k==0 else 1+.12*(1-ease(p)) if k==5 else 1
        x,y=389+shift,675-shift/2
        rx,ry=r/math.sqrt(extension),r*extension
        d.ellipse((x-rx,y-ry,x+rx,y+ry),fill='#1b5575',outline=CYAN,width=6)
        d.arc((x-rx+29,y-ry+28,x+rx-28,y+ry-29),199,298,fill=PAPER,width=7)
        disk(d,x+58,y-96,8,GOLD)


def compass(d,k,p):
    x,y=360,671
    disk(d,x,y,192,INK,MUTE,6); disk(d,x,y,160,'#234368',CYAN,3)
    rot=math.pi/2*(ease(p) if k in (0,5) else 1)
    for j,c in enumerate(('N','E','S','W')):
        a=-math.pi/2+j*math.pi/2+rot
        txt(d,(x+136*math.cos(a),y+136*math.sin(a)),c,24)
    field=-math.pi/2-.18
    if 2<=k<=5:
        dx=math.tan(.18)*100
        for shift in (-225,225): arrow(d,(x+shift+dx,y+100),(x+shift-dx,y-100),CYAN,5)
    a=field + (.57*(1-ease(p)) if k==3 else .57 if k==2 else 0)
    vx,vy=math.cos(a),math.sin(a); nx,ny=-vy,vx
    for sign,col in ((1,ORANGE),(-1,PAPER)):
        d.polygon([(x+vx*119*sign,y+vy*119*sign),(x+nx*20,y+ny*20),(x-nx*20,y-ny*20)],fill=col)
    disk(d,x,y,12,GOLD)
    if k==4:
        arrow(d,(545,530),(545,449),PAPER,5)
        txt(d,(548,414),'TRUE NORTH',19)


def paper(d,k,p):
    d.line((75,944,645,944),fill=MUTE,width=4)
    if k in (0,5,6):
        flat=477+345*ease(p*.63); crumpled=477+435*ease(p*1.5)
        crumpled=min(crumpled,908)
    elif k==3: flat=crumpled=579+165*p
    else: flat=crumpled=652
    wobble=12*math.sin(p*12)
    d.polygon([(142,flat-24+wobble),(303,flat-4),(277,flat+22-wobble),(112,flat+10)],fill=PAPER,outline=CYAN,width=3)
    x=510; y=crumpled
    d.polygon([(x-36,y-23),(x-9,y-36),(x+23,y-31),(x+37,y-4),(x+28,y+26),(x+4,y+34),(x-28,y+21)],fill=PAPER,outline=GOLD,width=3)
    d.line((x-27,y-13,x+9,y-4,x+23,y+19),fill='#b3a88d',width=4)
    if k in (2,3,4):
        for x0,y0 in ((217,flat),(510,crumpled)): arrow(d,(x0,y0+61),(x0,y0+148),GOLD,6)
        if k>=3:
            arrow(d,(219,flat-47),(219,flat-126),CYAN,7)
            arrow(d,(510,crumpled-47),(510,crumpled-94),CYAN,5)
    txt(d,(213,1000),'FLAT',24); txt(d,(510,1000),'CRUMPLED',24)


def balloon(d,k,p):
    wall=523
    d.rounded_rectangle((wall,392,629,963),radius=20,fill='#687793',outline=MUTE,width=4)
    for y in range(420,950,45): d.line((wall+8,y,616,y+15),fill='#7e8da6',width=2)
    bx=(290+135*ease(p)) if k==0 else (324+73*ease(p)) if k==3 else 425 if k>=5 else 370
    d.ellipse((bx-98,510,bx+98,805),fill='#f18c69',outline=PAPER,width=5)
    d.arc((bx-70,534,bx+56,716),200,278,fill='#ffd8be',width=8)
    d.polygon([(bx,793),(bx-13,829),(bx+13,827)],fill=ORANGE)
    d.arc((bx-28,797,bx+32,951),10,165,fill=PAPER,width=3)
    if k==1:
        contact=bx-94
        d.rounded_rectangle((138,568,contact+6,749),radius=18,fill=CYAN)
        arrow(d,(122,739),(122,561),GOLD)
        for i in range(3):
            txt(d,(contact-20+51*ease(p),625+i*36),'−',27,GOLD)
        txt(d,(188,779),'SWEATER',21)
    if 2<=k<=5:
        for y in range(553,759,41):
            txt(d,(bx+60,y),'−',29,INK)
    if k>=2:
        for y in range(553,759,41):
            gap=(18+18*ease(p)) if k==3 else 36 if k>=4 else 18
            d.ellipse((539,y-16,608,y+17),outline=MUTE,width=2)
            txt(d,(558,y),'+',23,PAPER)
            txt(d,(558+gap,y),'−',22,INK)
        txt(d,(578,990),'NEUTRAL WALL',19,MUTE)
    if k==4:
        arrow(d,(312,506),(462,506),GOLD,6)
        arrow(d,(312,465),(226,465),CYAN,5)
        txt(d,(356,424),'ELECTRIC FORCES',20,MUTE)
    if k==5:
        arrow(d,(429,650),(429,562),CYAN,6)
        arrow(d,(429,659),(429,747),GOLD,6)
        txt(d,(291,579),'FRICTION',18,CYAN)
        txt(d,(294,736),'WEIGHT',18,GOLD)
        txt(d,(360,952),'VERTICAL FORCES SHOWN',19,MUTE)


def condensation(d,k,p):
    if k==5:
        for x,cold in ((115,True),(393,False)):
            d.rounded_rectangle((x,482,x+212,853),radius=27,fill='#294d70',outline=PAPER,width=5)
            d.rounded_rectangle((x+9,611,x+203,841),radius=18,fill='#b56447')
            if cold:
                for xx,yy in ((x-7,636),(x-7,768),(x+219,671),(x+219,787)):
                    disk(d,xx,yy,8,CYAN,PAPER,2)
            txt(d,(x+106,908),'BELOW DEW POINT' if cold else 'ABOVE DEW POINT',19,CYAN if cold else PAPER)
            txt(d,(x+106,950),'COLD GLASS' if cold else 'ROOM-TEMP. GLASS',20,MUTE)
        return
    d.rounded_rectangle((207,422,502,936),radius=40,fill='#2a4774',outline=PAPER,width=5)
    d.rounded_rectangle((216,556,493,928),radius=29,fill='#b56447')
    d.line((221,556,486,556),fill=GOLD,width=5)
    for x,y in ((271,620),(345,580),(413,646)):
        d.rounded_rectangle((x-40,y-40,x+40,y+40),radius=10,fill='#8acfe9',outline=PAPER,width=3)
    if k in (1,2,3):
        for q in range(10):
            x=(125+q*31) if q<3 else 535+(q%4)*28
            y=480+(q*51)%391
            disk(d,x+7*math.sin(p*6+q),y,4,MUTE)
        txt(d,(540,985),'VAPOR MARKERS · SCHEMATIC',17,MUTE)
    cooling = ease(p)
    below_dew_point = 563+228*cooling >= 690
    if k>=4 or k==0 or (k==3 and below_dew_point):
        for q,(side,y) in enumerate(((-1,570),(-1,740),(1,597),(1,696),(1,825),(-1,832))):
            growth = (563+228*cooling-690)/101 if k==3 else .65+.35*p if k>=4 else p
            r=4+7*ease(min(1,growth+q*.065))
            x=(207 if side<0 else 502)+side*(r-1)
            disk(d,x,y,r,CYAN); disk(d,x-r*.24,y-r*.25,max(2,r*.22),PAPER)
    if k==2:
        d.arc((502,461,574,893),275,86,fill=CYAN,width=5)
        arrow(d,(585,652),(523,652),CYAN)
    if k==3:
        d.line((593,553,593,804),fill=PAPER,width=5)
        d.line((593,563+228*cooling,593,804),fill=CYAN,width=10)
        d.line((570,690,620,690),fill=GOLD,width=5)
        txt(d,(588,840),'DEW POINT',16,GOLD)


def wrench(d,k,p):
    if k in (3,4):
        entries=((208,'NEAR PUSH',.56),(508,'FAR PUSH',1))
    else:
        entries=((355,'PIVOT',.55 if k==0 else 1),)
    for cx,tag,position in entries:
        y,L=782,286
        scale=.73 if len(entries)==2 else 1
        angle=(ease(p)*(.17 if position<1 else .33)) if k in (4,6) else 0
        end=(cx+math.sin(angle)*L,y-math.cos(angle)*L)
        d.line((cx,y,*end),fill='#97b9da',width=round(40*scale))
        d.line((cx-5,y-4,end[0]-5,end[1]+4),fill='#d9e6f1',width=round(8*scale))
        disk(d,cx,y,55*scale,INK,PAPER,5)
        disk(d,cx,y,29*scale,GOLD)
        point=(cx+math.sin(angle)*L*position,y-math.cos(angle)*L*position)
        disk(d,*point,16*scale,CYAN)
        if k in (0,2,3,4,6):
            dx,dy=math.cos(angle)*63,math.sin(angle)*63
            arrow(d,(point[0]-dx,point[1]-dy),(point[0]+dx,point[1]+dy),ORANGE,6)
        if k==5:
            arrow(d,(cx,end[1]-65),(cx,y),ORANGE,6)
        if k in (2,4,6):
            d.arc((cx-88,y-88,cx+88,y+88),220,315 if position==1 else 277,fill=GOLD,width=7)
        if k in (3,4):
            xmark=cx-91
            d.line((xmark,y,xmark,point[1]),fill=MUTE,width=3)
            for yy in (y,point[1]): d.line((xmark-6,yy,xmark+6,yy),fill=MUTE,width=3)
        txt(d,(cx,915),tag,20)
    if k in (3,4): txt(d,(360,973),'SAME PERPENDICULAR FORCE',21,GOLD)


def evaporation(d,k,p):
    if 1<=k<=4:
        air='#203859'
        d.rounded_rectangle((75,470,645,880),radius=32,fill=air,outline=MUTE,width=3)
        d.rounded_rectangle((96,743,624,855),radius=18,fill=BLUE,outline=CYAN,width=3)
        for x in range(113,601,28):
            d.arc((x,781,x+60,835),195,345,fill='#83b4dc',width=4)
        for j in range(12):
            disk(d,125+j*42,759+(j%2)*14,6,PAPER)
        txt(d,(360,909),'Magnified wet fabric',25)
        txt(d,(360,949),'Water molecule symbols',21,MUTE)
        count=(3,5,11,7)[k-1]
        for j in range(count):
            t=ease(p*.7+j*.037)
            x=140+j*41
            if k==4:
                # Molecule symbols travel continuously with the air and cross the crop edge.
                x=150+j*52+p*228
                y=714-(j%3)*29
            elif k==3:
                y=722-(j%3)*42+16*math.sin(p*5+j)
            else:
                y=750-(62+(j%3)*37)*t
            if 87<x<634:
                disk(d,x,y,6,PAPER)
        if k==3:
            txt(d,(360,526),'Vapor gathers above the fabric',25)
            arrow(d,(257,692),(257,735),CYAN,4)
            arrow(d,(470,729),(470,679),CYAN,4)
        if k==4:
            arrow(d,(116,571),(612,571),GOLD,6)
            txt(d,(360,529),'Airflow',24,GOLD)
        return

    d.line((94,470,625,470),fill=MUTE,width=5)
    for side,x in enumerate((217,502)):
        sway=9*math.sin(p*7) if side else 0
        shirt=[(x-51,492),(x-113,530),(x-89,597),(x-67,582),
               (x-61+sway,793),(x+61+sway,793),(x+67,582),(x+89,597),
               (x+113,530),(x+51,492)]
        d.polygon(shirt,fill='#92abbf',outline=PAPER,width=4)
        d.arc((x-44,472,x+44,539),0,180,fill=PAPER,width=4)
        if k==5:
            wet=1-ease(p)*(.30 if side==0 else .76)
        else:
            wet={0:1,6:1,7:(.70,.24)[side]}[k]
        wet_width=5+40*wet
        d.ellipse((x+sway-wet_width,719-99*wet,x+sway+wet_width,719+38*wet),fill=BLUE)
        txt(d,(x,855),('Still air','Moving air')[side],26)
        if side and k!=6:
            arrow(d,(455,435),(625,435),GOLD,5)
    if k==6:
        txt(d,(360,920),'Same room humidity',25,CYAN)
        txt(d,(360,959),'Matched shirts at the start',21,MUTE)
    if k==7:
        for j in range(4):
            disk(d,513+j*34+24*p,638-j*18,6,PAPER)


def suction(d,k,p):
    ground=828
    cap=647
    if k==1:
        cap+=75*ease(p)
    elif k==2:
        cap+=75*(1-ease(p))
    lift=75*ease(max(0,(p-.38)/.62)) if k==6 else 0
    rim=62*ease(p*1.6) if k==5 else max(0,62-lift) if k==6 else 0
    cap-=lift
    edge=ground-lift
    d.rounded_rectangle((75,ground,645,906),radius=18,fill='#3d6d89',outline=MUTE,width=3)
    d.line((95,ground+25,619,ground+25),fill='#89c8df',width=3)
    d.line((112,ground+42,570,ground+42),fill='#6aa4bf',width=3)
    cup=[(168,edge),(219,cap+70),(305,cap),(415,cap),(501,cap+70),
         (552,edge-rim),(521,edge-rim),(475,cap+98),(410,cap+30),
         (310,cap+30),(243,cap+98),(202,edge)]
    d.polygon(cup,fill=BLUE,outline=CYAN,width=4)
    d.rounded_rectangle((330,cap-78,390,cap+10),radius=15,fill=CYAN,outline=PAPER,width=3)
    if k in (0,1):
        if k==0:
            arrow(d,(360,cap-105),(360,cap-193),PAPER,7)
            txt(d,(360,cap-224),'Pull',24)
        else:
            arrow(d,(360,cap-192),(360,cap-105),PAPER,7)
            for x,sign in ((196,-1),(524,1)):
                arrow(d,(x-sign*26,811),(x+sign*59,811),ORANGE,5)
    if k>=1:
        for j in range(9):
            if k==1 and j>=5:
                x=360+(-1 if j%2==0 else 1)*(70+j*9+120*p)
                y=803
            elif j<5 or k==6:
                x=(310,331,358,389,422)[j] if j<5 else 273+(j-5)*56
                y=min(810,cap+45+(j%3)*24)
                if k==6:
                    y+=lift*.7
            else:
                continue
            disk(d,x,y,5,PAPER)
    if k in (3,4):
        txt(d,(360,460),'Higher outside pressure',24,GOLD)
        txt(d,(360,783),'Lower inside pressure',22)
        for outside,inside in ((250,285),(470,435)):
            arrow(d,(outside,506),(outside,cap-34),GOLD,6)
            arrow(d,(inside,762),(inside,712),CYAN,4)
    if k==4:
        txt(d,(360,942),'Selected vertical pressure forces',22,MUTE)
        arrow(d,(360,976),(360,1030),ORANGE,8)
    if k in (5,6) and rim>18:
        arrow(d,(635,803),(502,803),GOLD,5)
        for j in range(3):
            disk(d,625-j*31-39*ease(p),804,5,PAPER)
        txt(d,(566,935),'Air enters',24,GOLD)
    if k>=6:
        txt(d,(360,998),'Pressures approach equality' if k==6 else 'Seal closed',25)


def friction(d,k,p):
    time=min(1,(k+p)/5)
    x=165+321*(1-(1-time)**2)
    d.rounded_rectangle((78,822,643,882),radius=14,fill='#655368',outline=MUTE,width=4)
    for j in range(105,610,38):
        d.line((j,847,j+31,847),fill='#af8891',width=2)
    d.rounded_rectangle((x-91,690,x+91,823),radius=12,fill='#af4f4d',outline=PAPER,width=4)
    d.rounded_rectangle((x-78,715,x+87,795),radius=6,fill='#e6c8a3')
    for y in range(726,791,15):
        d.line((x-68,y,x+83,y),fill='#af9487',width=2)
    if k==0 and p<.62:
        retraction=ease((p-.08)/.54)
        finger=x-93-142*retraction
        top=727-102*retraction
        d.polygon([(-32,top+30),(finger-51,top+29),(finger-43,top+15),
                   (finger-25,top+10),(finger,top+5),(finger+2,top+17),
                   (finger-21,top+23),(finger-16,top+33),(finger-26,top+48),
                   (finger-46,top+55),(-32,top+70)],fill='#dc9679',outline=PAPER,width=3)
    if k==1:
        d.rounded_rectangle((123,471,597,604),radius=20,fill=INK,outline=MUTE,width=3)
        d.line((148,530,566,530),fill=ORANGE,width=12)
        d.line((148,549,566,549),fill=MUTE,width=12)
        arrow(d,(272,497),(428,497),CYAN,4)
        txt(d,(360,578),'Magnified contact',22)
        d.line((360,604,x,817),fill=MUTE,width=3)
    if k in (2,3) and time<1:
        arrow(d,(x-12,648),(x-101,648),ORANGE,6)
        arrow(d,(x+15,565),(x+45+103*(1-time),565),CYAN,6)
        txt(d,(x-51,616),'Friction',23,ORANGE)
        txt(d,(x+48,525),'Motion',23,CYAN)
    if k==3:
        for j in range(5):
            mark=165+321*(1-(1-j/4)**2)
            disk(d,mark,928,6,CYAN)
        txt(d,(360,968),'Equal time between positions',22)
    if k in (4,5,7):
        share=1-(1-time)**2
        if k==4:
            txt(d,(111,415),'Energy during the slide',24,MUTE,'lm')
        for y,label,fraction,color in ((488,'Kinetic energy',1-share,CYAN),
                                       (591,'Thermal energy gained',share,GOLD)):
            txt(d,(111,y-27),label,25,PAPER,'lm')
            d.rounded_rectangle((111,y,611,y+24),radius=12,fill=INK,outline=MUTE,width=3)
            if fraction>0:
                d.rounded_rectangle((112,y+1,112+498*fraction,y+23),
                                    radius=10,fill=color)
        if k==5:
            for j in range(7):
                disk(d,x-63+j*21,812 if j%2 else 835,4,GOLD)
            txt(d,(360,949),'Book and tabletop warm slightly',24)
    if k==6:
        txt(d,(360,932),'Book stays here',25,CYAN)


def bridge(d,k,p):
    if k in (0,7):
        d.rounded_rectangle((76,685,645,777),radius=10,fill='#536d8c',outline=MUTE,width=4)
        d.rectangle((353,685,375,777),fill='#ad9c77')
        for j in range(104,622,36):
            d.line((j,737,j+16,737),fill=GOLD,width=3)
        x=147+396*ease(p)
        d.rounded_rectangle((x-56,641,x+57,682),radius=14,fill=ORANGE,outline=PAPER,width=3)
        d.polygon([(x-35,642),(x-25,613),(x+24,613),(x+43,642)],fill=BLUE,outline=PAPER,width=3)
        for wheel in (-32,34):
            disk(d,x+wheel,680,15,INK,outline=PAPER,width=3)
        arrow(d,(364,849),(364,789),CYAN,5)
        txt(d,(364,881),'Joint cover',25)
        return

    warm=ease(p) if k==4 else 1-ease(p) if k==5 else 0
    left_end=398+54*warm
    right_start=482
    deck_color=(round(101+84*warm),round(148-18*warm),round(182-75*warm))
    for x0,x1,color in ((73,left_end,deck_color),(right_start,647,'#6b7692')):
        d.rounded_rectangle((x0,661,x1,745),radius=8,fill=color,outline=PAPER,width=4)
        d.line((x0+14,691,x1-14,691),fill=GOLD,width=3)
    for x in (100,329,564):
        d.rectangle((x,778,x+49,896),fill='#4c617c',outline=MUTE,width=3)
        d.rectangle((x-4,749,x+53,777),fill=INK,outline=MUTE,width=3)
    for j in range(3):
        disk(d,338+j*16,763,5,CYAN)
    txt(d,(125,921),'Fixed end',23)
    txt(d,(354,921),'Sliding bearing',23)
    txt(d,(588,921),'Fixed reference',23)
    if k in (1,2,3,4,5):
        gap_center=(left_end+right_start)/2
        d.line((left_end,616,right_start,616),fill=CYAN,width=5)
        for boundary in (left_end,right_start):
            d.line((boundary,602,boundary,635),fill=CYAN,width=3)
        d.line((gap_center,583,gap_center,607),fill=CYAN,width=3)
        txt(d,(gap_center,556),'Expansion gap',24,CYAN)
    if k==2:
        d.line((76,510,left_end,510),fill=MUTE,width=3)
        for boundary in (76,left_end):
            d.line((boundary,496,boundary,523),fill=MUTE,width=3)
        txt(d,(238,474),'Length of this span',23)
    if k in (4,5):
        txt(d,(360,966),'Movement exaggerated',24,CYAN)
        if k==4:
            arrow(d,(left_end-83,647),(left_end-12,647),ORANGE,5)
        else:
            arrow(d,(left_end-8,647),(left_end-79,647),CYAN,5)
    if k==6:
        d.rounded_rectangle((157,489,563,586),radius=16,fill=INK,outline=MUTE,width=3)
        arrow(d,(190,530),(315,530),ORANGE,6)
        arrow(d,(530,530),(405,530),ORANGE,6)
        txt(d,(360,559),'Restrained span: stress',22)


def string(d,k,p):
    x0,x1=148,572
    d.rounded_rectangle((75,466,645,891),radius=47,fill='#875846',outline=PAPER,width=5)
    comparison = k in (1,3,4,5,6)
    y_positions = (587,753) if comparison else (676,)
    for i,y in enumerate(y_positions):
        disk(d,360,y,48,INK,ORANGE,4)
        for x in (x0,x1):
            d.rounded_rectangle((x-13,y-47,x+13,y+47),radius=7,fill='#ded0b7')
        cycles=(3 if i else 2) if comparison else 2.6
        amplitude=34 if k in (1,2,3) else 34*math.cos(p*math.tau*cycles)
        points=[(x,y+amplitude*math.sin(math.pi*(x-x0)/(x1-x0))) for x in range(x0,x1+1,4)]
        d.line(points,fill=GOLD if i else CYAN,width=5)
        if comparison:
            txt(d,(360,y-68),'HIGHER TENSION' if i else 'LOWER TENSION',22,GOLD if i else CYAN)
        if k in (2,3):
            # Each straight segment pulls along its own length. Horizontal components cancel.
            length=(116 if i else 80)
            d.line((x0,y,360,y+34,x1,y),fill=PAPER,width=2)
            arrow(d,(360,y+34),(360-length,y+34-length*34/212),GOLD,5)
            arrow(d,(360,y+34),(360+length,y+34-length*34/212),GOLD,5)
            arrow(d,(360,y+34),(360,y+34-2*length*34/212),CYAN,6)
            if k==2:
                txt(d,(360,788),'NET PULL TOWARD STRAIGHT',22,CYAN)
    if k in (4,5,6):
        d.rounded_rectangle((149,931,572,940),radius=4,fill='#576884')
        d.rounded_rectangle((149,931,149+423*p,940),radius=4,fill=PAPER)
        txt(d,(360,984),'SAME ELAPSED TIME · SLOWED DOWN',19,MUTE)
    else:
        txt(d,(360,930),'SAME TWO SUPPORTS',21,MUTE)


def swing(d,k,p):
    pivot=(360,437)
    d.rectangle((137,396,586,439),fill='#8297b3',outline=PAPER,width=4)
    for x in (137,580): d.line((x,436,x,910),fill='#6a849e',width=13)
    phase=p*math.tau*(2 if k in (0,4,5,6,7) else 1)-(0 if k==1 else math.pi/2)
    amplitude = (.28+.29*ease(p)) if k in (0,4,5,7) else (.55-.2*ease(p)) if k==6 else .38
    a=amplitude*math.sin(phase)
    end=(pivot[0]+334*math.sin(a),pivot[1]+334*math.cos(a))
    d.line((*pivot,*end),fill=PAPER,width=5)
    d.rounded_rectangle((end[0]-50,end[1]-16,end[0]+50,end[1]+16),radius=12,fill=ORANGE,outline=GOLD,width=4)
    d.arc((193,590,527,784),24,156,fill=MUTE,width=3)
    if k in (0,2,3,4,5,7) and abs(a)<.18 and math.cos(phase)>0:
        arrow(d,(end[0]-111,end[1]+43),(end[0]-6,end[1]+43),CYAN,7)
        txt(d,(360,937),'PUSH WITH MOTION',24,CYAN)
    elif k==6:
        d.rounded_rectangle((184,926,536,941),radius=6,fill='#586889')
        d.rounded_rectangle((184,926,184+352*(amplitude/.55)**2,941),radius=6,fill=ORANGE)
        txt(d,(360,967),'SWING ENERGY REMAINING',20,ORANGE)
        txt(d,(360,1002),'LOSS TO DRAG & FRICTION',17,MUTE)
    elif k in (2,3):
        txt(d,(360,937),'COAST BETWEEN PUSHES',21,MUTE)


def brake(d,k,p):
    d.line((55,888,666,888),fill=MUTE,width=5)
    for x in (180,548):
        disk(d,x,831,58,INK,CYAN,6)
    d.rounded_rectangle((82,669,634,800),radius=32,fill='#296778',outline=CYAN,width=5)
    d.polygon([(185,669),(254,525),(461,525),(548,669)],fill='#244363',outline=CYAN,width=5)
    d.line((331,674,309,600,265,600),fill=PAPER,width=12)
    lean=.48*ease(p) if k in (0,2,4) else 0 if k==1 else .48
    hx,hy=358+93*math.sin(lean),625-77*math.cos(lean)
    d.line((353,703,353,632,hx,hy+23),fill=ORANGE,width=22)
    disk(d,hx,hy,23,GOLD,PAPER,4)
    d.line((300,580,hx+9,hy+51,380,702),fill=PAPER,width=6)
    if k in (1,2,3,4,5):
        body_speed=120-(75*ease(p) if k==5 else 0)
        car_speed=120 if k==1 else 120-75*ease(p) if k==2 else 45
        arrow(d,(hx+31,hy-46),(hx+31+body_speed,hy-46),CYAN,6)
        arrow(d,(416,926),(416+car_speed,926),CYAN,6)
        txt(d,(265,925),'CAR SPEED',19,MUTE,'lm')
        txt(d,(261,hy-46),'RIDER',19,MUTE)
    if k in (5,7):
        arrow(d,(hx+8,hy+48),(hx-99,hy+48),GOLD,6)
        txt(d,(360,998),'BELT FORCE',21,GOLD)
    if k in (0,6):
        txt(d,(360,950),'CAR INTERIOR CUTAWAY',19,MUTE)
    if k==4:
        txt(d,(360,997),'RELATIVE TO THE CAR',19,MUTE)


def wetting_channel(d, center, width, surface):
    """Draw a concave wetting meniscus, with a connected reservoir underneath."""
    left,right=center-width/2,center+width/2
    meniscus=[(left+i,surface+17*(1-(2*i/width-1)**2)) for i in range(round(width)+1)]
    d.polygon([*meniscus,(right,865),(left,865)],fill=BLUE)
    d.line(meniscus,fill=CYAN,width=4)
    for edge in (left,right):
        d.line((edge,505,edge,854),fill=PAPER,width=5)


def towel(d,k,p):
    if k in (2,5,6):
        d.rounded_rectangle((83,794,637,889),radius=21,fill=BLUE,outline=CYAN,width=5)
        if k==2:
            y=682-84*ease(p)
            wetting_channel(d,360,224,y)
            for x in (265,455):
                arrow(d,(x,y+4),(x,y-65),GOLD,5)
            txt(d,(360,933),'WETTING MENISCUS · MODEL',20,MUTE)
        elif k==5:
            for x,width,pull,weight,label in ((202,82,49,34,'NARROWER'),(523,150,90,114,'WIDER')):
                wetting_channel(d,x,width,616)
                arrow(d,(x-15,709),(x-15,709-pull),GOLD,5)
                arrow(d,(x+15,709),(x+15,709+weight),CYAN,5)
                txt(d,(x,925),label,21)
            txt(d,(360,974),'SAME WETTING & HEIGHT',20,MUTE)
            txt(d,(360,1012),'UP: CAPILLARY PULL  ·  DOWN: WATER WEIGHT',16,PAPER)
        else:
            wetting_channel(d,360,151,616)
            arrow(d,(334,708),(334,636),GOLD,5)
            arrow(d,(387,708),(387,780),CYAN,5)
            txt(d,(360,934),'BALANCE AT A FINITE HEIGHT',20,MUTE)
        return
    if k in (1,3,4):
        d.rounded_rectangle((85,441,635,916),radius=40,fill='#29475d',outline=MUTE,width=4)
        liquid_top=(720-149*ease(p)) if k==4 else 653
        if k in (3,4):
            d.rounded_rectangle((308,liquid_top,423,879),radius=22,fill=BLUE,outline=CYAN,width=3)
        for x in (274,445):
            d.line((x-25,487,x-10,626,x+1,746,x-19,870),fill='#dcb790',width=19)
            d.line((x+25,487,x+13,640,x+8,746,x+22,870),fill='#dcb790',width=14)
        if k in (3,4):
            separation=(855-liquid_top-15)/7
            for j in range(8):
                disk(d,330+(j%3)*31,855-j*separation,10,CYAN,PAPER,2)
        if k==3:
            arrow(d,(325,722),(355,722),GOLD,4)
            arrow(d,(400,722),(371,722),GOLD,4)
        if k==4: arrow(d,(511,810),(511,560),CYAN,6)
        txt(d,(359,957),'FIBERS & WATER · MAGNIFIED MODEL',19,MUTE)
        return
    d.rounded_rectangle((131,730,590,921),radius=27,fill=BLUE,outline=CYAN,width=5)
    top=448
    hi=718-208*(ease(p) if k in (0,5) else 1)
    d.rounded_rectangle((247,top,473,876),radius=18,fill='#e9d8b9',outline=PAPER,width=4)
    d.rounded_rectangle((248,max(top+15,hi),472,875),radius=12,fill='#63bacd')
    jitter=random.Random(41)
    for _ in range(63):
        x=jitter.randrange(254,463); y=jitter.randrange(top+9,869)
        d.line((x,y,min(469,x+jitter.randrange(12,35)),min(872,y+jitter.randrange(3,18))),fill='#b7a788' if y<hi else '#397f9f',width=2)
    if k in (0,5): arrow(d,(563,780),(563,570),GOLD,5)


SCENES = {'04':straw, '05':coin, '06':metal, '07':bubble, '08':compass, '09':paper,
          '10':balloon, '11':condensation, '12':wrench, '13':evaporation, '14':suction,
          '15':friction, '16':bridge, '17':string, '18':swing, '19':brake, '20':towel}


@lru_cache(maxsize=100)
def illustration(episode_id, step):
    path = ART / episode_id / 'opening-art.png'
    if not path.exists():
        return None
    size = 606
    with Image.open(path) as asset:
        im = ImageOps.fit(asset.convert('RGB'), (size+step,size+step), Image.Resampling.LANCZOS)
    return im.crop((step//2,step//2,step//2+size,step//2+size))


def frame(episode, index, progress):
    num = int(episode['id'])
    cue = episode['cues'][index]
    im = background(num, index in (0,len(episode['cues'])-1)).copy()
    d=ImageDraw.Draw(im)
    txt(d,(58,86),'WHYNEST LAB',21,CYAN,'lm')
    d.line((61,124,656,124),fill='#7390a7',width=2)
    headline = cue.get('overlay_en') or episode['title_en']
    label = (' / '.join(headline) if isinstance(headline,list) else headline).replace('→','to')
    for heading_size in (46,42,38,34):
        lines=split_text(label,heading_size,556)
        if len(lines) <= 3:
            break
    if len(lines)>3: raise ValueError(f"{episode['id']} cue {index}: overlay exceeds mobile bounds")
    for j,line in enumerate(lines): txt(d,(58,192+j*(heading_size+8)),line,heading_size,PAPER,'lm',True)
    art = illustration(episode['id'], round(12*ease(progress))) if index==0 and progress<.42 else None
    if art:
        im.paste(art,(57,375))
    else:
        diagram_progress = ((progress-.42)/.58 if index==0 and illustration(episode['id'],0) is not None
                            else progress)
        SCENES[episode['id']](d,index,diagram_progress)
    txt(d,(61,1072),'ILLUSTRATED MODEL',17,MUTE,'lm')
    d.line((61,1108,657,1108),fill='#7890a1',width=2)
    for j in range(len(episode['cues'])):
        x=61+j*33
        d.rounded_rectangle((x,1134,x+23,1139),radius=2,fill=CYAN if j==index else '#46617a')
    return im
