# 共通: 統合HTMLから全3000問を読み込む
import re, json, os
ROOT=os.path.join(os.path.dirname(__file__),'..')
html=open(os.path.join(ROOT,'kakomon-webapp-all.html'),encoding='utf-8').read()
def load_all():
    qs=[]
    for m in re.finditer(r'const KOKUSHI_(\d\d) = (\[.*?\]);', html, re.S):
        qs.extend(json.loads(m.group(2)))
    return qs
if __name__=='__main__':
    qs=load_all()
    from collections import Counter
    print('total',len(qs))
    print(Counter(q['field'] for q in qs))
