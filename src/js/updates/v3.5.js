// ---------- v3.5: custody top-up (استلام مبلغ / تعزيز العهدة) ----------
function cDep(M){return Math.round(((M&&M.dep)||[]).reduce((a,d)=>a+(+d.amt||0),0)*100)/100}
function cAv(M){return Math.round(((+M.open||0)+cDep(M))*100)/100}
function cDepLab(M){const d=cDep(M);return d?`رصيد بداية الشهر ${f2(M.open)} + مستلم (تعزيز) ${f2(d)}`:'رصيد بداية الشهر'}
function cDepTxt(M){const L=(M&&M.dep)||[];return L.length?'مستلم (تعزيز): '+L.map(d=>f2(d.amt)+' بتاريخ '+cDd(d.dt)+(d.note?' — '+d.note:'')).join('، '):''}
function cKpiOpen(M){const d=cDep(M);return d?`<div><small>رصيد البداية + المستلم</small><b class="c-open">${f2(cAv(M))}</b><em class="cdpe">${f2(M.open)} + ${f2(d)}</em></div>`:`<div><small>رصيد بداية الشهر</small><b class="c-open">${f2(M.open)}</b></div>`}
function cDepHtml(M){const L=M.dep||[],lk=cLk(M);
 return `<div class="cdepw">${L.map(d=>`<div class="cdepr"><span>💵 مستلم <b>${f2(d.amt)}</b> · ${cDd(d.dt)}${d.note?' · '+esc(d.note):''}</span>${lk?'':`<button class="ib" data-cdepe="${d.id}" title="تعديل">${ic('edit')}</button><button class="ib" data-cdepx="${d.id}" title="حذف">${ic('trash')}</button>`}</div>`).join('')}
 ${lk?'':`<div class="cdepb"><button data-cdep="1">💵 استلام مبلغ</button><button data-copen="1">${ic('edit')}رصيد البداية</button></div>`}</div>`}
function cDepOpen(id){cShClose();const C=CU(),M=cMo(),d=id?(M.dep||[]).find(x=>String(x.id)==String(id)):null,base=+C.cfg.base||10000,r=cRem(M)-(d?+d.amt:0),fill=Math.round((base-r)*100)/100,el=document.createElement('div');el.className='csh';el.dataset.id=d?d.id:'';
 el.innerHTML=`<div class="cshb"><b>💵 ${d?'تعديل مبلغ مستلم':'استلام مبلغ (تعزيز العهدة)'} — شهر ${cMoLab(C.cur)}</b><small>المتبقي ${d?'من غير المبلغ ده':'دلوقتي'}: <b>${f2(r)}</b></small>
 ${fill>0?`<button data-cdepf="${fill}">كمّل المتبقي لـ ${f2(base)} ( + ${f2(fill)} )</button>`:''}
 <label>المبلغ المستلم<input type="number" inputmode="decimal" id="cdpa" value="${d?d.amt:''}"></label><label>التاريخ<input type="date" id="cdpd" value="${d?d.dt:TD()}"></label><label>ملاحظة (اختياري)<input id="cdpn" placeholder="مثلاً: تحويل من الشركة" value="${esc(d?d.note||'':'')}"></label>
 <div class="cshr"><button class="pr" data-cdeps="1">${ic('check')}حفظ</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el);setTimeout(()=>{const x=$('#cdpa');if(x)x.focus()},50)}
function cDepSave(){const sh=document.querySelector('.csh'),M=cMo(),a=Math.round(parseFloat(($('#cdpa')||{}).value)*100)/100,dt=($('#cdpd')||{}).value||TD(),note=(($('#cdpn')||{}).value||'').trim();if(!(a>0))return alert('اكتب المبلغ المستلم');
 M.dep=M.dep||[];const id=sh&&sh.dataset.id;if(id){const d=M.dep.find(x=>String(x.id)==id);if(d)Object.assign(d,{amt:a,dt,note})}else M.dep.push({id:Date.now(),amt:a,dt,note});M.dep.sort((x,y)=>String(x.dt).localeCompare(String(y.dt)));
 cShClose();sv();render();toastT('✓ اتسجل مبلغ مستلم '+f2(a)+' · المتبقي بقى '+f2(cRem(M)))}
function v35CustClick(d,b){
 if(V.v=='cust'&&cLk(cMo())&&(d.cdep||d.copen||d.cdepe||d.cdepx)){toastT('🔒 عهدة '+cMoLab(CU().cur)+' اتسلمت. اضغط «فتح للتعديل» الأول');return 1}
 if(d.cdep){cDepOpen();return 1}
 if(d.cdepe){cDepOpen(d.cdepe);return 1}
 if(d.cdepf){const x=$('#cdpa');if(x)x.value=d.cdepf;return 1}
 if(d.cdeps){cDepSave();return 1}
 if(d.cdepx){const M=cMo(),i=(M.dep||[]).findIndex(x=>String(x.id)==String(d.cdepx));if(i>=0&&confirm('حذف المبلغ المستلم '+f2(M.dep[i].amt)+'؟')){(M.dd=M.dd||{})[M.dep[i].id]=nowIso();M.dep.splice(i,1);sv();render()}return 1}
 if(d.copen){const M=cMo();let v=prompt('رصيد بداية شهر '+cMoLab(CU().cur)+' (من غير المبالغ المستلمة):',M.open);if(v==null)return 1;v=parseFloat(v);if(!(v>=0))return alert('اكتب رقم'),1;M.open=Math.round(v*100)/100;sv();render();return 1}
 return 0}

// ---------- v3.5: sync status ----------
var GDPL=0;
const gdAgo=iso=>{if(!iso)return '';const m=Math.max(0,Math.round((Date.now()-new Date(iso).getTime())/60000));return m<1?'دلوقتي':m<60?'من '+m+' دقيقة':m<1440?'من '+Math.round(m/60)+' ساعة':fd(iso).slice(0,10)};
function gdStat(){if(!DA())return '';const o=gdS();if(!o.on)return '';const w=GWEB()?'الموبايل':'اللاب توب';
 if(o.need)return '🔑 Google Drive محتاج تسجيل دخول';if(GDBUSY)return '☁️ ⏫ جاري الرفع…';
 if(GDE||(o.ed||0)>0||o.pend.day)return '☁️ ⏳ في تعديلات هتترفع'+(o.off?' لما النت يرجع':' خلال دقيقة');
 return '☁️ متزامن'+(o.last?' · آخر رفع '+gdAgo(o.last):'')+(o.pt?' · آخر قراءة من '+w+' '+gdAgo(o.pt):'')}
function gdStat0(){const e=document.getElementById('gdst');if(e)e.textContent=gdStat()}
setInterval(gdStat0,60e3);
