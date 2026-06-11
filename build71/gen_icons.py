# -*- coding: utf-8 -*-
"""PWAアプリアイコン生成 → docs/icon-*.png。ティール地にしろくま博士(検査技術ゼミナール)。"""
import os
from PIL import Image, ImageDraw
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,'..'); DOCS=os.path.join(ROOT,'docs')
os.makedirs(DOCS,exist_ok=True)
TEAL=(14,116,144)
BEAR=os.path.join(ROOT,'assets','icon_bear.png')   # 博士(micro笑み, 400px)
HEAD_BOX=(55,18,350,330)                            # 頭+襟を切り出す範囲(400px基準)

def rounded_mask(size,r):
    m=Image.new('L',(size,size),0); ImageDraw.Draw(m).rounded_rectangle([0,0,size-1,size-1],radius=r,fill=255); return m

def make(size, frac, rounded, out):
    base=Image.new('RGBA',(size,size),TEAL+(255,))
    head=Image.open(BEAR).convert('RGBA').crop(HEAD_BOX)
    w=int(size*frac); h=int(head.size[1]*w/head.size[0]); head=head.resize((w,h),Image.LANCZOS)
    base.alpha_composite(head,((size-w)//2,(size-h)//2))
    if rounded:
        out_img=Image.new('RGBA',(size,size),(0,0,0,0)); out_img.paste(base,(0,0),rounded_mask(size,int(size*0.22)))
    else:
        out_img=base
    out_img.convert('RGB').save(out)

make(192,0.86,True ,os.path.join(DOCS,'icon-192.png'))
make(512,0.86,True ,os.path.join(DOCS,'icon-512.png'))
make(512,0.66,False,os.path.join(DOCS,'icon-512-maskable.png'))  # マスク用は中央安全域に
make(180,0.84,False,os.path.join(DOCS,'icon-180.png'))           # apple(iOS側で角丸マスク)
print('icons -> docs/ (しろくま博士)')
