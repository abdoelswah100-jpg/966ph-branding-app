"""v1.8 part 2: sticker rolls in the warehouse (meters, 50 m a roll) and the 'needs a roll' alert for تخطيط in the print summary
(alert outside the sent part; a requested roll shows inside the print summary)."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'RLTY' not in s
rep("const whUnit=ty=>ty=='Wall Header'?'متر':'قطعة';", "const whUnit=ty=>ty=='Wall Header'||ty==RLTY?'متر':'قطعة';")
JS = r"""// ---- sticker rolls: width 1 m, 50 m a roll; stock in meters
const RLTY='رول ستيكر',RLM=50,RLK=['تخطيط','ثلجي شفاف','أخرى'],RLS=['Beauty','Personal','Health','Baby','Pharmacy','Mizan'];
const rlTxt=m=>{m=wq(m);const n=Math.floor((m+1e-9)/RLM),r=wq(m-n*RLM);return n&&r?`${n} رول + ${r} م`:n?`${n} رول`:`${r} م`};
const rlStock=sec=>wq(WU().filter(x=>x.ty==RLTY&&x.nm=='تخطيط'&&x.sec==sec).reduce((a,x)=>a+(+x.qty||0),0));
// linear meters of تخطيط needed per section: each piece laid on a 1 m wide roll the short way (approximate, no waste)
function rlNeed(p){const o={};(p.rows.ws||[]).forEach(r=>{if(r.kd!='تخطيط')return;const h=+r.h||0,w=+r.w||0,q=+r.q||0;if(!h||!w||!q)return;const op=[];if(w<=100)op.push(h);if(h<=100)op.push(w);const len=op.length?Math.min(...op):h*w/100;o[r.sec]=wq((o[r.sec]||0)+len*q/100)});return o}
function rlBox(p){const N=rlNeed(p),ks=Object.keys(N);if(!ks.length)return '';const rr=p.rr||{};
 return `<div class="sxw rlw np"><b>${ic('box')} رولات التخطيط (تنبيه ليك بس، مش بيتبعت)</b>${ks.map(k=>{const st=rlStock(k),def=N[k]>st,c=rr[k];return `<div class="rlr${def?' bad':''}"><span><b style="${bgc(COL[k]||'#999')};padding:0 6px;border-radius:6px">${esc(k)}</b> محتاج حوالي <b>${N[k]} م</b> · في المخزن <b>${st?rlTxt(st):'0'}</b> ${def?'← <b class="c-exp">⚠ محتاج رول</b>':'← ✓ يكفي'}</span>${c?`<span class="rlq">مطلوب ${c} رول <button class="np" data-rreq="${esc(k)}:-1">−</button><button class="np" data-rreq="${esc(k)}:1">+</button></span>`:`<button class="${def?'pr':''}" data-rreq="${esc(k)}:${Math.max(1,Math.ceil((N[k]-st)/RLM))}">اطلب رول</button>`}</div>`}).join('')}<small>الحساب تقريبي: كل قطعة على رول عرضه 1 م، من غير الهالك.</small></div>`}
