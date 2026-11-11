"""v1.9 part 1: warehouse also keeps Acrylic letters (by item: section, letter height, sentence width), Wall Sticker, Die Cut and
Acrylic boards (shelf-independent); '📦 من المخزن' button on existing rows (letters: any stock of the same section);
roll requests moved from p.rr (the management report extra rows) to p.rolls."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'whFrom' not in s
rep("const WXT=['ws','al','ab','dc','so'];", "const WXT=['so'],NOSH=['ws','al','ab','dc'];")
rep(" else if(t.id=='wh'){L.push({ty:t.n,nm,sec,size:wood(r)?(r.len||'')+'':szOf(z),mat:mtOf(z),f:wood(r)?1:(+r.len||0)/100})}",
    " else if(t.id=='wh'){L.push({ty:t.n,nm,sec,size:wood(r)?(r.len||'')+'':szOf(z),mat:mtOf(z),f:wood(r)?1:(+r.len||0)/100})}\n else if(t.id=='al'){L.push(r.pc?{ty:t.n,nm:'قطع 30×30',sec:r.sec,size:'30×30',mat:SZ('mt.al'),f:1}:{ty:t.n,nm:'',sec:r.sec,size:`حروف ${r.lh||'—'} سم · عرض ${r.w||'—'} سم`,mat:SZ('mt.al'),f:1})}\n else if(t.id=='ws'){L.push({ty:t.n,nm:r.kd||'',sec:r.sec,size:`${r.h}×${r.w}`,mat:SZ('mt.ws'),f:1})}\n else if(t.id=='ab'){const a=ABV(r.it);L.push({ty:t.n,nm:r.it,sec:'',size:a[0],mat:a[1],f:1})}")
rep(" return L.map(x=>Object.assign(x,{sh}))}", " return L.map(x=>Object.assign(x,{sh:NOSH.includes(t.id)?-1:sh}))}")
rep("${x.ty==RLTY?`<span class=\"rshc\">${rlTxt(x.qty)}</span>`:`<span class=\"rshc\">${SH[x.sh]||'—'}</span>`}", "${x.ty==RLTY?`<span class=\"rshc\">${rlTxt(x.qty)}</span>`:x.sh>=0?`<span class=\"rshc\">${SH[x.sh]||'—'}</span>`:''}")
JS = r"""// take from the warehouse for an item already in the pharmacy (what is not received yet); letters: any stock of the same section
function whFromOpts(p,t,r){if(!p||p._wh||!WU().length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),o=[];const L=whRowPlan(t,r,p.sh);
 if(L&&need>0&&L.nm>0)o.push({k:'x',n:Math.min(need,L.nm),txt:`${Math.min(need,L.nm)} ${['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة'} (نفس المقاس)`});
 if(L&&L.np>0)o.push({k:'p',n:L.np,txt:whTxt({nm:0,np:L.np,nps:L.nps,K:L.K},t)});
 if(t.id=='al'&&!r.pc&&need>0){const key=L&&L.M[0]?whKey(L.M[0]):'';WU().filter(x=>x.ty==t.n&&x.sec==r.sec&&+x.qty>=1&&whKey(x)!=key&&x.nm!='قطع 30×30').forEach(x=>o.push({k:'a',id:x.id,n:Math.min(need,Math.floor(+x.qty)),txt:`${Math.min(need,Math.floor(+x.qty))} من ${x.sec} · ${x.size} (في المخزن ${wq(x.qty)})`}))}
 return o}
function whFrom(p,t,r,i){const O=whFromOpts(p,t,r);if(!O.length)return toastT('مفيش حاجة في المخزن للبند ده');
 const tt=toast(`<span>📦 من المخزن للبند ده (${esc(t.n)}):</span>${O.map((o,j)=>`<button class="pr" data-whf2="${j}">اسحب ${esc(o.txt)}</button>`).join('')}<button data-tclose="1">لا</button>`);tt.classList.add('rem');tt._wf={pid:p.id,tid:t.id,i,O};snd('tick')}
function whFrom2(tt,j){const o=tt._wf,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i],c=o.O[j];if(!t||!r||!c)return;
 if(c.k=='a'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,'سحب لبند في الصيدلية (مقاس تاني)');r.wf=(+r.wf||0)+c.n;r.r=Math.min(qn(r),(+r.r||0)+c.n)}
 else{const L=whRowPlan(t,r,p.sh);if(!L)return;if(c.k=='x'){L.np=0;L.nps={};L.nm=Math.min(L.nm,c.n)}else{L.nm=0}whTake(p,t,r,L,'سحب لبند في الصيدلية')}
 sv();tt.remove();render();toastT('✓ اتسحب من المخزن واتحسب مستلم')}
"""
rep("function whPullOffer(p,t,r){", JS + "function whPullOffer(p,t,r){")
rep("<span class=\"bt\"><button data-ed=\"${t.id}:${i}\">${ic('edit')}تعديل</button>", "<span class=\"bt\">${whFromOpts(p,t,r).length?`<button data-whfrom=\"${t.id}:${i}\">📦 من المخزن</button>`:''}<button data-ed=\"${t.id}:${i}\">${ic('edit')}تعديل</button>")
rep(" if(d.whpull){", " if(d.whfrom){const p=curP(),[tid,i]=d.whfrom.split(':'),t=T.find(x=>x.id==tid),r=p&&(p.rows[tid]||[])[+i];if(r)whFrom(p,t,r,+i);return 1}\n if(d.whf2!=null){const tt=b.closest('.toast');if(tt&&tt._wf)whFrom2(tt,+d.whf2);return 1}\n if(d.whpull){")
rep("const PHEDIT=['rreq',", "const PHEDIT=['whfrom','whf2','rreq',")
# roll requests: own field p.rolls (p.rr is the management report extra rows)
for a, b in [("const rr=p.rr||{},ks=Object.keys(rr);if(!ks.length)return '';const rr", None)]:
    pass
rep("p.rr=p.rr||{};const c=p.rr[k]||0;p.rr[k]=c?Math.max(0,c+n):n;if(!p.rr[k])delete p.rr[k];", "p.rolls=p.rolls||{};const c=p.rolls[k]||0;p.rolls[k]=c?Math.max(0,c+n):n;if(!p.rolls[k])delete p.rolls[k];")
s = s.replace("p.rr||{}", "p.rolls||{}")
rep("function mig(p){mig2(p);migHR(p);migCK(p);migPK(p);", "function mig(p){mig2(p);migHR(p);migCK(p);migPK(p);if(p.rr&&!Array.isArray(p.rr)){if(Object.keys(p.rr).length)p.rolls=Object.assign(p.rolls||{},p.rr);p.rr=[]}")
assert "p.rr||{}" not in s and "p.rr[" not in s.replace("p.rr[]","")
EN = {'📦 من المخزن':'📦 From stock','مفيش حاجة في المخزن للبند ده':'Nothing in stock for this item','📦 من المخزن للبند ده':'📦 From stock for this item','(نفس المقاس)':'(same size)','✓ اتسحب من المخزن واتحسب مستلم':'✓ Taken from stock and counted as received','قطع 30×30':'30×30 pieces'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add, 'rolls refs', s.count('p.rolls'))
