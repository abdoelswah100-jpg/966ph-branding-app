"""v1.6 part 3: warehouse pull / print-missing per part group (header + side apart from the acrylic pocket),
section not repeated in warehouse names, rows waiting in 'إضافة للمخزن' kept until saved or cancelled."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:140]}')
    s = s.replace(a, b)
assert 'function whRowPlan' not in s
i = s.index('function whPullOffer(p,t,r){'); j = s.index('// maintenance: ask before taking from stock', i)
NEW = r"""// what the stock can cover for one row: header / side (and other parts) together, the Old Turkish acrylic pocket on its own
function whRowPlan(t,r,sh,st){const P=whParts(t,r,sh);if(!P.length)return null;const M=P.filter(y=>!y.pk),K=P.filter(y=>y.pk),qty=y=>st?(st[whKey(y)]||0):(+(whFind(whKey(y))||{}).qty||0);
 const nm=M.length?Math.min(Math.max(0,qn(r)-(+r.wf||0)),...M.map(y=>y.f>0?Math.floor((qty(y)+1e-9)/y.f):0)):0,np=K.length?Math.min(Math.max(0,egPq(r,sh)-(+r.wfp||0)),Math.floor((qty(K[0])+1e-9)/PARTS.eg[1][1])):0;return {M,K,nm,np}}
const whTxt=(L,t)=>[L.nm>0?`${L.nm} ${['eg','md'].includes(t&&t.id)?'هيدر وسايد':t&&t.id=='ga'?'طقم':'قطعة'}`:'',L.np>0?`${L.np} جيب أكريليك (1L + 1R)`:''].filter(Boolean).join(' + ');
function whTake(p,t,r,L,note){L.M.forEach(y=>{const x=whFind(whKey(y));if(x&&L.nm>0)whAdd(x,-L.nm*y.f,'out','ph:'+p.no,note)});if(L.np>0){const x=whFind(whKey(L.K[0]));if(x)whAdd(x,-L.np*PARTS.eg[1][1],'out','ph:'+p.no,note);r.wfp=(+r.wfp||0)+L.np;r.rp=Math.min(egPq(r,p.sh),pkv(r,'r')+L.np)}
 if(L.nm>0){r.wf=(+r.wf||0)+L.nm;r.r=Math.min(qn(r),(+r.r||0)+L.nm)}return L.nm+L.np}
function whPullOffer(p,t,r){if(!p||p._wh||!WU().length)return;const L=whRowPlan(t,r,p.sh);if(!L||!(L.nm>0||L.np>0))return;
 const tt=toast(`<span>📦 موجود في المخزن للبند ده (${esc(t.n)}${r.nm?' · '+esc(r.nm):''}): <b>${whTxt(L,t)}</b>. تسحبهم للصيدلية؟</span><button class="pr" data-whpull="1">اسحب</button><button data-tclose="1">لا</button>`);tt.classList.add('rem');tt._wp={pid:p.id,tid:t.id,i:(p.rows[t.id]||[]).indexOf(r)};snd('tick')}
function whPull(tt){const o=tt._wp,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i];if(!t||!r)return;const L=whRowPlan(t,r,p.sh);if(!L)return;const tx=whTxt(L,t);
 whTake(p,t,r,L,'سحب لبند في الصيدلية');sv();tt.remove();render();toastT(`✓ اتسحب من المخزن (${tx}) واتحسبوا مستلمين`)}
"""
s = s[:i] + NEW + s[j:]
# print only what is missing: per part group, a gondola can become "backlight + sticker only" or "acrylic only" in the net summary
i = s.index('function whNet(p){'); j = s.index('function sxBox(p,N){', i)
s = s[:i] + r"""function whNet(p){const c=JSON.parse(JSON.stringify(p)),st={},used=[];WU().forEach(x=>{const k=whKey(x);st[k]=(st[k]||0)+(+x.qty||0)});
 TY(c).forEach(t=>{const rs=c.rows[t.id];if(t.auto||!rs||!rs.length)return;c.rows[t.id]=rs.map((r,i)=>{const sub=t.id=='eg'&&egSub(r,c.sh);let q=qn(r)-(+r.wf||0),pq=sub?egPq(r,c.sh)-(+r.wfp||0):0;
   const L=whRowPlan(t,r,c.sh,st);if(L&&(L.nm>0||L.np>0)){L.M.forEach(y=>st[whKey(y)]=wq((st[whKey(y)]||0)-L.nm*y.f));if(L.np>0)st[whKey(L.K[0])]=wq((st[whKey(L.K[0])]||0)-L.np*PARTS.eg[1][1]);used.push({tid:t.id,i,n:L.nm,np:L.np,tx:whTxt(L,t),t:t.n,z:t.z(r,c.sh)});q-=L.nm;pq-=L.np}
   if(sub){if(q<=0&&pq<=0)return null;if(q<=0){r.egp=EGPO[2];r.q=pq;delete r.pq;return r}if(pq<=0)r.egp=EGPO[1];else r.pq=pq;r.q=q;return r}
   if(q<=0)return null;if(r.q!=null)r.q=q;return r}).filter(Boolean)});
 const pre=TY(p).reduce((a,t)=>a+(p.rows[t.id]||[]).reduce((b,r)=>b+Math.min(qn(r),+r.wf||0)+(+r.wfp||0),0),0);return {p:c,used,pre}}
