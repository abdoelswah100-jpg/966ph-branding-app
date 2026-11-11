"""v1.5 part 3: End gandola on Old Turkish: 'المطلوب' = كامل / باك لايت + ستيكر بس / أكريليك بس; the acrylic pocket is its own line everywhere."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'EGPO' not in s
# helpers next to EGR
rep("const EGR=/Header (\\S+) \\((.+?)\\) ×\\d+ \\+ Side (\\S+) \\((.+?)\\) ×\\d+/;",
    "const EGR=/Header (\\S+) \\((.+?)\\) ×\\d+ \\+ Side (\\S+) \\((.+?)\\) ×\\d+/;\n// Old Turkish gondola: what is needed (old items = full)\nconst EGPO=['كامل','باك لايت + ستيكر بس','أكريليك بس'];\nconst egpOf=(r,s)=>rsh(r,s)!==2?'':(EGPO.includes(r.egp)?r.egp:EGPO[0]),egHS=(r,s)=>egpOf(r,s)!==EGPO[2],egPK=(r,s)=>rsh(r,s)===2&&egpOf(r,s)!==EGPO[1];")
# field + text of the item
rep("sel('sz','الحجم',(r,s)=>s==2?['قياسي']:['صغير','كبير']),num('q','عدد الهيدر')],",
    "sel('sz','الحجم',(r,s)=>s==2?['قياسي']:['صغير','كبير']),Object.assign(sel('egp','المطلوب',()=>EGPO),{hide:(d,s)=>rsh(d,s)!==2}),num('q','عدد الجندولات')],")
rep("return `${r.nm} · Header ${h} (${hm}) ×${q} + Side ${sd} (${sm}) ×${PARTS.eg[1][1]*q}${s==2?` + Side Acrylic Pocket (1L + 1R)`:''}`}},",
    "const e=s==2?(EGPO.includes(r.egp)?r.egp:EGPO[0]):'';if(e==EGPO[2])return `${r.nm} · Side Acrylic Pocket (1L + 1R) ×${q}`;\n  return `${r.nm} · Header ${h} (${hm}) ×${q} + Side ${sd} (${sm}) ×${PARTS.eg[1][1]*q}${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket (1L + 1R)`:''}`}},")
# form: hidden fields
rep("function form0(t,s){const d=draft(t,s);return t.f.filter((f,i,a)=>a.findIndex(y=>y.k==f.k)==i)", "function form0(t,s){const d=draft(t,s);return t.f.filter((f,i,a)=>a.findIndex(y=>y.k==f.k)==i&&!(f.hide&&f.hide(d,s)))")
# sizes report: pocket even without header/side
rep("if(t.id=='eg'){const x=EGR.exec(z);if(x){k('End gandola - Header',x[1],x[2],q);k('End gandola - Side',x[3],x[4],PARTS.eg[1][1]*q);if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','—','أكريليك',PARTS.eg[1][1]*q)}continue}",
    "if(t.id=='eg'){const x=EGR.exec(z);if(x){k('End gandola - Header',x[1],x[2],q);k('End gandola - Side',x[3],x[4],PARTS.eg[1][1]*q)}if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','1L + 1R','أكريليك',PARTS.eg[1][1]*q);continue}")
# management report: the pocket is its own row (from the sizes rows), gondola rows only header / side
rep("const raw=sizeRows(P).filter(x=>!['End gandola - Header','End gandola - Side','Side Acrylic Pocket'].includes(x.n));", "const raw=sizeRows(P).filter(x=>!['End gandola - Header','End gandola - Side'].includes(x.n));")
rep("for(const p of P)for(const r of (p.rows&&p.rows.eg)||[]){const q=+r.q||0,sh=rsh(r,p.sh),", "for(const p of P)for(const r of (p.rows&&p.rows.eg)||[]){if(!egHS(r,p.sh))continue;const q=+r.q||0,sh=rsh(r,p.sh),")
rep("pocket:sh===2?'1L + 1R':'',shelf:sh};eg.push(x)}", "pocket:'',shelf:sh};eg.push(x)}")
rep("if(sh===2)x.pocket='1L + 1R';}", "}")
# print summary: gondola table without the pocket column + its own table for the pocket
i = s.index("if(t.id==='eg'){const pk=rs.some(r=>rsh(r,s)===2);"); j = s.index("continue;\n  }", i) + len("continue;\n  }")
NEW = r"""if(t.id==='eg'){const hs=rs.filter(r=>egHS(r,s)),pk=rs.filter(r=>egPK(r,s)),tg=r=>{const e=egpOf(r,s);return e&&e!=EGPO[0]?` <small class="rshc">${esc(e)}</small>`:''},nmc=r=>imgOf(r.nm,r.sec)?`<td class="nic"><img class="nimg" src="${imgOf(r.nm,r.sec)}" alt=""><small>${esc(r.nm)}</small></td>`:`<td>${esc(r.nm)}</td>`;
   if(hs.length)tb+=`<h3>${t.n}</h3><div class="sc"><table><tr><th>المسمى</th><th>المقاس</th><th>Header (العدد)</th><th>Side (العدد)</th><th>ملاحظات</th></tr>`+hs.map(r=>{const b=r.sz==='كبير',s2=rsh(r,s),hh=String(SZ(b?'eg.hl':'eg.hs')[s2]).replace(/\s+/g,''),ss=String(SZ(b?'eg.sl':'eg.ss')[s2]).replace(/\s+/g,'');return `<tr>${nmc(r)}<td>${esc(r.sz||'—')} · Header ${esc(hh)} / Side ${esc(ss)} سم${rshT(r,s)}${tg(r)}</td><td>${+r.q||0}</td><td>${2*(+r.q||0)}</td><td>${esc(r.nt||'')}</td></tr>`}).join('')+'</table></div>'+qtyBox(hs,t);
   if(pk.length){const n=pk.reduce((a,r)=>a+(+r.q||0),0);tb+=`<h3>Side Acrylic Pocket</h3><div class="sc"><table><tr><th>الجندولة</th><th>المقاس</th><th>الخامة</th><th>العدد</th><th>ملاحظات</th></tr>`+pk.map(r=>`<tr>${nmc(r)}<td>1L + 1R${rshT(r,s)}${tg(r)}</td><td>أكريليك</td><td>${+r.q||0}L + ${+r.q||0}R</td><td>${esc(egHS(r,s)?'':r.nt||'')}</td></tr>`).join('')+(pk.length>1?`<tr class="tot"><td colspan=5><b>إجمالي Side Acrylic Pocket: ${2*n} قطعة (${n}L + ${n}R)</b></td></tr>`:'')+'</table></div>'}
   continue;
  }"""
s = s[:i] + NEW + s[j:]
# warehouse: the pocket is its own stock item; acrylic only -> no header / side
rep("if(t.id=='eg'){const m=EGR.exec(z);if(m){L.push({ty:'End gandola - Header',nm,sec,size:m[1],mat:m[2],f:PARTS.eg[0][1]});L.push({ty:'End gandola - Side',nm,sec,size:m[3],mat:m[4],f:PARTS.eg[1][1]})}}",
    "if(t.id=='eg'){const m=EGR.exec(z);if(m){L.push({ty:'End gandola - Header',nm,sec,size:m[1],mat:m[2],f:PARTS.eg[0][1]});L.push({ty:'End gandola - Side',nm,sec,size:m[3],mat:m[4],f:PARTS.eg[1][1]})}if(/Acrylic Pocket/.test(z))L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:'1L + 1R',mat:'أكريليك',f:PARTS.eg[1][1]})}")
rep("'End gandola - Header','End gandola - Side','Medicated - Header'", "'End gandola - Header','End gandola - Side','Side Acrylic Pocket','Medicated - Header'")
rep("'End gandola: 2 Sides per Header (same size); Old Turkish adds Side Acrylic Pocket 1L + 1R'", "'End gandola: 2 Sides per Header (same size); Old Turkish: needed = full (header + side + Side Acrylic Pocket 1L + 1R) / backlight + sticker only / acrylic only; the pocket is its own line'")
CSS = ""
EN = {'المطلوب':'Needed','كامل':'Full','باك لايت + ستيكر بس':'Backlight + sticker only','أكريليك بس':'Acrylic only','عدد الجندولات':'Gondolas','الجندولة':'Gondola','إجمالي Side Acrylic Pocket':'Total Side Acrylic Pocket'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
# totals per ad type: acrylic-only gondolas are not header / side; the pocket is counted on its own
s = open(P, encoding='utf-8').read()
rep("function tTot(t,rs){const q=rs.reduce((a,r)=>a+(r.q==null?1:(+r.q||0)),0);", "function tTot(t,rs,s){const q=rs.reduce((a,r)=>a+(r.q==null?1:(+r.q||0)),0);\n if(t.id=='eg'&&s!=null){const hq=rs.filter(r=>egHS(r,s)).reduce((a,r)=>a+(+r.q||0),0),pq=rs.filter(r=>egPK(r,s)).reduce((a,r)=>a+(+r.q||0),0);return PARTS.eg.map(([n,f])=>n+' '+f*hq).join(' · ')+(pq?' · Side Acrylic Pocket '+2*pq:'')}")
rep("const v=tTot(t,p.rows[t.id]),m=", "const v=tTot(t,p.rows[t.id],p.sh),m=")
open(P, 'w', encoding='utf-8').write(s)
print('ok totals')
