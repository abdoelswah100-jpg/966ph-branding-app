// ---------- v3.7: End gandola parts (per gandola factors; empty field = automatic 1 header / 2 sides / 0 acrylic) ----------
const egSet=v=>v!==undefined&&v!==null&&v!=='';
const egRd=x=>Math.round((+x||0)*100)/100;
function egFh(r){if(!r||!egSet(r.eh))return 1;const q=qn(r);return q>0?Math.max(0,+r.eh||0)/q:0}
function egFs(r){if(!r||!egSet(r.es))return PARTS.eg[1][1];const q=qn(r);return q>0?Math.max(0,+r.es||0)/q:0}
function egFa(r){if(!r||!egSet(r.ea)||+r.ea<=0)return 0;const q=qn(r);return q>0?(+r.ea)/q:0}
function egSz(r,s){const b=r.sz=='كبير',c=x=>String(x).replace(/\s+/g,'');return {h:c(SZ(b?'eg.hl':'eg.hs')[s]),sd:c(SZ(b?'eg.sl':'eg.ss')[s]),hm:SZ('mt.egh')[s],sm:SZ('mt.egs')[s]}}

// ---------- v3.7: Floor Header «رولاند» ----------
const ROLM=' · رولاند';
const rolOn=()=>!(DB.cfg&&DB.cfg.rolOff);
function rolOpts(p,t,r){if(!p||p._wh||p._rc||t.id!='fh'||!rolOn())return [];const need=Math.max(0,qn(r)-(+r.r||0));if(!need)return [];const sz=v=>String(v||'').replace(/\s+/g,''),P=whParts(t,r,p.sh)[0];if(!P)return [];
 return WU().filter(x=>x.rol&&+x.qty>=1&&x.ty==P.ty&&x.nm==P.nm&&x.sec==P.sec&&sz(x.size)==sz(P.size)).sort((a,b)=>(a.sh==P.sh?0:1)-(b.sh==P.sh?0:1)).map(x=>{const n=Math.min(need,Math.floor(+x.qty));return {k:'a',id:x.id,n,rol:1,txt:`🖨 ${n} رولاند (مات فيلم) · ${x.size}${x.sh!=P.sh?' · من مخزن '+SH[x.sh]:''} (في المخزن ${wq(x.qty)})`}}).filter(o=>o.n>0)}
function rolBar(){const L=WU().filter(x=>x.rol),n=wq(L.reduce((a,x)=>a+(+x.qty||0),0));if(!rolOn())return '';return `<div class="rolbar"><span>🖨 Floor Header رولاند: <b>${n}</b> قطعة في ${L.length} صنف${L.length?'':' (ضيفه من «إضافة للمخزن» وعلّم «رولاند»)'}</span><button class="np" data-rolx="1">قفل رولاند</button></div>`}
function v37Click(d,b){
 if(d.whrolf){V.wf=V.wf||{};V.wf.rol=!V.wf.rol;if(V.wf.rol)V.wf.sh='';render();return 1}
 if(d.rolx){const n=wq(WU().filter(x=>x.rol).reduce((a,x)=>a+(+x.qty||0),0));if(confirm('قفل خيار رولاند؟'+(n?'\nلسه فيه '+n+' قطعة رولاند في المخزن (هتفضل في القائمة، بس مش هتتعرض للسحب).':'')+'\nتقدر تفتحه تاني من «إضافة للمخزن».')){DB.cfg.rolOff=1;sv();render()}return 1}
 if(d.rolon){delete DB.cfg.rolOff;sv();render();return 1}
 if(d.whimp){const i=$('#whimpin');if(i)i.click();return 1}
 if(d.whimgo){whImpGo();return 1}
 return 0}
function v37Change(x){
 if(x.id=='whrol'){V.whRol=x.checked;render();return 1}
 if(x.id=='whimpin'){const f=x.files&&x.files[0];x.value='';if(f)f.text().then(t=>{let q;try{q=JSON.parse(t)}catch(e){return alert('ملف غير صالح')}whImpOpen(q,f.name)});return 1}
 return 0}

// ---------- v3.7: warehouse import ----------
let WIMP=null;
function whImpNorm(z){const shi=typeof z.sh=='number'?z.sh:SH.indexOf(String(z.sh||''));const ty_=String(z.ty||'').trim();return {sh:shi>=0&&!NOSHT().has(ty_)?shi:-1,ty:ty_,nm:(ty_==RLTY&&String(z.nm||'').trim()=='رملي')?'ثلجي شفاف':String(z.nm||'').trim(),sec:String(z.sec||'').trim(),mat:String(z.mat||'').trim(),size:String(z.size||'').trim().replace(/\s*[x×*]\s*/i,'×'),qty:wq(+z.qty||0),old:z.old?1:0,real:z.real?String(z.real).trim():'',solo:z.solo?1:0,rol:z.rol?1:0,unit:z.unit||''}}
function whImpOpen(q,fn){const L=(q.items||[]).map(whImpNorm).filter(x=>x.ty&&x.qty>0);if(!L.length)return alert('الملف مفيهوش أصناف صالحة');WCK=null;WIMP={L,fn:fn||'ملف'};const NB=L.filter(x=>!whImpOk(x)).length;cShClose();const el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>📥 استيراد ${L.length} صنف للمخزن</b><small>${esc(WIMP.fn)}${q.note?' · '+esc(q.note):''}. الأصناف بتتضاف على الرصيد الحالي، ومفيش حاجة بتتمسح.${NB?'<br><b class="wimpbad">⚠ '+NB+' صنف مش مطابق لأسماء ومقاسات البرنامج: هيتضافوا، بس مش هيتسحبوا لأي صيدلية. راجعهم قبل الإضافة.</b>':''}</small>
 <div class="cnpl">${L.map(x=>{const e=WU().find(y=>whKey(y)==whKey(x));return `<div class="cnpi"><b>+${wq(x.qty)}</b><span>${esc(x.ty)}${x.nm?' · '+esc(x.nm):''}${x.sec?' · '+esc(x.sec):''}<small>${esc(x.size||'—')}${x.real?' (فعلي '+esc(x.real)+')':''} · ${esc(x.mat||'—')} · ${x.sh>=0?SH[x.sh]:'—'}${x.old?' · 🕰 تصميم قديم':''}${x.rol?' · 🖨 رولاند':''}${e?' · الرصيد دلوقتي '+wq(e.qty):' · صنف جديد'}${whImpOk(x)?'':'<b class="wimpbad"> · ⚠ مش مطابق — مش هيتسحب</b>'}</small></span></div>`}).join('')}</div>
 <div class="cshr"><button class="pr" data-whimgo="1">${ic('check')}ضيفهم للمخزن</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function whImpGo(){if(!WIMP)return;let n=0;WIMP.L.forEach(z=>{const o={sh:z.sh,ty:z.ty,nm:z.nm,sec:z.sec,mat:z.mat,size:z.size};if(z.old)o.old=1;const x=whAdd(o,z.qty,'in','import','استيراد من ملف · '+WIMP.fn);if(z.old)x.old=1;if(z.real)x.real=z.real;if(z.solo)x.solo=1;if(z.rol)x.rol=1;if(z.unit)x.unit=z.unit;n++});WIMP=null;cShClose();sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتضاف '+n+' صنف للمخزن')}
