const dayDiff=d=>d?Math.floor((Date.now()-new Date(d).getTime())/864e5):999;
function bkBanner(){const lb=DB.cfg.lb,sn=DB.cfg.sn;if(!DB.ph.length)return'';const d=dayDiff(lb);if(d<7)return `<div class="ph"><small>آخر نسخة احتياطية: ${lb.slice(0,10)}</small></div>`;if(sn&&dayDiff(sn)<1)return'';return `<div class="alr">⚠ ${lb?'مرّ '+d+' يوم على آخر نسخة احتياطية':'لم تحفظ نسخة احتياطية بعد'}. البيانات محفوظة على هذا الجهاز فقط.<div class="tt"><button class="pr" data-bkp="1">حفظ نسخة احتياطية الآن</button><button data-snz="1">ذكّرني لاحقًا</button></div></div>`}
function sf(x){const[tid,k]=x.dataset.sf.split(':'),t=T.find(y=>y.id==tid),p=curP(),d=draft(t,p.sh),f=t.f.find(y=>y.k==k),all=opts(f,d,p.sh),q=x.value.trim().toLowerCase(),L=all.filter(o=>o.toLowerCase().includes(q)||String(tr(o)).toLowerCase().includes(q)),se=document.querySelector(`select[data-t="${tid}"][data-k="${k}"]`);if(!se)return;se.innerHTML=L.length?L.map(o=>`<option${o==d[k]?' selected':''}>${esc(o)}</option>`).join(''):'<option value="">لا توجد نتائج</option>';if(L.length&&!L.includes(d[k]))d[k]=L[0]}
const pcT=(a,b)=>{if(!b)return'<td>—</td>';const v=Math.round(100*a/b),c=v>=80?'#CFEBD8':v>=40?'#FBE3BC':'#F6CDD0';return `<td style="background:${c};color:#111;font-weight:700">${v}%</td>`};
function cmpHtml(){const ms=[...new Set(DB.ph.map(p=>p.mo))].sort();
 const st=L=>({n:L.length,c:L.filter(p=>p.st=='مكتملة').length,j:L.filter(p=>p.st=='جاري').length,z:L.filter(p=>p.st=='لم تبدأ').length});
 const mm=L=>{let a=0,q=0;L.forEach(p=>TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{q+=(+r.q||0);if(t.m)a+=t.m(r)})));return{a,q}};
 let h='<h3>مقارنة بين الشهور</h3><div class="sc"><table><tr><th>الشهر</th><th>الصيدليات</th><th>مكتملة</th><th>جاري</th><th>لم تبدأ</th><th>نسبة التنفيذ</th><th>إجمالي القطع</th><th>أمتار Wall Sticker</th><th>الفرق عن الشهر السابق</th></tr>',prev=null;
 ms.forEach(m=>{const L=DB.ph.filter(p=>p.mo==m),s=st(L),x=mm(L),r=s.n?100*s.c/s.n:0;h+=`<tr><td>${m}</td><td>${s.n}</td><td>${s.c}</td><td>${s.j}</td><td>${s.z}</td>${pcT(s.c,s.n)}<td>${x.q}</td><td>${x.a.toFixed(2)}</td><td>${prev==null?'—':(r-prev>=0?'+':'')+Math.round(r-prev)+'%'}</td></tr>`;prev=r});
 h+='</table></div>';
 h+='<h3>الرسم البياني لنسبة التنفيذ الشهرية</h3><div style="display:flex;align-items:flex-end;gap:10px;min-height:160px;padding:12px;border:1px solid #ddd;border-radius:8px">'+ms.slice(-12).map(m=>{const L=DB.ph.filter(p=>p.mo==m),v=L.length?Math.round(100*L.filter(p=>p.st=='مكتملة').length/L.length):0;return `<div style="flex:1;min-width:28px;text-align:center"><div style="font-size:11px">${v}%</div><div style="height:${Math.max(3,v)}px;background:#2F6FD0;border-radius:4px 4px 0 0"></div><small>${m.slice(5)}</small></div>`}).join('')+'</div>';
 const P=PF(),rg=[...new Set(P.map(p=>p.rg||'—'))];
 h+=`<h3>نسبة التنفيذ حسب المنطقة (${V.q.mo||'كل الشهور'})</h3><div class="sc"><table><tr><th>المنطقة</th><th>الصيدليات</th><th>مكتملة</th><th>جاري</th><th>لم تبدأ</th><th>نسبة التنفيذ</th></tr>`;
 rg.forEach(g=>{const s=st(P.filter(p=>(p.rg||'—')==g));h+=`<tr><td>${esc(g)}</td><td>${s.n}</td><td>${s.c}</td><td>${s.j}</td><td>${s.z}</td>${pcT(s.c,s.n)}</tr>`});
 const s=st(P);h+=`<tr class="tot"><td>الإجمالي</td><td>${s.n}</td><td>${s.c}</td><td>${s.j}</td><td>${s.z}</td>${pcT(s.c,s.n)}</tr></table></div>`;
 const m6=ms.slice(-6),ar=[...new Set(DB.ph.map(p=>p.rg||'—'))];
 if(m6.length>1&&ar.length)h+=`<h3>نسبة التنفيذ: المنطقة × الشهر (آخر ${m6.length} شهور)</h3><div class="sc"><table><tr><th>المنطقة</th>${m6.map(m=>`<th>${m}</th>`).join('')}</tr>`+ar.map(g=>`<tr><td>${esc(g)}</td>${m6.map(m=>{const s=st(DB.ph.filter(p=>p.mo==m&&(p.rg||'—')==g));return pcT(s.c,s.n)}).join('')}</tr>`).join('')+'</table></div>';
 return DB.ph.length?h:'<p class="em">لا توجد بيانات.</p>'}
