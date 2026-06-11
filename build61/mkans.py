# -*- coding: utf-8 -*-
import re, json, subprocess
txt = subprocess.check_output(['pdftotext','-layout','seitou.pdf','-']).decode()
ans = {'A':{},'B':{}}
cur = None
for line in txt.split('\n'):
    for tk in re.split(r'\s{2,}', line.strip()):
        m = re.match(r'^([AB])0*(\d{1,3})$', tk)
        if m:
            cur = (m.group(1), str(int(m.group(2))))
            ans[cur[0]].setdefault(cur[1], '')
        elif cur and re.fullmatch(r'[1-5 ]+', tk):
            ans[cur[0]][cur[1]] += ''.join(tk.split())
bad = [(s,k,v) for s in 'AB' for k,v in ans[s].items() if not (1<=len(v)<=3) or any(c not in '12345' for c in v)]
miss = [s+str(i) for s in 'AB' for i in range(1,101) if not ans[s].get(str(i))]
print('A',len(ans['A']),'B',len(ans['B']))
print('A6,A10,A27,B12 =', ans['A']['6'], ans['A']['10'], ans['A']['27'], ans['B']['12'])
print('multi', sum(1 for s in 'AB' for v in ans[s].values() if len(v)>1))
print('bad', bad, 'missing', miss)
json.dump(ans, open('ans61.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
