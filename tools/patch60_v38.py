"""v3.8: End gandola pulled part by part (what is in stock is taken, the rest stays a shortage); Old Turkish
«مزيلات عرق طبية» header uses the Care (عناية) side; Fridge sticker two kinds everywhere (one total in the management
report); items that do not depend on the shelf type kept in one stock (Fridge, Care 4 life, Camera, ضفها للسلة, Door
sticker, + the existing ones); Acrylic board A3 names; automatic acrylic boards by modification type."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'abNm(' not in s
JS, CSS, EN = [], [], {}

# =====================================================================
# 0. shared constants (next to the acrylic boards list, so they exist before anything renders)
# =====================================================================
rep("const ABI=['Decorative nail',",
    "const ABN=['انسى الانتظار','ارباحي','اترك لهم الباقي','يحظر صرف دواء','الضمان الصحي','نقاتي stc'],ABA3='Acrylic board A3',abNm=r=>r?(r.it==ABA3&&r.an&&ABN.includes(r.an)?r.it+' · '+r.an:r.it||''):'';\n"
    "const FRK=['ثلاجة عصير','ثلاجة أدوية'],frAd=k=>'Fridge sticker - '+(k||FRK[0]);\n"
    "const EGS2={'Personal · Premium Deo · مزيلات عرق طبية':'عناية'},egSN=(r,sh)=>sh==2&&r&&EGS2[r.nm]?{nm:EGS2[r.nm],sec:''}:null,egX=(r,ep)=>+(r&&r['wx'+ep])||0,egXs=r=>egX(r,'h')+egX(r,'s')+egX(r,'a');\n"
    "const ABI=['Decorative nail',")
rep("const ABD=()=>['Acrylic board pockets 5','Acrylic board pockets 4','No smoking acrylic'].map(i=>({it:i,q:1,stt:'تصنيع وتركيب'}));",
    "const ABD0=()=>['Acrylic board pockets 5','Acrylic board pockets 4','No smoking acrylic'].map(i=>({it:i,q:1,stt:'تصنيع وتركيب'}));\n"
    "// automatic boards of a new pharmacy: Branding modification = install only (No smoking made + installed), new Branding = made + installed, maintenance = none\n"
    "const ABD=mod=>{if(mod===undefined)return ABD0();if(mod=='صيانة')return [];const m=mod=='تعديل براندنج'?'تركيب فقط':'تصنيع وتركيب';return ABN.slice(0,5).map(n=>({it:ABA3,an:n,q:1,stt:m})).concat([{it:'Acrylic board pockets 4',q:1,stt:m},{it:'Acrylic board pockets 5',q:1,stt:m},{it:'No smoking acrylic',q:1,stt:'تصنيع وتركيب'}])};")
rep("const isABD0=r=>r&&ABD().some", "const isABD0=r=>r&&ABD0().some")

# =====================================================================
# 1. Acrylic board A3 names
# =====================================================================
rep("{id:'ab',n:'Acrylic boards',f:[sel('it','البند',()=>ABI),Q,",
    "{id:'ab',n:'Acrylic boards',f:[sel('it','البند',()=>ABI),Object.assign(sel('an','اسم اللوحة',()=>['غير محدد',...ABN]),{hide:d=>d.it!=ABA3}),Q,")
rep("z:r=>`${r.it} · ${ABV(r.it).join(' · ')} · ${stD(r.stt)}`}]", "z:r=>`${abNm(r)} · ${ABV(r.it).join(' · ')} · ${stD(r.stt)}`}]")
rep("else if(t.id=='ab'){const a=ABV(r.it);L.push({ty:t.n,nm:r.it,", "else if(t.id=='ab'){const a=ABV(r.it);L.push({ty:t.n,nm:abNm(r),")
rep("const nm=t.id=='so'?son(r):r.nm||r.it||r.kd||'',", "const nm=t.id=='so'?son(r):t.id=='ab'?abNm(r):r.nm||r.it||r.kd||'',")
rep("if(t.id=='ab'){const a=ABV(r.it);k(r.it,a[0],a[1],q,0,t.n,0,stD(r.stt)||'—');continue}",
    "if(t.id=='ab'){const a=ABV(r.it);k(abNm(r),a[0],a[1],q,0,t.n,0,stD(r.stt)||'—');continue}")
rep("const sc=t.id=='ab'?r.it:scOf(r)", "const sc=t.id=='ab'?abNm(r):t.id=='fr'?(r.kd||''):scOf(r)")
# automatic boards by modification type
rep("rows:mod=='صيانة'?{}:{ab:ABD()}", "rows:mod=='صيانة'?{}:{ab:ABD(mod)}")
rep("rows:($('#pmod').value||'')=='صيانة'?{}:{ab:ABD()}", "rows:($('#pmod').value||'')=='صيانة'?{}:{ab:ABD($('#pmod').value||'براندنج جديد')}")
rep("if(x.id=='pmod'){if(V.v=='ph'||V.v=='qe'){curP().mod=x.value;sv()}}",
    "if(x.id=='pmod'){if(V.v=='ph'||V.v=='qe'){const p_=curP(),ch_=abModCh(p_,p_.mod,x.value);p_.mod=x.value;sv();if(ch_){render();toastT('✓ لوحات الأكريليك اتظبطت على «'+x.value+'»')}}}")
JS.append(r"""// ---------- v3.8: acrylic boards ----------
const abSig=a=>(a||[]).map(r=>[r.it,r.an||'',+r.q||0,r.stt||''].join('|')).sort().join('#');
const abUntouched=a=>(a||[]).every(r=>!r.r&&!r.x&&!r.nt&&!r.xi&&!r.wf);
// the modification type changed: boards still as the app put them follow the new type
function abModCh(p,a,b){if(!p||a==b)return 0;const R=p.rows=p.rows||{},cur=R.ab||[];if(!abUntouched(cur)||abSig(cur)!=abSig(ABD(a)))return 0;R.ab=ABD(b);if(!R.ab.length)delete R.ab;return 1}
""")

# =====================================================================
# 2. Fridge sticker: two kinds everywhere, one total in the management report
# =====================================================================
rep(" if(t.id=='al'){const pc=rs.filter(r=>r.pc)",
    " if(t.id=='fr'){const g={};rs.forEach(r=>{const k=r.kd||'—';g[k]=(g[k]||0)+(r.q==null?1:(+r.q||0))});return Object.keys(g).map(k=>k+' '+g[k]).join(' · ')}\n if(t.id=='al'){const pc=rs.filter(r=>r.pc)")
rep("   if(t.id=='cm'){k(t.n,'A5','ستيكر',q);continue}",
    "   if(t.id=='fr'){k(t.n+' - '+(r.kd||'—'),szOf(z),mtOf(z),q,0,t.n);continue}\n   if(t.id=='cm'){k(t.n,'A5','ستيكر',q);continue}")
rep(" const raw=sizeRows(P).filter(x=>!['End gandola - Header','End gandola - Side'].includes(x.n));",
    " const raw=mgMerge(sizeRows(P).filter(x=>!['End gandola - Header','End gandola - Side'].includes(x.n)));")
JS.append(r"""// management report: one line for Fridge sticker and for Acrylic board A3 (the kinds / names are for the work, not the report)
function mgMerge(L){const o=[],m={};L.forEach(x=>{const n=x.ty=='Fridge sticker'?'Fridge sticker':String(x.n).startsWith(ABA3+' · ')?ABA3:x.n;if(n==x.n){o.push(x);return}const k=n+'|'+x.sz+'|'+x.mat+'|'+(x.st||'');if(!m[k]){m[k]=Object.assign({},x,{n,q:0,a:0,lm:0});o.push(m[k])}m[k].q+=x.q;m[k].a+=x.a||0;m[k].lm+=x.lm||0});return o}
""")
rep("const mAds=()=>[...new Set(T.filter(t=>t.id!='ga').map(t=>t.n).concat([",
    "const mAds=()=>[...new Set(T.filter(t=>t.id!='ga').flatMap(t=>t.id=='fr'?FRK.map(frAd):[t.n]).concat([")
rep("o.push(Object.assign({},b,{ad:t.n,det:z,", "o.push(Object.assign({},b,{ad:t.id=='fr'?frAd(r.kd):t.n,det:z,")
rep("(w.ty==x.ad||w.ty.startsWith((x.ad||'')+' -'))", "(w.ty==x.ad||w.ty.startsWith((x.ad||'')+' -')||(/^Fridge sticker - /.test(x.ad||'')&&w.ty=='Fridge sticker'&&w.nm==x.ad.slice(17)))")
rep("(sh==null||w.sh==sh));if(!c.length)return;", "(sh==null||w.sh==sh||w.sh==-1));if(!c.length)return;")

# =====================================================================
# 3. one stock for items that do not depend on the shelf type
# =====================================================================
rep("NOSH=['ws','al','ab','dc'];", "NOSH=['ws','al','ab','dc','fr','c4','cm','ga','ds'];")
rep("if(DB.wh.some(x=>!x.m22))whFix22();", "if(DB.wh.some(x=>!x.m22))whFix22();if(DB.wh.some(x=>!x.m38))whFix38();")
rep("return {sh:shi>=0?shi:-1,ty:String(z.ty||'').trim(),", "const ty_=String(z.ty||'').trim();return {sh:shi>=0&&!NOSHT().has(ty_)?shi:-1,ty:ty_,")
JS.append(r"""// ---------- v3.8: one stock for items that do not depend on the shelf type ----------
function NOSHT(){const o=new Set();T.forEach(t=>{if(!NOSH.includes(t.id))return;if(t.id=='ga')GAP.forEach(([n])=>o.add(GAN+' - '+n));else o.add(t.n)});return o}
function whFix38(){const S=NOSHT(),W=DB.wh;let ch=0;W.forEach(x=>{if(x.m38)return;if(S.has(x.ty)&&x.sh!==-1){x.sh=-1;ch=1}x.m38=1});
 if(ch)for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));W.splice(i,1)}}}
