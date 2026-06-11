# -*- coding: utf-8 -*-
"""第78回データを base アプリ(radiology/kakomon-webapp.html)に埋め込んで
radiology/kakomon-webapp-78.html を出力。統合版生成 gen_all.py が
`const KOKUSHI_78 = [...]` を取り出して合成する(臨床検査技師版と同方式)。"""
import json, os
HERE=os.path.dirname(__file__)
src=open(os.path.join(HERE,'..','kakomon-webapp.html'),encoding='utf-8').read()
data=json.load(open(os.path.join(HERE,'kokushi78.json'),encoding='utf-8'))
js=json.dumps(data,ensure_ascii=False)
old_a='"use strict";\n\n// ===== 定数 ====='
new_a='"use strict";\n\nconst KOKUSHI_78 = '+js+';\n\n// ===== 定数 ====='
assert src.count(old_a)==1, 'A anchor'
src=src.replace(old_a,new_a)
open(os.path.join(HERE,'..','kakomon-webapp-78.html'),'w',encoding='utf-8').write(src)
print('wrote radiology/kakomon-webapp-78.html', len(src), 'bytes')
