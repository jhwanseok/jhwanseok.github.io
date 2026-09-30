# Mechanical pre-publish checks from docs/playbook/writing-rules.md (run from the repo root).
# Only checks committed pages; it cannot verify facts against the source, see writing-rules.md section 1.
import re, glob, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

tracked = set(subprocess.check_output(['git', 'ls-files', 'src/pages'], text=True).split())
files = sorted(glob.glob('src/pages/articles/*.md') + glob.glob('src/pages/projects/*.md'))
FWD = r'(뒤에서 볼|이후 시리즈|앞으로 살펴볼|이후 등장|다음 편에서|앞으로 볼|시리즈 후반|이후 세대|이후 모델|뒤 편|앞으로 만날)'
for f in files:
    f = f.replace(chr(92), '/')
    if f not in tracked:
        continue
    s = open(f, encoding='utf-8').read()
    body = s.split('---', 2)[2]
    print('==', f)
    abbrs = [(m.start(), m.group(1)) for m in re.finditer(r'<abbr[^>]*>(.*?)</abbr>', body)]
    seen = {}
    for pos, t in abbrs:
        seen.setdefault(t, []).append(pos)
    for t, ps in seen.items():
        if len(ps) > 1:
            print('  abbr repeated:', t, len(ps))
        pre = re.sub(r'<abbr[^>]*>.*?</abbr>', '', body[:ps[0]])
        # headings, image alt text and reference-list links are not prose mentions
        pre = '\n'.join(l for l in pre.split('\n') if not l.startswith(('#', '![', '- [')))
        if re.search(r'(?<![A-Za-z가-힣])' + re.escape(t) + r'(?![A-Za-z])', pre):
            print('  abbr NOT at first mention:', t)
    for i, l in enumerate(body.split('\n')):
        if l.strip().startswith('|') and '<abbr' in l:
            print('  abbr in table, body line', i)
    parts = re.split(r'\n## ', body)
    op = parts[0] + ('\n## ' + parts[1] if len(parts) > 1 else '')
    print('  marks total', body.count('<mark>'), 'opening', op.count('<mark>'))
    for p in body.split('\n\n'):
        if p.count('<mark>') > 1:
            print('  >1 mark in one paragraph')
    for m in re.finditer(r'\b([A-Z]{2,})(이|가|은|는|을|를|과|와)(?=[ ,.\n)])', body):
        w, j = m.groups()
        cons = w[-1] in 'LMNR'
        ok = (j in '이은을과') if cons else (j in '가는를와')
        if not ok:
            print('  josa?', w + j)
    for m in re.finditer(r'[^\n.]*' + FWD + r'[^\n.]*', body):
        print('  fwd?:', m.group(0).strip()[:120])
    print('  dashes', len(re.findall('[—–]', body)), ' h4 per h2:',
          [p.count('\n#### ') + (1 if p.startswith('#### ') else 0) for p in parts[1:]])