const rlReqHtml=p=>{const rr=p.rr||{},ks=Object.keys(rr).filter(k=>rr[k]>0);return ks.length?`<h3>مطلوب رولات</h3><div class="sc"><table><tr><th>الرول</th><th>القسم</th><th>المقاس</th><th>العدد</th></tr>${ks.map(k=>`<tr><td>تخطيط</td><td style="${bgc(COL[k]||'#999')};font-weight:700">${esc(k)}</td><td>عرض 1 م × ${RLM} م</td><td><b>${rr[k]} رول</b></td></tr>`).join('')}</table></div>`:''};
const rlReqTxt=p=>{const rr=p.rr||{},ks=Object.keys(rr).filter(k=>rr[k]>0);return ks.length?['','مطلوب رولات:'].concat(ks.map(k=>`  - تخطيط ${k} · عرض 1 م × ${RLM} م × ${rr[k]} رول`)):[]};
// add rolls to the warehouse
function whrHtml(){const d=V.wr=V.wr||{k:'تخطيط',sec:'Beauty',x:'',n:'',m:''};const tot=(+d.n||0)*RLM+(+d.m||0);
 return `<div class="wcard ced"><h2>${ic('box')}إضافة رول ستيكر</h2><p class="sub">الرول عرضه 1 متر وطوله ${RLM} متر. الرصيد بيتحسب بالمتر.</p><div class="fm">
 <label>النوع<select data-wrf="k">${RLK.map(x=>`<option${x==d.k?' selected':''}>${x}</option>`).join('')}</select></label>
 ${d.k=='تخطيط'?`<label>القسم<select data-wrf="sec">${RLS.map(x=>`<option${x==d.sec?' selected':''}>${x}</option>`).join('')}</select></label>`:''}${d.k=='أخرى'?`<label>اسم النوع<input data-wrf="x" value="${esc(d.x)}"></label>`:''}
 <div class="c2"><label>رولات جديدة (كل رول ${RLM} م)<input type="number" inputmode="numeric" min="0" data-wrf="n" value="${esc(d.n)}"></label><label>رول مفتوح: الباقي منه (متر)<input type="number" inputmode="decimal" min="0" data-wrf="m" value="${esc(d.m)}"></label></div>
 <div class="ph"><small>هيتضاف: <b id="wrtot">${wq(tot)} م${tot?' = '+rlTxt(tot):''}</b></small></div></div>
 <div class="tt"><button class="pr big" data-wrsave="1">${ic('check')}حفظ في المخزن</button><button data-wrx="1">إلغاء</button></div></div>`}
function whrSave(){const d=V.wr,tot=wq((+d.n||0)*RLM+(+d.m||0));if(!(tot>0))return alert('اكتب عدد الرولات أو الباقي بالمتر');if(d.k=='أخرى'&&!String(d.x||'').trim())return alert('اكتب اسم النوع');
 whAdd({sh:-1,ty:RLTY,nm:d.k=='أخرى'?String(d.x).trim():d.k,sec:d.k=='تخطيط'?d.sec:'',mat:'',size:'عرض 1 م'},tot,'in','manual','رول ستيكر');V.wr=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتضاف '+rlTxt(tot))}
function rlClick(d){
 if(d.whr){V.wr=null;goV({v:'whr',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.wrsave){whrSave();return 1}if(d.wrx){V.wr=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.rreq){const p=curP();if(!p)return 1;const i=d.rreq.lastIndexOf(':'),k=d.rreq.slice(0,i),n=+d.rreq.slice(i+1);p.rr=p.rr||{};const c=p.rr[k]||0;p.rr[k]=c?Math.max(0,c+n):n;if(!p.rr[k])delete p.rr[k];sv();render();return 1}
 return 0}
function rlChange(x){if(x.dataset&&x.dataset.wrf&&V.wr){V.wr[x.dataset.wrf]=x.value;if(x.tagName=='SELECT')render();return 1}return 0}
document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.wrf&&V.wr&&x.tagName=='INPUT'){V.wr[x.dataset.wrf]=x.value;const t=$('#wrtot');if(t){const v=wq((+V.wr.n||0)*RLM+(+V.wr.m||0));t.textContent=v+' م'+(v?' = '+rlTxt(v):'')}}});
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("||x15Click(d,b))return;", "||x15Click(d,b)||rlClick(d))return;")
rep("||x15Change(x))return;", "||x15Change(x)||rlChange(x))return;")
rep("const PHEDIT=['sxpull',", "const PHEDIT=['rreq','sxpull',")
rep("const STEDIT=['wha',", "const STEDIT=['whr','wrsave','wha',")
rep("wh:'wh',whe:'wh',wha:'wh',", "wh:'wh',whe:'wh',wha:'wh',whr:'wh',")
rep("const PARENT={ued:'usr',wha:'wh',", "const PARENT={ued:'usr',whr:'wh',wha:'wh',")
rep(" if(V.v=='wha'){", " if(V.v=='whr'){a.innerHTML=hdr('<button data-wrx=\"1\">‹ المخزن</button>','إضافة رول ستيكر')+`<main>${whrHtml()}</main>`;return}\n if(V.v=='wha'){")
rep("<button class=\"lnk\" data-whadd=\"1\">إضافة صنف بمقاس خاص (كتابة يدوي) ›</button>`}", "<button class=\"lnk\" data-whr=\"1\">إضافة رول ستيكر (تخطيط / ثلجي شفاف) ›</button><button class=\"lnk\" data-whadd=\"1\">إضافة صنف بمقاس خاص (كتابة يدوي) ›</button>`}")
# list: rolls show meters + rolls, no shelf chip
rep("<span class=\"rshc\">${SH[x.sh]||'—'}</span>", "${x.ty==RLTY?`<span class=\"rshc\">${rlTxt(x.qty)}</span>`:`<span class=\"rshc\">${SH[x.sh]||'—'}</span>`}")
rep("'Medicated - Header','Medicated - Side',GAN+' - سايد',GAN+' - هيدر','أخرى']))];", "'Medicated - Header','Medicated - Side',GAN+' - سايد',GAN+' - هيدر',RLTY,'أخرى']))];")
# print summary: alert outside, requested rolls inside
rep("${!c&&!m?sxBox(p,whNet(p)):''}", "${!c&&!m?rlBox(p)+sxBox(p,whNet(p)):''}")
rep("return `<div class=\"ph\">${logoChip(22)}<b>${PL(p)}</b><small>${esc(RL(p))} · ${SH[s]}</small></div>`+metaHtml(p)+tSum(p)+tb", "return `<div class=\"ph\">${logoChip(22)}<b>${PL(p)}</b><small>${esc(RL(p))} · ${SH[s]}</small></div>`+metaHtml(p)+tSum(p)+rlReqHtml(p)+tb")
rep("  if(t.m){const x=totRows(rs,t);for(const k in x.g)o.push(`  ${k}: ${x.g[k].toFixed(2)} م²`);o.push(`  إجمالي أمتار الصيدلية: ${x.tot.toFixed(2)} م²`)}}\n return o.join('\\n')}",
    "  if(t.m){const x=totRowsK(rs,t);for(const k in x.g)o.push(`  ${k}: ${x.g[k].toFixed(2)} م²`);o.push(`  إجمالي أمتار الصيدلية: ${x.tot.toFixed(2)} م²`)}}\n o.push(...rlReqTxt(p));return o.join('\\n')}")
