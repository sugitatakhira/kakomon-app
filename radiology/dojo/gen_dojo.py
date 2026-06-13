# -*- coding: utf-8 -*-
# 過去問道場（診療放射線技師＝ホウゼミ 演習アプリ）の配布版を生成する。
#   入力: radiology/kakomon-dojo.html（空テンプレ）＋ 各年度の単体HTML
#         (radiology/kakomon-webapp-NN.html) に埋め込み済みの問題データ KOKUSHI_NN
#   出力: radiology/houzemi-dojo-all.html（全15回=3000問を埋め込んだ単体HTML。配布用）
# 既存の編集アプリ（radiology/kakomon-webapp*.html）には一切手を加えない。
# 臨床検査技師(ケンゼミ)側のファイル(リポジトリ直下 dojo/ ・docs/dojo/)には触れない。
import os, re, json

HERE = os.path.dirname(__file__)            # radiology/dojo/
RAD = os.path.join(HERE, '..')              # radiology/

# 第78回→第64回（新しい順）。各単体HTMLから KOKUSHI_NN の配列リテラルを取り出す。
YEARS = list(range(78, 63, -1))             # 78..64

def extract(num):
    path = os.path.join(RAD, 'kakomon-webapp-%d.html' % num)
    h = open(path, encoding='utf-8').read()
    m = re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S)
    if not m:
        raise SystemExit('KOKUSHI_%d が %s に見つかりません' % (num, path))
    return m.group(1)

# 解説（ホウゼミ道場専用・別ファイル）。{ qid: {point, choices:[...]} }。あれば各問へ合体する。
#   既存の編集アプリ(radiology/kakomon-webapp*.html)のデータには手を加えない。
EXPL = {}
expl_path = os.path.join(HERE, 'explanations.json')
if os.path.exists(expl_path):
    EXPL = json.load(open(expl_path, encoding='utf-8'))

# KOKUSHI_SETS を組み立て（テンプレの `const KOKUSHI_SETS = [];` を置換）
sets_lines = []
n_expl = 0
for num in YEARS:
    data = json.loads(extract(num))
    for q in data:
        e = EXPL.get(q['id'])
        if not e:
            continue
        if e.get('point'):
            q['point'] = e['point']
        if e.get('choices'):
            q['cexpl'] = e['choices']
        n_expl += 1
    sets_lines.append('  { key: "%d", label: "第%d回", data: %s },' % (num, num, json.dumps(data, ensure_ascii=False)))
sets_js = 'const KOKUSHI_SETS = [\n' + '\n'.join(sets_lines) + '\n];'

# ホウゼミはマスコットを持たない（テンプレ側の typeof/存在ガードで無害）
mascots_js = 'const MASCOTS = {};'

tpl = open(os.path.join(RAD, 'kakomon-dojo.html'), encoding='utf-8').read()

assert tpl.count('const MASCOTS = {};') == 1, 'MASCOTS プレースホルダが見つかりません'
assert tpl.count('const KOKUSHI_SETS = [];') == 1, 'KOKUSHI_SETS プレースホルダが見つかりません'
out = tpl.replace('const MASCOTS = {};', mascots_js).replace('const KOKUSHI_SETS = [];', sets_js)

outpath = os.path.join(RAD, 'houzemi-dojo-all.html')
open(outpath, 'w', encoding='utf-8').write(out)

n_q = sum(len(json.loads(extract(num))) for num in YEARS)
print('wrote radiology/houzemi-dojo-all.html  %.1f MB  / %d問 / %d回 / 解説付き %d問' % (len(out) / 1e6, n_q, len(YEARS), n_expl))
