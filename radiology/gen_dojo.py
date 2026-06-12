# -*- coding: utf-8 -*-
"""ホウゼミ 過去問道場（演習アプリ）の配布版を生成。
入力: radiology/kakomon-dojo.html（空テンプレ）＋ 各回の単体HTML(kakomon-webapp-NN.html)の KOKUSHI_NN
出力: radiology/kakomon-dojo-all.html（全15回3000問を埋め込んだ単体HTML・配布用）
ゼミナール本体(kakomon-webapp*.html)には一切手を加えない。マスコットは持たない。"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))   # radiology/
YEARS = list(range(78, 63, -1))                      # 78..64
YEARLABEL = {78:2026,77:2025,76:2024,75:2023,74:2022,73:2021,72:2020,71:2019,70:2018,
             69:2017,68:2016,67:2015,66:2014,65:2013,64:2012}

def extract(num):
    h = open(os.path.join(HERE, 'kakomon-webapp-%d.html' % num), encoding='utf-8').read()
    m = re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S)
    if not m: raise SystemExit('KOKUSHI_%d が見つかりません' % num)
    return m.group(1)

sets_lines = ['  { key: "%d", label: "第%d回(%d)", data: %s },' % (n, n, YEARLABEL[n], extract(n)) for n in YEARS]
sets_js = 'const KOKUSHI_SETS = [\n' + '\n'.join(sets_lines) + '\n];'
mascots_js = 'const MASCOTS = {};'

tpl = open(os.path.join(HERE, 'kakomon-dojo.html'), encoding='utf-8').read()
assert tpl.count('const MASCOTS = {};') == 1, 'MASCOTS placeholder'
assert tpl.count('const KOKUSHI_SETS = [];') == 1, 'KOKUSHI_SETS placeholder'
out = tpl.replace('const MASCOTS = {};', mascots_js).replace('const KOKUSHI_SETS = [];', sets_js)

open(os.path.join(HERE, 'kakomon-dojo-all.html'), 'w', encoding='utf-8').write(out)
n_q = sum(len(json.loads(extract(n))) for n in YEARS)
print('wrote kakomon-dojo-all.html  %.1f MB / %d問 / %d回' % (len(out)/1e6, n_q, len(YEARS)))
