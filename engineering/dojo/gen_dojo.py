# -*- coding: utf-8 -*-
# 過去問道場（臨床工学技士＝コウゼミ 演習アプリ）の配布版を生成する。
#   入力: engineering/kakomon-dojo.html（空テンプレ・グリーン）＋ 各回の単体HTML
#         (engineering/kakomon-webapp-NN.html) に埋め込み済みの問題データ KOKUSHI_NN
#   出力: engineering/kouzemi-dojo-all.html（全回の問題を埋め込んだ単体HTML。配布用）
# 既存の編集アプリ（engineering/kakomon-webapp*.html）には一切手を加えない。
# ケンゼミ(リポジトリ直下 dojo/ ・docs/dojo/)・ホウゼミ(radiology/) 側のファイルには触れない。
#
# 各回単体HTML が未作成のうちは KOKUSHI_SETS が空 → 問題ゼロの土台道場(テンプレ既定の案内を表示)を出力する。
import os, re, json, glob

HERE = os.path.dirname(__file__)            # engineering/dojo/
ENG = os.path.join(HERE, '..')              # engineering/

# engineering/ 配下の単体HTMLを自動検出（新しい回が先）。
def discover():
    nums = []
    for p in glob.glob(os.path.join(ENG, 'kakomon-webapp-*.html')):
        m = re.search(r'kakomon-webapp-(\d+)\.html$', os.path.basename(p))
        if m:
            nums.append(int(m.group(1)))
    return sorted(nums, reverse=True)

YEARS = discover()

def extract(num):
    path = os.path.join(ENG, 'kakomon-webapp-%d.html' % num)
    h = open(path, encoding='utf-8').read()
    m = re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S)
    if not m:
        raise SystemExit('KOKUSHI_%d が %s に見つかりません' % (num, path))
    return m.group(1)

# KOKUSHI_SETS を組み立て（テンプレの `const KOKUSHI_SETS = [];` を置換）
sets_lines = []
for num in YEARS:
    sets_lines.append('  { key: "%d", label: "第%d回", data: %s },' % (num, num, extract(num)))
sets_js = 'const KOKUSHI_SETS = [\n' + '\n'.join(sets_lines) + '\n];'

# コウゼミはマスコットを持たない（テンプレ側の typeof/存在ガードで無害）
mascots_js = 'const MASCOTS = {};'

tpl = open(os.path.join(ENG, 'kakomon-dojo.html'), encoding='utf-8').read()

assert tpl.count('const MASCOTS = {};') == 1, 'MASCOTS プレースホルダが見つかりません'
assert tpl.count('const KOKUSHI_SETS = [];') == 1, 'KOKUSHI_SETS プレースホルダが見つかりません'
out = tpl.replace('const MASCOTS = {};', mascots_js).replace('const KOKUSHI_SETS = [];', sets_js)

outpath = os.path.join(ENG, 'kouzemi-dojo-all.html')
open(outpath, 'w', encoding='utf-8').write(out)

n_q = sum(len(json.loads(extract(num))) for num in YEARS)
print('wrote engineering/kouzemi-dojo-all.html  %.1f MB  / %d問 / %d回' % (len(out) / 1e6, n_q, len(YEARS)),
      '' if YEARS else '(問題なし=空の土台)')
