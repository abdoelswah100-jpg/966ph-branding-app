"""One-time: split src/app.html (one big file) into src/ folders for version 1.1.
The order is kept exactly (one classic script, shared global scope), so assembling the files gives the same app.
After this, src/app.html is no longer the source: edit the files listed in src/manifest.txt."""
import os, re, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(R, 'src')
src = open(os.path.join(S, 'app.html'), encoding='utf-8').read()
L = src.split('\n')
assert L[-1] == '', 'file must end with a newline'
L = L[:-1]

def find(pat, start=0):
    for i in range(start, len(L)):
        if re.match(pat, L[i]): return i
    sys.exit('not found: ' + pat)

i_style = find(r'^<style>$')
i_close = find(r'.*</style></head><body><div id="app"></div>$')
i_jsqr = find(r'^<script>/\*__JSQR__\*/</script>$')
i_js = find(r'^<script>$', i_jsqr)
i_end = find(r'^</script></body></html>$', i_js)
assert i_close == i_jsqr - 1 and i_js == i_jsqr + 1 and i_end == len(L) - 1

# the last CSS rule sits on the closing line: move it into the stylesheet
close = L[i_close]
css_tail, shell_close = close.split('</style>', 1)
shell_close = '</style>' + shell_close

FILES = []  # (path, lines)
def put(path, lines): FILES.append((path, lines))

put('shell/top.html', L[:i_style + 1])
put('styles/app.css', L[i_style + 1:i_close] + ([css_tail] if css_tail else []))
put('shell/middle.html', [shell_close, L[i_jsqr], L[i_js]])

JS = L[i_js + 1:i_end]
off = i_js + 1
def at(pat, start=0):
    for i in range(start, len(JS)):
        if re.match(pat, JS[i]): return i
    sys.exit('js not found: ' + pat)

# core: cut points (each starts a file) — the code is not reordered
CORE = [('js/core/00-base.js', r'^const APPSRC='),
        ('js/core/01-names.js', r'^const NM=\{'),
        ('js/core/02-colors-fields.js', r'^const RG='),
        ('js/core/03-sizes.js', r'^const SZD=\{'),
        ('js/core/04-data-fixes.js', r'^function mig2\('),
        ('js/core/05-ad-types.js', r'^const EMO='),
        ('js/core/06-language.js', r'^const ORD='),
        ('js/core/07-state-storage-icons.js', r'^const LOGO='),
        ('js/core/08-forms.js', r'^function draft\('),
        ('js/core/09-totals-summary.js', r'^function sumText\('),
        ('js/core/10-header-menu-cards.js', r'^function cfg\('),
        ('js/core/11-sync-file.js', r'^const cntRows='),
        ('js/core/12-reports.js', r'^const mtOf='),
        ('js/core/13-compare-settings.js', r'^const dayDiff='),
        ('js/core/14-checklists-shortages.js', r'^function priceCombos\('),
        ('js/core/15-tabs-home-route.js', r'^const TABS='),
        ('js/core/16-types-trash-backups.js', r'^function typesHtml\('),
        ('js/core/17-xlsx-native-save.js', r'^const xe='),
        ('js/core/18-app-lock.js', r'^const LKK='),
        ('js/core/19-pictures-excel-names.js', r'^let IMG='),
        ('js/core/20-photos-attachments.js', r'^const PHMAX='),
        ('js/core/21-import-excel-reports.js', r'^const IMH='),
        ('js/core/22-calculator-month.js', r'^function calcCfg\('),
        ('js/features/custody.js', r'^// ---------- custody '),
        ('js/features/maintenance.js', r'^// ---------- maintenance '),
        ('js/features/warehouse.js', r'^// ---------- warehouse '),
        ]
cuts = []
pos = 0
for path, pat in CORE:
    i = at(pat, pos); cuts.append((path, i)); pos = i + 1
# later versions: one file per version, in order
rest = [i for i in range(pos, len(JS)) if re.match(r'^// ---------- ', JS[i])]
names = {}
for i in rest:
    m = re.match(r'^// ---------- (v\d+\.\d+): (.*?) -*$', JS[i])
    if m:
        v = m.group(1)
        if v in names: continue  # same version continues in the same file
        names[v] = 1
        cuts.append((f'js/updates/{v}.js', i))
    else:
        t = JS[i]
        if 'v1.5 extras' in t: cuts.append(('js/app/extras-v1.5.js', i))
        elif 'users, permissions' in t: cuts.append(('js/app/users.js', i))
        elif t.startswith('// ---------- PDF'): cuts.append(('js/app/pdf-and-start.js', i))
cuts.sort(key=lambda x: x[1])
assert cuts[0][1] == 0
for k, (path, i) in enumerate(cuts):
    j = cuts[k + 1][1] if k + 1 < len(cuts) else len(JS)
    put(path, JS[i:j])
put('shell/bottom.html', [L[i_end]])

# the English dictionary (one long line) becomes data/en.json
os.makedirs(os.path.join(S, 'data'), exist_ok=True)
for k, (path, lines) in enumerate(FILES):
    for n, ln in enumerate(lines):
        if ln.startswith('const EN_D='):
            a = ln.index('const EN_D=') + len('const EN_D='); b = ln.index(';let TRX=null;')
            D = json.loads(ln[a:b])
            json.dump(D, open(os.path.join(S, 'data', 'en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
            lines[n] = ln[:a] + '/*@EN*/{}' + ln[b:]

os.makedirs(os.path.join(S, 'data'), exist_ok=True)
man = []
for path, lines in FILES:
    p = os.path.join(S, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write('\n'.join(lines) + '\n'); man.append(path)
open(os.path.join(S, 'manifest.txt'), 'w', encoding='utf-8').write(
    '# 966Ph Branding source (1.1+). The app = these files joined in this order (tools/assemble.py).\n'
    '# One shared script: a file can use what an earlier file defined. Do not reorder.\n' + '\n'.join(man) + '\n')
for f in ('bimg.json', 'logo.txt', 'cdocs.json'):
    if os.path.exists(os.path.join(S, f)): os.replace(os.path.join(S, f), os.path.join(S, 'data', f))
print(len(man), 'files')
