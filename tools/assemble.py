"""Join the source files listed in src/manifest.txt into the light app (logo / pictures / jsQR still placeholders).
  python3 tools/assemble.py [out.html]   (default: print nothing, used by build.py)"""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(R, 'src')
def assemble():
    files = [l.strip() for l in open(os.path.join(S, 'manifest.txt'), encoding='utf-8') if l.strip() and not l.startswith('#')]
    parts = []
    for f in files:
        t = open(os.path.join(S, f), encoding='utf-8').read()
        if not t.endswith('\n'): t += '\n'
        parts.append(t)
    s = ''.join(parts)
    en = json.load(open(os.path.join(S, 'data', 'en.json'), encoding='utf-8'))
    if s.count('/*@EN*/{}') != 1: sys.exit('EN placeholder missing')
    s = s.replace('/*@EN*/{}', json.dumps(en, ensure_ascii=False, separators=(',', ':')))
    return s
if __name__ == '__main__' and len(sys.argv) > 1:
    open(sys.argv[1], 'w', encoding='utf-8').write(assemble()); print('assembled ->', sys.argv[1])
