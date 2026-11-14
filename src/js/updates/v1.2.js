// ---------- v1.2: Medicated Header is one stock for every shelf type ----------
const MDHT='Medicated - Header';
const _whParts12=whParts;whParts=function(t,r,s){return _whParts12(t,r,s).map(y=>y.ty==MDHT?Object.assign(y,{sh:-1}):y)};
const _NOSHT12=NOSHT;NOSHT=function(){const o=_NOSHT12();o.add(MDHT);return o};
// a restore point once the data has loaded (the copy is taken now, before the change)
function snapLater(why,pre){setTimeout(()=>{try{SNAPS.unshift({at:nowIso(),day:TD(),why,db:pre});SNAPS=SNAPS.slice(0,5);if(IDB.ok)idbSet('snaps',SNAPS);else localStorage.setItem('ads_snaps',JSON.stringify(SNAPS.slice(0,3)))}catch(e){}},5000)}
function whFix12(){const W=DB.wh;if(W.some(x=>!x.m12&&x.ty==MDHT&&x.sh!==-1)){try{snapLater('قبل تحديث 1.2 (هيدر المديكيتيد مخزن واحد)',JSON.stringify(dbOut()))}catch(e){}}
 let ch=0;W.forEach(x=>{if(x.m12)return;if(x.ty==MDHT&&x.sh!==-1){x.sh=-1;ch=1}x.m12=1});
 if(ch){for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));if(W[i].min!==''&&W[i].min!=null&&(W[j].min===''||W[j].min==null))W[j].min=W[i].min;W.splice(i,1)}}svq()}}
const _WU12=WU;WU=function(){const W=_WU12();if(W.some(x=>!x.m12))whFix12();return DB.wh};
// transferred surplus of each pharmacy: same keys as the stock
function v12Fix(){DB.ph.forEach(p=>{if(p.m12)return;
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(!e)return;let k2=k;if(e.ty==MDHT&&e.sh!==-1){e.sh=-1;k2=whKey(e)}if(o[k2])o[k2].q=wq(+o[k2].q+(+e.q||0));else o[k2]=e});p.whT=o}
  p.m12=1});svq()}
const _render12=render;render=function(){try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m12))v12Fix()}catch(e){console.error(e)}return _render12.apply(this,arguments)};

// ---------- v1.2: warehouse import — repeated file, restore point + undo, new names ----------
const wiAl=s=>String(s||'').toLowerCase().replace(/[^a-z0-9؀-ۿ]/g,'');
const wiK0=o=>[o.sh,o.ty,nk(o.sec),nk(o.mat),String(o.size||'').replace(/\s+/g,'')].join('|');
const wiBase=x=>x.rol?Object.assign({},x,{mat:String(x.mat||'').replace(ROLM,'')}):x;
let WCL=null;const wiCat=()=>WCL||(WCL=whCatalog());
// the list a new name goes to (the same lists as «➕ مسمى جديد»)
const wiXK=x=>/^ضفها للسلة - /.test(x.ty)?'ga':/^Medicated - /.test(x.ty)?'md':x.ty=='End cap'?'ec:'+x.sec:(x.ty=='Floor Header'||x.ty=='Wall Header')?(x.sec=='Medicated'?'md':'nm:'+x.sec):'';
// same item as the app has, only the name is new
function wiNew(x){if(!x.nm||x.old||whImpOk(x))return '';const k=wiXK(x);if(!k||(/^ec:|^nm:/.test(k)&&!x.sec))return '';const o=wiBase(x),k0=wiK0(o);return wiCat().some(c=>wiK0(c)==k0)?k:''}
// the name differs only in spaces / dots / capitals: take the app's name
function wiFixNm(x){if(!x.nm||x.old||whImpOk(x))return;const o=wiBase(x),k0=wiK0(o),a=wiAl(x.nm),c=wiCat().find(c=>wiK0(c)==k0&&wiAl(c.nm)==a);if(c){x.fx=x.nm;x.nm=c.nm}}
const wiHash=L=>{const s=JSON.stringify(L.map(x=>[whKey(x),x.qty]).sort());let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))|0;return 'h'+(h>>>0).toString(36)};
const wiUnd=()=>DB.cfg.wiU||[];
// the same file (same items and numbers, or the same file name) already imported and not undone
function wiPrev(h,fn){const U=wiUnd();return (DB.wlog||[]).find(e=>e.src=='import'&&!(e.wi&&U.includes(e.wi))&&(e.wh==h||(fn&&e.note=='استيراد من ملف · '+fn)))}
// the last import not undone yet (from 1.2 on): undo again goes one import back
function wiLast(){const W=DB.wlog||[],U=wiUnd(),e=W.find(e=>e.src=='import'&&e.wi&&!U.includes(e.wi));if(!e)return null;const L=W.filter(u=>u.wi==e.wi&&u.src=='import');
 return {wi:e.wi,at:e.at,fn:String(e.note||'').replace('استيراد من ملف · ',''),L,n:new Set(L.map(u=>String(u.id))).size,q:wq(L.reduce((a,u)=>a+(+u.qty||0),0))}}
