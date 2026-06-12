# -*- coding: utf-8 -*-
"""ホウゼミ過去問道場 アイコン生成 → docs/houzemi-dojo/icon-*.png。
インディゴ地に白文字「ホウゼミ／道場」(ケンゼミ道場=ティールと別系統)。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..')
DOCS=os.path.join(ROOT,'docs','houzemi-dojo'); os.makedirs(DOCS,exist_ok=True)
FONT='/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'
TOP=(79,70,229); BOT=(30,27,75); AMBER=(251,191,36)

def vgrad(size, top, bot):
    base=Image.new('RGB',(size,size),top); top_=Image.new('RGB',(size,size),bot)
    mask=Image.new('L',(1,size))
    for y in range(size): mask.putpixel((0,y), int(255*(y/(size-1))**1.15))
    return Image.composite(top_, base, mask.resize((size,size))).convert('RGBA')
def rounded_mask(size,r):
    m=Image.new('L',(size,size),0); ImageDraw.Draw(m).rounded_rectangle([0,0,size-1,size-1],radius=r,fill=255); return m
def ctext(draw, cx, y, s, font, fill, sw=0, sf=None):
    l,t,r,b=draw.textbbox((0,0),s,font=font,stroke_width=sw)
    draw.text((cx-(r+l)/2, y-t), s, font=font, fill=fill, stroke_width=sw, stroke_fill=sf or fill); return b-t

def make(size, scale, rounded, out):
    img=vgrad(size,TOP,BOT); d=ImageDraw.Draw(img); cx=size//2; u=size*scale
    f_top=ImageFont.truetype(FONT,int(u*0.155)); f_big=ImageFont.truetype(FONT,int(u*0.40))
    block_top=size*(0.5 - scale*0.40)
    h1=ctext(d, cx, block_top, 'ホ ウ ゼ ミ', f_top, (199,205,253,255))
    y2=block_top+h1+u*0.085
    sh=Image.new('RGBA',img.size,(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ctext(ds, cx+max(1,int(size*0.006)), y2+max(1,int(size*0.006)), '道場', f_big, (20,18,60,150))
    sh=sh.filter(ImageFilter.GaussianBlur(max(1,int(size*0.008)))); img.alpha_composite(sh); d=ImageDraw.Draw(img)
    h2=ctext(d, cx, y2, '道場', f_big, (255,255,255,255), sw=max(1,int(u*0.006)), sf=(255,255,255,255))
    lw=u*0.34; ly=y2+h2+u*0.07
    d.rounded_rectangle([cx-lw/2, ly, cx+lw/2, ly+max(2,int(u*0.024))], radius=int(u*0.012), fill=AMBER+(255,))
    out_img=Image.new('RGBA',(size,size),(0,0,0,0)); out_img.paste(img,(0,0),rounded_mask(size,int(size*0.22))) if rounded else None
    (out_img if rounded else img).convert('RGB').save(out)

make(192,0.86,True ,os.path.join(DOCS,'icon-192.png'))
make(512,0.86,True ,os.path.join(DOCS,'icon-512.png'))
make(512,0.62,False,os.path.join(DOCS,'icon-512-maskable.png'))
make(180,0.86,False,os.path.join(DOCS,'icon-180.png'))
print('icons -> docs/houzemi-dojo/ (文字ロゴ ホウゼミ/道場)')
