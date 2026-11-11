"""v3.5: custody top-up («💵 استلام مبلغ»: amount, date, note, «كمّل لـ 10,000»; counted in the remaining, the statement and the
handover) + ✏️ opening balance; Google Drive inside «النسخ والاستيراد» (removed from the menu); empty-data message on the
web link offers Google sign-in; automatic sync: upload one minute after the last edit, read the other device when the app opens /
comes back and every 5 minutes, sync status line on the home screen."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'cDep(' not in s
JS, CSS, EN = [], [], {}

# =====================================================================
# 1. custody top-up
# =====================================================================
rep("const cRem=M=>Math.round(((+M.open||0)-cTot(M))*100)/100;", "const cRem=M=>Math.round(((+M.open||0)+cDep(M)-cTot(M))*100)/100;")
rep('<div class="ckpi"><div><small>رصيد بداية الشهر</small><b class="c-open">${f2(M.open)}</b></div>', '<div class="ckpi">${cKpiOpen(M)}', 2)
rep("x=>!x.qt).length}</b></div><button class=\"cnpk${V.cnpf?' on':''}\" data-cnpf=\"1\"><small>بدون فاتورة ورقية</small><b>${cNpN(M)}</b><em>${V.cnpf?'✓ معروضين بس · اعرض الكل':'اضغط لعرضهم بس'}</em></button></div>${cAlHtml()}",
    "x=>!x.qt).length}</b></div><button class=\"cnpk${V.cnpf?' on':''}\" data-cnpf=\"1\"><small>بدون فاتورة ورقية</small><b>${cNpN(M)}</b><em>${V.cnpf?'✓ معروضين بس · اعرض الكل':'اضغط لعرضهم بس'}</em></button></div>${cDepHtml(M)}${cAlHtml()}")
# statement (PDF): balance starts from opening + received
rep("rm=cRem(M);let bal=+M.open||0;const el=document.createElement('div');", "rm=cRem(M);let bal=cAv(M);const el=document.createElement('div');")
rep("<tr class=\"copen\"><td colspan=\"7\">رصيد بداية الشهر</td><td class=\"c-open\">${f2(M.open)}</td><td colspan=\"3\"></td></tr>",
    "<tr class=\"copen\"><td colspan=\"7\">${esc(cDepLab(M))}</td><td class=\"c-open\">${f2(cAv(M))}</td><td colspan=\"3\"></td></tr>")
rep("${M.dl?` · تاريخ التسليم: <b>${cDd(M.dl.at)}</b>`:''}</div>", "${M.dl?` · تاريخ التسليم: <b>${cDd(M.dl.at)}</b>`:''}${cDepTxt(M)?' · '+esc(cDepTxt(M)):''}</div>")
# statement (Excel)
rep("[0,2,'رصيد بداية الشهر','H7',+M.open,4,BLUE]", "[0,2,cDep(M)?'رصيد العهدة (بداية + مستلم)':'رصيد بداية الشهر','H7',cAv(M),4,BLUE]")
rep("M.open?tt/M.open:0,9,NAVY]", "cAv(M)?tt/cAv(M):0,9,NAVY]")
rep("for(let i=0;i<11;i++)cell(7,i,i==0?'رصيد بداية الشهر':i==7?+M.open:'',", "for(let i=0;i<11;i++)cell(7,i,i==0?cDepLab(M):i==7?cAv(M):'',")
rep(" let bal=+M.open||0;\n const HT=", " let bal=cAv(M);\n const HT=")
rep("(M.dl?'     ·     تاريخ التسليم: '+cDd(M.dl.at):''),", "(M.dl?'     ·     تاريخ التسليم: '+cDd(M.dl.at):'')+(cDepTxt(M)?'     ·     '+cDepTxt(M):''),")
# handover signature also covers the received amounts
JS.append(r"""// ---------- v3.5: custody top-up (استلام مبلغ / تعزيز العهدة) ----------
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
 if(d.cdepx){const M=cMo(),i=(M.dep||[]).findIndex(x=>String(x.id)==String(d.cdepx));if(i>=0&&confirm('حذف المبلغ المستلم '+f2(M.dep[i].amt)+'؟')){M.dep.splice(i,1);sv();render()}return 1}
 if(d.copen){const M=cMo();let v=prompt('رصيد بداية شهر '+cMoLab(CU().cur)+' (من غير المبالغ المستلمة):',M.open);if(v==null)return 1;v=parseFloat(v);if(!(v>=0))return alert('اكتب رقم'),1;M.open=Math.round(v*100)/100;sv();render();return 1}
 return 0}
