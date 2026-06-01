from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random

OUT = Path('assets')
OUT.mkdir(exist_ok=True)
W = H = 1080
paper = (246,242,233)
paper2 = (252,250,244)
ink = (18,22,16)
forest = (14,27,20)
forest2 = (19,37,27)
mint = (24,201,140)
mint_deep = (12,122,86)
clay = (238,101,57)
muted = (94,99,87)

font_paths = [
    '/System/Library/Fonts/Supplemental/Georgia.ttf',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/System/Library/Fonts/SFNS.ttf',
]

def font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates += ['/System/Library/Fonts/Supplemental/Georgia.ttf']
    if bold:
        candidates += ['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/System/Library/Fonts/Helvetica.ttc']
    candidates += ['/System/Library/Fonts/Supplemental/Arial.ttf','/System/Library/Fonts/Helvetica.ttc']
    for p in candidates:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text_wrap(draw, txt, fnt, maxw):
    words=txt.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= maxw or not cur:
            cur=test
        else:
            lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def grain(img, amount=18):
    random.seed(7)
    px=Image.new('L', img.size)
    data=bytearray(random.randrange(256) for _ in range(img.size[0]*img.size[1]))
    px.putdata(data)
    noise=Image.merge('RGBA',[px,px,px,Image.new('L', img.size, amount)])
    return Image.alpha_composite(img.convert('RGBA'), noise).convert('RGB')

def add_brand(d):
    d.rounded_rectangle((70,70,330,122), 26, fill=forest)
    d.text((104,90), 'Aestheria Studio', font=font(26,bold=True), fill=paper)
    d.ellipse((82,91,100,109), fill=mint)

def title(d, text, y, fill=ink):
    f=font(78, serif=True)
    lines=text_wrap(d,text,f,840)
    for line in lines:
        d.text((74,y), line, font=f, fill=fill)
        y+=88
    return y

def save(img,name):
    img=grain(img)
    img.save(OUT/name, quality=94)
    print(OUT/name)

def card1():
    img=Image.new('RGB',(W,H),paper); d=ImageDraw.Draw(img)
    # soft blobs
    for cx,cy,c,r in [(900,120,mint,260),(950,950,clay,320),(-80,740,mint_deep,280)]:
        layer=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(layer)
        ld.ellipse((cx-r,cy-r,cx+r,cy+r), fill=(*c,80))
        layer=layer.filter(ImageFilter.GaussianBlur(60)); img.paste(Image.alpha_composite(img.convert('RGBA'),layer).convert('RGB'))
    d=ImageDraw.Draw(img); add_brand(d)
    d.text((74,176),'CAROUSEL / WEBSITE AUDIT',font=font(24,bold=True),fill=mint_deep)
    y=title(d,'5 website fixes that bring more enquiries',230)
    # UI cards
    rounded(d,(78,650,1002,964),34,paper2,outline=(225,218,205),width=3)
    for i,(label,accent) in enumerate([('Clear offer',mint),('Fast CTA',clay),('Trust proof',mint_deep)]):
        x=122+i*292
        rounded(d,(x,710,x+238,884),28,(255,255,255),outline=(226,219,205),width=2)
        d.ellipse((x+28,744,x+66,782),fill=accent)
        d.text((x+28,804),label,font=font(31,bold=True),fill=ink)
        d.line((x+28,845,x+180,845),fill=(215,210,198),width=8)
    d.text((78,1000),'A practical audit-style carousel for small business owners',font=font(27),fill=muted)
    save(img,'social-website-fixes.jpg')

def card2():
    img=Image.new('RGB',(W,H),forest); d=ImageDraw.Draw(img)
    for i in range(0,W,54): d.line((i,0,i+240,H),fill=(22,45,33),width=2)
    add_brand(d)
    d.text((74,176),'LAUNCH SYSTEM',font=font(24,bold=True),fill=mint)
    y=title(d,'Small business launch checklist',230,fill=paper)
    items=['1-page website','WhatsApp CTA','Google listing','10 social posts','Offer graphic','Follow-up message']
    x0,y0=88,600
    for i,it in enumerate(items):
        x=x0+(i%2)*462; y=y0+(i//2)*124
        rounded(d,(x,y,x+410,y+88),24,(252,250,244),outline=None)
        d.rounded_rectangle((x+28,y+28,x+60,y+60),8,outline=mint,width=4)
        d.line((x+34,y+44,x+45,y+55),fill=mint,width=5)
        d.line((x+45,y+55,x+60,y+34),fill=mint,width=5)
        d.text((x+82,y+29),it,font=font(30,bold=True),fill=ink)
    d.text((76,1000),'A reusable checklist carousel template for founders and local brands',font=font(27),fill=(190,205,195))
    save(img,'social-launch-checklist.jpg')

def card3():
    img=Image.new('RGB',(W,H),paper2); d=ImageDraw.Draw(img)
    add_brand(d)
    d.text((74,176),'CONCEPT PACK',font=font(24,bold=True),fill=clay)
    y=title(d,'Cafe promo pack — concept',230)
    # latte cup
    d.ellipse((155,650,425,920),fill=(218,156,94),outline=forest,width=6)
    d.ellipse((190,685,390,885),fill=(246,219,174))
    d.arc((215,715,365,865),15,345,fill=(146,86,45),width=12)
    d.arc((262,760,338,836),15,345,fill=(146,86,45),width=8)
    # post stack
    for off,c in [(0,forest2),(34,mint),(68,clay)]:
        rounded(d,(565+off,610-off,900+off,910-off),32,c,outline=forest,width=4)
    rounded(d,(604,585,944,885),34,paper,outline=forest,width=5)
    d.text((638,632),'2 FOR 1',font=font(56,bold=True),fill=clay)
    d.text((638,705),'LATTE DAY',font=font(46,bold=True),fill=forest)
    d.line((638,775,870,775),fill=mint,width=10)
    d.text((638,810),'Story + post set',font=font(28),fill=muted)
    d.text((76,1000),'Clearly labeled concept artwork — useful for showing social design direction',font=font(27),fill=muted)
    save(img,'social-cafe-concept.jpg')

card1(); card2(); card3()
