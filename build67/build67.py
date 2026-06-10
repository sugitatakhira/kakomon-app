# -*- coding: utf-8 -*-
"""第67回(2021) ビルド: 問題/正答/別冊画像 -> CSV・images67.json・埋め込みJS(kokushi67.json)。
素材(すべて build68/ 配下・再現可):
  am_parsed.json / pm_parsed.json … 本文(cmapfix→parse)の自動抽出
  overrides.json … 組合せ「—」区切り・表/特殊グリフの手修正
  ans67.json … 正答表(A/B, 1始まり)
  /tmp/k67/eam/noNN.png, epm/noNN.png … 別冊画像(extract_beppu.pyで生成)
第68回は採点除外なし・設問内インライン図なし(全画像が別冊)。
"""
import json, re, base64, io, csv, os, sys
from PIL import Image

HERE = os.path.dirname(__file__)
TMP = '/tmp/k67'
YEAR = "第67回(2021)"

FIELD_RANGES = [(1,10,"臨床検査総論"),(11,15,"臨床検査医学総論"),(16,28,"臨床生理学"),
 (29,44,"臨床化学"),(45,58,"病理組織細胞学"),(59,67,"臨床血液学"),(68,78,"臨床微生物学"),
 (79,89,"臨床免疫学"),(90,94,"公衆衛生学"),(95,100,"医用工学概論")]
def field_for(n):
    for a,b,f in FIELD_RANGES:
        if a<=n<=b: return f
    raise ValueError(n)

Z2H = str.maketrans('０１２３４５６７８９ＡＢ','0123456789AB')

def img_datauri(path, quality=72):
    im = Image.open(path).convert('RGB')
    W,H = im.size; ls = max(W,H)
    if ls > 900:
        im = im.resize((round(W*900/ls), round(H*900/ls)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf,'JPEG',quality=quality,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()

TAIL = re.compile(r'別\s*(⟨GAP⟩)?\s*冊\s*No[\.．]?\s*[0-9０-９]*\s*(⟨GAP⟩)?\s*[ＡＢAB、，,・\s]*$')
def clean_text(s):
    s = TAIL.sub('', s)
    s = s.replace('⟨GAP⟩','')
    s = s.replace('‑','-')
    s = re.sub(r'\s+',' ', s).strip()
    s = re.sub(r'\s*-\s*(?=[ぁ-んァ-ヶ一-龠])', '-', s)
    s = re.sub(r'(?<=[ぁ-んァ-ヶ一-龠A-Za-z0-9])\s*-\s*', '-', s)
    return s

def beppu_suffix(orig_stem):
    st = orig_stem.translate(Z2H)
    nos = re.findall(r'別冊No\.?\s*(\d+)\s*([AB])?', st)
    if not nos:
        return '', None
    base = nos[0][0]
    parts = sorted({p for n,p in nos if n==base and p})
    if parts:
        suf = '【別冊No.%s%s 図】' % (base, '・'.join(parts) if len(parts)>1 else parts[0])
    else:
        suf = '【別冊No.%s 図】' % base
    return suf, int(base)

def strip_inline_beppu(stem):
    return re.sub(r'（\s*別冊No\.?\s*[0-9０-９]+[ＡＢAB・、，,\s]*）','', stem)

def build_side(parsed, ov, ans, prefix_label, id_label, img_dir):
    out = []; images = {}
    for q in parsed:
        n = q['n']
        o = ov.get(str(n), {})
        stem = o['text'] if 'text' in o else clean_text(strip_inline_beppu(q['text']))
        suf, beppu_no = beppu_suffix(o['text'] if 'text' in o else q['text'])
        if suf and '別冊' not in stem:
            stem = (stem.rstrip('。') + '。') if (stem and not stem.endswith('。')) else stem
            stem = (stem + suf) if stem else suf
        choices = [clean_text(c) for c in (o['choices'] if 'choices' in o else q['choices'])]
        choices = [c for c in choices if c != '']
        araw = ans[str(n)] if str(n) in ans else ans[n]
        answers = sorted(int(d)-1 for d in araw) if araw else []
        qid = "k67%s%s%03d" % (id_label, prefix_label, n)
        # text override は既に[午後85]等の接頭辞付き
        text = stem if (('text' in o) and stem.startswith('[')) else "[%s%d] %s" % (prefix_label, n, stem)
        item = {"id": qid, "text": text, "choices": choices, "answers": answers,
                "explanation": o.get("explanation",""), "field": field_for(n), "year": YEAR, "difficulty": "普通"}
        if beppu_no is not None:
            p = os.path.join(img_dir, 'no%02d.png' % beppu_no)
            if os.path.exists(p):
                uri = img_datauri(p); item['image'] = uri; images[qid] = uri
            else:
                print('  !! missing 別冊 image', p, 'for', qid, file=sys.stderr)
        out.append(item)
    return out, images

def main():
    am = json.load(open(os.path.join(HERE,'am_parsed.json'),encoding='utf-8'))
    pm = json.load(open(os.path.join(HERE,'pm_parsed.json'),encoding='utf-8'))
    ov = json.load(open(os.path.join(HERE,'overrides.json'),encoding='utf-8'))
    ans = json.load(open(os.path.join(HERE,'ans67.json'),encoding='utf-8'))

    am_q, am_img = build_side(am, ov['AM'], ans['A'], 'A', '午前', os.path.join(TMP,'eam'))
    pm_q, pm_img = build_side(pm, ov['PM'], ans['B'], 'B', '午後', os.path.join(TMP,'epm'))
    allq = am_q + pm_q
    images = {**am_img, **pm_img}

    json.dump(images, open(os.path.join(HERE,'..','images67.json'),'w',encoding='utf-8'), ensure_ascii=False)

    rows=[["設問","選択肢1","選択肢2","選択肢3","選択肢4","選択肢5","正解番号","解説","分野","年度","難易度"]]
    for q in allq:
        ch=(q['choices']+["","","","",""])[:5]
        seikai=",".join(str(a+1) for a in q['answers'])
        rows.append([q['text'],*ch,seikai,q['explanation'],q['field'],q['year'],q['difficulty']])
    with open(os.path.join(HERE,'..','臨床検査技師_第67回.csv'),'w',encoding='utf-8-sig',newline='') as f:
        csv.writer(f).writerows(rows)

    json.dump(allq, open(os.path.join(HERE,'kokushi67.json'),'w',encoding='utf-8'), ensure_ascii=False)
    print('built', len(allq), 'questions;', len(images), 'images')
    from collections import Counter
    print('fields', dict(Counter(q['field'] for q in allq)))
    print('multi-answer', sum(1 for q in allq if len(q['answers'])>1))
    print('no-answer(採点除外)', sum(1 for q in allq if len(q['answers'])==0))
    print('with image', sum(1 for q in allq if 'image' in q))

if __name__=='__main__':
    main()