""")
rep("if(usrClick(d,b)||v34WhClick(d,b)||", "if(usrClick(d,b)||v35CustClick(d,b)||v34WhClick(d,b)||")
rep(".concat([M.open]));", ".concat([M.open,JSON.stringify(M.dep||[])]));")
CSS.append(".cdepw{display:grid;gap:6px;margin:8px 0}.cdepr{display:flex;align-items:center;gap:6px;background:#E3F4E8;border:1px solid #9ED3AE;color:#145A2E;border-radius:10px;padding:6px 10px;font-size:13px}.cdepr span{flex:1}.cdepr .ib{width:32px;height:32px;padding:0}.cdepb{display:grid;grid-template-columns:2fr 1fr;gap:8px}.ckpi em.cdpe{display:block;font-style:normal;font-size:10.5px;color:var(--mu)}")
EN.update({'💵 استلام مبلغ (تعزيز العهدة)':'💵 Money received (custody top-up)','رصيد البداية':'Opening balance','رصيد البداية + المستلم':'Opening + received','المبلغ المستلم':'Amount received','ملاحظة (اختياري)':'Note (optional)','حفظ':'Save','مستلم':'Received'})

# =====================================================================
# 2. Google Drive inside «النسخ والاستيراد»; empty-data message on the web link
# =====================================================================
rep("['gd','Google Drive','db'],", "")
rep("if(V.v=='bk'){a.innerHTML=hdr(backBtn(),'النسخ')+`<main>${bkHtml()}</main>`;return}",
    "if(V.v=='bk'){a.innerHTML=hdr(backBtn(),'النسخ والاستيراد')+`<main><details class=\"pinfo gdbk\" data-id=\"__gdbk\"${V.op.__gdbk===false?'':' open'}><summary>☁️ Google Drive ${gdLine()}</summary>${gdHtml()}</details>${bkHtml()}</main>`;return}")
rep("function stEmpty(){if(document.querySelector('.toast.stem'))return;const t=toast('<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>لو كان عندك بيانات قبل كده، غالبًا المتصفح مسحها لما اتقفل. رجّعها من فولدر Drive (بيدمج آخر نسخة من الموبايل لوحده) أو من نسخة احتياطية.</span><button class=\"pr\" data-gddir=\"1\">ربط فولدر درايف</button><button data-stbk",
    "function stEmpty(){if(document.querySelector('.toast.stem')||(GWEB()&&gdS().on))return;const t=toast((GWEB()?'<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>اربط حساب Google والتطبيق هيجيب آخر بيانات الموبايل من Drive لوحده، أو استورد نسخة احتياطية.</span><button class=\"pr\" data-gdlogin=\"1\">ربط حساب Google</button>':'<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>لو كان عندك بيانات قبل كده، غالبًا المتصفح مسحها لما اتقفل. رجّعها من فولدر Drive (بيدمج آخر نسخة من الموبايل لوحده) أو من نسخة احتياطية.</span><button class=\"pr\" data-gddir=\"1\">ربط فولدر درايف</button>')+'<button data-stbk")
CSS.append(".gdbk>summary{display:flex;flex-wrap:wrap;align-items:center;gap:6px}.gdbk>summary .stb{flex-basis:100%;margin:0}")
EN.update({'النسخ والاستيراد':'Backup and import','ربط حساب Google':'Connect Google account','اربط حساب Google والتطبيق هيجيب آخر بيانات الموبايل من Drive لوحده، أو استورد نسخة احتياطية.':'Connect your Google account and the app brings the latest phone data from Drive by itself, or import a backup.'})

# =====================================================================
# 3. automatic sync: upload 1 minute after the last edit, read on open / return / every 5 minutes, status line
# =====================================================================
rep("function gdEdit(){gdU(o=>o.ed=(o.ed||0)+1);const o=gdS();if((CAPN()||GWEB())&&o.on&&o.ed>=30){clearTimeout(GDE);GDE=setTimeout(()=>gdTick(),8000)}",
    "function gdEdit(){if(GDPL)return;gdU(o=>o.ed=(o.ed||0)+1);const o=gdS();if((CAPN()||GWEB())&&o.on){clearTimeout(GDE);GDE=setTimeout(()=>{GDE=0;gdTick({day:1}).then(gdStat0)},60e3);gdStat0()}")
rep("setInterval(()=>{gdPull();gdTick()},15*60e3);", "setInterval(()=>gdTick(),15*60e3);setInterval(()=>gdPull(),5*60e3);document.addEventListener('visibilitychange',()=>{if(!document.hidden)setTimeout(()=>gdPull(),1500);else if(GDE){clearTimeout(GDE);GDE=0;gdTick({day:1})}});")
rep("const q=await gdGet(f.id),msg=await gdApply(q,'merge','قبل دمج '+f.name+' من Google Drive');",
    "const q=await gdGet(f.id);GDPL=1;let msg;try{msg=await gdApply(q,'merge','قبل دمج '+f.name+' من Google Drive')}finally{GDPL=0}document.querySelectorAll('.toast.stem').forEach(x=>x.remove());")
rep("finally{GDPB=0;if(t)t.remove()}}", "finally{GDPB=0;if(t)t.remove();gdStat0()}}")
rep("function gdRender(){if(V&&(V.v=='gd'||V.v=='bk'||V.v=='gen'))render()}", "function gdRender(){gdStat0();if(V&&(V.v=='gd'||V.v=='bk'||V.v=='gen'))render()}")
rep("<small id=\"hcnt\">${n} صيدلية دعاية</small></div>", "<small id=\"hcnt\">${n} صيدلية دعاية</small><small id=\"gdst\">${gdStat()}</small></div>")
JS.append(r"""// ---------- v3.5: sync status ----------
var GDPL=0;
const gdAgo=iso=>{if(!iso)return '';const m=Math.max(0,Math.round((Date.now()-new Date(iso).getTime())/60000));return m<1?'دلوقتي':m<60?'من '+m+' دقيقة':m<1440?'من '+Math.round(m/60)+' ساعة':fd(iso).slice(0,10)};
function gdStat(){if(!DA())return '';const o=gdS();if(!o.on)return '';const w=GWEB()?'الموبايل':'اللاب توب';
 if(o.need)return '🔑 Google Drive محتاج تسجيل دخول';if(GDBUSY)return '☁️ ⏫ جاري الرفع…';
 if(GDE||(o.ed||0)>0||o.pend.day)return '☁️ ⏳ في تعديلات هتترفع'+(o.off?' لما النت يرجع':' خلال دقيقة');
 return '☁️ متزامن'+(o.last?' · آخر رفع '+gdAgo(o.last):'')+(o.pt?' · آخر قراءة من '+w+' '+gdAgo(o.pt):'')}
