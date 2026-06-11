# -*- coding: utf-8 -*-
import re, json, subprocess
txt = subprocess.check_output(['pdftotext','-layout','seitou.pdf','-']).decode()
ans = {'A':{},'B':{}}
for m in re.finditer(r'([AB])0*(\d{1,3})((?:[ \t]*[1-5])+)', txt):
    side, num, a = m.group(1), str(int(m.group(2))), m.group(3)
    ans[side][num] = ''.join(re.findall(r'[1-5]', a))
bad = [(s,k,v) for s in 'AB' for k,v in ans[s].items() if not (1<=len(v)<=3) or any(c not in '12345' for c in v)]
miss = [s+str(i) for s in 'AB' for i in range(1,101) if not ans[s].get(str(i))]
print('A',len(ans['A']),'B',len(ans['B']))
print('A2,A6,A10,B27 =', ans['A'].get('2'), ans['A'].get('6'), ans['A'].get('10'), ans['B'].get('27'))
print('multi', sum(1 for s in 'AB' for v in ans[s].values() if len(v)>1))
print('bad', bad, 'missing', miss)
json.dump(ans, open('ans60.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
