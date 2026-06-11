# -*- coding: utf-8 -*-
"""第73回データを base アプリ(radiology/kakomon-webapp.html)に埋め込んで
radiology/kakomon-webapp-73.html を出力。統合版生成 gen_all.py が
`const KOKUSHI_73 = [...]` を取り出して合成する(臨床検査技師版と同方式)。"""
import json, os
HERE=os.path.dirname(__file__)
src=open(os.path.join(HERE,'..','kakomon-webapp.html'),encoding='utf-8').read()
data=json.load(open(os.path.join(HERE,'kokushi73.json'),encoding='utf-8'))
js=json.dumps(data,ensure_ascii=False)
old_a='"use strict";\n\n// ===== 定数 ====='
new_a='"use strict";\n\nconst KOKUSHI_73 = '+js+';\n\n// ===== 定数 ====='
assert src.count(old_a)==1, 'A anchor'
src=src.replace(old_a,new_a)

# 単体HTMLを「開くだけで表示」できるよう初回自動投入を注入(localStorageが空のときだけ)。
old_b='// ===== 起動 =====\nloadData();\nrender();'
new_b=('// ===== 起動 =====\nloadData();\n'
       'if (questions.length === 0 && typeof KOKUSHI_73 !== "undefined") {\n'
       '  questions = KOKUSHI_73.map(q => ({ ...q }));\n'
       '  saveData();\n'
       '}\nrender();')
assert src.count(old_b)==1, 'B anchor (起動)'
src=src.replace(old_b,new_b)
open(os.path.join(HERE,'..','kakomon-webapp-73.html'),'w',encoding='utf-8').write(src)
print('wrote radiology/kakomon-webapp-73.html', len(src), 'bytes')
