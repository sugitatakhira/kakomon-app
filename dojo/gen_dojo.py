# -*- coding: utf-8 -*-
# 過去問道場（演習アプリ）の配布版を生成する。
#   入力: kakomon-dojo.html（空テンプレ）＋ 各年度の単体HTML（kakomon-webapp-NN.html）に
#         埋め込み済みの問題データ KOKUSHI_NN ＋ assets/mascot/*.png
#   出力: kakomon-dojo-all.html（全15回=3000問を埋め込んだ単体HTML。配布用）
# 既存の編集アプリ（kakomon-webapp*.html）には一切手を加えない。
import os, re, json, base64

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..')

# 第72回→第58回（新しい順）。各単体HTMLから KOKUSHI_NN の配列リテラルを取り出す。
YEARS = [72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58]

def extract(num):
    path = os.path.join(ROOT, 'kakomon-webapp-%d.html' % num)
    h = open(path, encoding='utf-8').read()
    m = re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S)
    if not m:
        raise SystemExit('KOKUSHI_%d が %s に見つかりません' % (num, path))
    return m.group(1)

def b64png(path):
    return "data:image/png;base64," + base64.b64encode(open(path, 'rb').read()).decode()

# マスコット画像（あれば埋め込む。無くてもアプリは動く）
MASCOTS = {}
mdir = os.path.join(ROOT, 'assets', 'mascot')
if os.path.isdir(mdir):
    for n in ['upa_happy', 'upa_think', 'upa_smile', 'bear_point', 'bear_wow', 'bear_smile']:
        p = os.path.join(mdir, n + '.png')
        if os.path.exists(p):
            MASCOTS[n] = b64png(p)

# 解説（過去問道場専用・別ファイル）。{ qid: {point, choices:[...]} }。あれば各問へ合体する。
#   既存の編集アプリ(kakomon-webapp*.html)のデータには手を加えない。
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
mascots_js = 'const MASCOTS = ' + json.dumps(MASCOTS, ensure_ascii=False) + ';'

tpl = open(os.path.join(ROOT, 'kakomon-dojo.html'), encoding='utf-8').read()

assert tpl.count('const MASCOTS = {};') == 1, 'MASCOTS プレースホルダが見つかりません'
assert tpl.count('const KOKUSHI_SETS = [];') == 1, 'KOKUSHI_SETS プレースホルダが見つかりません'
out = tpl.replace('const MASCOTS = {};', mascots_js).replace('const KOKUSHI_SETS = [];', sets_js)

outpath = os.path.join(ROOT, 'kakomon-dojo-all.html')
open(outpath, 'w', encoding='utf-8').write(out)

n_q = sum(len(json.loads(extract(num))) for num in YEARS)
print('wrote kakomon-dojo-all.html  %.1f MB  / %d問 / %d回 / 解説付き %d問' % (len(out) / 1e6, n_q, len(YEARS), n_expl))