// one time per pharmacy: transferred surplus keys, A3 rows split by name; maintenance fridge lines by kind
function v38Fix(){const S=NOSHT();
 DB.ph.forEach(p=>{if(p.m38)return;
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(e&&S.has(e.ty)&&e.sh!==-1){const y=Object.assign({},e,{sh:-1}),k2=whKey(y);if(o[k2])o[k2].q=wq(+o[k2].q+(+y.q||0));else o[k2]=y}else if(o[k])o[k].q=wq(+o[k].q+(+e.q||0));else o[k]=e});p.whT=o}
  const R=p.rows||{};if(Array.isArray(R.ab)){const o=[];R.ab.forEach(r=>{const q=+r.q||0;if(r&&r.it==ABA3&&!r.an&&(q==5||q==6)){const rr=+r.r||0,xx=+r.x||0,wf=+r.wf||0;
    ABN.slice(0,q).forEach((n,i)=>{const y=Object.assign({},r,{an:n,q:1});if(r.r!=null)y.r=i<rr?1:0;if(r.x!=null)y.x=i<xx?1:0;if(r.wf!=null)y.wf=i<wf?1:0;if(i){delete y._i;delete y.nt;delete y.xi;delete y.xn}o.push(y)})}else o.push(r)});R.ab=o}
  p.m38=1});
 const M=DB.mnt&&DB.mnt.items;if(M&&!DB.mnt.m38){M.forEach(x=>{if(x.ad=='Fridge sticker'){const s=String(x.det||'')+' '+String(x.note||'');const k=/عصير/.test(s)?FRK[0]:/أدوية|ادوية|دواء/.test(s)?FRK[1]:'';if(k)x.ad=frAd(k)}});DB.mnt.m38=1}
 svq()}