function gdStat0(){const e=document.getElementById('gdst');if(e)e.textContent=gdStat()}
setInterval(gdStat0,60e3);
""")
CSS.append("#gdst{display:block;font-size:11.5px;color:rgba(255,255,255,.78)}#gdst:empty{display:none}")
EN.update({'☁️ متزامن':'☁️ In sync','في تعديلات هتترفع':'changes waiting to upload','خلال دقيقة':'within a minute','آخر رفع':'last upload','آخر قراءة من':'last read from'})

# =====================================================================
# write
# =====================================================================
rep("// ---------- v1.5 extras ----------", '\n'.join(JS) + "// ---------- v1.5 extras ----------")
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}\n" + ''.join(CSS) + "\n")
rep("VER='v3.4'", "VER='v3.5'")
rep(" changelog:[{version:'v3.4',", " changelog:[{version:'v3.5',date:'2026-11-09',changes:['Custody: «💵 استلام مبلغ (تعزيز العهدة)» with amount, date and note, quick «كمّل المتبقي لـ 10,000»; counted in the remaining, the Excel/PDF statement (opening + received) and the handover; ✏️ opening balance button','Google Drive moved inside «النسخ والاستيراد» (removed from the menu); on the web link the empty-data message offers «ربط حساب Google»','Automatic sync: upload one minute after the last edit (and when leaving the app), read the other device when the app opens or comes back and every 5 minutes; sync status line on the home screen']},{version:'v3.4',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
