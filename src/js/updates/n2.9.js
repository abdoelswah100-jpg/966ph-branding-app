// ---------- 2.9 (file n2.9.js) ----------
// 1) tab title = app version (build)                       2) old Drive-folder reminder quiet (web link never, local file at most weekly)
// 3) Drive merge keeps photos/attachments with the pharmacy even when its inner id differs; laptop pulls missing photos from the newest full copy
// 4) Drive files list: «كاملة بالصور» first, the others folded  5) warehouse transfer: ✓ per line (unchecked stays pending), material per line
// 6) 🏥 health room button under Wall Sticker                7) Wall Sticker default kind «تخطيط» (core)
// 8) management report: English file names, Excel laid out like the PDF with the logo fixed in the first cell
// A) «✓ الكل» skips swapped / not executed rows (core)        B) transfer lines show the section when there is no name
// C) full backup includes pharmacies on hold (core)           S1) every shared file gets an English name   S2/S3) laptop: clear «not updated» bar, old sync chip hidden while Drive works
// W) Wall Header counted in pieces in the warehouse (was meters); the management report still sums meters from the rows
const C29=()=>DB.cfg.c29=DB.cfg.c29||{};
const mm4=r=>!!r&&(r.mm==4||r.sec==HRI);
const HRB=['نصائح غذائية','الصحة واللياقة','قياس ضغط الدم','العناية بالسكري'],AL4='أكريليك أخضر 4 مم';
(function(){['باب غرفة الصحة','باب غرفة الجمال'].forEach(n=>{if(!SON.includes(n))SON.splice(Math.max(0,SON.indexOf('أخرى')),0,n)})})();
(function(){const t=T.find(x=>x.id=='al');if(!t)return;const z0=t.z;t.z=function(r){const z=z0.apply(this,arguments);return mm4(r)?z.replace(SZ('mt.al'),AL4):z}})();
(function(){const s=document.createElement('style');s.textContent=`.w29 th:first-child,.w29 td:first-child{width:34px}.w29 input[type=checkbox]{width:20px;height:20px}.w29 tr.w29off td{opacity:.45}.w29 select{max-width:128px;font-size:12px;padding:4px}
.hr29b{border:1px dashed #2E7D4F;border-radius:12px;padding:10px;display:grid;gap:6px;margin:6px 0;background:color-mix(in srgb,#2E7D4F 9%,var(--c));min-width:0}.hr29h{display:grid;gap:2px}.hr29h small,.hr29g small{color:var(--mu);overflow-wrap:anywhere}.hr29g{display:grid;gap:3px;border-top:1px solid var(--ln);padding-top:6px;min-width:0}.hr29g .tt{display:flex;flex-wrap:wrap;gap:6px}
.hr29 fieldset{border:1px solid var(--ln);border-radius:10px;padding:8px;display:grid;gap:6px;min-width:0;margin:0}.hr29 legend{font-weight:800;padding:0 4px;max-width:100%}.hr29 legend label{display:flex;gap:6px;align-items:center;white-space:normal}.hr29 .c2{display:grid;grid-template-columns:1fr 1fr;gap:8px}.hr29 input:not([type=checkbox]),.hr29 select,.hr29 textarea{width:100%;box-sizing:border-box}.hr29 small{color:var(--mu)}
.ph29{display:grid;gap:6px;margin:6px 0}.ph29 button,.gd29 button{justify-self:start;white-space:normal;max-width:100%}.gd29{display:grid;gap:6px;margin:8px 0}.gdf29>summary{cursor:pointer;font-weight:800;padding:6px 0}`;document.head.appendChild(s)})();

// ---- W) Wall Header in pieces: one row piece = one stock piece whatever its length (100 / 80 / 50)
const _whParts29=whParts;whParts=function(t,r,s){const L=_whParts29(t,r,s);if(t&&t.id=='wh')L.forEach(y=>{y.f=1});if(t&&t.id=='al'&&mm4(r))L.forEach(y=>{y.mat=AL4});return L};
function whFix29(){const cv=(q,sz)=>{const L=+(String(sz||'').split('×')[1]);return L>0&&L!=85?wq((+q||0)*100/L):(+q||0)};
 (DB.wh||[]).forEach(x=>{if(x.ty!='Wall Header'||x.m29)return;if(x.unit=='متر')x.qty=cv(x.qty,x.size);x.unit='قطعة';x.m29=1});
 const c=C29();if(!c.wlg){(DB.wlog||[]).forEach(e=>{if(e.ty=='Wall Header'&&!e.m29){e.qty=cv(e.qty,e.size);e.m29=1}});c.wlg=1}
 if(!c.wht){DB.ph.concat(typeof HID!='undefined'&&HIDDB===DB?HID:[]).forEach(p=>Object.values(p.whT||{}).forEach(e=>{if(e&&e.ty=='Wall Header'&&!e.m29){e.q=cv(e.q,e.size);e.m29=1}}));c.wht=1}}
const _WU29=WU;WU=function(){if((DB.wh||[]).some(x=>x.ty=='Wall Header'&&!x.m29))whFix29();return _WU29()};

