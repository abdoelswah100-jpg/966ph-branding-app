"""v2.3: screw caps (غطاء مسمار) with the side acrylic (pocket / floor 4 per piece, wall 6 per piece): own table under the
side / gandola in the print summary and the management report (requested), taken out of the warehouse by the executed;
alerts only for errors."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'capN' not in s

# ---- alerts: errors only
rep("  if(ws.length && !ws.some(r=>r.sec=='Pharmacy'))a.push('Wall Sticker: لا يوجد سطر لقسم Pharmacy');\n  if(!(R.ds||[]).length)a.push('Door sticker: غير مضاف');\n  if(!(R.c4||[]).length)a.push('Sticker care 4 life: غير مضاف')}",
    "}")
rep("  if(r.lh!==''&&r.lh!=null&&r.h!==''&&r.h!=null&&+r.lh>+r.h)",
    "  if(alMax(r)&&+r.w>alMax(r))a.push(`Acrylic letters (${r.sec}): عرض جملة الحروف ${r.w} أكبر من (عرض التخطيط ${r.tw} − 10) = ${alMax(r)} سم`);\n  if(r.lh!==''&&r.lh!=null&&r.h!==''&&r.h!=null&&+r.lh>+r.h)")

# ---- print summary: caps table right after the last side / gandola section
rep("for(const t of TY(p)){const rs=p.rows[t.id]||[];", "const cL=capLast(p);let cP=0;for(const t of TY(p)){if(cP){tb+=capHtml(p);cP=0}if(t.id===cL)cP=1;const rs=p.rows[t.id]||[];")
rep("+metaHtml(p)+odBanner(p)+tSum(p)+rlReqHtml(p)+tb+curveNote(p)", "+metaHtml(p)+odBanner(p)+tSum(p)+rlReqHtml(p)+tb+(cP?capHtml(p):'')+curveNote(p)")
# ---- management report: caps row, table under the gandola / pockets
rep("return raw.concat(eg,xiList(P0));", "return raw.concat(eg,capRows(P0),xiList(P0));")
rep("ord0=all.filter(x=>x.kind!=='eg'&&x.kind!=='xi')", "ord0=all.filter(x=>x.kind!=='eg'&&x.kind!=='xi'&&x.kind!=='cap'),capR=all.filter(x=>x.kind==='cap')")
rep("return egTable+pkTbl(pkR,hidden)+", "return egTable+pkTbl(pkR,hidden)+capTbl(capR,hidden)+")
# ---- warehouse: add caps, take them by the executed on every save
rep("<button class=\"lnk\" data-whr=\"1\">", "<button class=\"lnk\" data-whcap=\"1\">إضافة غطاء مسمار ›</button><button class=\"lnk\" data-whr=\"1\">")
rep("const STEDIT=[", "const STEDIT=['whcap',")
rep("v21Click(d,b)||", "v21Click(d,b)||v23Click(d,b)||")
rep("const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}", "const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}try{capAuto()}catch(e){console.error(e)}")
rep("q.id=Date.now();q.no=n.trim();delete q.rcv;q.m20=1;", "q.id=Date.now();q.no=n.trim();delete q.rcv;q.m20=1;q.capx=0;q.m23=1;")
rep("try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m22))v22Fix()}catch(e){console.error(e)}", "try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m22))v22Fix()}catch(e){console.error(e)}try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m23)){DB.ph.forEach(p=>{if(!p.m23){p.capx=capN(p,'x');p.m23=1}});svq()}}catch(e){console.error(e)}")

JS = r"""// ---------- v2.3: screw caps with the side acrylic ----------
const CPNM='غطاء مسمار',CAPO={sh:-1,ty:CPNM,nm:'',sec:'',mat:'',size:''};
const CAPS=[['eg','Side Acrylic Pocket (جندولة تركي قديم)',4],['saf','Side Acrylic Shelves Floor',4],['saw','Side Acrylic Shelves Wall',6]];
// pieces of one source: k='q' requested, 'x' executed
function capPcs(p,id,k){const sh=p.sh;return ((p.rows||{})[id]||[]).reduce((a,r)=>{if(id=='eg'){if(!egSub(r,sh))return a;return a+SDS.reduce((b,[sd])=>b+(k=='x'?pkv(r,'x',sd):egN(r,sh,sd)),0)}return a+(k=='x'?(+r.x||0):qn(r))},0)}
const capN=(p,k)=>CAPS.reduce((a,[id,,f])=>a+capPcs(p,id,k)*f,0);
const capLast=p=>{let l=null;TY(p).forEach(t=>{if(CAPS.some(c=>c[0]==t.id)&&capPcs(p,t.id,'q')>0)l=t.id});return l};
function capHtml(p){const L=CAPS.map(([id,n,f])=>[n,capPcs(p,id,'q'),f]).filter(x=>x[1]>0);if(!L.length)return '';const N=L.reduce((a,x)=>a+x[1]*x[2],0);
 return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>مع</th><th>عدد القطع</th><th>لكل قطعة</th><th>عدد الأغطية</th></tr>${L.map(([n,q,f])=>`<tr><td>${esc(n)}</td><td>${q}</td><td>${f}</td><td><b>${q*f}</b></td></tr>`).join('')}<tr class="tot"><td colspan="3"><b>إجمالي ${CPNM}</b></td><td><b>${N} قطعة</b></td></tr></table></div>`}
function capRows(P){const parts=CAPS.map(([id,n,f])=>({n,q:P.reduce((a,p)=>a+capPcs(p,id,'q'),0),f})).filter(x=>x.q>0);if(!parts.length)return [];return [{kind:'cap',n:CPNM,ty:CPNM,sz:'',mat:'',q:parts.reduce((a,x)=>a+x.q*x.f,0),a:0,lm:0,parts}]}
function capTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const x=v[0];return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>مع</th><th>عدد القطع</th><th>لكل قطعة</th><th>عدد الأغطية</th><th class="act">إجراء</th></tr>${x.parts.map(y=>`<tr><td>${esc(y.n)}</td><td>${y.q}</td><td>${y.f}</td><td>${y.q*y.f}</td><td class="act"></td></tr>`).join('')}<tr class="tot"><td colspan="3">إجمالي ${CPNM}</td><td>${x.q} قطعة</td><td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td></tr></table></div>`}
// warehouse: executed caps leave the stock (difference since the last save, p.capx)
function capAuto(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(!p||!p.m23||uStoreRO()||!uEditP(p))return;const t=capN(p,'x'),d=t-(+p.capx||0);if(!d)return;whAdd(CAPO,-d,d>0?'out':'in','ph:'+p.no,d>0?CPNM+' مع السايد أكريليك (متنفذ)':'تصحيح '+CPNM+' (المتنفذ قل)');p.capx=t}
function v23Click(d,b){
 if(d.whcap){const v=prompt('عدد '+CPNM+' اللي هيتضاف للمخزن');const n=Math.round(+String(v||'').replace(/[^\d.]/g,''));if(!(n>0))return 1;whAdd(CAPO,n,'in','manual','إضافة '+CPNM);sv();snd('ok');toastT('✓ اتضاف '+n+' '+CPNM+' للمخزن');render();return 1}
 return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("VER='v2.2'", "VER='v2.3'")
rep(" changelog:[{version:'v2.2',", " changelog:[{version:'v2.3',date:'2026-11-02',changes:['غطاء مسمار: 4 per Side Acrylic Pocket piece (Old Turkish gandola) and per Side Acrylic Shelves Floor piece, 6 per Side Acrylic Shelves Wall piece; own table under the side / gandola in the print summary and the management report (requested); taken out of the warehouse by the executed; add to the warehouse from إضافة للمخزن','Alerts only for errors: no more Door sticker / Care 4 life / Wall Sticker Pharmacy missing; new alert when the letters sentence is wider than tahtit − 10 cm']},{version:'v2.2',")
EN = {'Side Acrylic Pocket (جندولة تركي قديم)':'Side Acrylic Pocket (Old Turkish gandola)','غطاء مسمار':'Screw cap','إضافة غطاء مسمار ›':'Add screw caps ›','لكل قطعة':'Per piece','عدد الأغطية':'Caps','مع':'With','عدد القطع':'Pieces'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