whImpOpen=function(q,fn){const L=(q.items||[]).map(whImpNorm).filter(x=>x.ty&&x.qty>0);if(!L.length)return alert('الملف مفيهوش أصناف صالحة');WCK=null;WCL=null;
 L.forEach(wiFixNm);const h=wiHash(L),pv=wiPrev(h,fn||'');WIMP={L,fn:fn||'ملف',q,h,dup:!!pv};
 const NW=L.filter(x=>wiNew(x)),NB=L.filter(x=>!whImpOk(x)&&!wiNew(x)).length,NF=L.filter(x=>x.fx).length,nn=[...new Set(NW.map(x=>x.nm))];
 cShClose();const el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>📥 استيراد ${L.length} صنف للمخزن</b><small>${esc(WIMP.fn)}${q.note?' · '+esc(q.note):''}. الأصناف بتتضاف على الرصيد الحالي، ومفيش حاجة بتتمسح. البرنامج بياخد نقطة استرجاع قبل الإضافة، وتقدر تتراجع عن آخر استيراد من «إضافة للمخزن».
 ${pv?`<br><b class="wimpdup">⚠ الملف ده اتستورد قبل كده يوم ${esc(fd(pv.at))}${pv.note?' ('+esc(String(pv.note).replace('استيراد من ملف · ',''))+')':''}. لو ضفته تاني الرصيد هيتضاعف.</b>`:''}
 ${NF?`<br><b class="winew">✎ ${NF} اسم اتصحح لاسم البرنامج (مسافات أو نقط أو حروف كبيرة).</b>`:''}
 ${nn.length?`<br><b class="winew">🆕 ${nn.length} اسم جديد مش في البرنامج: ${nn.map(esc).join('، ')}. هيتضافوا للمخزن، بس مش هيتسحبوا لصيدلية غير لما تضيف الاسم.</b>`:''}
 ${NB?'<br><b class="wimpbad">⚠ '+NB+' صنف مش مطابق لأسماء ومقاسات البرنامج: هيتضافوا، بس مش هيتسحبوا لأي صيدلية. راجعهم قبل الإضافة.</b>':''}</small>
 ${nn.length?`<div class="cshr"><button data-wixn="1">➕ ضيف ${nn.length==1?'الاسم الجديد':nn.length+' أسماء جديدة'} للبرنامج</button></div>`:''}
 <div class="cnpl">${L.map(x=>{const e=WU().find(y=>whKey(y)==whKey(x)),nw=wiNew(x);return `<div class="cnpi"><b>+${wq(x.qty)}</b><span>${esc(x.ty)}${x.nm?' · '+esc(x.nm):''}${x.sec?' · '+esc(x.sec):''}<small>${esc(x.size||'—')}${x.real?' (فعلي '+esc(x.real)+')':''} · ${esc(x.mat||'—')} · ${x.sh>=0?SH[x.sh]:'مشترك'}${x.old?' · 🕰 تصميم قديم':''}${x.rol?' · 🖨 رولاند':''}${e?' · الرصيد دلوقتي '+wq(e.qty):' · صنف جديد'}${x.fx?' · ✎ كان «'+esc(x.fx)+'»':''}${whImpOk(x)?'':nw?'<b class="winew"> · 🆕 اسم جديد</b>':'<b class="wimpbad"> · ⚠ مش مطابق — مش هيتسحب</b>'}</small></span></div>`}).join('')}</div>
 <div class="cshr"><button class="${pv?'':'pr'}" data-whimgo="1">${ic('check')}${pv?'ضيفهم تاني (الرصيد هيتضاعف)':'ضيفهم للمخزن'}</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)};
