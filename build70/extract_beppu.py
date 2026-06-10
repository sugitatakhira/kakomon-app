# -*- coding: utf-8 -*-
from PIL import Image, ImageChops, ImageDraw
import os
ROT = {'eam':{2}, 'epm':{3,5,14}}
def autotrim(im, pad=8):
    g = im.convert('L'); bg = Image.new('L', g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda p: 255 if p > 12 else 0)
    bbox = diff.getbbox()
    if not bbox: return im
    l,t,r,b = bbox
    l=max(0,l-pad); t=max(0,t-pad); r=min(im.size[0],r+pad); b=min(im.size[1],b+pad)
    return im.crop((l,t,r,b))
def process(srcdir, maxno, outdir):
    os.makedirs(outdir, exist_ok=True)
    for no in range(1, maxno+1):
        page = no + 4
        im = Image.open('%s/p-%02d.png'%(srcdir,page)).convert('RGB')
        rotated = no in ROT.get(outdir,set())
        if rotated:
            im = im.transpose(Image.ROTATE_270)
        w,h = im.size
        if rotated:
            crop = im.crop((int(w*0.09), int(h*0.11), int(w*0.985), int(h*0.97)))
        else:
            crop = im.crop((int(w*0.05), int(h*0.11), int(w*0.95), int(h*0.93)))
        crop = autotrim(crop)
        W,H = crop.size; ls=max(W,H)
        if ls>900:
            crop = crop.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
        crop.save('%s/no%02d.png'%(outdir,no))
    print(outdir,'done',maxno,'images')
process('bam',15,'eam')
process('bpm',16,'epm')
