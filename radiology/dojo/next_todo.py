# -*- coding: utf-8 -*-
# ホウゼミ道場の解説づくりの「次にやる未作成問題」を順番に出すヘルパー。
#   既に radiology/dojo/explanations.json にある問題は済みとみなす。
#   出題順: 年度 第78回→…→第64回、各年度内は HTML 配列の並び。
# 使い方: python3 radiology/dojo/next_todo.py [N]
import re, json, os, sys
HERE = os.path.dirname(__file__); RAD = os.path.join(HERE, '..')
YEARS = list(range(78, 63, -1))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
EXPL = json.load(open(os.path.join(HERE, 'explanations.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'explanations.json')) else {}
def load(num):
    h = open(os.path.join(RAD, 'kakomon-webapp-%d.html' % num), encoding='utf-8').read()
    return json.loads(re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S).group(1))
done_total = len(EXPL); out = []; remaining_total = 0
for num in YEARS:
    for q in load(num):
        if q['id'] in EXPL: continue
        remaining_total += 1
        if len(out) < N: out.append(q)
print("=== 進捗: 解説済み %d / 残り %d ===" % (done_total, remaining_total))
if not out:
    print("ALL DONE")
else:
    print("=== 次の %d 問 ===" % len(out))
    for q in out:
        ans = q.get('answers', [])
        tag = '（採点除外＝正答なし。pointのみでよい）' if not ans else ''
        print("\n%s | %s %s" % (q['id'], q.get('field', ''), tag))
        print("  " + q['text'])
        for i, c in enumerate(q['choices']):
            print("   %d.%s%s" % (i + 1, c, '  ★正解' if i in ans else ''))