""" + s[j:]
rep("${N.used.map(u=>`<small>• ${esc(u.t)} · ${esc(u.z)} — <b>${u.n}</b></small>`).join('')}", "${N.used.map(u=>`<small>• ${esc(u.t)} · ${esc(u.z)} — <b>${esc(u.tx)}</b></small>`).join('')}")
i = s.index('function sxPull(p){'); j = s.index('\n', i)
s = s[:i] + "function sxPull(p){const N=whNet(p);let n=0;N.used.forEach(u=>{const t=T.find(x=>x.id==u.tid),r=(p.rows[u.tid]||[])[u.i];if(!t||!r)return;const L=whRowPlan(t,r,p.sh);if(L)n+=whTake(p,t,r,L,'سحب لملخص الطباعة')});sv();snd('ok');render();toastT(`✓ اتسحب ${n} من المخزن واتحسبوا مستلمين`)}" + s[j:]
rep("if(tt&&tt._wp)whPull(tt,+d.whpull);", "if(tt&&tt._wp)whPull(tt);")
# section not repeated
rep("const whKey=x=>", "const whNm=x=>x.sec&&String(x.nm||'').startsWith(x.sec)?String(x.nm):[x.sec,x.nm].filter(Boolean).join(' · ');\nconst whKey=x=>")
n1 = s.count("[x.sec,x.nm].filter(Boolean).join(' · ')") - 1  # the helper itself
s = s.replace("const whNm=x=>x.sec&&String(x.nm||'').startsWith(x.sec)?String(x.nm):[x.sec,x.nm].filter(Boolean).join(' · ');", "@@WHNM@@")
s = s.replace("[x.sec,x.nm].filter(Boolean).join(' · ')", "whNm(x)")
s = s.replace("[x.ty,x.sec,x.nm].filter(Boolean).join(' · ')", "[x.ty,whNm(x)].filter(Boolean).join(' · ')")
s = s.replace("@@WHNM@@", "const whNm=x=>x.sec&&String(x.nm||'').startsWith(x.sec)?String(x.nm):[x.sec,x.nm].filter(Boolean).join(' · ');")
rep("esc([x.sec,x.nm,x.size,SH[x.sh]].filter(Boolean).join(' · '))", "esc([whNm(x),x.size,SH[x.sh]].filter(Boolean).join(' · '))")
# rows waiting in 'إضافة للمخزن' survive closing the app
rep("function WHP(){if(!WHPO)WHPO={id:-7,_wh:1,no:'المخزن',sh:+(DB.cfg.whsh||0),rows:{},an:{},st:'جاري',uid:U().id};return WHPO}",
    "const WHAK=()=>'wha966:'+(U().id||'');\nfunction WHP(){if(!WHPO){let rows={};try{rows=JSON.parse(localStorage.getItem(WHAK())||'{}')||{}}catch(e){}WHPO={id:-7,_wh:1,no:'المخزن',sh:+(DB.cfg.whsh||0),rows,an:{},st:'جاري',uid:U().id}}return WHPO}\nfunction whaKeep(){try{const n=whaN();if(n)localStorage.setItem(WHAK(),JSON.stringify(WHPO.rows));else localStorage.removeItem(WHAK())}catch(e){}}")
rep("function whaHtml(){const p=WHP(),n=whaN();", "function whaHtml(){const p=WHP(),n=whaN();whaKeep();")
rep(" WHPO=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT(`✓ اتضاف ${n} صنف للمخزن`)}", " WHPO.rows={};whaKeep();WHPO=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT(`✓ اتضاف ${n} صنف للمخزن`)}")
rep("if(whaN()&&!confirm('البنود دي ما اتحفظتش في المخزن. تلغيها؟'))return 1;WHPO=null;", "if(whaN()&&!confirm('البنود دي ما اتحفظتش في المخزن. تلغيها؟'))return 1;WHP().rows={};whaKeep();WHPO=null;")
EN = {'طقم':'set','موجود في المخزن للبند ده':'In the warehouse for this item','هيدر وسايد':'header and side','جيب أكريليك (1L + 1R)':'acrylic pocket (1L + 1R)','تسحبهم للصيدلية؟':'Take them for the pharmacy?','اسحب':'Take','اتسحب من المخزن':'Taken from the warehouse','واتحسبوا مستلمين':'and counted as received'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add, 'whNm uses', s.count('whNm(x)'))
