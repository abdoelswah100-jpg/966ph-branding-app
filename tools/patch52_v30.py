"""v3.0: Medicated «المطلوب» (Header + Side / Header only / Side only); custody invoices from PDF (QR read from the PDF:
native page render on the phone, embedded images elsewhere; attach / open; appendix shares PDFs as separate files; 5 MB);
custody quotes (عرض سعر مستني الفاتورة): not in the accountant's statement, debt box, "invoice arrived" flow (invoice in the
current month with its date), pending card, notification after N days, warning before export / new month;
laptop: reminder with the Drive folder steps on open until the folder is linked."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'mdLab' not in s

# ================= Medicated: required parts =================
rep("{id:'md',n:'Medicated',nq:1,f:[sel('nm','المسمى',()=>MED),num('q','العدد (نفس العدد للـ Header والـ Side)')],z:(r,s)=>`${r.nm} · Header ${SZ('md.h')} سم (${SZ('mt.md')}) ×${r.q} + Side ${SZ('md.s')[s]} سم (${SZ('mt.md')}) ×${r.q}`},",
    "{id:'md',n:'Medicated',nq:1,f:[sel('nm','المسمى',()=>MED),sel('mdp','المطلوب',()=>MDP),num('q','العدد')],z:(r,s)=>`${r.nm} · `+[mdH(r)?`Header ${SZ('md.h')} سم (${SZ('mt.md')}) ×${r.q}`:'',mdS(r)?`Side ${SZ('md.s')[s]} سم (${SZ('mt.md')}) ×${r.q}`:''].filter(Boolean).join(' + ')},")
rep("const qn=r=>r.q==null?1:(+r.q||0);", "const qn=r=>r.q==null?1:(+r.q||0);\nconst MDP=['Header + Side','Header بس','Side بس'],mdH=r=>!r||r.mdp!==MDP[2],mdS=r=>!r||r.mdp!==MDP[1],mdLab=(t,r)=>t&&t.id=='md'&&r?(mdH(r)&&mdS(r)?'هيدر وسايد':mdH(r)?'هيدر':'سايد'):'';")
# summary / management table
rep("+rs.map(r=>`<tr><td>${esc(r.nm)}</td><td>Header ${SZ('md.h')} · ${SZ('mt.md')}<br>Side ${SZ('md.s')[rsh(r,s)]} · ${SZ('mt.md')}${rshT(r,s)}</td><td>${r.q}</td><td>${r.q}</td><td>${esc(r.nt||'')}</td></tr>`).join('')+`<tr class=\"tot\"><td colspan=\"2\"><b>الإجمالي</b></td><td><b>${q}</b></td><td><b>${q}</b></td><td></td></tr></table></div>`};",
    "+rs.map(r=>`<tr><td>${esc(r.nm)}${mdH(r)&&mdS(r)?'':`<small class=\"rshc\">${esc(r.mdp)}</small>`}</td><td>${[mdH(r)?`Header ${SZ('md.h')} · ${SZ('mt.md')}`:'',mdS(r)?`Side ${SZ('md.s')[rsh(r,s)]} · ${SZ('mt.md')}`:''].filter(Boolean).join('<br>')}${rshT(r,s)}</td><td>${mdH(r)?r.q:0}</td><td>${mdS(r)?r.q:0}</td><td>${esc(r.nt||'')}</td></tr>`).join('')+`<tr class=\"tot\"><td colspan=\"2\"><b>الإجمالي</b></td><td><b>${rs.reduce((a,r)=>a+(mdH(r)?+r.q||0:0),0)}</b></td><td><b>${rs.reduce((a,r)=>a+(mdS(r)?+r.q||0:0),0)}</b></td><td></td></tr></table></div>`};")
# sizes / materials and the management report
rep("if(t.id=='md'){k('Medicated - Header',SZ('md.h'),SZ('mt.md'),q,0,'Medicated');k('Medicated - Side',SZ('md.s')[rsh(r,p.sh)],SZ('mt.md'),q,0,'Medicated');continue}",
    "if(t.id=='md'){if(mdH(r))k('Medicated - Header',SZ('md.h'),SZ('mt.md'),q,0,'Medicated');if(mdS(r))k('Medicated - Side',SZ('md.s')[rsh(r,p.sh)],SZ('mt.md'),q,0,'Medicated');continue}")
# shortages
rep("if(t.id=='md'){o.push({...b,nm:r.nm,pt:'Header',sz:SZ('md.h'),mat:SZ('mt.md'),q,v,d});o.push({...b,nm:r.nm,pt:'Side',sz:SZ('md.s')[rsh(r,p.sh)],mat:SZ('mt.md'),q,v,d});return}",
    "if(t.id=='md'){if(mdH(r))o.push({...b,nm:r.nm,pt:'Header',sz:SZ('md.h'),mat:SZ('mt.md'),q,v,d});if(mdS(r))o.push({...b,nm:r.nm,pt:'Side',sz:SZ('md.s')[rsh(r,p.sh)],mat:SZ('mt.md'),q,v,d});return}")
# warehouse parts
rep("else if(t.id=='md'){L.push({ty:'Medicated - Header',nm,sec,size:String(SZ('md.h')),mat:SZ('mt.md'),f:1});L.push({ty:'Medicated - Side',nm,sec,size:String(SZ('md.s')[sh]),mat:SZ('mt.md'),f:1})}",
    "else if(t.id=='md'){if(mdH(r))L.push({ty:'Medicated - Header',nm,sec,size:String(SZ('md.h')),mat:SZ('mt.md'),f:1});if(mdS(r))L.push({ty:'Medicated - Side',nm,sec,size:String(SZ('md.s')[sh]),mat:SZ('mt.md'),f:1})}")
rep("return {M,K,nm,np,nps}}", "return {M,K,nm,np,nps,lab:mdLab(t,r)}}")
rep("const whTxt=(L,t)=>[L.nm>0?`${L.nm} ${['eg','md'].includes(t&&t.id)?'هيدر وسايد'", "const whTxt=(L,t)=>[L.nm>0?`${L.nm} ${L.lab?L.lab:['eg','md'].includes(t&&t.id)?'هيدر وسايد'")
rep("txt:`${Math.min(need,L.nm)} ${['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة'} (نفس المقاس)`", "txt:`${Math.min(need,L.nm)} ${L.lab||(['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة')} (نفس المقاس)`")
# receiving / execution progress (pieces)
rep("const q=qn(x.r),f=x.t.id=='eg'&&egAO(x.r,x.s)?0:pcs(x.t);", "const q=qn(x.r),f=x.t.id=='eg'&&egAO(x.r,x.s)?0:x.t.id=='md'?(mdH(x.r)?1:0)+(mdS(x.r)?1:0):pcs(x.t);")

# ================= custody: quotes + PDF invoices =================
rep("const cTot=M=>Math.round(M.items.reduce((a,x)=>a+(+x.amt||0),0)*100)/100;", "const cTot=M=>Math.round(M.items.reduce((a,x)=>a+(x.qt?0:+x.amt||0),0)*100)/100;")
rep("function custXlsx(k){const C=CU(),M=C.m[k],L=M.items.slice(),", "function custXlsx(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),")
rep("function custPdfEl(k){const C=CU(),M=C.m[k],L=M.items,", "function custPdfEl(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),")
rep("async function cAppEl(k){const C=CU(),M=C.m[k],L=M.items,el=document.createElement('div'),no=[];",
    "async function cAppEl(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),el=document.createElement('div'),no=[],pdfs=[];")
rep(" for(const[i,x] of L.entries()){const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}for(const[j,key] of ks.entries()){const b=await idbGet(key);if(!b)continue;",
    " for(const[i,x] of L.entries()){const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}const pk=ks.filter(isPdfK);pk.forEach((key,j)=>pdfs.push({i:i+1,j:pk.length>1?j+1:0,x,key}));for(const[j,key] of ks.filter(y=>!isPdfK(y)).entries()){const b=await idbGet(key);if(!b)continue;")
rep(" if(no.length)h+=`<div class=\"cpsub\">فواتير من غير صورة: ${no.map(n=>'م '+n).join('، ')}</div>`;el.innerHTML=h;return {el,n:L.length-no.length}}",
    " if(no.length)h+=`<div class=\"cpsub\">فواتير من غير صورة: ${no.map(n=>'م '+n).join('، ')}</div>`;if(pdfs.length)h+=`<div class=\"cpsub\">فواتير PDF (مبعوتة كملفات منفصلة): ${[...new Set(pdfs.map(y=>'م '+y.i))].join('، ')}</div>`;el.innerHTML=h;return {el,n:L.filter(x=>(x.imgs||[]).some(y=>!isPdfK(y))).length,pdfs}}")
rep("async function cAppx(mode){const k=CU().cur;const t=toast('جاري تجهيز صور الفواتير…');let o;try{o=await cAppEl(k)}finally{t.remove()}if(!o.n)return alert('مفيش صور فواتير في الشهر ده على الجهاز ده');",
    "async function cAppx(mode){if(!cQtOk())return;const k=CU().cur;const t=toast('جاري تجهيز صور الفواتير…');let o;try{o=await cAppEl(k)}finally{t.remove()}if(!o.n&&!o.pdfs.length)return alert('مفيش صور ولا ملفات PDF فواتير في الشهر ده على الجهاز ده');if(o.pdfs.length)return cAppxF(k,o,mode);")
rep("async function cExport(kind,mode){const k=CU().cur;", "async function cExport(kind,mode){if(!cQtOk())return;const k=CU().cur;")
# list rows: quotes without a number, tags
rep("const rows=L.map((x,i)=>{const o=cOut(x,k),np=(x.note||'').includes('فاتورة ورقية');return `<tr class=\"${o?'co-'+o:''}\" data-ced=\"${x.id}\"><td class=\"cnum\">${i+1}</td>",
    "let cn=0;const rows=L.map((x,i)=>{const o=cOut(x,k),np=(x.note||'').includes('فاتورة ورقية'),no=x.qt?'':++cn;return `<tr class=\"${o?'co-'+o:''}${x.qt==1?' cqt':x.qt==2?' cqd':''}\" data-ced=\"${x.id}\"><td class=\"cnum\">${x.qt==1?'⏳':x.qt==2?'✓':no}</td>")
rep("<small class=\"ck\" style=\"background:#${CKC[x.kind]||'EFEFEF'}\">${esc(x.kind)}</small>${np?'<small class=\"cnp\">⚠ لا توجد فاتورة ورقية</small>':''}</td>",
    "<small class=\"ck\" style=\"background:#${CKC[x.kind]||'EFEFEF'}\">${esc(x.kind)}</small>${np?'<small class=\"cnp\">⚠ لا توجد فاتورة ورقية</small>':''}${x.qt==1?'<small class=\"cqtg\">⏳ عرض سعر · مستني الفاتورة</small>':x.qt==2?`<small class=\"cqtg d\">✓ اتسدد بفاتورة ${esc(ddmm((x.qi||{}).dt))}</small>`:''}</td>")
rep("<div><small>عدد الفواتير</small><b>${L.length}</b></div></div>${cAlHtml()}", "<div><small>عدد الفواتير</small><b>${L.filter(x=>!x.qt).length}</b></div></div>${cAlHtml()}${cQtHtml()}")
rep("<button class=\"pr\" data-pick=\"cimgs\">${ic('img')}فاتورة من صورة</button>", "<button class=\"pr\" data-pick=\"cimgs\">${ic('img')}فاتورة من صورة أو PDF</button>")
rep("<input type=\"file\" id=\"cimgs\" accept=\"image/*\" multiple hidden>", "<input type=\"file\" id=\"cimgs\" accept=\"image/*,application/pdf,.pdf\" multiple hidden>")
rep("<p class=\"sub\">اضغط على أي فاتورة علشان تعدّلها أو تمسحها. ■ أحمر = تاريخها قبل الشهر · ■ أزرق = بعد الشهر.</p>",
    "<p class=\"sub\">اضغط على أي فاتورة علشان تعدّلها أو تمسحها. ■ أحمر = تاريخها قبل الشهر · ■ أزرق = بعد الشهر · ⏳ = عرض سعر مستني الفاتورة (مش في كشف المحاسب).</p>")
rep(" return `<div class=\"wcard cust\"><div class=\"cuh\"><b>كشف مصروفات العهدة", " return `${cqfHtml()}<div class=\"wcard cust\"><div class=\"cuh\"><b>كشف مصروفات العهدة")
# editor
rep(" ${d.src=='qr'?'<div class=\"ph\"><small>✓ اتقرت البيانات من كود QR الفاتورة. راجعها قبل الحفظ.</small></div>':d.src=='img'?'<div class=\"alr\"><small>⚠ ما قدرتش أقرا كود QR من الصورة. كمّل البيانات يدوي من الصورة.</small></div>':''}",
    " ${d.src=='qr'?'<div class=\"ph\"><small>✓ اتقرت البيانات من كود QR الفاتورة. راجعها قبل الحفظ.</small></div>':d.src=='img'?'<div class=\"alr\"><small>⚠ ما قدرتش أقرا كود QR من الصورة. كمّل البيانات يدوي من الصورة.</small></div>':d.src=='pdf'?'<div class=\"alr\"><small>⚠ ما قدرتش أقرا كود QR من الـ PDF. كمّل البيانات يدوي (اضغط على الملف علشان تفتحه).</small></div>':''}${cqEdHtml(d)}")
rep("${d.imgs&&d.imgs.length?`<div class=\"cimgs\">${d.imgs.map(k=>`<span><button class=\"cimgb\" data-cimgz=\"${k}\"><img data-cimg=\"${k}\" alt=\"\"></button><button class=\"np cimgx\" data-cimgx=\"${k}\">✕</button></span>`).join('')}</div>`:''}",
    "${d.imgs&&d.imgs.length?`<div class=\"cimgs\">${d.imgs.map(k=>isPdfK(k)?`<span><button class=\"cimgb cpdfb\" data-cpdfo=\"${k}\"><b>📄 PDF</b><small>${esc(((d.fn||{})[k]||{}).n||'فاتورة.pdf')}</small><small>${fsz(((d.fn||{})[k]||{}).sz||0)}</small></button><button class=\"np cimgx\" data-cimgx=\"${k}\">✕</button></span>`:`<span><button class=\"cimgb\" data-cimgz=\"${k}\"><img data-cimg=\"${k}\" alt=\"\"></button><button class=\"np cimgx\" data-cimgx=\"${k}\">✕</button></span>`).join('')}</div>`:''}")
rep(" <label>رقم الفاتورة<input data-cf=\"ref\" value=\"${esc(d.ref)}\"></label>", " <label>${d.qt?'رقم عرض السعر':'رقم الفاتورة'}<input data-cf=\"ref\" value=\"${esc(d.ref)}\"></label>")
rep("<div class=\"cbtn\"><button class=\"pr\" data-cpic=\"1\">${ic('cam')}إرفاق صورة</button></div><input type=\"file\" id=\"cimg1\" accept=\"image/*\" multiple hidden></div>",
    "<div class=\"cbtn\"><button class=\"pr\" data-cpic=\"1\">${ic('cam')}إرفاق صورة أو PDF</button></div><input type=\"file\" id=\"cimg1\" accept=\"image/*,application/pdf,.pdf\" multiple hidden></div>")
rep("<button class=\"pr big\" data-csave=\"1\">${ic('check')}حفظ الفاتورة</button>", "<button class=\"pr big\" data-csave=\"1\">${ic('check')}${d.qt==1?'حفظ عرض السعر':'حفظ الفاتورة'}</button>")
# picking images / PDFs
rep("async function cFromImages(files){const Q=[];const t=toast(`<span>جاري قراءة ${files.length} صورة…</span>`);try{for(const f of files){const z=await qrFromBlobN(f)||await qrFromBlobB(f)||await qrFromBlob(f);const d=cDraft(z?{comp:z.comp,amt:z.amt,dt:z.dt,tm:z.tm,_alt:z.alt,src:'qr'}:{src:'img'});const k=await cImgPut(d.id,f);if(k)d.imgs=[k];d._qr=!!z;Q.push(d)}}finally{t.remove()}",
    "async function cFromImages(files){const Q=[];const t=toast(`<span>جاري قراءة ${files.length} ملف…</span>`);try{for(const f of files){const pdf=isPdfF(f);if(pdf&&f.size>CPMAX){alert('⚠ الملف '+f.name+' حجمه '+fsz(f.size)+'، والحد الأقصى 5 ميجا.');continue}const z=pdf?await qrFromPdf(f):await qrFromBlobN(f)||await qrFromBlobB(f)||await qrFromBlob(f);const d=cDraft(z?{comp:z.comp,amt:z.amt,dt:z.dt,tm:z.tm,_alt:z.alt,src:'qr'}:{src:pdf?'pdf':'img'});const k=pdf?await cPdfPut(d,f):await cImgPut(d.id,f);if(k)d.imgs=[k];d._qr=!!z;Q.push(d)}}finally{t.remove()}")
rep(" if(x.id=='cimg1'){const L=[...x.files];x.value='';(async()=>{for(const f of L){const k=await cImgPut(V.ce.id,f);if(k)V.ce.imgs=(V.ce.imgs||[]).concat(k)}render()})();return 1}",
    " if(x.id=='cimg1'){const L=[...x.files];x.value='';(async()=>{for(const f of L){if(isPdfF(f)&&f.size>CPMAX){alert('⚠ الملف '+f.name+' حجمه '+fsz(f.size)+'، والحد الأقصى 5 ميجا.');continue}const k=isPdfF(f)?await cPdfPut(V.ce,f):await cImgPut(V.ce.id,f);if(k)V.ce.imgs=(V.ce.imgs||[]).concat(k)}render()})();return 1}")
# save: quotes, linked invoice
rep("const x=Object.assign({},d,{amt,desc:d.desc.trim(),comp:d.comp.trim(),at:d.at||nowIso()});const seq=d._seq;['_alt','_qr','_new','_seq'].forEach(k=>delete x[k]);",
    "const x=Object.assign({},d,{amt,desc:d.desc.trim(),comp:d.comp.trim(),at:d.at||nowIso()});const seq=d._seq,qref=d._q;['_alt','_qr','_new','_seq','_q'].forEach(k=>delete x[k]);if(!x.qt)delete x.qt;if(qref&&x.qt){delete x.qt}")
rep(" const M=cMo(),i=M.items.findIndex(y=>y.id==x.id);if(i>=0)M.items[i]=x;else M.items.push(x);cSort(M.items);",
    " if(qref)cQtClose(qref,x);const M=cMo(),i=M.items.findIndex(y=>y.id==x.id);if(i>=0)M.items[i]=x;else M.items.push(x);cSort(M.items);")
rep("function cDup(d){const M=cMo();return M.items.find(x=>x.id!=d.id&&(", "function cDup(d){const M=cMo();return M.items.find(x=>x.id!=d.id&&!!x.qt==!!d.qt&&(")
rep("function cDraft(o){const M=cMo(),", "function cDraft(o){o=cqfFill(o);const M=cMo(),")
# new month: warning
rep(" if(d.cnewgo){const C=CU(),v=d.cnewgo=='v'?", " if(d.cnewgo){if(!cQtOk())return 1;const C=CU(),v=d.cnewgo=='v'?")
# notifications
rep("const NTD={on:{due:1,stall:1,low:1,bk:1,cust:1},tm:'11:00',sd:3,list:[]};", "const NTD={on:{due:1,stall:1,low:1,bk:1,cust:1,qt:1},tm:'11:00',sd:3,qd:3,list:[]};")
rep("cust:'العهدة المتبقي أقل من الحد'};", "cust:'العهدة المتبقي أقل من الحد',qt:'عرض سعر مستني فاتورة'};")
rep(" if(c.on.cust){try{const M=cMo(),lim=cAl();", " if(c.on.qt){try{cQts().forEach(({x})=>{const n=dayDiff(x.dt);if(n>=c.qd)o.push({k:'qt',t:'عرض سعر مستني فاتورة من '+n+' يوم: '+x.desc+' · '+x.comp+' · '+f2(x.amt)})})}catch(e){}}\n if(c.on.cust){try{const M=cMo(),lim=cAl();")
rep(" if(c.on.bk){const t=DB.cfg.lb?", " if(c.on.qt){try{const Q=cQts();if(Q.length){for(let i=0;i<14;i++){const day=new Date(Date.now()+i*864e5),dIso=day.getFullYear()+'-'+z2(day.getMonth()+1)+'-'+z2(day.getDate()),L=Q.filter(({x})=>Math.floor((new Date(dIso)-new Date(x.dt))/864e5)>=c.qd);if(L.length)add('qt:'+dIso,'⏳ عرض سعر مستني فاتورة','عندك '+L.length+' عرض سعر من غير فاتورة بإجمالي '+f2(L.reduce((a,y)=>a+(+y.x.amt||0),0))+' ريال. ما ينفعش تسلّم العهدة من غيرها.',atDay(day,tm),{v:'cust'})}}}catch(e){}}\n if(c.on.bk){const t=DB.cfg.lb?")
rep("<label>الصيدلية تعتبر واقفة بعد (يوم)<input type=\"number\" inputmode=\"numeric\" min=\"1\" id=\"ntfsd\" value=\"${c.sd}\"></label>",
    "<label>الصيدلية تعتبر واقفة بعد (يوم)<input type=\"number\" inputmode=\"numeric\" min=\"1\" id=\"ntfsd\" value=\"${c.sd}\"></label><label>نبّهني على عرض السعر اللي مستني فاتورة بعد (يوم)<input type=\"number\" inputmode=\"numeric\" min=\"0\" id=\"ntfqd\" value=\"${c.qd}\"></label>")
# laptop reminder
rep("async function gdlInit(){if(CAPN()||!window.showDirectoryPicker)return;try{GDH=(await idbGet('gddir'))||null}catch(e){GDH=null}if(!GDH)return;",
    "async function gdlInit(){if(CAPN())return;if(window.showDirectoryPicker){try{GDH=(await idbGet('gddir'))||null}catch(e){GDH=null}}if(!GDH){gdlRemind();return}")
# hooks
rep("v28Click(d,b)||v29Click(d,b)||", "v28Click(d,b)||v29Click(d,b)||v30Click(d,b)||")
rep("v28Change(x)||v29Change(x)||", "v28Change(x)||v29Change(x)||v30Change(x)||")

JS = r"""// ---------- v3.0: custody PDF invoices and quotes ----------
const CPMAX=5*1048576,isPdfK=k=>/:pdf$/.test(String(k||'')),ddmm=d=>d?String(d).slice(8,10)+'-'+String(d).slice(5,7):'';
async function cPdfPut(d,f){if(f.size>CPMAX)return null;const k='cimg:'+d.id+':'+Date.now()+Math.random().toString(36).slice(2,6)+':pdf';if(await idbSet(k,new Blob([f],{type:'application/pdf'}))){d.fn=d.fn||{};d.fn[k]={n:f.name||'فاتورة.pdf',sz:f.size};return k}return null}
async function cPdfOpen(k){const b=await idbGet(k);if(!b)return alert('الملف مش موجود على الجهاز ده. انقله بـ "نسخة كاملة مع الصور والمرفقات".');const n=(((V.ce||{}).fn||{})[k]||{}).n||'فاتورة.pdf';
 const P=CP('PdfTools'),FS=CP('Filesystem');if(P&&FS){try{const w=await FS.writeFile({path:'open-'+Date.now()+'.pdf',data:await b64of(b),directory:'CACHE'});await P.open({path:w.uri,mime:'application/pdf'});return}catch(e){console.warn(e)}}
 if(CAPN()){dl(n,b,'application/pdf');return}const u=URL.createObjectURL(b);const w=window.open(u,'_blank');if(!w)dl(n,b,'application/pdf')}