const SDEF=(()=>{const a=[],h=g=>a.push({g}),d=(k,l,t)=>a.push({k,l,t});
 h('Wall Header');d('wh.h','الارتفاع حسب نوع الرف (سم)','shelf');d('wh.len','الأطوال المتاحة (سطر لكل خيار)','list');d('wh.wood','مقاسات WALL WOOD (سطر لكل خيار)','list');
 h('Floor Header');d('fh.s','الصغير / القياسي حسب نوع الرف','shelf');d('fh.l','الكبير (Health و OTC)','one');
 h('End cap');SH.forEach((n,i)=>d('ec.'+i,n+' — خيارات الحجم (سطر لكل خيار، مثال: صغير 64×111)','list'));
 h('End gandola');d('eg.hs','Header الصغير','shelf');d('eg.hl','Header الكبير','shelf');d('eg.ss','Side الصغير','shelf');d('eg.sl','Side الكبير','shelf');
 h('Medicated');d('md.h','Header','one');d('md.s','Side حسب نوع الرف','shelf');
 h('Side Acrylic Shelves');d('saw','Wall — المقاسات (سطر لكل خيار)','list');SH.forEach((n,i)=>d('saf.'+i,'Floor — '+n+' (سطر لكل خيار، مثال: صغير 30×120)','list'));
 h('بنود أخرى');d('ds','Door sticker (سطر لكل خيار)','list');d('c4','Sticker care 4 life (سطر لكل خيار)','list');d('fr','Fridge sticker','one');d('dc','Die Cut','one');
 h('Acrylic boards (المقاس | الخامة)');ABI.forEach(i=>d('abs.'+i,i,'one'));
 h('الخامات');[['mt.ws','Wall Sticker'],['mt.so','ستيكر خارجي (Sticker outdoor)'],['mt.wh','Wall Header'],['mt.ec','End cap'],['mt.md','Medicated'],['mt.sa','Side Acrylic Shelves'],['mt.al','Acrylic letters'],['mt.st','Door / Care 4 life / Fridge / Die Cut']].forEach(x=>d(x[0],x[1],'one'));
 d('mt.fh','Floor Header حسب نوع الرف','shelf');d('mt.egh','End gandola Header حسب نوع الرف','shelf');d('mt.egs','End gandola Side حسب نوع الرف','shelf');
 return a})();
function rtoRows(){const o=[];DB.ph.forEach(p=>((p.rows||{}).al||[]).forEach((r,i)=>{if(r.pc)return;const c=ratW(r.sec,r.lh);if(c==null)return;if(r.w!==''&&r.w!=null&&Math.abs(+r.w-c)<=0.01)return;o.push({p,i,r,c})}));return o}
function rtoHtml(){const L=rtoRows(),X=V.rx=V.rx||{};return `<div class="wcard"><h2>${ic('calc')}تطبيق النسب على حروف الأكريليك القديمة</h2><p class="sub">العرض بيتحسب من ارتفاع الحروف بنسبة ثابتة لكل قسم. دي البنود القديمة اللي عرضها مختلف عن النسبة. اختار اللي عايز تعدّله، وفيه نقطة استعادة وزر تراجع.</p>${L.length?`<div class="sc"><table><tr><th></th><th>الصيدلية</th><th>القسم</th><th>الحروف</th><th>عرض جملة الحروف: الحالي ← الجديد</th></tr>${L.map((x,j)=>`<tr><td><input type="checkbox" data-rx="${j}"${X[j]===false?'':' checked'}></td><td>${esc(x.p.no)}</td><td>${esc(x.r.sec)}</td><td>${esc(x.r.lh)}</td><td>${esc(x.r.w||'—')} ← <b>${x.c}</b></td></tr>`).join('')}</table></div><button class="pr big" data-rxgo="1">تطبيق على المحدد (${L.filter((x,j)=>X[j]!==false).length})</button>`:'<p class="em">كل البنود ماشية على النسب. مفيش حاجة تتعدّل.</p>'}<details class="mg"><summary><span>جدول النسب</span></summary><div class="sc"><table><tr><th>القسم</th><th>الارتفاع المرجعي</th><th>العرض المرجعي</th></tr>${Object.keys(RATIO).map(k=>`<tr><td>${esc(k)}</td><td>${RATIO[k][0]}</td><td>${RATIO[k][1]}</td></tr>`).join('')}</table></div></details></div>`}
function setHtml(){return SDEF.map(x=>{if(x.g)return `<h3>${esc(x.g)}</h3>`;const v=SZ(x.k),ov=DB.cfg.sz[x.k]!=null;let inp;
 if(x.t=='shelf')inp=SH.map((n,i)=>`<label>${n}<input data-sk="${x.k}" data-si="${i}" value="${esc(v[i])}"></label>`).join('');
 else if(x.t=='list')inp=`<textarea data-sk="${x.k}" rows="${Math.max(2,v.length)}">${esc(v.join('\n'))}</textarea>`;
 else inp=`<input data-sk="${x.k}" value="${esc(v)}">`;
 return `<div class="fm"><b>${esc(x.l)}</b>${inp}${ov?`<button data-sreset="${x.k}">↺ استرجاع الافتراضي</button>`:''}</div>`}).join('')}
function setSz(x){const k=x.dataset.sk,d=SDEF.find(y=>y.k==k);let v;if(d.t=='shelf'){v=[...SZ(k)];v[+x.dataset.si]=x.value.trim()}else if(d.t=='list'){v=x.value.split('\n').map(z=>z.trim()).filter(Boolean);if(!v.length)return}else v=x.value.trim();DB.cfg.sz[k]=v;sv()}
