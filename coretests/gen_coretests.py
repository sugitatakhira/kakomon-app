# -*- coding: utf-8 -*-
"""コアテスト章（またはトピック）→問題ID対応を coretests.json に出力（IDの存在検証つき）。
btn = フィルタのボタン表示名。chapter=True の本は「N章 名前」、False（臨床化学）はトピック名のみ。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _load import load_all
from map_byori import BYORI
from map_bisei import BISEI
from map_seiri import SEIRI
from map_ketsueki import KETSUEKI
from map_kagaku import KAGAKU
from map_meneki import MENEKI
qids = {q['id'] for q in load_all()}
MENEKI_LABELS={1:"免疫総論(自然・獲得・MHC)",2:"基礎(細胞・サイトカイン・Ig)",3:"検査(測定法・自己抗体・梅毒)",4:"補体",5:"腫瘍マーカー・肝炎・異常Ig・アレルギー",6:"血液型(ABO・Rh)",7:"交差適合・不規則抗体",8:"直接抗グロブリン・輸血"}
KETSUEKI_LABELS={1:"血球造血",2:"赤血球 基礎",3:"赤血球 臨床①",4:"赤血球 臨床②",5:"白血球 基礎",6:"白血球 臨床①",7:"白血球 臨床②",8:"血小板・凝固",9:"凝固検査・線溶",10:"血小板 臨床",11:"測定法・診断"}
BYORI_LABELS={1:"基礎",2:"固定・脱灰",3:"包埋・薄切・凍結",4:"染色①",5:"染色②",6:"免疫染色",7:"電子顕微鏡",8:"細胞診"}
BISEI_LABELS={1:"基礎",2:"染色・培地",3:"滅菌・消毒・抗菌薬",4:"同定①",5:"同定②",6:"ビブリオ・マイコ",7:"偏性嫌気性菌",8:"真菌・ウイルス"}
SEIRI_LABELS={1:"心電図 基礎",2:"心電図 異常波形",3:"心電図 ホルター・運動負荷",4:"呼吸器①",5:"呼吸器②",6:"超音波 基礎",7:"超音波 心臓",8:"超音波 腹部",9:"脳波 基礎",10:"脳波 臨床",11:"筋電図 基礎・針筋電図",12:"筋電図 神経伝導・反復刺激"}
KAGAKU_LABELS={1:"糖質",2:"脂質",3:"蛋白質・アミノ酸",4:"非蛋白性窒素",5:"酵素",6:"電解質・無機質",7:"生体色素",8:"ホルモン",9:"ビタミン・骨代謝",10:"疾患マーカー",11:"機能検査",12:"分析・測定法"}

out=[]; missing=[]
def add(book, M, labels, chapter=True):
    for ch in sorted(M):
        ids=[]
        for qid in M[ch]:
            if qid in qids: ids.append(qid)
            else: missing.append(qid)
        seen=set(); ids=[x for x in ids if not(x in seen or seen.add(x))]
        if chapter:
            label="%s%d章 %s"%(book,ch,labels[ch]); btn="%d章 %s"%(ch,labels[ch])
        else:
            label="%s：%s"%(book,labels[ch]); btn=labels[ch]
        out.append({"book":book,"ch":ch,"btn":btn,"label":label,"count":len(ids),"ids":ids})
add("血液学", KETSUEKI, KETSUEKI_LABELS)
add("免疫学", MENEKI, MENEKI_LABELS)
add("臨床化学", KAGAKU, KAGAKU_LABELS, chapter=False)
add("生理学", SEIRI, SEIRI_LABELS)
add("病理学", BYORI, BYORI_LABELS)
add("微生物学", BISEI, BISEI_LABELS)

if missing:
    print("!! 存在しないID:", missing, file=sys.stderr)
json.dump(out, open(os.path.join(os.path.dirname(__file__),'coretests.json'),'w',encoding='utf-8'), ensure_ascii=False)
print("項目数:", len(out), " 総ひも付け:", sum(o['count'] for o in out))
for o in out: print("  %-24s %d問"%(o['label'], o['count']))