CSS = "\n.rlw .rlr{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;border-top:1px dashed var(--ln);padding-top:6px}.rlw .rlr.bad{background:#FFF5F5;border-radius:8px;padding:6px}:root[data-th=dark] .rlw .rlr.bad{background:#3A1A1C}.rlw .rlq{display:flex;gap:4px;align-items:center;font-weight:800}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'رول ستيكر':'Sticker roll','ثلجي شفاف':'Clear frosted','رولات التخطيط (تنبيه ليك بس، مش بيتبعت)':'Planning rolls (for you only, not sent)','محتاج حوالي':'needs about','في المخزن':'in stock','⚠ محتاج رول':'⚠ needs a roll','✓ يكفي':'✓ enough','اطلب رول':'Request a roll','مطلوب':'Requested','رول':'roll','الحساب تقريبي: كل قطعة على رول عرضه 1 م، من غير الهالك.':'Approximate: each piece on a 1 m wide roll, no waste.','مطلوب رولات':'Rolls requested','الرول':'Roll','إضافة رول ستيكر':'Add a sticker roll','إضافة رول ستيكر (تخطيط / ثلجي شفاف) ›':'Add a sticker roll (planning / clear frosted) ›','اسم النوع':'Type name','رولات جديدة (كل رول 50 م)':'New rolls (50 m each)','رول مفتوح: الباقي منه (متر)':'Open roll: meters left','هيتضاف:':'Will be added:','اكتب عدد الرولات أو الباقي بالمتر':'Enter the rolls or the meters left','اكتب اسم النوع':'Enter the type name','الرول عرضه 1 متر وطوله 50 متر. الرصيد بيتحسب بالمتر.':'A roll is 1 m wide and 50 m long. Stock is counted in meters.'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
