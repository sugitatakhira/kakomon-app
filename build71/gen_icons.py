# -*- coding: utf-8 -*-
"""PWAアプリアイコン生成 → docs/icon-*.png。ティール地に白「過去問」。"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(__file__); DOCS=os.path.join(HERE,'..','docs'); os.makedirs(DOCS,exist_ok=True)
FONT='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
TEAL=(14,116,144); WHITE=(255,255,255); TEXT='過去問'

def rounded_mask(size, radius):
    m=Image.new('L',(size,size),0); ImageDraw.Draw(m).rounded_rectangle([0,0,size-1,size-1],radius=radius,fill=255); return m

def make(size, maskable=False, rounded=True, out=None):
    img=Image.new('RGB',(size,size),TEAL); d=ImageDraw.Draw(img)
    target_w=size*(0.62 if maskable else 0.80)   # maskableは中央安全域に収める
    fs=int(size*0.34); f=ImageFont.truetype(FONT,fs)
    bb=d.textbbox((0,0),TEXT,font=f); fs=int(fs*target_w/(bb[2]-bb[0])); f=ImageFont.truetype(FONT,fs)
    bb=d.textbbox((0,0),TEXT,font=f); tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((size-tw)//2-bb[0],(size-th)//2-bb[1]),TEXT,font=f,fill=WHITE)
    if rounded and not maskable:
        bg=Image.new('RGB',(size,size),(245,245,244)); bg.paste(img,(0,0),rounded_mask(size,int(size*0.18))); img=bg
    img.save(out)

make(192,out=os.path.join(DOCS,'icon-192.png'))
make(512,out=os.path.join(DOCS,'icon-512.png'))
make(512,maskable=True,out=os.path.join(DOCS,'icon-512-maskable.png'))
make(180,rounded=False,out=os.path.join(DOCS,'icon-180.png'))   # apple-touch-icon(iOS側でマスクされる)
print('icons -> docs/')
