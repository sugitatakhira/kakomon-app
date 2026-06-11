# -*- coding: utf-8 -*-
"""コアテスト章→問題ID対応を coretests.json に出力（IDの存在検証つき）。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _load import load_all
from map_byori import BYORI
from map_bisei import BISEI
from map_seiri import SEIRI
qids = {q['id'] for q in load_all()}

BYORI_LABELS={1:"基礎",2:"固定・脱灰",3:"包埋・薄切・凍結",4:"染色①",5:"染色②",6:"免疫染色",7:"電子顕微鏡",8:"細胞診"}
BISEI_LABELS={1:"基礎",2:"染色・培地",3:"滅菌・消毒・抗菌薬",4:"同定①",5:"同定②",6:"ビブリオ・マイコ",7:"偏性嫌気性菌",8:"真菌・ウイルス"}
SEIRI_LABELS={1:"心電図 基礎",2:"心電図 異常波形",3:"心電図 ホルター・運動負荷",4:"呼吸器①",5:"呼吸器②",6:"超音波 基礎",7:"超音波 心臓",8:"超音波 腹部",9:"脳波 基礎",10:"脳波 臨床",11:"筋電図 基礎・針筋電図",12:"筋電図 神経伝導・反復刺激"}

out=[]; missing=[]
def add(book, M, labels):
    for ch in sorted(M):
        ids=[]
        for qid in M[ch]:
            if qid in qids: ids.append(qid)
            else: missing.append(qid)
        # 重複除去
        seen=set(); ids=[x for x in ids if not(x in seen or seen.add(x))]
        out.append({"book":book,"ch":ch,"label":"%s%d章 %s"%(book,ch,labels[ch]),"count":len(ids),"ids":ids})
add("生理学", SEIRI, SEIRI_LABELS)
add("病理学", BYORI, BYORI_LABELS)
add("微生物学", BISEI, BISEI_LABELS)

if missing:
    print("!! 存在しないID:", missing, file=sys.stderr)
json.dump(out, open(os.path.join(os.path.dirname(__file__),'coretests.json'),'w',encoding='utf-8'), ensure_ascii=False)
print("章数:", len(out), " 総ひも付け:", sum(o['count'] for o in out))
for o in out: print("  %-22s %d問"%(o['label'], o['count']))
