"""cleanup 6: the piece rules of composite ad types live in one place (PARTS / GAP).
End gandola = Header x1 + Side x2, Medicated = Header x1 + Side x1, ضفها للسلة = سايد x2 (68x102) + هيدر x4 (20x65), مات فيلم.
Zero behaviour change: every output string stays the same."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'const PARTS=' not in s
rep("const L=s=>s.split(';');", "const L=s=>s.split(';');\n// pieces of composite ad types, used by every total, report, checklist and shortage list\nconst GAP=[['سايد',2,'68×102'],['هيدر',4,'20×65']],GAM='مات فيلم',PARTS={eg:[['Header',1],['Side',2]],md:[['Header',1],['Side',1]],ga:GAP};")
# type definition of ضفها للسلة
rep("z:r=>{const q=+r.q||0;return `سايد 68×102 سم (مات فيلم) ×${2*q} + هيدر 20×65 سم (مات فيلم) ×${4*q}`}",
    "z:r=>{const q=+r.q||0;return GAP.map(([n,f,z])=>`${n} ${z} سم (${GAM}) ×${f*q}`).join(' + ')}")
# End gandola side count in its description
rep("Side ${sd} (${sm}) ×${2*q}", "Side ${sd} (${sm}) ×${PARTS.eg[1][1]*q}")
# summary table of ضفها للسلة
rep("rs.map(r=>{const q=+r.q||0;return `<tr><td>سايد</td><td>68×102 سم</td><td>مات فيلم</td><td>${2*q}</td><td>${esc(r.nt||'')}</td></tr><tr><td>هيدر</td><td>20×65 سم</td><td>مات فيلم</td><td>${4*q}</td><td></td></tr>`}).join('')",
    "rs.map(r=>{const q=+r.q||0;return GAP.map(([n,f,z],i)=>`<tr><td>${n}</td><td>${z} سم</td><td>${GAM}</td><td>${f*q}</td><td>${i?'':esc(r.nt||'')}</td></tr>`).join('')}).join('')")
# totals under each type
rep(" if(t.id=='eg')return 'Header '+q+' · Side '+2*q;\n if(t.id=='md')return 'Header '+q+' · Side '+q;\n if(t.id=='ga')return 'سايد '+2*q+' · هيدر '+4*q;\n",
    " if(PARTS[t.id])return PARTS[t.id].map(([n,f])=>n+' '+f*q).join(' · ');\n")
# sizes report
rep("if(t.id=='ga'){k(GAN+' - سايد','68×102','مات فيلم',2*q,0,t.n);k(GAN+' - هيدر','20×65','مات فيلم',4*q,0,t.n);continue}",
    "if(t.id=='ga'){GAP.forEach(([n,f,z])=>k(GAN+' - '+n,z,GAM,f*q,0,t.n));continue}")
rep("k('End gandola - Side',x[3],x[4],2*q);if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','—','أكريليك',2*q)",
    "k('End gandola - Side',x[3],x[4],PARTS.eg[1][1]*q);if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','—','أكريليك',PARTS.eg[1][1]*q)")
# management report
rep("x.q+=q;x.header+=q;x.side+=2*q;", "x.q+=q;x.header+=PARTS.eg[0][1]*q;x.side+=PARTS.eg[1][1]*q;")
# all-pharmacies aggregation
rep("if(t.id=='ga'){k(GAN+' - سايد',sc,2*q,0);k(GAN+' - هيدر',sc,4*q,0);continue}k(t.n,sc,q,t.m?t.m(r):0);if(t.id=='eg')k('End gandola (Side)',sc,2*q,0)",
    "if(t.id=='ga'){GAP.forEach(([n,f])=>k(GAN+' - '+n,sc,f*q,0));continue}k(t.n,sc,q,t.m?t.m(r):0);if(t.id=='eg')k('End gandola (Side)',sc,PARTS.eg[1][1]*q,0)")
# shortages
rep("o.push({...b,nm:r.nm,pt:'Side',sz:m?m[3]:'—',mat:m?m[4]:'—',q:2*q,v:2*v,d:2*d});return}",
    "const f=PARTS.eg[1][1];o.push({...b,nm:r.nm,pt:'Side',sz:m?m[3]:'—',mat:m?m[4]:'—',q:f*q,v:f*v,d:f*d});return}")
rep("if(t.id=='ga'){o.push({...b,nm:'',pt:'سايد',sz:'68×102',mat:'مات فيلم',q:2*q,v:2*v,d:2*d});o.push({...b,nm:'',pt:'هيدر',sz:'20×65',mat:'مات فيلم',q:4*q,v:4*v,d:4*d});return}",
    "if(t.id=='ga'){GAP.forEach(([n,f,z])=>o.push({...b,nm:'',pt:n,sz:z,mat:GAM,q:f*q,v:f*v,d:f*d}));return}")
# piece counts (progress) and month stats
rep("const pcs=t=>t.id=='ga'?6:t.id=='eg'?3:t.id=='md'?2:1;", "const pcs=t=>PARTS[t.id]?PARTS[t.id].reduce((a,x)=>a+x[1],0):1;")
rep("q+=(+r.q||0)*(t.id=='ga'?6:1);", "q+=(+r.q||0)*(t.id=='ga'?pcs(t):1);")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