// ---- 5) + B) transfer to the warehouse: choose the lines, change the material
const W29=()=>V.w29=V.w29||{off:{},mat:{}};
whtHtml=function(){const p=curP();if(!p)return '';const L=whPlan(p),S=W29(),M0=p.whM||{},on=x=>!S.off[x.k],add=L.filter(x=>x.dl>0&&on(x)),sub=L.filter(x=>x.dl<0&&on(x)),n=a=>a.reduce((s,x)=>s+Math.abs(x.dl),0),
  mo=m=>[...new Set([m,'ستيكر + أكريليك','أكريليك','ستيكر','باك لايت'].filter(Boolean))],left=L.length-add.length-sub.length;
 return `<div class="wcard"><h2>${ic('box')}يرجع للمخزن — صيدلية ${esc(p.no)}</h2><p class="sub">الراجع = المستلم − المتنفذ − الهالك لكل بند، بنوع رفوف البند. شيل العلامة ✓ من أي سطر مش عايزه يترحّل دلوقتي: هيفضل معلّق ويتعرض عليك تاني. وتقدر تغيّر الخامة قبل الترحيل.</p>
 ${add.length?`<div class="ph"><small>هيتضاف <b>${add.length} صنف · ${wq(n(add))}</b></small></div>`:''}${sub.length?`<div class="alr"><small>⚠ الصيدلية اتعدلت بعد ترحيل سابق: هيتخصم <b>${sub.length} صنف · ${wq(n(sub))}</b></small></div>`:''}${left?`<div class="ywarn">⏸ ${left} سطر معلّق (مش هيترحّل دلوقتي)</div>`:''}
 <div class="sc"><table class="ctab w29"><tr><th>✓</th><th>الصنف</th><th>المقاس</th><th>الخامة</th><th>الرفوف</th><th>الكمية</th><th>السبب</th></tr>${L.map(x=>{const m=S.mat[x.k]||M0[x.k]||x.mat,sb=x.nm?whNm(x):x.sec||'';
  return `<tr class="${on(x)?'':'w29off'}"><td><input type="checkbox" data-w29c="${esc(x.k)}"${on(x)?' checked':''} aria-label="ترحيل السطر"></td><td>${esc(x.ty)}${sb?`<small>${esc(sb)}</small>`:''}</td><td>${esc(x.size||'—')}</td><td>${x.dl>0?`<select data-w29m="${esc(x.k)}">${mo(m).map(o=>`<option${o==m?' selected':''}>${esc(o)}</option>`).join('')}</select>`:esc(m||'—')}</td><td>${esc(SH[x.sh]||'—')}</td><td><b class="${x.dl<0?'c-exp':'c-rem'}">${x.dl>0?'+':''}${x.dl} ${whUnit(x.ty)}</b></td><td><small>${esc(x.dl<0?'اتعدّل بعد الترحيل':(x.why||[]).join(' + ')||'فائض')}</small></td></tr>`}).join('')}</table></div>
 <div class="tt"><button class="pr big" data-whgo="1">${ic('check')}ترحيل ${add.length+sub.length} للمخزن</button><button data-whno="1">تجاهل</button></div></div>`};
whApply=function(){const p=curP();if(!p)return;const S=W29(),L=whPlan(p).filter(x=>!S.off[x.k]);if(!L.length)return alert('مفيش ولا سطر متعلّم عليه ✓');p.whT=p.whT||{};p.whM=p.whM||{};
 L.forEach(x=>{const m=S.mat[x.k]||p.whM[x.k]||x.mat;if(m!=x.mat)p.whM[x.k]=m;whAdd({sh:x.sh,ty:x.ty,nm:x.nm,sec:x.sec,mat:m,size:x.size},x.dl,x.dl>0?'in':'out','ph:'+p.no,x.dl>0?'فائض صيدلية'+(m!=x.mat?' (الخامة: '+m+')':''):'تعديل صيدلية بعد الترحيل');p.whT[x.k]={sh:x.sh,ty:x.ty,nm:x.nm,sec:x.sec,mat:x.mat,size:x.size,q:x.now,m29:1}});
 Object.keys(p.whT).forEach(k=>{if(!p.whT[k].q){delete p.whT[k];delete p.whM[k]}});const left=whPlan(p).length;p.whAt=nowIso();V.w29=null;sv();snd('ok');toastT(`✓ اترحّل ${L.length} صنف للمخزن`+(left?` · ${left} معلّق`:''));goV({v:'ph',p:p.id,op:{},dr:{},q:V.q})};