// QR from a PDF: phone = render the pages (Android PdfRenderer), then images embedded in the PDF (laptop too)
async function qrFromPdf(b){const P=CP('PdfTools'),FS=CP('Filesystem');
 if(P&&FS){try{const w=await FS.writeFile({path:'qp-'+Date.now()+'.pdf',data:await b64of(b),directory:'CACHE'});let r;try{r=await P.render({path:w.uri,pages:2,width:1600})}finally{FS.deleteFile({path:w.uri,directory:'CACHE'}).catch(()=>{})}
  for(const pg of (r&&r.pages)||[]){const jb=await (await fetch('data:image/jpeg;base64,'+pg)).blob();const z=await qrFromBlobN(jb)||await qrFromBlobB(jb)||await qrFromBlob(jb);if(z)return z}}catch(e){console.warn('pdf render',e)}}
 try{const L=await pdfImgs(await b.arrayBuffer(),20);for(const x of L){const jb=x.blob||await imgDataBlob(x.img);if(!jb)continue;const z=await qrFromBlobB(jb)||await qrFromBlob(jb);if(z)return z}}catch(e){console.warn('pdf imgs',e)}return null}
function a85(u){const o=[];let t=[],i=0;const s=new TextDecoder('latin1').decode(u).replace(/^\s*<~/,'');for(;i<s.length;i++){const c=s[i];if(c=='~')break;if(c<=' ')continue;if(c=='z'&&!t.length){o.push(0,0,0,0);continue}const v=c.charCodeAt(0)-33;if(v<0||v>84)return null;t.push(v);if(t.length==5){let n=0;for(const x of t)n=n*85+x;o.push(n>>>24&255,n>>>16&255,n>>>8&255,n&255);t=[]}}
 if(t.length){const k=t.length;while(t.length<5)t.push(84);let n=0;for(const x of t)n=n*85+x;const b=[n>>>24&255,n>>>16&255,n>>>8&255,n&255];o.push(...b.slice(0,k-1))}return new Uint8Array(o)}
