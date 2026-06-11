# -*- coding: utf-8 -*-
"""第62回データを base アプリに埋め込んで kakomon-webapp-62.html を出力。
gen_all.py が `const KOKUSHI_62 = [...]` を取り出して統合版に合成する。"""
import json, os
HERE=os.path.dirname(__file__)
src=open(os.path.join(HERE,'..','kakomon-webapp.html'),encoding='utf-8').read()
data=json.load(open(os.path.join(HERE,'kokushi62.json'),encoding='utf-8'))
js=json.dumps(data,ensure_ascii=False)
old_a='"use strict";\n\n// ===== 定数 ====='
new_a='"use strict";\n\nconst KOKUSHI_62 = '+js+';\n\n// ===== 定数 ====='
assert src.count(old_a)==1, 'A anchor'
src=src.replace(old_a,new_a)
open(os.path.join(HERE,'..','kakomon-webapp-62.html'),'w',encoding='utf-8').write(src)
print('wrote kakomon-webapp-62.html', len(src), 'bytes')
