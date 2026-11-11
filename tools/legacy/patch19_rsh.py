"""v1.4 part 3: optional shelf type per item (Floor Header, Wall Header, End cap, End gandola, Medicated)."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'const RSHT=' not in s
# helpers (top of script, next to PARTS)
rep("PARTS={eg:[['Header',1],['Side',2]],md:[['Header',1],['Side',1]],ga:GAP};",
    "PARTS={eg:[['Header',1],['Side',2]],md:[['Header',1],['Side',1]],ga:GAP};\n// an item may sit on a different shelf type than the pharmacy (e.g. vitamins on New Turkish); '' / 'زي الصيدلية' = the pharmacy's\nconst RSHT=['fh','wh','ec','eg','md'],RSAME='زي الصيدلية',rsh=(r,s)=>{const i=r&&r.rsh?SH.indexOf(r.rsh):-1;return i>=0?i:s},rshT=(r,s)=>{const i=r&&r.rsh?SH.indexOf(r.rsh):-1;return i>=0&&i!==s?` <small class=\"rshc\">رفوف ${SH[i]}</small>`:''};")
# field + description/sizes follow the item's shelf type
rep("T.forEach(t=>{if(t.f)t.f.push({k:'nt',l:'ملاحظات (اختياري)'})});",
    "T.forEach(t=>{if(RSHT.includes(t.id)){t.f.push(sel('rsh','نوع الرفوف',()=>[RSAME].concat(SH)));const z0=t.z;t.z=(r,x)=>z0(r,rsh(r,x))}if(t.f)t.f.push({k:'nt',l:'ملاحظات (اختياري)'})});")
rep("const opts=(f,r,s)=>f.o(r,s);", "const opts=(f,r,s)=>f.o(r,f.k=='rsh'?s:rsh(r,s));")
# duplicate check: 'same as pharmacy' and an old item without the field are the same
rep("const sg=y=>JSON.stringify(t.f.filter(f=>f.k!='q'&&f.k!='nt').map(f=>y[f.k]));", "const sg=y=>JSON.stringify(t.f.filter(f=>f.k!='q'&&f.k!='nt').map(f=>f.k=='rsh'&&(!y[f.k]||y[f.k]==RSAME)?'':y[f.k]));")
# pharmacy page rows
rep("${esc(t.z(r,s))}${r.q!=null&&!t.nq?` <b>×${r.q}</b>`:''}", "${esc(t.z(r,s))}${rshT(r,s)}${r.q!=null&&!t.nq?` <b>×${r.q}</b>`:''}")
# print summary
i = s.index('function sumHtml(p){'); j = s.index('\nfunction ', i + 5); b = s[i:j]; b0 = b
def rb(a, c, n=1):
    global b
    if b.count(a) != n: sys.exit(f'SUM COUNT {b.count(a)}!={n}: {a[:100]}')
    b = b.replace(a, c)
rb("if(t.id==='eg'){\n   tb+=", "if(t.id==='eg'){const pk=rs.some(r=>rsh(r,s)===2);\n   tb+=")
rb("${s===2?'<th>Side Acrylic Pocket</th>':''}", "${pk?'<th>Side Acrylic Pocket</th>':''}")
rb("rs.map(r=>{const b=r.sz==='كبير',hh=String(SZ(b?'eg.hl':'eg.hs')[s]).replace(/\\s+/g,''),ss=String(SZ(b?'eg.sl':'eg.ss')[s]).replace(/\\s+/g,'');",
   "rs.map(r=>{const b=r.sz==='كبير',s2=rsh(r,s),hh=String(SZ(b?'eg.hl':'eg.hs')[s2]).replace(/\\s+/g,''),ss=String(SZ(b?'eg.sl':'eg.ss')[s2]).replace(/\\s+/g,'');")
rb("<td>${esc(r.sz||'—')} · Header ${esc(hh)} / Side ${esc(ss)} سم</td>", "<td>${esc(r.sz||'—')} · Header ${esc(hh)} / Side ${esc(ss)} سم${rshT(r,s)}</td>")
rb("${s===2?'<td>1L + 1R</td>':''}", "${pk?'<td>'+(s2===2?'1L + 1R':'—')+'</td>':''}")
rb("pl+=`<tr><td>${t.n}</td><td>${esc(t.z(r,s))}</td>", "pl+=`<tr><td>${t.n}</td><td>${esc(t.z(r,s))}${rshT(r,s)}</td>")
rb("material=SZ('mt.fh')[s]}", "material=SZ('mt.fh')[rsh(r,s)]}")
rb("const fm=' · '+SZ('mt.fh')[s];", "const fm=' · '+SZ('mt.fh')[rsh(r,s)];")
rb("<small>${esc(details)}</small></td>", "<small>${esc(details)}${rshT(r,s)}</small></td>")
rb(":`<td>${esc(details)}</td>`}", ":`<td>${esc(details)}${rshT(r,s)}</td>`}")
s = s[:i] + b + s[j:]
# Medicated table
rep("<br>Side ${SZ('md.s')[s]} · ${SZ('mt.md')}</td>", "<br>Side ${SZ('md.s')[rsh(r,s)]} · ${SZ('mt.md')}${rshT(r,s)}</td>")
# sizes report + shortages (Medicated side by the item's shelf)
rep("SZ('md.s')[p.sh]", "SZ('md.s')[rsh(r,p.sh)]", 2)
# management report: End gandola grouped per shelf type of the item
rep("const q=+r.q||0,key=String(r.nm||'')+'|'+String(r.sz||'');let x=eg.find(y=>y._key===key);if(!x){x={kind:'eg',_key:key,n:'End gandola',sz:r.nm||'—',mat:'',q:0,header:0,side:0,pocket:p.sh===2?'1L + 1R':'',shelf:p.sh};eg.push(x)}",
    "const q=+r.q||0,sh=rsh(r,p.sh),key=String(r.nm||'')+'|'+String(r.sz||'')+(sh!==p.sh?'|'+sh:'');let x=eg.find(y=>y._key===key);if(!x){x={kind:'eg',_key:key,n:'End gandola',sz:r.nm||'—',mat:'',q:0,header:0,side:0,pocket:sh===2?'1L + 1R':'',shelf:sh};eg.push(x)}")
rep("if(p.sh===2)x.pocket='1L + 1R';", "if(sh===2)x.pocket='1L + 1R';")
# checklist / execution rows and shortages show the tag
rep("${esc(sc||'—')}</td><td>${esc(dt)}</td>", "${esc(sc||'—')}</td><td>${esc(dt)}${rshT(x.r,x.s)}</td>")
rep("<td>${esc(x.sz||'—')}</td><td>${esc(x.mat||'—')}</td><td>${x.q}</td>", "<td>${esc(x.sz||'—')}${rshT(x.r,x.p.sh)}</td><td>${esc(x.mat||'—')}</td><td>${x.q}</td>")
CSS = "\n.rshc{display:inline-block;background:#E8EEF9;color:#12305C;border:1px solid #B9C8E6;border-radius:6px;padding:0 6px;font-size:10.5px;font-weight:800;margin-inline-start:4px;white-space:nowrap}:root[data-th=dark] .rshc{background:#1C2A44;color:#BFD3FF;border-color:#33507E}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'زي الصيدلية': 'Same as pharmacy', 'رفوف': 'shelves'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a, c in EN.items():
    if a not in D: D[a] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("changes:['Maintenance (الصيانة):", "changes:['Shelf type per item (optional) for Floor Header, Wall Header, End cap, End gandola and Medicated: sizes and material follow the item shelf type, a tag shows it everywhere','Maintenance (الصيانة):")
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