""")
rep("try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m22))v22Fix()}catch(e){console.error(e)}",
    "try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m22))v22Fix()}catch(e){console.error(e)}try{if(DB&&DB.ph&&(DB.ph.some(p=>!p.m38)||(DB.mnt&&!DB.mnt.m38)))v38Fix()}catch(e){console.error(e)}")

# =====================================================================
# 4. End gandola part by part; Old Turkish deodorant header uses the Care side
# =====================================================================
rep("if(egFh(r))L.push({ty:'End gandola - Header',nm,sec,size:m.h,mat:m.hm,f:egFh(r)});if(egFs(r))L.push({ty:'End gandola - Side',nm,sec,size:m.sd,mat:m.sm,f:egFs(r)});if(egFa(r))L.push({ty:'End gandola - Side Acrylic',nm,sec,size:m.sd,mat:'أكريليك',f:egFa(r)})",
    "const sn=egSN(r,sh);if(egFh(r))L.push({ty:'End gandola - Header',nm,sec,size:m.h,mat:m.hm,f:egFh(r),ep:'h'});if(egFs(r))L.push({ty:'End gandola - Side',nm:sn?sn.nm:nm,sec:sn?sn.sec:sec,size:m.sd,mat:m.sm,f:egFs(r),ep:'s'});if(egFa(r))L.push({ty:'End gandola - Side Acrylic',nm:sn?sn.nm:nm,sec:sn?sn.sec:sec,size:m.sd,mat:'أكريليك',f:egFa(r),ep:'a'})")
rep("const np=K.reduce((a,y)=>a+nps[y.pk],0);return {M,K,nm,np,nps,lab:mdLab(t,r)}}",
    "const np=K.reduce((a,y)=>a+nps[y.pk],0),pe=t.id=='eg'&&M.some(y=>y.ep),ex=pe?egEx(r,M,0,qty):{};return {M,K,nm:pe?0:nm,np,nps,ex,exAll:pe&&egExAll(r,M,ex),lab:mdLab(t,r)}}")
rep("const whTxt=(L,t)=>[", "const whTxt0=(L,t)=>[")
rep("if(L.nm>0){r.wf=(+r.wf||0)+L.nm;r.r=Math.min(qn(r),(+r.r||0)+L.nm)}return L.nm+L.np}",
    "if(L.nm>0){r.wf=(+r.wf||0)+L.nm;r.r=Math.min(qn(r),(+r.r||0)+L.nm)}const ne=egExTake(p,r,L,note);return L.nm+L.np+ne}")
rep("if(L&&L.np>0)o.push({k:'p',n:L.np,txt:whTxt({nm:0,np:L.np,nps:L.nps,K:L.K},t)});",
    "if(L&&L.np>0)o.push({k:'p',n:L.np,txt:whTxt({nm:0,np:L.np,nps:L.nps,K:L.K},t)});if(L&&need>0&&egExN(L.ex))o.push({k:'e',n:egExN(L.ex),txt:egExT(L.ex)+(L.exAll?'':' — والباقي يتسجل نقص')+egExXT(L)});")
rep("if(c.k=='x'){L.np=0;L.nps={};L.nm=Math.min(L.nm,c.n)}else{L.nm=0}whTake(p,t,r,L,'سحب لبند في الصيدلية')",
    "if(c.k=='x'){L.np=0;L.nps={};L.ex={};L.nm=Math.min(L.nm,c.n)}else if(c.k=='e'){L.np=0;L.nps={}}else{L.nm=0;L.ex={}}whTake(p,t,r,L,'سحب لبند في الصيدلية')")
rep("const L=whRowPlan(t,r,p.sh);if(!L||!(L.nm>0||L.np>0))return;", "const L=whRowPlan(t,r,p.sh);if(!L||!(L.nm>0||L.np>0||egExN(L.ex)))return;")
rep("${whXT(t,r,p.sh,L.nm)} تسحبهم للصيدلية؟</span>", "${whXT(t,r,p.sh,L.nm)}${egExN(L.ex)?egExXT(L)+(L.exAll?'':' (والباقي يتسجل نقص)'):''} تسحبهم للصيدلية؟</span>")
rep("const L=whRowPlan(t,r,c.sh,st);if(L&&(L.nm>0||L.np>0)){", "const L=whRowPlan(t,r,c.sh,st);if(t.id=='eg'&&!ao)q=egNet(r,L,st,used,t,i,c,q);if(L&&(L.nm>0||L.np>0)){")
rep("+(+r.wfpR||0)+(+r.wfpL||0),0),0);return {p:c,used,pre}}", "+(+r.wfpR||0)+(+r.wfpL||0)+(t.id=='eg'?egXs(r):0),0),0);return {p:c,used,pre}}")
JS.append(r"""// print only what is missing: End gandola parts after the stock (each part on its own)
function egNet(r,L,st,used,t,i,c,q){if(!L||!L.M.some(y=>y.ep))return q;const F={h:egFh(r),s:egFs(r),a:egFa(r)},left={};let any=0;
 L.M.forEach(y=>{if(!y.ep)return;const n=(L.ex||{})[y.ep]||0;if(n)st[whKey(y)]=wq((st[whKey(y)]||0)-n);left[y.ep]=Math.max(0,Math.round(F[y.ep]*q-egX(r,y.ep)-n+1e-9));if(left[y.ep])any=1});
 if(egExN(L.ex))used.push({tid:t.id,i,n:0,np:0,tx:egExT(L.ex),xw:egExXT(L),t:t.n,z:t.z(r,c.sh)});
 if(!any)return 0;r.eh=left.h||0;r.es=left.s||0;if(F.a>0)r.ea=left.a||0;return q}
