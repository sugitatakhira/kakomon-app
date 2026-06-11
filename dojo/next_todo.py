# -*- coding: utf-8 -*-
# 過去問道場の解説づくりの「次にやる未作成問題」を順番に出すヘルパー。
#   既に dojo/explanations.json にある問題は済みとみなす。
#   出題順: 年度 第72回→…→第58回、各年度内は HTML 配列の並び(午前A001..A100, 午後B001..B100)。
# 使い方: python3 dojo/next_todo.py [N]   (Nは出力する問題数。既定12)
import re, json, os, sys

HERE = os.path.dirname(__file__); ROOT = os.path.join(HERE, '..')
YEARS = [72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12

EXPL = json.load(open(os.path.join(HERE, 'explanations.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'explanations.json')) else {}

def load(num):
    h = open(os.path.join(ROOT, 'kakomon-webapp-%d.html' % num), encoding='utf-8').read()
    return json.loads(re.search(r'const KOKUSHI_%d = (\[.*?\]);' % num, h, re.S).group(1))

done_total = len(EXPL)
out = []
remaining_total = 0
for num in YEARS:
    for q in load(num):
        if q['id'] in EXPL:
            continue
        remaining_total += 1
        if len(out) < N:
            out.append(q)

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