whImpGo=function(){if(!WIMP)return;if(WIMP.dup&&!confirm('الملف ده اتستورد قبل كده.\nتضيفه تاني والرصيد يتضاعف؟'))return;
 snap('قبل استيراد مخزن · '+WIMP.fn);const wi='i'+Date.now(),h=WIMP.h;let n=0;
 WIMP.L.forEach(z=>{const o={sh:z.sh,ty:z.ty,nm:z.nm,sec:z.sec,mat:z.mat,size:z.size};if(z.old)o.old=1;const nw=!whFind(whKey(o)),x=whAdd(o,z.qty,'in','import','استيراد من ملف · '+WIMP.fn);
  if(DB.wlog[0]){DB.wlog[0].wi=wi;DB.wlog[0].wh=h}if(nw)x.wi=wi;if(z.old)x.old=1;if(z.real)x.real=z.real;if(z.solo)x.solo=1;if(z.rol)x.rol=1;if(z.unit)x.unit=z.unit;n++});
 WIMP=null;cShClose();sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتضاف '+n+' صنف للمخزن')};
function wiAddNames(){if(!WIMP)return;const X=DB.cfg.xn=DB.cfg.xn||{},A=[];WIMP.L.forEach(x=>{const k=wiNew(x);if(!k)return;X[k]=X[k]||[];if(!X[k].some(v=>nk(v)==nk(x.nm))){X[k].push(x.nm);A.push(x.nm)}});
 if(!A.length)return;if(!confirm('هيتضاف للبرنامج '+A.length+' اسم:\n'+[...new Set(A)].join('\n')+'\n\nتقدر تعدّلهم أو تمسحهم من الإعدادات ← المسميات المضافة.')){A.forEach(nm=>Object.keys(X).forEach(k=>{const i=X[k].lastIndexOf(nm);if(i>=0)X[k].splice(i,1)}));return}
 xnApply();WCK=null;WCL=null;sv();toastT('✓ اتضاف '+[...new Set(A)].length+' اسم');whImpOpen(WIMP.q,WIMP.fn)}
function wiUndo(){const o=wiLast();if(!o)return;const m={};o.L.forEach(u=>{m[u.id]=wq((m[u.id]||0)+(+u.qty||0))});
 if(!confirm(`تراجع عن استيراد «${o.fn}» (${fd(o.at)})؟\nهيتخصم ${o.n} صنف · ${o.q} من المخزن.`))return;
 snap('قبل التراجع عن استيراد · '+o.fn);const W=WU(),short=[];let n=0;
 Object.keys(m).forEach(id=>{const x=W.find(y=>String(y.id)==String(id));if(!x){short.push('صنف اتمسح');return}const d=Math.min(m[id],Math.max(0,+x.qty||0));if(d<m[id]-1e-9)short.push((x.nm||x.ty)+' (اتخصم '+wq(d)+' من '+m[id]+')');
  if(d>0){whAdd(x,-d,'out','undo:'+o.wi,'تراجع عن استيراد · '+o.fn);n++}if(x.wi==o.wi&&!(+x.qty>0))W.splice(W.indexOf(x),1)});
 DB.cfg.wiU=wiUnd().concat(o.wi).slice(-50);sv();snd('ok');render();toastT('✓ اتلغى استيراد «'+o.fn+'»');
 if(short.length)setTimeout(()=>alert('فيه أصناف اتسحب منها بعد الاستيراد، فاتخصم الموجود بس:\n'+short.join('\n')),300)}
const _whaHtml12=whaHtml;whaHtml=function(){const h=_whaHtml12(),o=wiLast();if(!o)return h;
 return h.replace('<input type="file" id="whimpin"',`<button class="lnk" data-wiundo="1">↩ تراجع عن آخر استيراد: ${esc(o.fn)} · ${esc(fd(o.at))} (${o.n} صنف · ${o.q}) ›</button><input type="file" id="whimpin"`)};
const _v37Click12=v37Click;v37Click=function(d,b){if(d.wixn){wiAddNames();return 1}if(d.wiundo){wiUndo();return 1}return _v37Click12(d,b)};
