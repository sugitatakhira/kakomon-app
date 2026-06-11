import sys, json
sys.path.insert(0,__import__('os').path.dirname(__file__))
from _load import load_all
field=sys.argv[1]
qs=[q for q in load_all() if q['field']==field]
# sort by year(desc via label in id) then num — keep stable
def out(q):
    ans=','.join(str(a+1) for a in q['answers'])
    stem=q['text'].replace('\n',' ')
    ch=' / '.join('%d.%s'%(i+1,c) for i,c in enumerate(q['choices']))
    return '%s\n   %s  [正:%s]'%(stem, ch, ans)
for q in qs:
    print('@'+q['id'])
    print(out(q))
print('COUNT',len(qs),file=sys.stderr)