""")
# shortages: parts received from the warehouse count
rep("if(d>0){if(fh)o.push({...b,nm:r.nm,pt:'Header',sz:m.h,mat:m.hm,q:egRd(fh*q),v:egRd(fh*v),d:egRd(fh*q)-egRd(fh*v)});if(f)o.push({...b,nm:r.nm,pt:'Side',sz:m.sd,mat:m.sm,q:egRd(f*q),v:egRd(f*v),d:egRd(f*q)-egRd(f*v)});if(fa)o.push({...b,nm:r.nm,pt:'Side Acrylic',sz:m.sd,mat:'أكريليك',q:egRd(fa*q),v:egRd(fa*v),d:egRd(fa*q)-egRd(fa*v)})}",
    "if(d>0){const sn=egSN(r,rsh(r,p.sh));[['h','Header',fh,m.h,m.hm],['s','Side',f,m.sd,m.sm],['a','Side Acrylic',fa,m.sd,'أكريليك']].forEach(([ep,pt,ff,sz,mat])=>{if(!ff)return;const Q=egRd(ff*q),W=Math.min(Q,egRd(egRd(ff*v)+(k=='r'?egX(r,ep):0)));if(Q>W)o.push({...b,nm:ep!='h'&&sn?sn.nm+' (لـ '+r.nm+')':r.nm,pt,sz,mat,q:Q,v:W,d:egRd(Q-W)})})}")
rep("n+=q*f;d+=(x.r.cx?q:Math.min(q,+x.r[k]||0))*f;", "n+=q*f;d+=(x.r.cx?q:Math.min(q,+x.r[k]||0))*f+(k=='r'&&x.t.id=='eg'&&!x.r.cx&&!egAO(x.r,x.s)?egXs(x.r):0);")
rep("const dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f;", "const dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f+(y.ep?egX(r,y.ep):0);")
JS.append(r"""// ---------- v3.8: End gandola part by part ----------
const EGPN={h:'هيدر',s:'سايد',a:'أكريليك سايد'};
const egExN=ex=>Object.values(ex||{}).reduce((a,n)=>a+(+n||0),0);
const egExT=ex=>Object.keys(ex||{}).filter(k=>ex[k]>0).map(k=>ex[k]+' '+EGPN[k]).join(' + ');
const whTxt=(L,t)=>[whTxt0(L,t),egExT(L&&L.ex)].filter(Boolean).join(' + ');
// what the stock gives for the gondolas it cannot make whole: each part on its own
function egEx(r,M,nm,qty){const o={},rem=Math.max(0,qn(r)-Math.max(+r.r||0,+r.wf||0)-nm);if(!rem)return o;
 M.forEach(y=>{if(!y.ep||!(y.f>0))return;const need=Math.max(0,Math.round(y.f*rem-egX(r,y.ep)+1e-9)),av=Math.floor(qty(y)-nm*y.f+1e-9),n=Math.min(need,Math.max(0,av));if(n>0)o[y.ep]=n});return o}
