"""v1.6 part 1: custody Excel / PDF as the owner edited it (yellow title, purple subtitle, no blank row, his row heights),
the م column stands out, the no-paper sentence stays clear with the invoice number small under it, narrow car column,
invoices by pharmacy in the summary sheet, invoice photos appendix PDF, page footer."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1, src=None):
    global s
    t = s if src is None else src
    if t.count(a) != n: sys.exit(f'COUNT {t.count(a)}!={n}: {a[:140]}')
    if src is None: s = s.replace(a, b)
    return t.replace(a, b)
assert 'function cAppEl' not in s
i = s.index('function custXlsx(k){'); j = s.index('// ---- PDF element (same table, A4)', i); f = s[i:j]
def fr(a, b, n=1):
    global f
    f = rep(a, b, n, f)
fr("first=9,", "first=8,")
fr("st({sz:15,b:1,c:'FFFFFF',bg:NAVY,nb:1})", "st({sz:14,b:1,c:'FFFF00',bg:NAVY,nb:1})")
fr("st({sz:10,c:MUTE,nb:1}));merges.push('A2:K2');", "st({sz:10,c:'50164A',nb:1}));merges.push('A2:K2');")
fr("const cards=[[0,2,'رصيد بداية الشهر','H8',", "const cards=[[0,2,'رصيد بداية الشهر','H7',")
fr("`IF(H8=0,0,G${tot}/H8)`", "`IF(H7=0,0,G${tot}/H7)`")
fr("cell(4,i,i==a?lab:'',st({sz:9,b:1,c:MUTE,bg:CARD}));cell(5,i,", "cell(3,i,i==a?lab:'',st({sz:9,b:1,c:MUTE,bg:CARD}));cell(4,i,")
fr("merges.push(`${ref(a,4)}:${ref(b,4)}`,`${ref(a,5)}:${ref(b,5)}`)", "merges.push(`${ref(a,3)}:${ref(b,3)}`,`${ref(a,4)}:${ref(b,4)}`)")
fr("cell(6,0,'■ أحمر", "cell(5,0,'■ أحمر")
fr("st({sz:9,b:1,c:MUTE,nb:1}));merges.push('A6:K6');", "st({sz:9,b:1,c:MUTE,nb:1}));merges.push('A5:K5');")
fr("H.forEach((h,i)=>cell(7,i,h,", "H.forEach((h,i)=>cell(6,i,h,")
fr("for(let i=0;i<11;i++)cell(8,i,i==0?'رصيد بداية الشهر'", "for(let i=0;i<11;i++)cell(7,i,i==0?'رصيد بداية الشهر'")
fr("merges.push('A8:F8');", "merges.push('A7:F7');")
# item rows: م column, car column small, no-paper sentence clear with the number small under it
fr("""  const nt=(x.note||'').includes('فاتورة ورقية')?'⚠ '+x.note.replace(/^⚠\\s*/,''):x.note||'',nr=[nt,x.ref].filter(Boolean).join(' · ');
  const V0=[j+1,serial(x.dt),x.tm||'',x.desc,x.kind,x.comp,+x.amt,bal,x.car||'',x.ph||'',nr];
  V0.forEach((v,i)=>cell(r,i,v,st({bg:i==4?(CKC[x.kind]||'EFEFEF'):z,b:i==6||i==7||i==4,sz:i==4?9:10,c:i==7?MUTE:'000000',n:i==1?164:(i==6||i==7)?4:0}),i==7?`H${r-1}-G${r}`:null))});""",
"""  const np=(x.note||'').includes(NOPAPER),rest=[(x.note||'').replace(NOPAPER,'').replace(/^[\\s·⚠]+|[\\s·]+$/g,''),x.ref].filter(Boolean).join(' · '),nr=np?{rich:[['⚠ '+NOPAPER,10,1,'C00000']].concat(rest?[['\\n'+rest,8,0,MUTE]]:[])}:rest;if(np&&rest)HT[r]=32;
  const V0=[j+1,serial(x.dt),x.tm||'',x.desc,x.kind,x.comp,+x.amt,bal,x.car||'',x.ph||'',nr];
  V0.forEach((v,i)=>cell(r,i,v,i==0?st({b:1,sz:11,c:NAVY,bg:OPENBG}):i==10&&np?st({bg:'FDE2E2'}):st({bg:i==4?(CKC[x.kind]||'EFEFEF'):z,b:i==6||i==7||i==4,sz:i==4?9:i==8?8:10,c:i==7?MUTE:'000000',n:i==1?164:(i==6||i==7)?4:0}),i==7?`H${r-1}-G${r}`:null))});""")
fr("(N?L:[null]).forEach((x,j)=>{", "const HT={1:24.5,2:20,3:17,4:22,5:12.5,6:23.5,7:20.5};\n (N?L:[null]).forEach((x,j)=>{")
fr("i==7?`H8-G${tot}`:null);", "i==7?`H7-G${tot}`:null);")
fr("const W=[5,11,7,30,10,27,12,14,20,10,30],HT={1:34,2:20,4:18,5:26,7:30,8:24,[tot]:28};", "const W=[5,11,7,30,10,27,12,14,17,10,30];HT[tot]=28;HT[sg]=14;")
fr("map(x=>{const rf=ref(x.c,r);if(x.f)return", "map(x=>{const rf=ref(x.c,r);if(x.v&&x.v.rich)return `<c r=\"${rf}\" s=\"${x.s}\" t=\"inlineStr\"><is>${x.v.rich.map(([t,sz,b,c])=>`<r><rPr>${b?'<b/>':''}<sz val=\"${sz}\"/><color rgb=\"FF${c}\"/><rFont val=\"Arial\"/></rPr><t xml:space=\"preserve\">${xe(t)}</t></r>`).join('')}</is></c>`;if(x.f)return")
fr("const cf=N?['A','B','D','F'].map(", "const cf=N?['B','D','F'].map(")
fr("""+`<conditionalFormatting sqref="K${first}:K${last}"><cfRule type="containsText" dxfId="2" priority="9" operator="containsText" text="فاتورة ورقية"><formula>NOT(ISERROR(SEARCH("فاتورة ورقية",K${first})))</formula></cfRule></conditionalFormatting>`:'';""", ":'';")
fr('<pane ySplit="7" topLeftCell="A8" activePane="bottomLeft" state="frozen"/>', '<pane ySplit="6" topLeftCell="A7" activePane="bottomLeft" state="frozen"/>')
fr("<oddFooter>&amp;Cصفحة &amp;P من &amp;N</oddFooter>", "<oddFooter>&amp;L${xe('عهدة شهر '+cMoLab(k))}&amp;Cصفحة &amp;P من &amp;N</oddFooter>")
fr("'العهدة'!$7:$7", "'العهدة'!$6:$6")
# summary sheet: by pharmacy (shared invoices split evenly)
fr("""const sheet2=`<?xml""", """const PH={};let shr2=0;L.forEach(x=>{const ns=String(x.ph||'').split(/[^0-9A-Za-z\\u0660-\\u0669]+/).filter(Boolean),a=+x.amt||0;if(ns.length>1)shr2=1;(ns.length?ns:['—']).forEach(n=>{const o=PH[n]=PH[n]||{n:0,a:0};o.n++;o.a+=a/(ns.length||1)})});
 const pk=Object.keys(PH).sort((a,b)=>a=='—'?1:b=='—'?-1:a.localeCompare(b,undefined,{numeric:true})),p0=e+2;
 if(pk.length){s2+=`<row r="${p0}" ht="24" customHeight="1">${[0,1,2,3].map(i=>s2c(p0,i,i?'':'المصروف حسب الصيدلية',st({sz:12,b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row><row r="${p0+1}">${['رقم الصيدلية','عدد الفواتير','الإجمالي (ر.س)','النسبة'].map((h,i)=>s2c(p0+1,i,h,st({b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row>`;
  pk.forEach((n,j)=>{const r=p0+2+j,a=Math.round(PH[n].a*100)/100;s2+=`<row r="${r}" ht="20" customHeight="1">${s2c(r,0,n=='—'?'بدون رقم صيدلية':n,st({b:1,bg:OPENBG}))}${s2c(r,1,PH[n].n,st({}))}${s2c(r,2,a,st({n:4,c:RED}))}${s2c(r,3,tt?a/tt:0,st({n:9}))}</row>`});
  if(shr2){const r=p0+2+pk.length;s2+=`<row r="${r}">${s2c(r,0,'الفاتورة المشتركة بين أكتر من صيدلية متقسمة عليهم بالتساوي',st({sz:9,c:MUTE,nb:1}))}</row>`}}
 const sheet2=`<?xml""")
fr('<mergeCells count="1"><mergeCell ref="A1:D1"/></mergeCells></worksheet>`;', '<mergeCells count="${pk.length?2+(shr2?1:0):1}"><mergeCell ref="A1:D1"/>${pk.length?`<mergeCell ref="A${p0}:D${p0}"/>`:\'\'}${pk.length&&shr2?`<mergeCell ref="A${p0+2+pk.length}:D${p0+2+pk.length}"/>`:\'\'}</mergeCells></worksheet>`;')
s = s[:i] + f + s[j:]
# PDF: same look
rep('el.innerHTML=`<div class="cpt"><b>كشف مصروفات العهدة — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b><small>المشرف: ${esc(C.cfg.sup)} · 966 Motors — صيدليات الدواء · تاريخ الكشف: ${TD().split(\'-\').reverse().join(\'-\')}</small></div>',
    'el.innerHTML=`<div class="cpt cy"><b>كشف مصروفات العهدة — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div><div class="cpsub">المشرف: ${esc(C.cfg.sup)} · 966 Motors — صيدليات الدواء · تاريخ الكشف: ${TD().split(\'-\').reverse().join(\'-\')}</div>')
rep("""const o=cOut(x,k),np=(x.note||'').includes('فاتورة ورقية'),nt=np?'⚠ '+x.note.replace(/^⚠\\s*/,''):x.note||'';return `<tr class="${o?'co-'+o:''}"><td class="cmk">${i+1}</td>""",
    """const o=cOut(x,k),np=(x.note||'').includes(NOPAPER),rest=[(x.note||'').replace(NOPAPER,'').replace(/^[\\s·⚠]+|[\\s·]+$/g,''),x.ref].filter(Boolean).join(' · ');return `<tr class="${o?'co-'+o:''}"><td class="cnum">${i+1}</td>""")
rep("""<td>${esc(x.car||'')}</td><td>${esc(x.ph||'')}</td><td${np?' class="cnpt"':''}>${esc([nt,x.ref].filter(Boolean).join(' · '))}</td></tr>`}).join('')}""",
    """<td class="ccar">${esc(x.car||'')}</td><td>${esc(x.ph||'')}</td>${np?`<td class="cnpt"><b>⚠ ${esc(NOPAPER)}</b>${rest?`<small class="cref">${esc(rest)}</small>`:''}</td>`:`<td>${esc(rest)}</td>`}</tr>`}).join('')}""")
# app list: the number stands out too
rep("return `<tr class=\"${o?'co-'+o:''}\" data-ced=\"${x.id}\"><td>${i+1}</td>", "return `<tr class=\"${o?'co-'+o:''}\" data-ced=\"${x.id}\"><td class=\"cnum\">${i+1}</td>")
# invoice photos appendix (PDF), numbered like the statement
JS = r"""// invoice photos appendix: one block per photo with the same number (م) as the statement
async function cAppEl(k){const C=CU(),M=C.m[k],L=M.items,el=document.createElement('div'),no=[];let h=`<div class="cpt cy"><b>ملحق صور فواتير العهدة — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div><div class="cpsub">المشرف: ${esc(C.cfg.sup)} · الرقم على كل صورة = رقم «م» في الكشف</div>`;
 for(const[i,x] of L.entries()){const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}for(const[j,key] of ks.entries()){const b=await idbGet(key);if(!b)continue;const u=URL.createObjectURL(b),d=await shrink(u,1000);URL.revokeObjectURL(u);if(!d)continue;
  h+=`<div class="cax"><div class="caxh"><b class="caxn">م ${i+1}${ks.length>1?' ('+(j+1)+')':''}</b><span>${x.dt.split('-').reverse().join('-')} · ${esc(x.desc)} · ${esc(x.comp)} · <b>${f2(x.amt)}</b></span></div><img src="${d}" alt=""></div>`}}
 if(no.length)h+=`<div class="cpsub">فواتير من غير صورة: ${no.map(n=>'م '+n).join('، ')}</div>`;el.innerHTML=h;return {el,n:L.length-no.length}}
async function cAppx(mode){const k=CU().cur;const t=toast('جاري تجهيز صور الفواتير…');let o;try{o=await cAppEl(k)}finally{t.remove()}if(!o.n)return alert('مفيش صور فواتير في الشهر ده على الجهاز ده');
 const n=cName(k,'pdf').replace(/^عهدة/,'صور فواتير عهدة').replace(/\.pdf$/,''),ttl='ملحق صور فواتير العهدة — شهر '+cMoLab(k);
 if(mode=='share')return sharePdf({src:o.el,name:n,title:ttl});const t2=toast('جاري تجهيز ملف PDF…');try{const b=await buildPdf(o.el,ttl);t2.remove();if(CAPN())return nativeSave(n+'.pdf',b,'application/pdf',false);return out(n+'.pdf',b,'application/pdf')}catch(e){t2.remove();console.error(e);alert('تعذّر تجهيز ملف PDF')}}
"""
rep("// ---- import (file prepared by Claude): {kind:'966cust',items:[...]}", JS + "// ---- import (file prepared by Claude): {kind:'966cust',items:[...]}")
rep("""<button data-cxl="save">${ic('download')}حفظ Excel</button><button data-cpdf="save">${ic('download')}حفظ PDF</button></div></div>""",
    """<button data-cxl="save">${ic('download')}حفظ Excel</button><button data-cpdf="save">${ic('download')}حفظ PDF</button><button data-capx="share">${ic('img')}مشاركة صور الفواتير PDF</button><button data-capx="save">${ic('download')}حفظ صور الفواتير PDF</button></div></div>""")
rep(" if(d.cxl){cExport('x',d.cxl);return 1}", " if(d.capx){cAppx(d.capx);return 1}\n if(d.cxl){cExport('x',d.cxl);return 1}")
CSS = """
.cpt.cy b{color:#FFFF00}.cpsub{text-align:center;color:#50164A;font-size:10px;font-weight:700;margin:3px 0 6px}
.cpdf td.cnum{background:#FFF6D6!important;color:#0B1B33!important;font-weight:800;font-size:10px}.cpdf td.ccar{font-size:7px}.cpdf td.cnpt b{display:block}.cpdf td small.cref{display:block;color:#5B6B80;font-size:7px;font-weight:400}
.ctab td.cnum{background:#FFF6D6!important;color:#0B1B33!important;font-weight:800;font-size:13.5px}
.cax{border:1px solid #D5DCE6;border-radius:6px;padding:6px;margin:6px 0;text-align:center}.caxh{display:flex;gap:8px;align-items:center;justify-content:center;font-size:11px;margin-bottom:4px;flex-wrap:wrap}.caxn{background:#FFF6D6;color:#0B1B33;border:1px solid #F2B705;border-radius:6px;padding:1px 10px;font-size:15px}.cax img{max-width:100%;max-height:820px;object-fit:contain}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'مشاركة صور الفواتير PDF':'Share invoice photos PDF','حفظ صور الفواتير PDF':'Save invoice photos PDF','جاري تجهيز صور الفواتير…':'Preparing invoice photos…','مفيش صور فواتير في الشهر ده على الجهاز ده':'No invoice photos for this month on this device','ملحق صور فواتير العهدة':'Custody invoice photos appendix','فواتير من غير صورة:':'Invoices without a photo:','المصروف حسب الصيدلية':'Expenses by pharmacy','بدون رقم صيدلية':'No pharmacy number'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
