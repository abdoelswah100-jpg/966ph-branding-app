"""v1.6 (same name): shortages show the side (يمين / يسار) for Side Acrylic Shelves Wall / Floor and the gondola pocket,
the name column is dropped when it is empty, and the WhatsApp text lists only what is missing, short."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'nqHasNm' not in s
# side on the lines
rep("if(c>w)o.push({...PK,sz:n,q:c,v:w,d:c-w})", "if(c>w)o.push({...PK,sz:'—',sd:n,q:c,v:w,d:c-w})")
rep("  o.push({...b,nm,pt:'',sz,mat,q,v,d})});return o}", "  o.push({...b,nm,pt:'',sz,mat,sd:r.sd||'',q,v,d})});return o}")
# table: الجهة column when the group has sides, المسمى column only when it has names
rep("h+=`<${H}>${esc(g.t.n)}</${H}><div class=\"sc\"><table><tr><th>المسمى</th><th>القسم</th><th>المقاس</th><th>الخامة</th><th>المطلوب</th><th>${lab}</th><th>الباقي</th></tr>${g.a.map(x=>{const c=x.sec?COL[x.sec]:'';return `<tr><td>${esc([x.nm,x.pt].filter(Boolean).join(' · ')||'—')}</td><td${c?` style=\"${bgc(c)};font-weight:700\"`:''}>${esc(x.sec||'—')}</td><td>${esc(x.sz||'—')}${rshT(x.r,x.p.sh)}</td><td>${esc(x.mat||'—')}</td>",
    "const hn=g.a.some(nqHasNm),hs=g.a.some(x=>x.sd);h+=`<${H}>${esc(g.t.n)}</${H}><div class=\"sc\"><table><tr>${hn?'<th>المسمى</th>':''}<th>القسم</th><th>المقاس</th>${hs?'<th>الجهة</th>':''}<th>الخامة</th><th>المطلوب</th><th>${lab}</th><th>الباقي</th></tr>${g.a.map(x=>{const c=x.sec?COL[x.sec]:'';return `<tr>${hn?`<td>${esc([x.nm,x.pt].filter(Boolean).join(' · ')||'—')}</td>`:''}<td${c?` style=\"${bgc(c)};font-weight:700\"`:''}>${esc(x.sec||'—')}</td><td>${esc(x.sz||'—')}${rshT(x.r,x.p.sh)}</td>${hs?`<td><b>${esc(x.sd||'—')}</b></td>`:''}<td>${esc(x.mat||'—')}</td>")
rep("function nqHtml(){", "const nqHasNm=x=>!!(x.nm||x.pt);\nfunction nqHtml(){")
# WhatsApp: only what is missing, short
rep("o.push('• '+([x.nm,x.pt].filter(Boolean).join(' · ')||'—')+(x.sec?' ('+x.sec+')':'')+' · '+x.sz+' · '+x.mat+' — باقي '+x.d+' من '+x.q);tot+=x.d",
    "o.push('• '+[[x.nm,x.pt].filter(Boolean).join(' · '),x.sec&&!String(x.nm||'').startsWith(x.sec)?x.sec:'',x.sz&&x.sz!='—'?x.sz:'',x.sd,x.mat&&x.mat!='—'?x.mat:''].filter(Boolean).join(' · ')+' ×'+x.d);tot+=x.d")
rep("o.push('',tot?'إجمالي الباقي: '+tot+' قطعة':'✅ مفيش نواقص');", "o.push('',tot?'الإجمالي: '+tot+' قطعة':'✅ مفيش نواقص');")
rep(" changelog:[{version:'v1.6',date:'2026-10-27',changes:[", " changelog:[{version:'v1.6',date:'2026-10-27',changes:['Shortages: side column (يمين / يسار) for Side Acrylic Shelves Wall / Floor and the gondola pocket; the name column only when a type has names; WhatsApp text lists only what is missing (name · section · size · side · material ×count)',")
EN = {'الجهة':'Side','الإجمالي:':'Total:'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