// the stock covers every part still needed
function egExAll(r,M,ex){const rem=Math.max(0,qn(r)-Math.max(+r.r||0,+r.wf||0));return M.filter(y=>y.ep&&y.f>0).every(y=>(ex[y.ep]||0)>=Math.max(0,Math.round(y.f*rem-egX(r,y.ep)+1e-9)))}
function egExXT(L){const o=new Set();(L.M||[]).forEach(y=>{const n=(L.ex||{})[y.ep];if(n>0)whCross(y,n).forEach(x=>o.add(x))});return o.size?` ⚠ هيتسحب من مخزن ${[...o].join(' و')} (نوع رفوف مختلف، نفس المقاس).`:''}
// parts received count; when every part of one gondola is in, it becomes a received gondola
function egNorm(r){const q=qn(r),F={h:egFh(r),s:egFs(r),a:egFa(r)},E=Object.keys(F).filter(k=>F[k]>0);let g=0;
 if(E.length)while((+r.r||0)<q&&E.every(k=>egX(r,k)+1e-9>=F[k])){E.forEach(k=>r['wx'+k]=egRd(egX(r,k)-F[k]));r.r=(+r.r||0)+1;r.wf=(+r.wf||0)+1;if(++g>999)break}
 ['h','s','a'].forEach(k=>{if((+r.r||0)>=q||!(egX(r,k)>0))delete r['wx'+k]})}
