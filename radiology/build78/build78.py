# -*- coding: utf-8 -*-
"""第78回(2026) 診療放射線技師 ビルド: 問題/正答/別冊画像 -> CSV・images78.json・埋め込みJS(kokushi78.json)。
臨床検査技師版(build58.py 等)と同一スキーマ・同一手順。診療放射線技師の分野ブロックを適用。
素材(build78/ 配下・再現可):
  am_parsed.json / pm_parsed.json … 本文(pdftotext -layout → parse.py)の自動抽出
  ans78.json … 正答表(A/B, 1始まり)。AM23は採点除外(空)。
  overrides.json … 数式/表/グラフ選択肢の図問題(figure)と PM9 別冊No.3 復元
  /tmp/k78/eam/noNN.png, epm/noNN.png … 別冊画像(extract_beppu.py)
  /tmp/k78/fig_amNN.png, fig_pm29.png … 図問題の原本クロップ
別冊・図ともポートレートで回転無し。設問内インライン図(figure)= AM12/13/16/32/56/77/93・PM29。
"""
import json, re, base64, io, csv, os, sys
from PIL import Image

HERE = os.path.dirname(__file__)
TMP = '/tmp/k78'
YEAR = "第78回(2026)"

# 診療放射線技師 分野ブロック(午前・午後 共通。第78回の出題順から導出)。合計100。
FIELD_RANGES = [(1,10,"診療画像検査学"),(11,20,"核医学検査技術学"),(21,30,"放射線治療技術学"),
 (31,35,"医用画像情報学"),(36,39,"診療画像検査学"),(40,54,"基礎医学大要"),
 (55,59,"放射線生物学"),(60,64,"放射線物理学"),(65,67,"医用工学"),
 (68,72,"放射線計測学"),(73,82,"診療画像機器学"),(83,92,"X線撮影技術学"),
 (93,95,"画像工学"),(96,100,"放射線安全管理学")]
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

def clean_choice(s):
    s = TAIL.sub('', s)
    s = s.replace('⟨GAP⟩', ' — ')
    s = s.replace('‑','-')
    s = re.sub(r'\s+',' ', s).strip()
    s = re.sub(r'\s*-\s*(?=[ぁ-んァ-ヶ一-龠])', '-', s)
    s = re.sub(r'(?<=[ぁ-んァ-ヶ一-龠A-Za-z0-9])\s*-\s*', '-', s)
    s = re.sub(r'\s*—\s*', ' — ', s).strip()
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
        choices = [clean_choice(c) for c in (o['choices'] if 'choices' in o else q['choices'])]
        choices = [c for c in choices if c != '']
        araw = ans[str(n)] if str(n) in ans else ans[n]
        answers = sorted(int(d)-1 for d in araw) if araw else []
        qid = "k78%s%s%03d" % (id_label, prefix_label, n)
        text = stem if (('text' in o) and stem.startswith('[')) else "[%s%d] %s" % (prefix_label, n, stem)
        expl = o.get("explanation","")
        if not araw:
            expl = (expl + " ※採点除外問題").strip()
        item = {"id": qid, "text": text, "choices": choices, "answers": answers,
                "explanation": expl, "field": field_for(n), "year": YEAR, "difficulty": "普通"}
        if 'figure' in o:
            fp = os.path.join(TMP, 'fig_%s.png' % o['figure'])
            uri = img_datauri(fp); item['image'] = uri; images[qid] = uri
        elif beppu_no is not None:
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
    ans = json.load(open(os.path.join(HERE,'ans78.json'),encoding='utf-8'))

    am_q, am_img = build_side(am, ov['AM'], ans['A'], 'A', '午前', os.path.join(TMP,'eam'))
    pm_q, pm_img = build_side(pm, ov['PM'], ans['B'], 'B', '午後', os.path.join(TMP,'epm'))
    allq = am_q + pm_q
    images = {**am_img, **pm_img}

    json.dump(images, open(os.path.join(HERE,'..','images78.json'),'w',encoding='utf-8'), ensure_ascii=False)

    rows=[["設問","選択肢1","選択肢2","選択肢3","選択肢4","選択肢5","正解番号","解説","分野","年度","難易度"]]
    for q in allq:
        ch=(q['choices']+["","","","",""])[:5]
        seikai=",".join(str(a+1) for a in q['answers'])
        rows.append([q['text'],*ch,seikai,q['explanation'],q['field'],q['year'],q['difficulty']])
    with open(os.path.join(HERE,'..','診療放射線技師_第78回.csv'),'w',encoding='utf-8-sig',newline='') as f:
        csv.writer(f).writerows(rows)

    json.dump(allq, open(os.path.join(HERE,'kokushi78.json'),'w',encoding='utf-8'), ensure_ascii=False)
    print('built', len(allq), 'questions;', len(images), 'images')
    from collections import Counter
    print('fields', dict(Counter(q['field'] for q in allq)))
    print('multi-answer', sum(1 for q in allq if len(q['answers'])>1))
    print('no-answer(採点除外)', sum(1 for q in allq if len(q['answers'])==0))
    print('with image', sum(1 for q in allq if 'image' in q))

if __name__=='__main__':
    main()
