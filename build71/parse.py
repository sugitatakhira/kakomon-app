# -*- coding: utf-8 -*-
import re, json, sys

CJK = r'[぀-ヿ㐀-鿿＀-￯　-〿]'

def is_cjk(ch):
    return bool(re.match(CJK, ch))

def clean(s):
    # collapse big gaps -> placeholder GAP, keep info; first mark runs >=5 spaces
    s = s.replace('　', ' ')  # fullwidth space -> normal for analysis
    # mark large gaps (>=5 spaces) as a special token
    s = re.sub(r' {5,}', ' \x00 ', s)
    # collapse remaining runs of spaces to single
    s = re.sub(r' {2,}', ' ', s).strip()
    # remove spaces adjacent to CJK characters
    out = []
    for i, ch in enumerate(s):
        if ch == ' ':
            prev = out[-1] if out else ''
            nxt = s[i+1] if i+1 < len(s) else ''
            if (prev and is_cjk(prev)) or (nxt and is_cjk(nxt)):
                continue
        out.append(ch)
    s = ''.join(out)
    s = re.sub(r' {2,}', ' ', s).strip()
    return s

def parse(path, prefix):
    lines = open(path, encoding='utf-8').read().split('\n')
    questions = []
    cur = None
    expected = 1
    for raw in lines:
        if 'DKIX' in raw or '.indd' in raw:
            continue
        if re.match(r'^\s*\d{4}/\d{2}/\d{2}', raw.strip()):
            continue
        if not raw.strip():
            continue
        # choice line
        mc = re.match(r'^\s*([1-5])．(.*)$', raw)
        # question line: number then >=2 spaces then text, number == expected
        mq = re.match(r'^\s*(\d{1,3})\s{2,}(\S.*)$', raw)
        if mc and cur is not None:
            cur['choices'].append(mc.group(2).rstrip())
            cur['_inchoice'] = True
            continue
        if mq and int(mq.group(1)) == expected:
            if cur:
                questions.append(cur)
            cur = {'n': expected, 'stem_lines': [mq.group(2).rstrip()], 'choices': [], '_inchoice': False}
            expected += 1
            continue
        # continuation
        if cur is not None:
            if cur.get('_inchoice') and cur['choices']:
                cur['choices'][-1] = cur['choices'][-1] + ' ' + raw.strip()
            else:
                cur['stem_lines'].append(raw.strip())
    if cur:
        questions.append(cur)

    result = []
    for q in questions:
        stem_raw = ' '.join(q['stem_lines'])
        # extract 別冊 No
        beppu = None
        mb = re.search(r'別冊No\.?\s*([0-9０-９]+[ＡＢA-B]*)', stem_raw)
        if mb:
            beppu = mb.group(1)
        stem = clean(stem_raw)
        choices = [clean(c) for c in q['choices']]
        # flag if any GAP placeholder present
        flag = ('\x00' in stem) or any('\x00' in c for c in choices)
        beppuflag = beppu is not None
        # replace placeholder with a visible marker for now
        stem = stem.replace('\x00', '⟨GAP⟩')
        choices = [c.replace('\x00', '⟨GAP⟩') for c in choices]
        result.append({'n': q['n'], 'text': stem, 'choices': choices,
                       'beppu': beppu, 'nchoices': len(choices),
                       'flag_gap': flag})
    return result

if __name__ == '__main__':
    path, prefix = sys.argv[1], sys.argv[2]
    res = parse(path, prefix)
    print('parsed', len(res), 'questions')
    bad = [r['n'] for r in res if r['nchoices'] not in (2,5) and r['nchoices']!=4 and r['nchoices']!=3]
    print('non-5-choice:', [(r['n'], r['nchoices']) for r in res if r['nchoices'] != 5])
    print('GAP flagged:', [r['n'] for r in res if r['flag_gap']])
    print('BEPPU:', [(r['n'], r['beppu']) for r in res if r['beppu']])
    json.dump(res, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