function egExTake(p,r,L,note){let n=0;Object.keys(L.ex||{}).forEach(ep=>{const y=L.M.find(z=>z.ep==ep),c=L.ex[ep];if(!y||!(c>0))return;const g=whTakeQ(y,c,'ph:'+p.no,(note||'')+' (جزء من الجندولة: '+EGPN[ep]+')');r['wx'+ep]=egRd(egX(r,ep)+g);n+=g});if(n)egNorm(r);return n}
""")

# =====================================================================
# write
# =====================================================================
EN.update({'اسم اللوحة':'Board name','غير محدد':'Not set','والباقي يتسجل نقص':'the rest stays a shortage','جندولة كاملة':'full gondola'})
rep("// ---------- v1.5 extras ----------", '\n'.join(JS) + "// ---------- v1.5 extras ----------")
rep("VER='v3.7'", "VER='v3.8'")
rep(" changelog:[{version:'v3.7',", " changelog:[{version:'v3.8',date:'2026-11-10',changes:['End gandola pulled from the warehouse part by part: what is in stock is taken (header, side or side acrylic), the rest stays in the shortages; parts become a received gondola when all are in','Old Turkish «Personal · Premium Deo · مزيلات عرق طبية» End gandola: its own header, the Care (عناية) side','Fridge sticker: ثلاجة عصير and ثلاجة أدوية apart in the summary, reports, sizes, shortages, maintenance and its types; one total in the management report','One warehouse stock for Fridge sticker, Sticker care 4 life, Camera sticker, ضفها للسلة and Door sticker (with Acrylic boards, letters, Wall Sticker, Die Cut): no shelf type warning; existing stock merged','Acrylic board A3 names (انسى الانتظار · ارباحي · اترك لهم الباقي · يحظر صرف دواء · الضمان الصحي · نقاتي stc), own stock per name, existing A3 rows of 5 or 6 split by name; one A3 total in the management report','Automatic acrylic boards: Branding modification = A3 ×5 names + pockets 4 + pockets 5 install only and No smoking made + installed; new Branding = all made + installed; maintenance none; follow a change of the modification type while untouched']},{version:'v3.7',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