// ---- 6) 🏥 health room (or beauty room): one screen, every part goes to its own type
function hrOpen(k){const B=k=='b',v=(a,b)=>B?b:a;cShClose();const el=document.createElement('div');el.className='csh';
 const ck=(id,t)=>`<legend><label><input type="checkbox" id="${id}" checked> ${t}</label></legend>`,ni=(id,l,val)=>`<label>${l}<input id="${id}" type="number" inputmode="decimal" value="${val==null?'':val}"></label>`;
 el.innerHTML=`<div class="cshb hr29"><b>${v('🏥 غرفة الصحة','💄 غرفة الجمال')}</b><small>كل جزء بيتضاف في نوعه (ستيكر خارجي · Wall Sticker · حروف أكريليك) عشان المخزن والطباعة وتقرير الإدارة. شيل العلامة من أي جزء مش موجود، وكل بند تقدر تعدّله بعدين من نوعه.</small>
 <label>الغرفة<select id="hr29k"><option value="h"${B?'':' selected'}>غرفة صحة</option><option value="b"${B?' selected':''}>غرفة جمال</option></select></label>
 <fieldset>${ck('hr29d','🚪 الباب — ستيكر خارجي على الزجاج (الباب بس)')}<div class="c2">${ni('hr29dh','الارتفاع (سم)')}${ni('hr29dw','العرض (سم)')}</div></fieldset>
 <fieldset>${ck('hr29r','R · جدار يمين — Wall Sticker')}<label>الاسم<input id="hr29rn" value="${esc(v('اطمئن على صحتك هنا',''))}"></label><div class="c2">${ni('hr29rh','الارتفاع (سم)')}<label>العرض (سم) — أكتر من مقاس: افصل بـ +<input id="hr29rw" inputmode="decimal" placeholder="مثال: 120 + 80"></label></div></fieldset>
 <fieldset>${ck('hr29l','L · جدار يسار — Wall Sticker')}<label>الاسم<input id="hr29ln" value="${esc(v('رعاية بلا حدود',''))}"></label><div class="c2">${ni('hr29lh','الارتفاع (سم)')}<label>العرض (سم) — أكتر من مقاس: افصل بـ +<input id="hr29lw" inputmode="decimal" placeholder="مثال: 100 + 60"></label></div></fieldset>
 <fieldset>${ck('hr29p','💚 خط نبض القلب — '+AL4)}<div class="c2">${ni('hr29ph','الارتفاع (سم)',28)}${ni('hr29pw','العرض (سم)',200)}</div></fieldset>
 <fieldset>${ck('hr29b','🟩 لوحات أكريليك أخضر 30×30 — 4 مم')}${ni('hr29bn','العدد',4)}<label>الأسماء (كل اسم في سطر)<textarea id="hr29bt" rows="4">${esc(v(HRB.join('\n'),''))}</textarea></label></fieldset>
 <fieldset>${ck('hr29o','🔤 حروف خارجية — أكريليك 8 مم')}<label>الجملة<input id="hr29ot" value="${esc(v('عيش الصحة · Live healthy',''))}"></label><div class="c2">${ni('hr29oh','ارتفاع الحروف (سم)',35)}${ni('hr29ow','عرض الجملة (سم)',100)}</div><small>العرض بيتحسب من الارتفاع بنفس نسبة «Health Room – Outside»، وتقدر تعدّله.</small></fieldset>
 <div class="cshr"><button class="pr" data-hr29go="${B?'b':'h'}">إضافة للصيدلية</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function hrGo(k){const p=curP();if(!p)return;const B=k=='b',g=id=>{const e=document.getElementById(id);return e?String(e.value||'').trim():''},on=id=>{const e=document.getElementById(id);return !!(e&&e.checked)},n=id=>+g(id)||0,
  ws=id=>g(id).split(/[+،,\s]+/).map(Number).filter(x=>x>0),lab=B?'غرفة الجمال':'غرفة الصحة',hr='hr'+Date.now(),add=[];
 if(on('hr29d')){if(!n('hr29dh')||!n('hr29dw'))return alert('اكتب ارتفاع وعرض الباب، أو شيل علامته');add.push(['so',{nm:B?'باب غرفة الجمال':'باب غرفة الصحة',h:n('hr29dh'),w:n('hr29dw'),q:1}])}
 for(const[s,t]of[['r','R · جدار يمين'],['l','L · جدار يسار']]){if(!on('hr29'+s))continue;const h=n('hr29'+s+'h'),W=ws('hr29'+s+'w');if(!h||!W.length)return alert('اكتب الارتفاع والعرض لـ «'+t+'»، أو شيل علامته');const nm=g('hr29'+s+'n'),m={};W.forEach(w=>m[w]=(m[w]||0)+1);
  Object.keys(m).forEach(w=>add.push(['ws',{sec:'Health Room',kd:'تخطيط',h,w:+w,q:m[w],nt:t+(nm?': '+nm:'')+' · '+lab}]))}
 if(on('hr29p')){if(!n('hr29ph')||!n('hr29pw'))return alert('اكتب مقاس خط نبض القلب');add.push(['al',{sec:HRI,h:n('hr29ph'),lh:n('hr29ph'),w:n('hr29pw'),wm:1,sz:'غير محدد',ar:'سطر واحد',q:1,nt:'خط نبض القلب · '+lab,mm:4}])}
 if(on('hr29b')){const c=Math.max(1,Math.round(n('hr29bn')||4)),L=g('hr29bt').split(/\n+/).map(x=>x.trim()).filter(Boolean);add.push(['al',{sec:HRI,h:30,lh:'',w:30,sz:'غير محدد',ar:'غير محدد',q:c,nt:'لوحات'+(L.length?': '+L.join(' · '):'')+' · '+lab,pc:1,mm:4}])}
 if(on('hr29o')){if(!n('hr29oh'))return alert('اكتب ارتفاع الحروف الخارجية');const w=n('hr29ow')||ratW(HRO,n('hr29oh'))||'';add.push(['al',{sec:HRO,h:'',lh:n('hr29oh'),w,wm:n('hr29ow')&&n('hr29ow')!=ratW(HRO,n('hr29oh'))?1:0,sz:'غير محدد',ar:'سطر واحد',q:1,nt:(g('hr29ot')||'حروف خارجية')+' · '+lab}])}
 if(!add.length)return alert('اختار جزء واحد على الأقل');p.rows=p.rows||{};add.forEach(([id,r])=>{r.hr=hr;(p.rows[id]=p.rows[id]||[]).push(r)});p.modAt=nowIso();sv();snd('ok');cShClose();V.op.ws=true;render();toastT(`✓ اتضاف ${add.length} بند لـ ${lab}`)}
function hrLine(id,r){if(id=='so')return 'الباب · '+r.h+'×'+r.w+' سم';if(id=='ws')return 'Wall Sticker · '+String(r.nt||'').replace(/ · غرفة (الصحة|الجمال)$/,'')+' · '+r.h+'×'+r.w+(r.q>1?' ×'+r.q:'');
 return String(r.nt||'').replace(/ · غرفة (الصحة|الجمال)$/,'')+' · '+(r.pc?'30×30 ×'+r.q:(r.lh||'—')+'×'+(r.w||'—'))+' · '+(mm4(r)?AL4:'أكريليك 8 مم')}
function hrBlock(p){const A=[];['so','ws','al'].forEach(id=>((p.rows||{})[id]||[]).forEach(r=>{if(r.hr)A.push({id,r})}));const G=[...new Set(A.map(x=>x.r.hr))];
 return `<div class="hr29b"><div class="hr29h"><b>🏥 غرفة الصحة</b><small>${A.length?A.length+' بند متوزعين على الستيكر الخارجي و Wall Sticker والحروف':'الباب + جدار يمين ويسار + نبض القلب واللوحات + الحروف الخارجية، في شاشة واحدة'}</small></div>
 ${G.map(h=>{const L=A.filter(x=>x.r.hr==h),bt=/غرفة الجمال/.test(L.map(x=>x.r.nt||'').join(' '))?'غرفة الجمال':'غرفة الصحة';return `<div class="hr29g"><b>${bt}</b>${L.map(x=>`<small>• ${esc(hrLine(x.id,x.r))}</small>`).join('')}<div class="tt"><button data-hr29del="${esc(h)}">${ic('trash')}حذف الغرفة</button></div></div>`}).join('')}
 <button class="addb" data-hr29="h">${ic('add')}${G.length?'غرفة تانية':'إضافة غرفة صحة'}</button></div>`}
function hrDel(h){const p=curP();if(!p)return;const A=[];['so','ws','al'].forEach(id=>((p.rows||{})[id]||[]).forEach(r=>{if(r.hr==h)A.push(r)}));if(!A.length)return;const done=A.some(r=>(+r.r||0)>0||(+r.x||0)>0);
 if(!confirm('حذف '+A.length+' بند بتوع الغرفة دي؟'+(done?'\n⚠ فيه منهم بنود متعلّم عليها استلام أو تنفيذ.':'')))return;snap('قبل حذف غرفة صحة · صيدلية '+p.no);['so','ws','al'].forEach(id=>{if(p.rows[id])p.rows[id]=p.rows[id].filter(r=>r.hr!=h)});p.modAt=nowIso();sv();render();toastT('✓ اتحذفت الغرفة')}
const _card29=card;card=function(t,p){const h=_card29.apply(this,arguments);return t&&t.id=='ws'&&p&&V.v=='ph'?h+hrBlock(p):h};

// ---- 3) photos follow the pharmacy (merge under another inner id) + pull missing photos on the laptop
function exMap(E,idm){if(!E||!idm||!Object.keys(idm).length)return;['photos','files'].forEach(k=>{const o=E[k];if(!o)return;const n={};Object.keys(o).forEach(key=>{const m=key.match(/^(pho|f):([^:]+):(.*)$/);n[m&&idm[m[2]]!=null?m[1]+':'+idm[m[2]]+':'+m[3]:key]=o[key]});E[k]=n})}
async function exPhotos(q){const ALL=DB.ph.concat(typeof HID!='undefined'&&HIDDB===DB?HID:[]),idm={};(q.ph||[]).forEach(z=>{const l=ALL.find(x=>x.id==z.id)||ALL.find(x=>String(x.no)==String(z.no)&&x.mo==z.mo);if(l&&l.id!=z.id)idm[z.id]=l.id});
 const E={photos:q._photos||{},files:q._files||{}};exMap(E,idm);let n=0;
 for(const k of Object.keys(E.photos)){if(!/^pho:/.test(k))continue;try{const b=await (await fetch(E.photos[k])).blob();if(await idbSet(k,b)){n++;if(PHU[k]){URL.revokeObjectURL(PHU[k]);delete PHU[k]}}}catch(e){}}
 for(const k of Object.keys(E.files)){if(!/^f:/.test(k))continue;try{const b=await (await fetch(E.files[k])).blob();await idbSet(k,b)}catch(e){}}return n}
async function gdPhotoPull(){const t=toast('☁️ بدوّر على آخر نسخة كاملة على Drive…');try{const L=await gdList(),A=L.filter(f=>/^966-(full|month|lapfull|lapmonth)-.*\.json$/.test(f.name)).sort((a,b)=>String(b.modifiedTime||b.mt||'').localeCompare(String(a.modifiedTime||a.mt||''))),f=A[0];
 if(!f){t.remove();return alert('مفيش نسخة كاملة على Drive. ارفع النسخة الكاملة من الموبايل الأول (☰ ← Google Drive ← رفع النسخة الكاملة).')}
 t.innerHTML='☁️ جاري تحميل '+esc(f.name.replace(/^966-|\.json$/g,''))+(f.size?' ('+gdMb(f.size)+')':'')+'…';const q=await gdGet(f.id);const n=await exPhotos(q);t.remove();render();toastT(n?'✓ اتجابت '+n+' صورة من '+f.name.replace(/^966-|\.json$/g,''):'النسخة دي مفيهاش صور')}
 catch(e){t.remove();alert(e&&e.need?'محتاج تسجيل دخول Google Drive الأول':'⚠ ما نجحش: '+((e&&e.message)||e))}}
const _phoFill29=phoFill;phoFill=async function(){const r=await _phoFill29.apply(this,arguments);try{document.querySelectorAll('.ph29').forEach(x=>x.remove());if(!GWEB())return r;const m=document.querySelectorAll('.pht.miss').length;if(!m)return r;const b=document.querySelector('.phb');
 if(b)b.insertAdjacentHTML('beforebegin',`<div class="ph29 ywarn">📷 ${m} صورة مش على الجهاز ده (الصور بتيجي في النسخة الكاملة بس، مش اليومية).<button class="pr" data-ph29="1">☁️ جيب الصور من آخر نسخة كاملة على Drive</button></div>`)}catch(e){}return r};
// ---- 4) Drive list: the full copies (with photos) first, the rest folded
gdListHtml=function(L){if(!L.length)return '<p class="em">مفيش ملفات لسه.</p>';const G=[['full','📷 كاملة بالصور'],['month','شهرية (بالصور)'],['lapfull','اللاب توب كاملة'],['lapmonth','اللاب توب شهرية'],['laptop','اللاب توب'],['day','يومية (من غير صور)']];
 const row=f=>`<div class="ph gdr"><small style="flex:1"><b>${esc(f.name.replace(/^966-|\.json$/g,''))}</b> · ${fd(f.mt)} · ${gdMb(f.size)}</small><button data-gdrs="${esc(f.id||f.name)}">دمج</button><button data-gdrr="${esc(f.id||f.name)}" style="color:var(--rd)">استبدال</button></div>`;
 return G.map(([k,t],i)=>{const A=L.filter(f=>f.name.startsWith('966-'+k+'-')&&/\.json$/.test(f.name));if(!A.length)return '';return k=='full'?`<h4>${t} (${A.length})</h4><small class="hint">دي اللي فيها الصور والمرفقات. لو الصور مش ظاهرة على الجهاز ده، استخدم أحدث واحدة.</small>`+A.map(row).join(''):`<details class="gdf29"><summary>${t} (${A.length})</summary>${A.map(row).join('')}</details>`}).join('')};
// ---- 2) old Drive-folder reminder: never on the web link, at most once a week on the local file, never while Drive works
const _gdlRemind29=gdlRemind;gdlRemind=function(){try{if(GWEB()||gdOk())return;const c=C29();if(c.gdrm&&(new Date(TD())-new Date(c.gdrm))/864e5<7)return;c.gdrm=TD()}catch(e){}return _gdlRemind29.apply(this,arguments)};
// ---- S2/S3) home: while Drive works the old sync chip is hidden; on the web link a clear bar when the data is not updated from the phone
const _syncChip29=syncChip;syncChip=function(){try{if(gdOk())return '';if(GWEB()){const o=gdS();return `<div class="alr gd29"><small>⚠ <b>بيانات الجهاز ده مش متحدّثة من الموبايل</b> — ${o.pt?'آخر دمج من الموبايل: '+esc(fd(o.pt)):'لسه ما اتدمجتش بيانات الموبايل'}${o.need?' · جوجل محتاج تسجيل دخول تاني':''}. سجّل دخول عشان يجيب آخر بيانات لوحده.</small><button class="pr" data-gdlogin="1">تسجيل دخول Google Drive</button></div>`}}catch(e){}return _syncChip29.apply(this,arguments)};

// ---- 8) + S1) English file names (WhatsApp breaks Arabic file names)
const FNE=[[/تقرير تنفيذ للإدارة|تقرير الإدارة/g,'Management Report'],[/صور قبل وبعد/g,'Before-After Photos'],[/فواتير بدون ورقي/g,'Invoices without paper'],[/فاتورة م/g,'Invoice'],[/كشف مصروفات العهدة|كشف مصروفات/g,'Custody Expenses'],[/عهدة|العهدة/g,'Custody'],[/كشف الصيانة|كشف صيانة|الصيانة|صيانة/g,'Maintenance'],[/المخزن|مخزن/g,'Warehouse'],[/الجرد|جرد/g,'Stock-take'],[/نواقص الطباعة/g,'Print shortages'],[/نواقص التنفيذ/g,'Execution shortages'],[/النواقص|نواقص/g,'Shortages'],[/الملخص|ملخص/g,'Summary'],[/الطباعة|طباعة/g,'Print'],[/التنفيذ|تنفيذ/g,'Execution'],[/الاستلام|استلام/g,'Receiving'],[/عروض الأسعار|عرض سعر|عروض/g,'Quotes'],[/الفواتير|فواتير|فاتورة/g,'Invoices'],[/كل الصيدليات/g,'All pharmacies'],[/الوسطى/g,'Central'],[/الشرقية/g,'Eastern'],[/الغربية/g,'Western'],[/الجنوبية/g,'Southern'],[/الشمالية/g,'Northern'],[/الرياض/g,'Riyadh'],[/الخبر/g,'Khobar'],[/الدمام/g,'Dammam'],[/جدة/g,'Jeddah'],[/مكة/g,'Makkah'],[/المدينة/g,'Madinah'],[/شهر/g,'']];
function fnEn(n){n=String(n==null?'':n);if(!/[\u0600-\u06FF]/.test(n))return n;const m=n.match(/^(.*?)(\.[A-Za-z0-9]{2,5})?$/),ext=m[2]||'';let b=m[1],r;
 if(r=b.match(/^تقرير الإدارة - صيدلية (\S+) - (.+)$/))return 'Al-Dawaa '+r[1]+' - Management Report - '+r[2]+ext;
 if(r=b.match(/^صور قبل وبعد - صيدلية (\S+) - (.+)$/))return 'Al-Dawaa '+r[1]+' - Before-After Photos - '+r[2]+ext;
 b=b.replace(/صيدلية\s*/g,'Ph ');FNE.forEach(([a,c])=>{b=b.replace(a,c)});b=b.replace(/[\u0600-\u06FF\u0640]+/g,' ').replace(/\(\s*\)/g,'').replace(/\s*-\s*(?:-\s*)+/g,' - ').replace(/\s{2,}/g,' ').replace(/^[\s\-·_]+|[\s\-·_]+$/g,'');return (b||'966-file')+ext}
const _dl29=dl;dl=function(n,t,ty){return _dl29.call(this,fnEn(n),t,ty)};
const _shareFile29=shareFile;shareFile=function(d,n,ty){return _shareFile29.call(this,d,fnEn(n),ty)};
const _pickSave29=pickSave;pickSave=function(bl,o){if(o&&o.suggestedName)o=Object.assign({},o,{suggestedName:fnEn(o.suggestedName)});return _pickSave29.call(this,bl,o)};
const _nWrite29=nWrite;nWrite=function(path,blob){const a=String(path).split('/');a[a.length-1]=fnEn(a[a.length-1]);return _nWrite29.call(this,a.join('/'),blob)};
const _shareFiles29=shareFiles;shareFiles=function(F,msg){return _shareFiles29.call(this,(F||[]).map(f=>f&&f.name&&fnEn(f.name)!=f.name?new File([f],fnEn(f.name),{type:f.type}):f),msg)};
const _fname29=fname;fname=function(){const p=curP();if(p&&V.sm=='mgmt'&&V.v!='nq'&&!(V.v=='all'&&V.am!='ph'))return 'Al-Dawaa '+p.no+' - Management Report - '+mLab(p.mo);return _fname29.apply(this,arguments)};

// ---- 8) management report Excel = the PDF layout (chips, blue title band with the logo, dates, headings, tables, totals)
const _rpXlsx29=rpXlsx;rpXlsx=function(el){const src=el||$('#rp');try{const h=src&&src.querySelector('.rhd');if(h&&src.querySelector('.meta-panel')&&/للإدارة/.test(h.textContent))return mgXlsx(pdfClone(src))}catch(e){console.error(e)}return _rpXlsx29.apply(this,arguments)};
function mgXlsx(src){const txt=e=>e?e.textContent.replace(/\s+/g,' ').trim():'',num=t=>/^-?\d+(\.\d+)?$/.test(t)?+t:t,B=[];
 const walk=el=>{for(const c of [...el.children]){const cl=c.classList;
  if(cl.contains('meta-panel')){B.push({k:'meta',a:[...c.children].map(x=>({t:txt(x),c:x.classList.contains('meta-co')?7:x.classList.contains('meta-mod')?8:6}))});continue}
  if(cl.contains('rhd')){B.push({k:'ttl',t:txt(c)});continue}
  if(cl.contains('dts')){B.push({k:'dts',a:[...c.querySelectorAll('label')].map(l=>{const s=l.querySelector('span'),v=txt(s);return {l:txt(l).replace(v,'').trim(),v}})});continue}
  if(c.tagName=='TABLE'){const R=[...c.rows].map(r=>({hd:[...r.cells].every(x=>x.tagName=='TH'),tot:r.classList.contains('tot'),c:[...r.cells].map(x=>({t:txt(x),sp:x.colSpan||1}))})).filter(r=>r.c.length);if(R.length)B.push({k:'tb',R});continue}
  if(/^H[1-6]$/.test(c.tagName)){const t=txt(c);if(t)B.push({k:'h',t});continue}
  if(c.tagName=='LABEL'){const s=c.querySelector('span'),v=s?s.textContent.trim():'';if(v&&v!='—')B.push({k:'note',l:txt(c).replace(txt(s),'').trim(),v});continue}
  if(c.querySelector('table,h3,h4,.rhd,.meta-panel,.dts,label')){walk(c);continue}
  const t=txt(c);if(t)B.push({k:'p',t})}};
 walk(src);
 const G=12,CW=8.6,rows=[],mg=[],ht=[],L=t=>{let n=0;for(const ch of String(t))n+=/[A-Z0-9]/.test(ch)?1.1:1;return n},
  newRow=h=>{rows.push([]);ht.push(h);return rows.length-1},put=(r,c0,k,v,s)=>{for(let q=0;q<k;q++)rows[r][c0+q]={v:q?'':v,s};if(k>1)mg.push([r,c0,r,c0+k-1])},
  lines=(v,k)=>Math.max(1,Math.ceil(L(v)/Math.max(1,k*CW*0.92-2))),spans=n=>{const w=Array(n).fill(1);if(n>1)w[0]=1.6;const s=w.reduce((a,x)=>a+x,0),raw=w.map(x=>x/s*G),out=raw.map(x=>Math.max(1,Math.floor(x)));let d=G-out.reduce((a,x)=>a+x,0);const ord=raw.map((x,i)=>[x-Math.floor(x),i]).sort((a,b)=>b[0]-a[0]);for(let i=0;d>0;i=(i+1)%n){out[ord[i][1]]++;d--}while(out.reduce((a,x)=>a+x,0)>G){const i=out.indexOf(Math.max(...out));out[i]--}return out};
 let title='';
 B.forEach(b=>{
  if(b.k=='meta'){const r=newRow(24),n=b.a.length||1,S=spans(n).map(()=>Math.floor(G/n));S[0]+=G-S.reduce((a,x)=>a+x,0);let c0=0;b.a.forEach((x,i)=>{put(r,c0,S[i],x.t,x.c);c0+=S[i]});newRow(6);return}
  if(b.k=='ttl'){title=b.t;const r=newRow(38);put(r,0,2,'',12);put(r,2,G-2,b.t,5);newRow(6);return}
  if(b.k=='dts'){const a=b.a,r1=newRow(16),r2=newRow(20);if(a[0]){put(r1,0,4,a[0].l,9);put(r2,0,4,a[0].v,10)}if(a[1]){put(r1,G-4,4,a[1].l,13);put(r2,G-4,4,a[1].v,14)}newRow(8);return}
  if(b.k=='h'){const r=newRow(24);put(r,0,G,b.t,2);newRow(4);return}
  if(b.k=='tb'){const n=Math.max(...b.R.map(r=>r.c.reduce((a,x)=>a+x.sp,0))),S=spans(n);
   b.R.forEach(r0=>{const r=newRow(18);let ci=0,c0=0,h=1;r0.c.forEach(x=>{let k=0;for(let q=0;q<x.sp;q++)k+=S[ci+q]||1;const v=r0.hd?x.t:num(x.t),s=r0.hd?1:r0.tot?3:typeof v=='number'?11:4;put(r,c0,k,v,s);h=Math.max(h,lines(x.t,k));c0+=k;ci+=x.sp});if(c0<G)put(r,c0,G-c0,'',r0.hd?1:r0.tot?3:4);ht[r]=Math.max(r0.hd?20:18,15*h+4)});newRow(10);return}
  if(b.k=='note'){const r=newRow(18);put(r,0,G,b.l,15);const r2=newRow(18);put(r2,0,G,b.v,16);ht[r2]=Math.max(18,15*b.v.split('\n').reduce((a,l)=>a+lines(l,G),0)+4);newRow(6);return}
  if(b.k=='p'){const r=newRow(18);put(r,0,G,b.t,16);ht[r]=Math.max(18,15*lines(b.t,G)+4)}});
 while(rows.length&&!rows[rows.length-1].length){rows.pop();ht.pop()}
 const R=rows.map((r,ri)=>`<row r="${ri+1}" ht="${ht[ri]||15}" customHeight="1">${r.map((x,ci)=>{if(!x)return '';const ref=colL(ci)+(ri+1),st=` s="${x.s}"`;return typeof x.v=='number'&&isFinite(x.v)?`<c r="${ref}"${st}><v>${x.v}</v></c>`:x.v===''?`<c r="${ref}"${st}/>`:`<c r="${ref}" t="inlineStr"${st}><is><t xml:space="preserve">${xe(tr(x.v))}</t></is></c>`}).join('')}</row>`).join('');
 // logo: one-cell anchor in the first cell of the title band, fixed size (wider or narrower columns do not stretch it)
 let img=null;try{if(/^data:image\/png;base64,/.test(LOGO)){const s=atob(LOGO.split(',')[1]);img=new Uint8Array(s.length);for(let i=0;i<s.length;i++)img[i]=s.charCodeAt(i)}}catch(e){img=null}
 const ti=rows.findIndex(r=>r[2]&&r[2].s==5),E=9525,lh=30,lw=Math.round(lh*1059/562),cwp=Math.round(CW*7+5),rhp=Math.round((ht[ti]||38)*4/3);
 const NS='http://schemas.openxmlformats.org',dr=img&&ti>=0;
 const sheet=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="${NS}/spreadsheetml/2006/main" xmlns:r="${NS}/officeDocument/2006/relationships"><sheetPr><pageSetUpPr fitToPage="1"/></sheetPr><sheetViews><sheetView rightToLeft="${isEN()?0:1}" showGridLines="0" workbookViewId="0"/></sheetViews><sheetFormatPr defaultRowHeight="15"/><cols><col min="1" max="${G}" width="${CW}" customWidth="1"/></cols><sheetData>${R}</sheetData>${mg.length?`<mergeCells count="${mg.length}">${mg.map(m=>`<mergeCell ref="${colL(m[1])}${m[0]+1}:${colL(m[3])}${m[2]+1}"/>`).join('')}</mergeCells>`:''}<pageMargins left="0.3" right="0.3" top="0.4" bottom="0.5" header="0.2" footer="0.25"/><pageSetup paperSize="9" orientation="portrait" fitToWidth="1" fitToHeight="0"/><headerFooter><oddFooter>${xe('&L&8&P / &N&R&8'+tr(title).slice(0,90))}</oddFooter></headerFooter>${dr?'<drawing r:id="rId1"/>':''}</worksheet>`;
 const drawing=dr?`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><xdr:wsDr xmlns:xdr="${NS}/drawingml/2006/spreadsheetDrawing" xmlns:a="${NS}/drawingml/2006/main" xmlns:r="${NS}/officeDocument/2006/relationships"><xdr:oneCellAnchor><xdr:from><xdr:col>0</xdr:col><xdr:colOff>${Math.max(0,Math.round((2*cwp-lw)/2))*E}</xdr:colOff><xdr:row>${ti}</xdr:row><xdr:rowOff>${Math.max(0,Math.round((rhp-lh)/2))*E}</xdr:rowOff></xdr:from><xdr:ext cx="${lw*E}" cy="${lh*E}"/><xdr:pic><xdr:nvPicPr><xdr:cNvPr id="2" name="Al-Dawaa logo"/><xdr:cNvPicPr><a:picLocks noChangeAspect="1"/></xdr:cNvPicPr></xdr:nvPicPr><xdr:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></xdr:blipFill><xdr:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${lw*E}" cy="${lh*E}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></xdr:spPr></xdr:pic><xdr:clientData/></xdr:oneCellAnchor></xdr:wsDr>`:'';
 const rtl=isEN()?1:2,al=(h,w)=>`<alignment horizontal="${h}" vertical="center"${w?' wrapText="1"':''} readingOrder="${rtl}"/>`,st=isEN()?'left':'right',en=isEN()?'right':'left';
 const fonts=['<font><sz val="11"/><name val="Arial"/></font>','<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Arial"/></font>','<font><b/><sz val="13"/><color rgb="FF12305C"/><name val="Arial"/></font>','<font><b/><sz val="11"/><color rgb="FF3A2A08"/><name val="Arial"/></font>','<font><b/><sz val="12"/><color rgb="FFFFFFFF"/><name val="Arial"/></font>','<font><sz val="9"/><color rgb="FF5B6475"/><name val="Arial"/></font>','<font><b/><sz val="11"/><color rgb="FF1B2430"/><name val="Arial"/></font>','<font><b/><sz val="10"/><color rgb="FF1B2430"/><name val="Arial"/></font>'];
 const fl=c=>`<fill><patternFill patternType="solid"><fgColor rgb="FF${c}"/><bgColor indexed="64"/></patternFill></fill>`,fills=['<fill><patternFill patternType="none"/></fill>','<fill><patternFill patternType="gray125"/></fill>',fl('12305C'),fl('FFF1D6'),fl('E3EEFA'),fl('E2F3EC'),fl('F9EFD3')];
 const bd=c=>`<border><left style="thin"><color rgb="FF${c}"/></left><right style="thin"><color rgb="FF${c}"/></right><top style="thin"><color rgb="FF${c}"/></top><bottom style="thin"><color rgb="FF${c}"/></bottom><diagonal/></border>`,borders=['<border><left/><right/><top/><bottom/><diagonal/></border>',bd('C9D2DF'),'<border><left/><right/><top/><bottom style="medium"><color rgb="FFF2B705"/></bottom><diagonal/></border>',bd('3984D6'),bd('26966D'),bd('C99A20'),'<border><left/><right/><top/><bottom style="medium"><color rgb="FFF2B705"/></bottom><diagonal/></border>'];
 const xf=(f,fi,b,a)=>`<xf numFmtId="0" fontId="${f}" fillId="${fi}" borderId="${b}" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">${a}</xf>`;
 // 0 default · 1 table head · 2 heading · 3 total · 4 cell · 5 title band · 6/7/8 chips · 9 date label (start) · 10 date (start) · 11 number · 12 logo cell · 13 date label (end) · 14 date (end) · 15 note label · 16 text
 const X=[xf(0,0,0,al('center',1)),xf(1,2,1,al('center',1)),xf(2,0,2,al(st,0)),xf(3,3,1,al('center',1)),xf(0,0,1,al('center',1)),xf(4,2,6,al(st,1)),xf(6,4,3,al(st,1)),xf(6,5,4,al(st,1)),xf(6,6,5,al(st,1)),xf(5,0,0,al(st,0)),xf(6,0,0,al(st,0)),xf(0,0,1,al('center',0)),xf(0,2,6,al('center',0)),xf(5,0,0,al(en,0)),xf(6,0,0,al(en,0)),xf(7,0,0,al(st,0)),xf(0,0,0,al(st,1))];
 const styles=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="${NS}/spreadsheetml/2006/main"><fonts count="${fonts.length}">${fonts.join('')}</fonts><fills count="${fills.length}">${fills.join('')}</fills><borders count="${borders.length}">${borders.join('')}</borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="${X.length}">${X.join('')}</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`;
 const sn=(tr(title).replace(/^.*?—\s*/,'').replace(/[\[\]:*?\/\\]/g,' ').trim()||'966 Report').slice(0,31);
 const f=[{n:'[Content_Types].xml',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="${NS}/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>${dr?'<Default Extension="png" ContentType="image/png"/>':''}<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>${dr?'<Override PartName="/xl/drawings/drawing1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>':''}</Types>`},
  {n:'_rels/.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`},
  {n:'xl/workbook.xml',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="${NS}/spreadsheetml/2006/main" xmlns:r="${NS}/officeDocument/2006/relationships"><sheets><sheet name="${xe(sn)}" sheetId="1" r:id="rId1"/></sheets></workbook>`},
  {n:'xl/_rels/workbook.xml.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="${NS}/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`},
  {n:'xl/styles.xml',d:styles},{n:'xl/worksheets/sheet1.xml',d:sheet}];
 if(dr)f.push({n:'xl/worksheets/_rels/sheet1.xml.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/drawing" Target="../drawings/drawing1.xml"/></Relationships>`},
  {n:'xl/drawings/drawing1.xml',d:drawing},{n:'xl/drawings/_rels/drawing1.xml.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/image" Target="../media/image1.png"/></Relationships>`},{n:'xl/media/image1.png',d:img});
 return zipBlob(f,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

// ---- management report: a swapped item (the client asked for another one) is not counted — its replacement is in the extra items
const noSw=r=>!(r&&r.cx&&r.sw);
const mrNoSw=o=>{const n={};Object.keys(o||{}).forEach(k=>{n[k]=Array.isArray(o[k])?o[k].filter(noSw):o[k]});return n};
const _capPcs29=capPcs;capPcs=function(p,id,k){const a=((p&&p.rows)||{})[id]||[];if(k!='q'||a.every(noSw))return _capPcs29.apply(this,arguments);return _capPcs29.call(this,Object.assign({},p,{rows:Object.assign({},p.rows,{[id]:a.filter(noSw)})}),id,k)};
// caps: only the count (the sides are already in the table above)
capTbl=function(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const x=v[0];return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>البند</th><th>العدد</th><th class="act">إجراء</th></tr><tr class="tot"><td>${CPNM}</td><td>${x.q} قطعة</td><td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td></tr></table></div>`};

// ---- clicks and changes
const _v24Click29=v24Click;v24Click=function(d,b){
 if(d.hr29){hrOpen(d.hr29);return 1}
 if(d.hr29go){hrGo(d.hr29go);return 1}
 if(d.hr29del){hrDel(d.hr29del);return 1}
 if(d.ph29){gdPhotoPull();return 1}
 return _v24Click29(d,b)};
const _v33Change29=v33Change;v33Change=function(x){const ds=x.dataset||{};
 if(x.id=='hr29k'){hrOpen(x.value);return 1}
 if(ds.w29c!=null){const S=W29();if(x.checked)delete S.off[ds.w29c];else S.off[ds.w29c]=1;render();return 1}
 if(ds.w29m!=null){W29().mat[ds.w29m]=x.value;return 1}
 return _v33Change29(x)};
