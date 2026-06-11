# -*- coding: utf-8 -*-
"""第78回 別冊抽出。No→ページの対応は ink 計測で白紙頁を除いた内容頁順に確定:
  午前(a_02 24p): No.1-5=p5-9, [p10白紙], No.6=p11, No.7=p12, [p13白紙], No.8-12=p14-18
  午後(b_02 16p): No.1-8=p5-12 (白紙シフト無し, page=No+4)
回転(ROTATE_270)対象は無し(全頁ポートレート, bbox aspect<1)。
出力: eam/noNN.png, epm/noNN.png (長辺900px)。build78.py が読む。
"""
from PIL import Image, ImageChops
import os, sys

AM_MAP = {1:5,2:6,3:7,4:8,5:9, 6:11, 7:12, 8:14,9:15,10:16,11:17,12:18}
PM_MAP = {n:n+4 for n in range(1,9)}
ROT = {'eam': set(), 'epm': set()}

def autotrim(im, pad=8):
    g = im.convert('L'); bg = Image.new('L', g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda p: 255 if p > 12 else 0)
    bbox = diff.getbbox()
    if not bbox: return im
    l,t,r,b = bbox
    l=max(0,l-pad); t=max(0,t-pad); r=min(im.size[0],r+pad); b=min(im.size[1],b+pad)
    return im.crop((l,t,r,b))

def process(srcdir, pmap, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no, page in sorted(pmap.items()):
        im = Image.open('%s/p-%02d.png' % (srcdir, page)).convert('RGB')
        rotated = no in ROT.get(outdir, set())
        if rotated:
            im = im.transpose(Image.ROTATE_270)
        w,h = im.size
        # トンボ/フッタを除く内側をcrop → autotrimで余白除去
        crop = im.crop((int(w*0.05), int(h*0.07), int(w*0.95), int(h*0.95)))
        crop = autotrim(crop)
        W,H = crop.size; ls = max(W,H)
        if ls > 900:
            crop = crop.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
        crop.save('%s/no%02d.png' % (outdir, no))
    print(outdir, 'done', len(pmap), 'images')

if __name__ == '__main__':
    TMP = sys.argv[1] if len(sys.argv) > 1 else '/tmp/k78'
    process(os.path.join(TMP,'bam150'), AM_MAP, os.path.join(TMP,'eam'))
    process(os.path.join(TMP,'bpm150'), PM_MAP, os.path.join(TMP,'epm'))