function pngUnfilter(d,W,nc,bpc,H){const bpp=Math.max(1,Math.ceil(nc*bpc/8)),rl=Math.ceil(W*nc*bpc/8),o=new Uint8Array(rl*H);let p=0;
 for(let y=0;y<H;y++){if(p>=d.length)return null;const ft=d[p++],r=y*rl,pr=r-rl;for(let x=0;x<rl;x++){const a=x>=bpp?o[r+x-bpp]:0,b2=y?o[pr+x]:0,c=y&&x>=bpp?o[pr+x-bpp]:0,v=d[p++]||0;let q;
  if(ft==0)q=v;else if(ft==1)q=v+a;else if(ft==2)q=v+b2;else if(ft==3)q=v+((a+b2)>>1);else{const pp=a+b2-c,pa=Math.abs(pp-a),pb=Math.abs(pp-b2),pc=Math.abs(pp-c);q=v+(pa<=pb&&pa<=pc?a:pb<=pc?b2:c)}o[r+x]=q&255}}return o}
async function pdfImgs(buf,max){const u=new Uint8Array(buf),S=new TextDecoder('latin1').decode(u),out=[],re=/<<((?:[^<>]|<<(?:[^<>]|<<[^<>]*>>)*>>)*)>>\s*stream\r?\n/g;let m;
 while((m=re.exec(S))&&out.length<(max||20)){const d=m[1];if(!/\/Subtype\s*\/Image/.test(d))continue;const st=m.index+m[0].length,en=S.indexOf('endstream',st);if(en<0)continue;
  const lm=/\/Length\s+(\d+)(?!\s+\d+\s+R)/.exec(d);let e2=lm?st+(+lm[1]):en;if(e2>en)e2=en;while(!lm&&e2>st&&(u[e2-1]==10||u[e2-1]==13))e2--;const raw=u.subarray(st,e2);
  const W=+((/\/Width\s+(\d+)/.exec(d)||[])[1]||0),H=+((/\/Height\s+(\d+)/.exec(d)||[])[1]||0);if(!W||!H||W*H>16e6)continue;
  const FL=(((/\/Filter\s*(\[[^\]]*\]|\/\w+)/.exec(d)||[])[1]||'').match(/\/\w+/g)||[]).map(x=>x.slice(1));let data=raw,jpg=0,bad=0;
  for(const f of FL){if(f=='ASCII85Decode'||f=='A85')data=a85(data);else if(f=='FlateDecode'||f=='Fl'){try{data=new Uint8Array(await new Response(new Blob([data]).stream().pipeThrough(new DecompressionStream('deflate'))).arrayBuffer())}catch(e){bad=1;break}}else if(f=='DCTDecode'||f=='DCT')jpg=1;else{bad=1;break}}
  if(bad||!data)continue;if(jpg){out.push({blob:new Blob([data],{type:'image/jpeg'})});continue}
  if(/Indexed/.test(d))continue;const mask=/\/ImageMask\s+true/.test(d),bpc=mask?1:+((/\/BitsPerComponent\s+(\d+)/.exec(d)||[])[1]||8);if(bpc!=1&&bpc!=8)continue;
  const pred=+((/\/Predictor\s+(\d+)/.exec(d)||[])[1]||1);let nc=mask?1:/\/DeviceRGB|\/CalRGB/.test(d)?3:/\/DeviceCMYK/.test(d)?4:/\/DeviceGray|\/CalGray/.test(d)?1:0;
  if(!nc){for(const n of [1,3,4]){const rb=Math.ceil(W*n*bpc/8);if(data.length==rb*H||data.length==(rb+1)*H){nc=n;break}}if(!nc)continue}
  if(pred>=10){data=pngUnfilter(data,W,nc,bpc,H);if(!data)continue}
  const rb=Math.ceil(W*nc*bpc/8);if(data.length<rb*H)continue;const id=new ImageData(W,H),px=id.data;
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const q=(y*W+x)*4;let r,g,bl;if(bpc==1){const v=((data[y*rb+(x>>3)]>>(7-(x&7)))&1)?255:0;r=g=bl=v}else{const o=y*rb+x*nc;if(nc==1)r=g=bl=data[o];else if(nc==3){r=data[o];g=data[o+1];bl=data[o+2]}else{const k=data[o+3];r=255-Math.min(255,data[o]+k);g=255-Math.min(255,data[o+1]+k);bl=255-Math.min(255,data[o+2]+k)}}px[q]=r;px[q+1]=g;px[q+2]=bl;px[q+3]=255}
  out.push({img:id})}
 return out}
