# -*- coding: utf-8 -*-
"""第77回 別冊抽出。No→ページは ink計測(内容頁)＋OCRアンカー＋連番で確定。
  午前(a_02 20p): No.1-5=p5-9, No.6=p10+p11(6A/6B別頁→連結), No.7-11=p12-16
  午後(b_02 20p): No.1-2=p5-6, [p7白紙], No.3=p8+p9(3A/3B別頁→連結), No.4-10=p10-16
回転対象は無し(ink解析で wide頁なし)。出力: eam/noNN.png, epm/noNN.png(長辺900px)。
複数ページのNoは横に連結して1枚にする。"""
from PIL import Image, ImageChops
import os, sys

AM_MAP = {1:[5],2:[6],3:[7],4:[8],5:[9],6:[10,11],7:[12],8:[13],9:[14],10:[15],11:[16]}
PM_MAP = {1:[5],2:[6],3:[8,9],4:[10],5:[11],6:[12],7:[13],8:[14],9:[15],10:[16]}
ROT = {'eam': set(), 'epm': set()}

def autotrim(im, pad=8):
    g = im.convert('L'); bg = Image.new('L', g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda p: 255 if p > 12 else 0)
    bbox = diff.getbbox()
    if not bbox: return im
    l,t,r,b = bbox
    l=max(0,l-pad); t=max(0,t-pad); r=min(im.size[0],r+pad); b=min(im.size[1],b+pad)
    return im.crop((l,t,r,b))

def load_trim(srcdir, page, rotated):
    im = Image.open('%s/p-%02d.png' % (srcdir, page)).convert('RGB')
    if rotated:
        im = im.transpose(Image.ROTATE_270)
    w,h = im.size
    crop = im.crop((int(w*0.05), int(h*0.07), int(w*0.95), int(h*0.95)))
    return autotrim(crop)

def hcat(ims, gap=12):
    H = max(i.size[1] for i in ims)
    W = sum(i.size[0] for i in ims) + gap*(len(ims)-1)
    out = Image.new('RGB', (W, H), (255,255,255)); x=0
    for i in ims:
        out.paste(i, (x, (H-i.size[1])//2)); x += i.size[0]+gap
    return out

def process(srcdir, pmap, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no, pages in sorted(pmap.items()):
        rotated = no in ROT.get(os.path.basename(outdir), set())
        tiles = [load_trim(srcdir, p, rotated) for p in pages]
        im = tiles[0] if len(tiles)==1 else hcat(tiles)
        W,H = im.size; ls = max(W,H)
        if ls > 900:
            im = im.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
        im.save('%s/no%02d.png' % (outdir, no))
    print(outdir, 'done', len(pmap), 'images')

if __name__ == '__main__':
    TMP = sys.argv[1] if len(sys.argv) > 1 else '/tmp/k77'
    process(os.path.join(TMP,'bam'), AM_MAP, os.path.join(TMP,'eam'))
    process(os.path.join(TMP,'bpm'), PM_MAP, os.path.join(TMP,'epm'))
