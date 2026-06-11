# -*- coding: utf-8 -*-
"""PWAアプリアイコン生成 → docs/icon-*.png。文字ロゴ「ケンゼミ／過去問／DB」。
ティール系グラデーション地に白文字。マスカブルは中央安全域に収める。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..'); DOCS=os.path.join(ROOT,'docs')
os.makedirs(DOCS,exist_ok=True)
FONT='/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'
TOP=(13,148,136)      # teal-600
BOT=(8,47,73)         # slate-900 寄りの濃紺
AMBER=(251,191,36)    # アクセント

def vgrad(size, top, bot):
    base=Image.new('RGB',(size,size),top)
    top_=Image.new('RGB',(size,size),bot)
    mask=Image.new('L',(1,size))
    for y in range(size):
        mask.putpixel((0,y), int(255*(y/(size-1))**1.15))
    base=Image.composite(top_, base, mask.resize((size,size)))
    return base.convert('RGBA')

def rounded_mask(size,r):
    m=Image.new('L',(size,size),0); ImageDraw.Draw(m).rounded_rectangle([0,0,size-1,size-1],radius=r,fill=255); return m

def ctext(draw, cx, y, s, font, fill, sw=0, sf=None):
    l,t,r,b=draw.textbbox((0,0),s,font=font,stroke_width=sw)
    draw.text((cx-(r+l)/2, y-t), s, font=font, fill=fill, stroke_width=sw, stroke_fill=sf or fill)
    return b-t

def make(size, scale, rounded, out):
    img=vgrad(size,TOP,BOT)
    d=ImageDraw.Draw(img)
    cx=size//2
    # 安全域 scale（マスカブルは小さめ）。3段組み: ケンゼミ / 過去問 / DB
    u=size*scale
    f_top=ImageFont.truetype(FONT, int(u*0.150))
    f_big=ImageFont.truetype(FONT, int(u*0.340))
    f_db =ImageFont.truetype(FONT, int(u*0.150))
    block_top = size*(0.5 - scale*0.42)
    # 上段「ケンゼミ」(字間ひろめ)
    spaced='ケ ン ゼ ミ'
    h1=ctext(d, cx, block_top, spaced, f_top, (199,236,234,255))
    # 中段「過去問」(大・白・わずかに影)
    y2=block_top+h1+u*0.075
    sh=Image.new('RGBA',img.size,(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ctext(ds, cx+max(1,int(size*0.006)), y2+max(1,int(size*0.006)), '過去問', f_big, (0,40,55,150))
    sh=sh.filter(ImageFilter.GaussianBlur(max(1,int(size*0.008)))); img.alpha_composite(sh)
    d=ImageDraw.Draw(img)
    h2=ctext(d, cx, y2, '過去問', f_big, (255,255,255,255), sw=max(1,int(u*0.006)), sf=(255,255,255,255))
    # アクセント下線
    lw=u*0.30; ly=y2+h2+u*0.055
    d.rounded_rectangle([cx-lw/2, ly, cx+lw/2, ly+max(2,int(u*0.022))], radius=int(u*0.012), fill=AMBER+(255,))
    # 下段「DB」(アンバー)
    y3=ly+u*0.075
    ctext(d, cx, y3, 'D B', f_db, AMBER+(255,))
    if rounded:
        out_img=Image.new('RGBA',(size,size),(0,0,0,0)); out_img.paste(img,(0,0),rounded_mask(size,int(size*0.22)))
    else:
        out_img=img
    out_img.convert('RGB').save(out)

make(192,0.86,True ,os.path.join(DOCS,'icon-192.png'))
make(512,0.86,True ,os.path.join(DOCS,'icon-512.png'))
make(512,0.62,False,os.path.join(DOCS,'icon-512-maskable.png'))
make(180,0.86,False,os.path.join(DOCS,'icon-180.png'))
print('icons -> docs/ (文字ロゴ ケンゼミ/過去問/DB)')