function imgDataBlob(id){const s=Math.max(1,Math.ceil(600/Math.max(id.width,id.height))),pad=Math.round(Math.max(id.width,id.height)*s*0.12),a=document.createElement('canvas');a.width=id.width;a.height=id.height;a.getContext('2d').putImageData(id,0,0);
 const c=document.createElement('canvas');c.width=id.width*s+pad*2;c.height=id.height*s+pad*2;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.imageSmoothingEnabled=false;x.drawImage(a,pad,pad,id.width*s,id.height*s);return new Promise(ok=>c.toBlob(b=>ok(b),'image/png'))}
const cSafe=t=>String(t||'').replace(/[\\/:*?"<>|\n\r]+/g,' ').trim().slice(0,60);
async function cAppxF(k,o,mode){const n=cName(k,'pdf').replace(/^عهدة/,'صور فواتير عهدة').replace(/\.pdf$/,''),ttl='ملحق صور فواتير العهدة — شهر '+cMoLab(k),F=[];
 if(o.n){const t=toast('جاري تجهيز ملف PDF…');try{F.push(new File([await buildPdf(o.el,ttl)],n+'.pdf',{type:'application/pdf'}))}catch(e){console.error(e)}finally{t.remove()}}
 for(const y of o.pdfs){const b=await idbGet(y.key);if(b)F.push(new File([b],cSafe('فاتورة م '+y.i+(y.j?'-'+y.j:'')+' - '+y.x.desc+' - '+y.x.comp)+'.pdf',{type:'application/pdf'}))}
 if(!F.length)return alert('ما قدرتش أجهز الملفات');if(mode=='share')return shareFiles(F,ttl);
 for(const f of F){if(CAPN())await nativeSave(f.name,f,'application/pdf',false);else{dl(f.name,f,'application/pdf');await new Promise(r=>setTimeout(r,350))}}}
// ---- quotes: x.qt 1 = paid with a quote, invoice not here yet (not in the accountant's statement); 2 = closed by an invoice in a later month (x.qi)
function cQts(){const C=CU(),o=[];Object.keys(C.m).sort().forEach(mo=>(C.m[mo].items||[]).forEach(x=>{if(x.qt==1)o.push({mo,x})}));return o.sort((a,b)=>(a.x.dt||'').localeCompare(b.x.dt||''))}
function cQtHtml(){const Q=cQts();if(!Q.length)return '';const sum=Math.round(Q.reduce((a,y)=>a+(+y.x.amt||0),0)*100)/100,rem=cRem(cMo());
 return `<div class="alr cqal"><b>⚠ عندك ${Q.length} عرض سعر مستني فاتورة · إجمالي ${f2(sum)}</b><small>ما ينفعش تسلّم العهدة من غير فواتيرهم. عروض السعر مش في كشف المحاسب.</small>${Q.map(({mo,x})=>`<button class="lnk" data-cqo="${mo}|${x.id}">${esc(ddmm(x.dt))} · ${esc(x.desc)} · ${esc(x.comp)} · <b>${f2(x.amt)}</b> · من ${dayDiff(x.dt)} يوم ›</button>`).join('')}</div>
 <div class="ckpi cqk"><div><small>دين بعرض سعر</small><b class="c-exp">${f2(sum)}</b></div><div><small>الكاش اللي معاك فعليًا</small><b class="c-rem">${f2(Math.round((rem-sum)*100)/100)}</b></div></div>`}
function cQtOk(){const Q=cQts();if(!Q.length)return true;return confirm(`⚠ عندك ${Q.length} عرض سعر مستني فاتورة بإجمالي ${f2(Q.reduce((a,y)=>a+(+y.x.amt||0),0))}:\n`+Q.map(({x})=>`• ${ddmm(x.dt)} · ${x.desc} · ${x.comp} · ${f2(x.amt)}`).join('\n')+`\nعروض السعر مش هتظهر في الكشف. تكمّل؟`)}
function cqEdHtml(d){const saved=cMo().items.some(x=>x.id==d.id);if(d.qt==2)return `<div class="ph"><small>✓ عرض السعر ده اتسدد بفاتورة بتاريخ ${esc(ddmm((d.qi||{}).dt))} في عهدة شهر ${esc(cMoLab((d.qi||{}).mo||''))}${(d.qi||{}).amt!=null?' بمبلغ '+f2(d.qi.amt):''}.</small></div>`;
 if(d._q){const q=cQf(d._q);return q?`<div class="ph"><small>📥 دي فاتورة عرض السعر: ${esc(ddmm(q.dt))} · ${esc(q.desc)} · ${esc(q.comp)} · ${f2(q.amt)}. لما تحفظها، عرض السعر بيتقفل.</small></div>`:''}
 return `<div class="cqsw"><button class="${d.qt==1?'':'pr'}" data-cqt="0">فاتورة</button><button class="${d.qt==1?'pr':''}" data-cqt="1">⏳ عرض سعر (مستني الفاتورة)</button></div>${d.qt==1?`<small class="hint">عرض السعر مش بيدخل في كشف المحاسب، وبيظهر عندك كدين لحد ما الفاتورة توصل.</small>${saved?'<div class="tt"><button class="pr big" data-cqarr="1">✓ وصلت الفاتورة</button></div>':''}`:''}`}
const cQf=r=>{const M=r&&CU().m[r.mo];return M&&(M.items||[]).find(x=>x.id==r.id)||null};
function cqfHtml(){const r=V.cqf,q=cQf(r);if(!q)return '';return `<div class="wcard cqf"><b>📥 إضافة فاتورة لعرض السعر</b><small>${esc(ddmm(q.dt))} · ${esc(q.desc)} · ${esc(q.comp)} · ${f2(q.amt)} · الفاتورة هتتسجل في عهدة شهر ${cMoLab(CU().cur)} بتاريخها</small><div class="cbtn"><button class="pr" data-cscan="1">${ic('cam')}امسح QR</button><button class="pr" data-pick="cimgs">${ic('img')}صورة أو PDF</button><button data-cqman="1">${ic('edit')}يدوي</button><button data-cqfx="1">إلغاء</button></div></div>`}
function cqfFill(o){o=o||{};const r=V.cqf;if(!r||o._q||o.src=='import')return o;const q=cQf(r);V.cqf=null;if(!q)return o;const b={comp:q.comp,desc:q.desc,kind:q.kind,ph:q.ph,car:q.car,amt:q.amt,_q:{mo:r.mo,id:r.id}};Object.keys(o).forEach(k=>{if(o[k]!==undefined&&o[k]!=='')b[k]=o[k]});return b}
function cQtClose(r,x){const M=CU().m[r.mo];if(!M)return;const q=(M.items||[]).find(y=>y.id==r.id);if(!q)return;const df=Math.abs((+q.amt||0)-(+x.amt||0))>0.004;
 const nt='عرض سعر بتاريخ '+ddmm(q.dt)+(df?' · عرض السعر كان '+f2(q.amt):'');x.note=[x.note,nt].filter(Boolean).join(' · ');x.qf={dt:q.dt,amt:q.amt,ref:q.ref||''};
 if(r.mo==CU().cur){x.imgs=(x.imgs||[]).concat((q.imgs||[]).filter(k=>!(x.imgs||[]).includes(k)));x.fn=Object.assign({},q.fn||{},x.fn||{});M.items=M.items.filter(y=>y.id!=q.id)}
 else{q.qt=2;q.qi={dt:x.dt,mo:CU().cur,id:x.id,amt:x.amt}}}
// ---- laptop: Drive folder steps until it is linked (once a day)
function gdlRemind(){const o=gdS();if(navigator.webdriver||o.rmd==TD()||document.querySelector('.toast.gdrem'))return;const t=toast(`<span><b>☁️ تذكير: ربط فولدر Google Drive</b><br>1) Google Drive for desktop: في «sync folders» اضغط Skip.<br>2) G:\\My Drive\\966Ph Backups ← كليك يمين ← Offline access ← Available offline.<br>3) Chrome أو Edge: ☰ ← Google Drive ← «ربط فولدر درايف» ← Allow on every visit.</span><button class="pr" data-gdremgo="1">افتح الخطوات</button><button data-gdremx="1">بكرة</button>`);t.classList.add('rem','gdrem')}
function v30Click(d,b){
 if(d.cpdfo){cPdfOpen(d.cpdfo);return 1}
 if(d.cqt!==undefined&&V.ce){V.ce.qt=d.cqt=='1'?1:0;render();return 1}
 if(d.cqarr&&V.ce){const id=V.ce.id,mo=CU().cur;if(!cMo().items.some(x=>x.id==id&&x.qt==1))return 1;const ks=Object.keys(CU().m).sort();CU().cur=ks[ks.length-1];svq();V={v:'cust',op:{},dr:{},q:V.q,cq:[],cqf:{mo,id}};render();scrollTo(0,0);return 1}
 if(d.cqman){V.cq=[];cOpen(cDraft({}));return 1}
 if(d.cqfx){V.cqf=null;render();return 1}
 if(d.cqo){const[mo,id]=d.cqo.split('|');CU().cur=mo;const x=(CU().m[mo].items||[]).find(y=>String(y.id)==id);if(x){V.cq=[];cOpen(JSON.parse(JSON.stringify(x)))}return 1}
 if(d.gdremgo){const t=b.closest('.toast');if(t)t.remove();goV({v:'gd',from:V.v,op:{},dr:{},q:V.q});return 1}
 if(d.gdremx){const t=b.closest('.toast');if(t)t.remove();gdU(o=>o.rmd=TD());return 1}
 return 0}
function v30Change(x){if(x.id=='ntfqd'){NTF().qd=Math.max(0,Math.round(+x.value||0));svq();ntfLater();return 1}return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.cqt td{background:#FFF4E0!important}.cqd td{color:var(--mu)}.cqtg{display:block;color:#B45309;font-weight:700}.cqtg.d{color:#1E7B45}.cqal{display:flex;flex-direction:column;gap:4px}.cqal .lnk{text-align:start}.cqk{margin-top:6px}.cqsw{display:flex;gap:6px;margin:6px 0}.cqsw button{flex:1}.cqf{border:2px solid #F59E0B}.cqf small{display:block;margin:4px 0}.cpdfb{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;width:120px;height:120px;padding:6px!important;background:#FFF5F5!important}.cpdfb b{color:#B42318;font-size:18px}.cpdfb small{font-size:10px;word-break:break-all;line-height:1.2}.gdrem span{line-height:1.6}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
rep("VER='v2.9'", "VER='v3.0'")
rep(" changelog:[{version:'v2.9',", " changelog:[{version:'v3.0',date:'2026-11-04',changes:['Medicated: new field المطلوب (Header + Side / Header only / Side only) used in the summary, management report, shortages, receiving / execution and the warehouse; old items stay Header + Side','Custody: invoice from an image or a PDF; the QR is read from the PDF (phone: page render, laptop: images inside the PDF); PDF attached to the invoice and opened in the phone viewer; max 5 MB; the photos appendix sends the PDFs as separate files','Custody quotes (عرض سعر مستني الفاتورة): not in the accountant statement, debt box and actual cash, pending card, «وصلت الفاتورة» (the invoice goes to the current month with its date, the quote closes), notification after 3 days (editable), warning before Excel / PDF / new month','Laptop: reminder with the Drive folder steps on open (once a day) until the folder is linked']},{version:'v2.9',")
EN = {'المطلوب':'Required','Header بس':'Header only','Side بس':'Side only','فاتورة من صورة أو PDF':'Invoice from an image or PDF','إرفاق صورة أو PDF':'Attach an image or PDF','فاتورة':'Invoice','⏳ عرض سعر (مستني الفاتورة)':'⏳ Quote (waiting for the invoice)','حفظ عرض السعر':'Save quote','رقم عرض السعر':'Quote number','✓ وصلت الفاتورة':'✓ The invoice arrived','دين بعرض سعر':'Paid by quote (debt)','الكاش اللي معاك فعليًا':'Actual cash in hand','📥 إضافة فاتورة لعرض السعر':'📥 Add the invoice for the quote','امسح QR':'Scan QR','صورة أو PDF':'Image or PDF','يدوي':'Manual','عرض سعر مستني فاتورة':'Quote waiting for an invoice','افتح الخطوات':'Open the steps','بكرة':'Tomorrow','⏳ عرض سعر · مستني الفاتورة':'⏳ Quote · waiting for the invoice','نبّهني على عرض السعر اللي مستني فاتورة بعد (يوم)':'Remind me about a quote waiting for its invoice after (days)'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
