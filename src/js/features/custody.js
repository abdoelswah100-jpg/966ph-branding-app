// ---------- custody (العهدة): monthly expense sheet per supervisor ----------
const CK=['وجبات','وقود','شحن','سكن','مشتريات','سيارة','تنقلات','إيجار'];
const CKC={'وجبات':'FDE7D9','وقود':'DCEBFA','شحن':'E5E1F5','سكن':'DDF1E4','مشتريات':'FFF4D1','سيارة':'DCEBFA','تنقلات':'F3E3EE','إيجار':'EFEFEF'};
const NOPAPER='لا توجد فاتورة ورقية الرجاء الطباعة';
function CU(){const c=DB.cust=DB.cust||{};c.m=c.m||{};c.mem=c.mem||{};c.cfg=Object.assign({car:'متسوبيشي ( ب ق ن 2890 )',region:uRegTitle(),sup:U().nm||DB.cfg.dsup||'عبدالله السواح',base:10000,min:2000},c.cfg||{});if(!c.cur)c.cur=MN();if(!c.m[c.cur])c.m[c.cur]={open:c.cfg.base,why:'',items:[]};return c}
const cMo=()=>CU().m[CU().cur];
const cMoLab=k=>{const[y,m]=String(k).split('-');return `${+m} / ${y}`};
const cNext=k=>{const[y,m]=k.split('-').map(Number);return m==12?`${y+1}-01`:`${y}-${z2(m+1)}`};
const cSort=L=>L.sort((a,b)=>(a.dt||'').localeCompare(b.dt||'')||(a.tm||'99').localeCompare(b.tm||'99')||(a.at||'').localeCompare(b.at||''));
const cTot=M=>Math.round(M.items.reduce((a,x)=>a+(x.qt?0:+x.amt||0),0)*100)/100;
const cRem=M=>Math.round(((+M.open||0)+cDep(M)-cTot(M))*100)/100;
const f2=v=>(+v||0).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const cOut=(x,k)=>x.dt&&x.dt.slice(0,7)<k?'old':x.dt&&x.dt.slice(0,7)>k?'next':'';
function mealOf(tm){const h=parseInt(String(tm||'').split(':')[0],10);if(isNaN(h))return '';return h<4?'عشاء':h<11?'فطار':h<19?'غداء':'عشاء'}
const cnk=t=>anorm(t).replace(/[ـ]/g,'');
function kindOf(comp,desc){const m=CU().mem[cnk(comp)];if(m&&m.kind)return m.kind;const t=(comp||'')+' '+(desc||'');
 for(const[k,w] of [['وقود',['وقود','محطه','محطة','بترول','الدريس','ساسكو','نفط','diesel','ديزيل','بنزين','sasco','aldrees']],['شحن',['شحن','السيف','alsaif','express','بريد']],['سكن',['شقق','فندق','أجنحة','اجنحة','سكن','apartments','suites','hotel','نزل']],['تنقلات',['باص','تذكرة','حافلات','درب الوطن','نقل جماعي','سابتكو']],['سيارة',['مغسلة','غسيل','ورشة','زيوت','كفرات']],['وجبات',['مطعم','مطاعم','شاورما','فوال','بوفيه','كافيه','كوفي','مخبز','حلويات','وجبات','بروست','كبسة','بخاري','تموينات','سوبرماركت','اسواق','أسواق','restaurant','shawarma','cafe','house']]])if(w.some(x=>t.toLowerCase().includes(x.toLowerCase())))return k;return 'مشتريات'}
function descOf(kind,tm,comp){const m=CU().mem[cnk(comp)],ml=mealOf(tm);if(m&&m.desc){if(kind=='وجبات'&&ml)return m.desc.replace(/فطار|غداء|عشاء/,ml);return m.desc}
 return kind=='وجبات'?(ml||'وجبة')+' عمال الشركة':kind=='وقود'?'ديزيل':kind=='شحن'?'استلام شحن':kind=='سكن'?'سكن عمال الشركة':kind=='تنقلات'?'تنقلات':kind=='سيارة'?'غسيل سيارة':'مشتريات'}
// ---- ZATCA QR (TLV in base64): 1 seller · 2 VAT no · 3 time · 4 total incl. VAT · 5 VAT
function zatca(s){try{const b=Uint8Array.from(atob(String(s).trim()),c=>c.charCodeAt(0)),o={};let i=0;while(i+2<=b.length){const t=b[i],l=b[i+1];if(i+2+l>b.length)break;o[t]=new TextDecoder().decode(b.slice(i+2,i+2+l));i+=2+l}
 if(!o[1]||!o[4]||isNaN(parseFloat(o[4])))return null;const ts=String(o[3]||''),m=ts.match(/(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})/);let dt='',tm='',alt=null;
 if(m){dt=`${m[1]}-${m[2]}-${m[3]}`;tm=`${m[4]}:${m[5]}`;if(/Z$|[+-]00:?00$/.test(ts)){const d=new Date(Date.UTC(+m[1],+m[2]-1,+m[3],+m[4]+3,+m[5]));alt={dt:d.toISOString().slice(0,10),tm:d.toISOString().slice(11,16)}}}
 return{comp:o[1].trim(),vat:o[2]||'',dt,tm,alt,amt:Math.round(parseFloat(o[4])*100)/100,tax:parseFloat(o[5])||0}}catch(e){return null}}
function qrGray(id,W,H,th){const g=new Uint8ClampedArray(W*H*4);let hist=th?new Array(256).fill(0):null;const L=new Uint8Array(W*H);for(let i=0,j=0;i<W*H;i++,j+=4){const v=(id[j]*299+id[j+1]*587+id[j+2]*114)/1000|0;L[i]=v;if(hist)hist[v]++}
 let t=128;if(hist){let sum=0,sb=0,wb=0,mx=0;for(let i=0;i<256;i++)sum+=i*hist[i];for(let i=0;i<256;i++){wb+=hist[i];if(!wb)continue;const wf=W*H-wb;if(!wf)break;sb+=i*hist[i];const mb=sb/wb,mf=(sum-sb)/wf,v=wb*wf*(mb-mf)*(mb-mf);if(v>mx){mx=v;t=i}}}
 for(let i=0,j=0;i<W*H;i++,j+=4){const v=hist?(L[i]>t?255:0):L[i];g[j]=g[j+1]=g[j+2]=v;g[j+3]=255}return g}
async function qrFromBlob(blob){if(!window.jsQR)return null;const u=URL.createObjectURL(blob);try{const im=await new Promise((ok,no)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=no;i.src=u});
  const cv=document.createElement('canvas'),x=cv.getContext('2d',{willReadFrequently:true}),W0=im.naturalWidth,H0=im.naturalHeight,R=[];
  const tryR=(sx,sy,sw,sh,sc,th)=>{const W=Math.max(1,Math.round(sw*sc)),H=Math.max(1,Math.round(sh*sc));if(W*H>9e6)return null;cv.width=W;cv.height=H;x.imageSmoothingQuality='high';x.drawImage(im,sx,sy,sw,sh,0,0,W,H);const d=qrGray(x.getImageData(0,0,W,H).data,W,H,th);const r=jsQR(d,W,H,{inversionAttempts:th?'dontInvert':'attemptBoth'});return r&&r.data?r.data:null};
  const big=Math.max(W0,H0),base=big>2200?2200/big:1;
  for(const[sc,th] of [[base,0],[base,1],[base*2,1],[base*1.5,0]]){const r=tryR(0,0,W0,H0,Math.min(sc,4000/big),th);if(r){R.push(r);const z=zatca(r);if(z)return z}}
  for(let gy=0;gy<4;gy++)for(let gx=0;gx<3;gx++){const sw=W0/2,sh=H0/2.5,sx=gx*W0/4,sy=gy*(H0-sh)/3;const r=tryR(sx,sy,sw,sh,Math.min(3,1800/Math.max(sw,sh)),1);if(r){const z=zatca(r);if(z)return z}}
  for(let gy=0;gy<3;gy++)for(let gx=0;gx<2;gx++){const sw=W0*2/3,sh=H0/2,sx=gx*W0/3,sy=gy*H0/4;for(const th of [1,0]){const r=tryR(sx,sy,sw,sh,Math.min(3,2400/Math.max(sw,sh)),th);if(r){const z=zatca(r);if(z)return z}}}
  return null}catch(e){console.warn(e);return null}finally{URL.revokeObjectURL(u)}}
// ---- invoice images (IndexedDB, key cimg:<item>:<n>)
async function cImgPut(id,blob){const L=[];const u=URL.createObjectURL(blob);try{const r=await shrink(u,1600)||null;if(!r)return null;const b=await (await fetch(r)).blob();const k='cimg:'+id+':'+Date.now()+Math.random().toString(36).slice(2,6);if(await idbSet(k,b))return k}finally{URL.revokeObjectURL(u)}return null}
const CIU={};
async function cImgUrl(k){if(CIU[k])return CIU[k];const b=await idbGet(k);if(!b)return '';return CIU[k]=URL.createObjectURL(b)}
async function cImgFill(){for(const e of document.querySelectorAll('img[data-cimg]')){const u=await cImgUrl(e.dataset.cimg);if(u)e.src=u}}
// ---- editor queue: each picked image becomes one draft invoice
function cDraft(o){o=cqfFill(o);const M=cMo(),k=CU().cur,today=TD(),dt=o.dt||(today.slice(0,7)==k?today:k+'-01'),kind=o.kind||kindOf(o.comp,o.desc),tm=o.tm||'';
 return Object.assign({id:Date.now()+Math.floor(Math.random()*1000),dt,tm,comp:'',amt:'',car:'',ph:'',ref:'',note:'',imgs:[],src:'manual'},o,{kind,desc:o.desc||descOf(kind,tm,o.comp||''),car:o.car!=null&&o.car!==''?o.car:((kind=='وقود'||kind=='سيارة')?CU().cfg.car:'')})}
async function cFromImages(files){const Q=[];const t=toast(`<span>جاري قراءة ${files.length} ملف…</span>`);try{for(const f of files){const pdf=isPdfF(f);if(pdf&&f.size>CPMAX){alert('⚠ الملف '+f.name+' حجمه '+fsz(f.size)+'، والحد الأقصى 5 ميجا.');continue}const z=pdf?await qrFromPdf(f):await qrFromBlobN(f)||await qrFromBlobB(f)||await qrFromBlob(f);const d=cDraft(z?{comp:z.comp,amt:z.amt,dt:z.dt,tm:z.tm,_alt:z.alt,src:'qr'}:{src:pdf?'pdf':'img'});const k=pdf?await cPdfPut(d,f):await cImgPut(d.id,f);if(k)d.imgs=[k];d._qr=!!z;Q.push(d)}}finally{t.remove()}
 if(!Q.length)return;V.cq=Q;V.ce=Q.shift();goV(Object.assign(V,{v:'ced'}))}
function cOpen(d){V.ce=d;V.cq=V.cq||[];goV(Object.assign(V,{v:'ced'}))}
function cDup(d){const M=cMo();return M.items.find(x=>x.id!=d.id&&!!x.qt==!!d.qt&&((d.ref&&x.ref&&cnk(x.ref)==cnk(d.ref))||(Math.abs((+x.amt||0)-(+d.amt||0))<0.005&&x.dt==d.dt&&(cnk(x.comp)==cnk(d.comp)||x.kind==d.kind||cnk(x.desc)==cnk(d.desc)))))}
function cSave(){const d=V.ce;if(!d)return;const amt=Math.round(parseFloat(String(d.amt).replace(/,/g,''))*100)/100;if(!(amt>0))return alert('اكتب المبلغ');if(!/^\d{4}-\d{2}-\d{2}$/.test(d.dt||''))return alert('اختار التاريخ');if(!String(d.desc||'').trim()||!String(d.comp||'').trim())return alert('اكتب البيان واسم الشركة');
 const x=Object.assign({},d,{amt,desc:d.desc.trim(),comp:d.comp.trim(),at:d.at||nowIso()});const seq=d._seq,qref=d._q;['_alt','_qr','_new','_seq','_q'].forEach(k=>delete x[k]);if(!x.qt)delete x.qt;if(qref&&x.qt){delete x.qt}
 const du=cDup(x);if(du&&!confirm(`⚠ فيه فاتورة شبهها متسجلة: ${du.desc} · ${du.comp} · ${f2(du.amt)} · ${du.dt}${du.ref?' · '+du.ref:''}.\nتسجلها برضه؟`))return;
 if(qref)cQtClose(qref,x);const M=cMo(),i=M.items.findIndex(y=>y.id==x.id);if(i>=0)M.items[i]=x;else M.items.push(x);cSort(M.items);
 CU().mem[cnk(x.comp)]={desc:x.desc,kind:x.kind};sv();snd('ok');
 const nx=(V.cq||[]).shift();if(nx){V.ce=nx;render();scrollTo(0,0);toastT('✓ اتحفظت. الفاتورة اللي بعدها');return}V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q,from:V.from});toastT('✓ اتحفظت الفاتورة');{const a=cAlert();if(a&&a.r+amt>=a.a)setTimeout(()=>toastT('⚠ رصيد العهدة المتبقي بقى '+f2(a.r)+' (أقل من '+f2(a.a)+'). اطلب تعزيز العهدة.'),2500)}if(seq&&cSeq()){CSN++;setTimeout(cScan,450)}else CSN=0}
// ---- screens
function custHtml(){const C=CU(),M=cMo(),k=C.cur,tot=cTot(M),rem=cRem(M),L=M.items,ks=Object.keys(C.m).sort().reverse();
 let cn=0;const rows=L.map((x,i)=>{const o=cOut(x,k),np=(x.note||'').includes('فاتورة ورقية'),no=x.qt?'':++cn;if(V.cnpf&&(!np||x.qt))return '';return `<tr class="${o?'co-'+o:''}${x.qt==1?' cqt':x.qt==2?' cqd':''}" data-ced="${x.id}"><td class="cnum">${x.qt==1?'⏳':x.qt==2?'✓':no}</td><td class="cdt">${esc(x.dt.slice(8,10)+'-'+x.dt.slice(5,7))}${x.tm?`<small>${esc(x.tm)}</small>`:''}</td><td>${esc(x.desc)}<small class="ck" style="background:#${CKC[x.kind]||'EFEFEF'}">${esc(x.kind)}</small>${np?'<small class="cnp">⚠ لا توجد فاتورة ورقية</small>':''}${x.qt==1?'<small class="cqtg">⏳ عرض سعر · مستني الفاتورة</small>':x.qt==2?`<small class="cqtg d">✓ اتسدد بفاتورة ${esc(ddmm((x.qi||{}).dt))}</small>`:''}</td><td>${esc(x.comp)}${x.car?`<small>${esc(x.car)}</small>`:''}</td><td class="cam"><b>${f2(x.amt)}</b>${x.imgs&&x.imgs.length?'<small>📎</small>':''}</td></tr>`}).join('');
 return `${cqfHtml()}<div class="wcard cust"><div class="cuh"><b>كشف مصروفات العهدة — ${esc(C.cfg.region)}</b><small>شهر ${cMoLab(k)} · ${esc(C.cfg.sup)}</small></div>
 <div class="ckpi">${cKpiOpen(M)}<div><small>إجمالي المصروف</small><b class="c-exp">${f2(tot)}</b></div><div><small>المتبقي في العهدة</small><b class="c-rem">${f2(rem)}</b></div><div><small>عدد الفواتير</small><b>${L.filter(x=>!x.qt).length}</b></div><button class="cnpk${V.cnpf?' on':''}" data-cnpf="1"><small>بدون فاتورة ورقية</small><b>${cNpN(M)}</b><em>${V.cnpf?'✓ معروضين بس · اعرض الكل':'اضغط لعرضهم بس'}</em></button></div>${cDepHtml(M)}${cAlHtml()}${cQtHtml()}
 ${cDlStamp(M)}<div class="cbtn"${cLk(M)?' hidden':''}><button class="pr" data-cscan="1">${ic('cam')}امسح QR بالكاميرا</button><button class="pr" data-pick="cimgs">${ic('img')}فاتورة من صورة أو PDF</button><button data-cman="1">${ic('edit')}إضافة يدوي</button></div>
 <input type="file" id="cimgs" accept="image/*,application/pdf,.pdf" multiple hidden><input type="file" id="cjson" accept=".json,application/json" hidden></div>
 <div class="wcard"><div class="cmo"><label>الشهر<select id="cmosel">${ks.map(x=>`<option value="${x}"${x==k?' selected':''}>${cMoLab(x)}</option>`).join('')}</select></label><button data-cnew="1">${ic('add')}بدء شهر جديد</button></div>
 ${V.cnew?cNewHtml():''}
 ${L.length?`<div class="sc"><table class="ctab"><tr><th>م</th><th>التاريخ</th><th class="cdsc">البيان</th><th>الشركة</th><th>المبلغ</th></tr>${rows}<tr class="tot"><td colspan="4">الإجمالي</td><td class="c-exp">${f2(tot)}</td></tr><tr class="tot"><td colspan="4">المتبقي في رصيد العهدة</td><td class="c-rem">${f2(rem)}</td></tr></table></div><p class="sub">اضغط على أي فاتورة علشان تعدّلها أو تمسحها. ■ أحمر = تاريخها قبل الشهر · ■ أزرق = بعد الشهر · ⏳ = عرض سعر مستني الفاتورة (مش في كشف المحاسب).</p>`:'<p class="em">لسه مفيش فواتير في الشهر ده.</p>'}
 <div class="cshare c2b"><button class="pr" data-cmenu="share">${ic('share')}مشاركة…</button><button data-cmenu="save">${ic('download')}حفظ…</button></div>${cDlBtn(M)}</div>
 <details class="pinfo" data-id="__cset"${V.op.__cset?' open':''}><summary>${ic('gear')} إعدادات العهدة والاستيراد</summary><div class="fm">
 <label>المنطقة في عنوان الكشف<input data-cc="region" value="${esc(C.cfg.region)}"></label><label>اسم المشرف<input data-cc="sup" value="${esc(C.cfg.sup)}"></label><label>لوحة العربية (للوقود والسيارة)<input data-cc="car" value="${esc(C.cfg.car)}"></label>
 <div class="c2"><label>رصيد العهدة الكامل<input type="number" inputmode="decimal" data-cc="base" value="${C.cfg.base}"></label><label>أقل متبقي ينقل للشهر الجديد<input type="number" inputmode="decimal" data-cc="min" value="${C.cfg.min}"></label></div><label>نبّهني لو المتبقي أقل من (0 = من غير تنبيه)<input type="number" inputmode="decimal" data-cc="al" value="${cAl()}"></label>
 <label>رصيد بداية شهر ${cMoLab(k)}<input type="number" inputmode="decimal" data-cmopen="1" value="${M.open}"></label>
 <button data-pick="cjson">${ic('upload')}استيراد فواتير من ملف (اللي Claude بيجهّزه)</button></div></details>`}
function cNewHtml(){const C=CU(),M=cMo(),r=cRem(M),sg=r>C.cfg.min?r:C.cfg.base,nk2=cNext(C.cur);return `<div class="cnew"><b>بدء شهر ${cMoLab(nk2)}</b><p>المتبقي من شهر ${cMoLab(C.cur)}: <b class="c-rem">${f2(r)}</b>. ${r>C.cfg.min?`أكتر من ${f2(C.cfg.min)}، فالاقتراح يبدأ بالمتبقي.`:`أقل من ${f2(C.cfg.min)}، فالاقتراح يبدأ بالعهدة كاملة.`}</p>
 <div class="cbtn"><button class="${sg==r?'pr':''}" data-cnewgo="${r}">ابدأ بالمتبقي ${f2(r)}</button><button class="${sg==r?'':'pr'}" data-cnewgo="${C.cfg.base}">ابدأ بـ ${f2(C.cfg.base)}</button></div><label>مبلغ تاني<input type="number" inputmode="decimal" id="cnewv"></label><div class="cbtn"><button data-cnewgo="v">ابدأ بالمبلغ ده</button><button data-cnew="0">إلغاء</button></div></div>`}
function cedHtml(){const d=V.ce;if(!d)return '';const C=CU(),comps=[...new Set(Object.values(C.m).flatMap(m=>m.items.map(x=>x.comp)))].sort(),descs=[...new Set(Object.values(C.m).flatMap(m=>m.items.map(x=>x.desc)))].sort(),ml=mealOf(d.tm),np=(d.note||'').includes(NOPAPER),q=V.cq||[];
 return `<div class="wcard ced">${q.length?`<p class="sub">فاتورة جديدة · باقي ${q.length} صورة بعدها</p>`:''}
 ${d.src=='qr'?'<div class="ph"><small>✓ اتقرت البيانات من كود QR الفاتورة. راجعها قبل الحفظ.</small></div>':d.src=='img'?'<div class="alr"><small>⚠ ما قدرتش أقرا كود QR من الصورة. كمّل البيانات يدوي من الصورة.</small></div>':d.src=='pdf'?'<div class="alr"><small>⚠ ما قدرتش أقرا كود QR من الـ PDF. كمّل البيانات يدوي (اضغط على الملف علشان تفتحه).</small></div>':''}${cqEdHtml(d)}
 ${d.imgs&&d.imgs.length?`<div class="cimgs">${d.imgs.map(k=>isPdfK(k)?`<span><button class="cimgb cpdfb" data-cpdfo="${k}"><b>📄 PDF</b><small>${esc(((d.fn||{})[k]||{}).n||'فاتورة.pdf')}</small><small>${fsz(((d.fn||{})[k]||{}).sz||0)}</small></button><button class="np cimgx" data-cimgx="${k}">✕</button></span>`:`<span><button class="cimgb" data-cimgz="${k}"><img data-cimg="${k}" alt=""></button><button class="np cimgx" data-cimgx="${k}">✕</button></span>`).join('')}</div>`:''}
 <div class="fm"><div class="c2"><label>التاريخ<input type="date" data-cf="dt" value="${esc(d.dt)}"></label><label>الوقت<input type="time" data-cf="tm" value="${esc(d.tm)}"></label></div>
 ${d._alt?`<div class="ph"><small>الوقت في الكود ممكن يكون بالتوقيت العالمي. لو الوقت المطبوع على الفاتورة <b>${esc(d._alt.tm)}</b> اضغط هنا:</small><button data-calt="1">استخدم ${esc(d._alt.tm)}</button></div>`:''}
 <div class="c2"><label>النوع<select data-cf="kind">${CK.map(k=>`<option${k==d.kind?' selected':''}>${k}</option>`).join('')}</select></label><label>المبلغ شامل الضريبة<input type="number" inputmode="decimal" step="0.01" data-cf="amt" value="${esc(d.amt)}"></label></div>
 <label>البيان${d.kind=='وجبات'&&ml?` <small>(الوقت ده = ${ml})</small>`:''}<input list="cdl" data-cf="desc" value="${esc(d.desc)}"><small class="cdsp"${String(d.desc||'').length>30?'':' hidden'}>${esc(d.desc)}</small></label><datalist id="cdl">${descs.map(x=>`<option value="${esc(x)}">`).join('')}</datalist>
 <label>اسم الشركة<input list="ccl" data-cf="comp" value="${esc(d.comp)}"></label><datalist id="ccl">${comps.map(x=>`<option value="${esc(x)}">`).join('')}</datalist>
 <div class="c2"><label>السيارة<input data-cf="car" value="${esc(d.car)}"></label><label>رقم الصيدلية<input inputmode="numeric" data-cf="ph" value="${esc(d.ph)}"></label></div>
 <label>${d.qt?'رقم عرض السعر':'رقم الفاتورة'}<input data-cf="ref" value="${esc(d.ref)}"></label>
 <label class="chk cnpl"><input type="checkbox" id="cnp"${np?' checked':''}> ⚠ لا توجد فاتورة ورقية (الرجاء الطباعة)</label>
 <label>ملاحظات<input data-cf="note" value="${esc((d.note||'').replace(NOPAPER,'').replace(/^\s*[·⚠]\s*/,'').trim())}"></label>
 <div class="cbtn"><button class="pr" data-cpic="1">${ic('cam')}إرفاق صورة أو PDF</button></div><input type="file" id="cimg1" accept="image/*,application/pdf,.pdf" multiple hidden></div>
 <div class="tt"><button class="pr big" data-csave="1">${ic('check')}${d.qt==1?'حفظ عرض السعر':'حفظ الفاتورة'}</button>${q.length?'<button data-cskip="1">تخطي</button>':''}<button data-ccancel="1">إلغاء</button>${cMo().items.some(x=>x.id==d.id)?`<button data-cdel="1" style="color:var(--rd)">${ic('trash')}مسح</button>`:''}</div></div>`}
// ---- camera QR scan (live): Google ML Kit inside the app, browser reader / jsQR otherwise
let CSC=null,CSN=0,CLR='';// CLR = last code read in this continuous session (so the same invoice is not read twice)
const MLK=()=>CAPN()&&CP('BarcodeScanner');
const cSeq=()=>CU().cfg.seq!==0;
async function cScan(){if(CSC)return;if(MLK()){try{if(await cScanN())return}catch(e){console.warn('mlkit',e);toastT('⚠ قارئ Google مش شغال على الجهاز ده، هيشتغل القارئ العادي')}}return cScanW()}
function cScanUi(nat){const o=document.createElement('div');o.className='ovl cscan'+(nat?' nat':'');
 o.innerHTML=`<div class="cvw">${nat?'':'<video playsinline muted></video>'}<div class="cfr"></div></div><p class="cmsg">وجّه الكاميرا على كود QR الفاتورة جوه المربع</p>${CSN?`<p class="ccnt">✓ اتحفظ ${CSN} فاتورة في الجلسة دي</p>`:''}<div class="czm" hidden><span>🔍</span><input type="range" class="czr" min="1" max="1" step="0.1" value="1"></div><div class="cbtn"><div class="c2b"><button data-ctorch="1" hidden>🔦 فلاش</button><label class="chk"><input type="checkbox" id="cseq"${cSeq()?' checked':''}> مسح متتالي</label></div><button class="pr" data-cshot="1">📷 صوّر من غير QR</button><button data-cscanx="1">✕ إغلاق</button></div>`;
 document.body.appendChild(o);o.querySelector('.czr').addEventListener('input',e=>{if(CSC&&CSC.zoom)CSC.zoom(e.target.value)});return o}
let CMSGT=0;function cScanMsg(o,m){const p=o.querySelector('.cmsg');if(!p)return;p.textContent=m;p.classList.add('w');clearTimeout(CMSGT);CMSGT=setTimeout(()=>{p.textContent='وجّه الكاميرا على كود QR الفاتورة جوه المربع';p.classList.remove('w')},2200)}
function cShotInput(){const i=document.createElement('input');i.type='file';i.accept='image/*';i.setAttribute('capture','environment');i.onchange=()=>{if(i.files&&i.files.length)cFromImages([...i.files])};i.click()}
async function cAfterScan(z,b){const d=cDraft({comp:z.comp,amt:z.amt,dt:z.dt,tm:z.tm,_alt:z.alt,src:'qr'});if(cSeq())d._seq=1;const k=b?await cImgPut(d.id,b):null;if(k)d.imgs=[k];snd('ok');if(navigator.vibrate)try{navigator.vibrate(60)}catch(e){}V.cq=[];cOpen(d)}
async function cScanN(){const B=MLK();try{const s=await B.isSupported();if(s&&s.supported===false)return false}catch(e){}
 let p;try{p=await B.requestPermissions()}catch(e){p=null}if(p&&p.camera&&!['granted','limited'].includes(p.camera)){alert('مفيش إذن للكاميرا. اسمح للتطبيق باستخدام الكاميرا من إعدادات الموبايل، أو استخدم "فاتورة من صورة".');return true}
 const o=cScanUi(1);document.documentElement.classList.add('bscan');let busy=0;
 const stop=async()=>{if(!CSC)return;CSC=null;document.documentElement.classList.remove('bscan');o.remove();try{await B.removeAllListeners()}catch(e){}try{await B.stopScan()}catch(e){}};
 const hit=async raw=>{if(busy||!CSC)return;if(raw===CLR){cScanMsg(o,'✓ الفاتورة دي اتسجلت. وجّه على الفاتورة اللي بعدها');return}const z=zatca(raw);if(!z){cScanMsg(o,'⚠ الكود ده مش كود فاتورة ضريبية');return}busy=1;CLR=raw;await stop();cAfterScan(z,null)};
 const on=ev=>{const bs=ev?(ev.barcodes||(ev.barcode?[ev.barcode]:[])):[];for(const b of bs){const r=b&&(b.rawValue||b.displayValue);if(r){hit(r);break}}};
 CSC={stop,nat:1,shot:async()=>{await stop();cShotInput()},torch:async()=>{try{await B.toggleTorch()}catch(e){}},zoom:v=>{B.setZoomRatio({zoomRatio:+v}).catch(()=>{})}};
 try{await B.addListener('barcodesScanned',on)}catch(e){}try{await B.addListener('barcodeScanned',on)}catch(e){}
 try{await B.startScan({formats:['QR_CODE'],lensFacing:'BACK'})}catch(e){await stop();throw e}
 try{const t=await B.isTorchAvailable();if(t&&t.available)o.querySelector('[data-ctorch]').hidden=false}catch(e){}
 try{const a=await B.getMinZoomRatio(),c=await B.getMaxZoomRatio();if(c&&a&&c.zoomRatio>a.zoomRatio){const r=o.querySelector('.czr');r.min=a.zoomRatio;r.max=Math.min(c.zoomRatio,8);r.value=a.zoomRatio;o.querySelector('.czm').hidden=false}}catch(e){}
 return true}
async function cScanW(){if(!window.jsQR&&!('BarcodeDetector' in window))return alert('قارئ QR مش موجود في النسخة دي');if(!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia))return alert('الكاميرا مش متاحة هنا. استخدم "فاتورة من صورة".');
 let st;try{st=await navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:'environment'},width:{ideal:1920},height:{ideal:1080}},audio:false})}catch(e){return alert('مفيش إذن للكاميرا. اسمح للتطبيق باستخدام الكاميرا من إعدادات الموبايل، أو استخدم "فاتورة من صورة".')}
 const o=cScanUi(0),v=o.querySelector('video');v.srcObject=st;await v.play().catch(()=>{});const tr=st.getVideoTracks()[0];let cap={},tor=false;try{cap=tr.getCapabilities?tr.getCapabilities():{}}catch(e){}
 if(cap.focusMode&&cap.focusMode.includes('continuous'))tr.applyConstraints({advanced:[{focusMode:'continuous'}]}).catch(()=>{});
 if(cap.torch)o.querySelector('[data-ctorch]').hidden=false;
 if(cap.zoom&&cap.zoom.max>cap.zoom.min){const r=o.querySelector('.czr');r.min=cap.zoom.min;r.max=Math.min(cap.zoom.max,8);r.step=cap.zoom.step||0.1;r.value=(tr.getSettings&&tr.getSettings().zoom)||cap.zoom.min;o.querySelector('.czm').hidden=false}
 let BD=null;try{if('BarcodeDetector' in window){const f=await BarcodeDetector.getSupportedFormats();if(f.includes('qr_code'))BD=new BarcodeDetector({formats:['qr_code']})}}catch(e){BD=null}
 const cv=document.createElement('canvas'),x=cv.getContext('2d',{willReadFrequently:true});
 const stop=()=>{if(!CSC)return;st.getTracks().forEach(t=>t.stop());o.remove();CSC=null};
 const frame=()=>new Promise(ok=>{cv.width=v.videoWidth;cv.height=v.videoHeight;x.drawImage(v,0,0);cv.toBlob(b=>ok(b),'image/jpeg',0.85)});
 const done=async z=>{const b=await frame();stop();if(z)return cAfterScan(z,b);const d=cDraft({src:'img'});const k=b?await cImgPut(d.id,b):null;if(k)d.imgs=[k];snd('tick');V.cq=[];cOpen(d)};
 CSC={stop,shot:()=>done(null),torch:()=>{tor=!tor;tr.applyConstraints({advanced:[{torch:tor}]}).catch(()=>{})},zoom:z=>{tr.applyConstraints({advanced:[{zoom:+z}]}).catch(()=>{})}};
 let n=0,bad=0;const got=r=>{if(!r)return false;if(r===CLR){if(Date.now()-bad>2500){bad=Date.now();cScanMsg(o,'✓ الفاتورة دي اتسجلت. وجّه على الفاتورة اللي بعدها')}return false}const z=zatca(r);if(z){CLR=r;done(z);return true}if(Date.now()-bad>2500){bad=Date.now();cScanMsg(o,'⚠ الكود ده مش كود فاتورة ضريبية')}return false};
 const loop=async()=>{if(!CSC)return;const vw=v.videoWidth,vh=v.videoHeight;if(vw){n++;
   if(BD){try{const R=await BD.detect(v);for(const r of R)if(got(r.rawValue))return}catch(e){}}
   if(window.jsQR&&(!BD||n%2==0)){const m=n%3;let W,H;if(m<2){const s=Math.round(Math.min(vw,vh)*0.72),sx=(vw-s)>>1,sy=(vh-s)>>1,T=Math.min(s,760);W=H=T;cv.width=T;cv.height=T;x.drawImage(v,sx,sy,s,s,0,0,T,T)}else{W=Math.min(960,vw);H=Math.round(vh*W/vw);cv.width=W;cv.height=H;x.drawImage(v,0,0,W,H)}
    let d=x.getImageData(0,0,W,H).data;if(m==1)d=qrGray(d,W,H,1);const r=jsQR(d,W,H,{inversionAttempts:m==1?'dontInvert':'attemptBoth'});if(r&&r.data&&got(r.data))return}}
  if(CSC)setTimeout(loop,BD?90:60)};loop()}
// read a QR from a photo: ML Kit inside the app, then the browser reader, then jsQR
async function qrFromBlobN(blob){const B=MLK(),FS=CP('Filesystem');if(!B||!FS||!B.readBarcodesFromImage)return null;try{const w=await FS.writeFile({path:'qr-'+Date.now()+'.jpg',data:await b64of(blob),directory:'CACHE'});let R;try{R=await B.readBarcodesFromImage({path:w.uri,formats:['QR_CODE']})}finally{FS.deleteFile({path:w.uri}).catch(()=>{})}for(const b of (R&&R.barcodes)||[]){const z=zatca(b.rawValue||'');if(z)return z}}catch(e){console.warn('mlkit img',e)}return null}
async function qrFromBlobB(blob){try{if(!('BarcodeDetector' in window))return null;const f=await BarcodeDetector.getSupportedFormats();if(!f.includes('qr_code'))return null;const bm=await createImageBitmap(blob),R=await new BarcodeDetector({formats:['qr_code']}).detect(bm);for(const r of R){const z=zatca(r.rawValue);if(z)return z}}catch(e){}return null}
// ---- Excel (same layout every time) ----
function custXlsx(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),N=L.length,first=8,last=first+Math.max(N,1)-1,tot=last+1,tt=cTot(M),rm=cRem(M);
 const F=[],FI={},font=(sz,b,c)=>{const key=sz+'|'+(b?1:0)+'|'+(c||'000000');if(FI[key]==null){FI[key]=F.length;F.push(`<font>${b?'<b/>':''}<sz val="${sz}"/><color rgb="FF${c||'000000'}"/><name val="Arial"/><family val="2"/></font>`)}return FI[key]};
 const P=['<fill><patternFill patternType="none"/></fill>','<fill><patternFill patternType="gray125"/></fill>'],PI={},fill=c=>{if(!c)return 0;if(PI[c]==null){PI[c]=P.length;P.push(`<fill><patternFill patternType="solid"><fgColor rgb="FF${c}"/><bgColor indexed="64"/></patternFill></fill>`)}return PI[c]};
 const X=['<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'],XI={},st=(o)=>{const f=font(o.sz||10,o.b,o.c),p=fill(o.bg),n=o.n||0,bd=o.nb?0:1,key=[f,p,n,bd].join('|');if(XI[key]==null){XI[key]=X.length;X.push(`<xf numFmtId="${n}" fontId="${f}" fillId="${p}" borderId="${bd}" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"${n?' applyNumberFormat="1"':''}><alignment horizontal="center" vertical="center" wrapText="1" readingOrder="2"/></xf>`)}return XI[key]};
 font(10,0,'000000');
 const NAVY='0B1B33',GOLD='F2B705',BLUE='1F3864',RED='8B0000',GREEN='1E7B45',ZEB='F5F7FA',CARD='EEF2F7',OPENBG='FFF6D6',MUTE='5B6B80';
 const serial=d=>{const[y,m,dd]=d.split('-').map(Number);return Math.round((Date.UTC(y,m-1,dd)-Date.UTC(1899,11,30))/864e5)};
 const R={},cell=(r,c,v,s,f)=>{(R[r]=R[r]||[]).push({c,v,s,f})},merges=[];
 const ref=(c,r)=>colL(c)+r;
 // title
 cell(1,0,`كشف مصروفات العهدة — ${C.cfg.region} — شهر ${cMoLab(k)}`,st({sz:14,b:1,c:'FFFF00',bg:NAVY,nb:1}));merges.push('A1:K1');
 cell(2,0,`المشرف: ${C.cfg.sup}  ·  966 Motors — صيدليات الدواء  ·  تاريخ الكشف: ${TD().split('-').reverse().join('-')}`,st({sz:10,c:'50164A',nb:1}));merges.push('A2:K2');
 const cards=[[0,2,cDep(M)?'رصيد العهدة (بداية + مستلم)':'رصيد بداية الشهر','H7',cAv(M),4,BLUE],[3,3,'إجمالي المصروف',`G${tot}`,tt,4,RED],[4,6,'المتبقي في العهدة',`H${tot}`,rm,4,GREEN],[7,8,'عدد الفواتير',`COUNT(G${first}:G${last})`,N,1,NAVY],[9,10,'نسبة المصروف',`IF(H7=0,0,G${tot}/H7)`,cAv(M)?tt/cAv(M):0,9,NAVY]];
 cards.forEach(([a,b,lab,f,v,n,c])=>{for(let i=a;i<=b;i++){cell(3,i,i==a?lab:'',st({sz:9,b:1,c:MUTE,bg:CARD}));cell(4,i,i==a?v:'',st({sz:14,b:1,c,bg:CARD,n}),i==a?f:null)}if(b>a){merges.push(`${ref(a,3)}:${ref(b,3)}`,`${ref(a,4)}:${ref(b,4)}`)}});
 cell(5,0,'■ أحمر = فاتورة تاريخها قبل الشهر     ■ أزرق = فاتورة تاريخها بعد الشهر     ⚠ = لا توجد فاتورة ورقية (الرجاء الطباعة)',st({sz:9,b:1,c:MUTE,nb:1}));merges.push('A5:K5');
 const H=['م','التاريخ','الوقت','البيان','النوع','اسم الشركة','المصروف (ر.س)','الرصيد بعد المصروف','السيارة','رقم الصيدلية','رقم الفاتورة / ملاحظات'];
 H.forEach((h,i)=>cell(6,i,h,st({b:1,c:'FFFFFF',bg:NAVY})));
 for(let i=0;i<11;i++)cell(7,i,i==0?cDepLab(M):i==7?cAv(M):'',st({b:1,c:i==7?BLUE:NAVY,bg:OPENBG,sz:i==7?11:10,n:i==7?4:0}));merges.push('A7:F7');
 let bal=cAv(M);
 const HT={1:24.5,2:20,3:17,4:22,5:12.5,6:23.5,7:20.5};
 (N?L:[null]).forEach((x,j)=>{const r=first+j,z=j%2?ZEB:null;if(!x){for(let i=0;i<11;i++)cell(r,i,'',st({bg:z}));return}bal=Math.round((bal-(+x.amt||0))*100)/100;
  const np=(x.note||'').includes(NOPAPER),rest=[(x.note||'').replace(NOPAPER,'').replace(/^[\s·⚠]+|[\s·]+$/g,''),x.ref].filter(Boolean).join(' · '),nr=np?{rich:[['⚠ '+NOPAPER,10,1,'C00000']].concat(rest?[['\n'+rest,8,0,MUTE]]:[])}:rest;if(np&&rest)HT[r]=32;{const ln=Math.max(Math.ceil(String(x.desc||'').length/44),Math.ceil(String(x.comp||'').length/30));if(ln>1)HT[r]=Math.max(HT[r]||21,13*ln+8)}
  const V0=[j+1,serial(x.dt),x.tm||'',x.desc,x.kind,x.comp,+x.amt,bal,x.car||'',x.ph||'',nr];
  V0.forEach((v,i)=>cell(r,i,v,i==0?st({b:1,sz:11,c:NAVY,bg:OPENBG}):i==10&&np?st({bg:'FDE2E2'}):st({bg:i==4?(CKC[x.kind]||'EFEFEF'):z,b:i==6||i==7||i==4,sz:i==4?9:i==8?8:10,c:i==7?MUTE:'000000',n:i==1?164:(i==6||i==7)?4:0}),i==7?`H${r-1}-G${r}`:null))});
 for(let i=0;i<11;i++)cell(tot,i,i==0?'الإجمالي':i==6?tt:i==7?rm:i==8?'← المتبقي في رصيد العهدة':'',st({b:1,sz:12,c:i==6?RED:i==7?GREEN:NAVY,bg:GOLD,n:i==6||i==7?4:0}),i==6?`SUM(G${first}:G${last})`:i==7?`H7-G${tot}`:null);
 merges.push(`A${tot}:F${tot}`,`I${tot}:K${tot}`);
 cell(tot+1,0,'عدد الفواتير بدون فاتورة ورقية: '+L.filter(cNp).length+(M.dl?'     ·     تاريخ التسليم: '+cDd(M.dl.at):'')+(cDepTxt(M)?'     ·     '+cDepTxt(M):''),st({b:1,sz:11,c:'C00000',nb:1}));merges.push(`A${tot+1}:K${tot+1}`);HT[tot+1]=20;
 const sg=tot+3;[['A','D','توقيع المشرف: ....................'],['E','H','مراجعة المحاسب: ....................'],['I','K','اعتماد المدير: ....................']].forEach(([a,b,t])=>{const ci=a.charCodeAt(0)-65;cell(sg,ci,t,st({c:MUTE,nb:1}));merges.push(`${a}${sg}:${b}${sg}`)});
 const W=[5,11,7,45,10,27,12,14,17,10,30];HT[tot]=28;HT[sg]=14;
 const cv=x=>{if(x.f)return `<f>${xe(x.f)}</f><v>${x.v}</v>`;return ''};
 const rowsXml=Object.keys(R).map(Number).sort((a,b)=>a-b).map(r=>`<row r="${r}"${HT[r]||r>=first&&r<=last?` ht="${HT[r]||21}" customHeight="1"`:''}>${R[r].sort((a,b)=>a.c-b.c).map(x=>{const rf=ref(x.c,r);if(x.v&&x.v.rich)return `<c r="${rf}" s="${x.s}" t="inlineStr"><is>${x.v.rich.map(([t,sz,b,c])=>`<r><rPr>${b?'<b/>':''}<sz val="${sz}"/><color rgb="FF${c}"/><rFont val="Arial"/></rPr><t xml:space="preserve">${xe(t)}</t></r>`).join('')}</is></c>`;if(x.f)return `<c r="${rf}" s="${x.s}"><f>${xe(x.f)}</f><v>${x.v}</v></c>`;return typeof x.v=='number'?`<c r="${rf}" s="${x.s}"><v>${x.v}</v></c>`:x.v===''?`<c r="${rf}" s="${x.s}"/>`:`<c r="${rf}" s="${x.s}" t="inlineStr"><is><t xml:space="preserve">${xe(x.v)}</t></is></c>`}).join('')}</row>`).join('');
 const cf=N?['B','D','F'].map((c,i)=>`<conditionalFormatting sqref="${c}${first}:${c}${last}"><cfRule type="expression" dxfId="0" priority="${i*2+1}"><formula>$B${first}&lt;DATE(${k.slice(0,4)},${+k.slice(5,7)},1)</formula></cfRule><cfRule type="expression" dxfId="1" priority="${i*2+2}"><formula>$B${first}&gt;=DATE(${cNext(k).slice(0,4)},${+cNext(k).slice(5,7)},1)</formula></cfRule></conditionalFormatting>`).join(''):'';
 const sheet1=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheetPr><pageSetUpPr fitToPage="1"/></sheetPr><sheetViews><sheetView rightToLeft="1" workbookViewId="0"><pane ySplit="6" topLeftCell="A7" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>${W.map((w,i)=>`<col min="${i+1}" max="${i+1}" width="${w}" customWidth="1"/>`).join('')}</cols><sheetData>${rowsXml}</sheetData><mergeCells count="${merges.length}">${merges.map(m=>`<mergeCell ref="${m}"/>`).join('')}</mergeCells>${cf}<printOptions horizontalCentered="1"/><pageMargins left="0.3" right="0.3" top="0.4" bottom="0.4" header="0.2" footer="0.2"/><pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="0"/><headerFooter><oddFooter>&amp;L${xe('عهدة شهر '+cMoLab(k))}&amp;Cصفحة &amp;P من &amp;N</oddFooter></headerFooter></worksheet>`;
 // summary sheet
 const used=CK.filter(c=>L.some(x=>x.kind==c)),SR=[];let s2='';
 const s2c=(r,c,v,s,f)=>`<c r="${ref(c,r)}" s="${s}"${f?'':typeof v=='number'?'':' t="inlineStr"'}>${f?`<f>${xe(f)}</f><v>${v}</v>`:typeof v=='number'?`<v>${v}</v>`:`<is><t>${xe(v)}</t></is>`}</c>`;
 s2+=`<row r="1" ht="28" customHeight="1">${[0,1,2,3].map(i=>s2c(1,i,i?'':`ملخص المصروف حسب النوع — شهر ${cMoLab(k)}`,st({sz:13,b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row>`;
 s2+=`<row r="3">${['النوع','عدد الفواتير','الإجمالي (ر.س)','النسبة'].map((h,i)=>s2c(3,i,h,st({b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row>`;
 const rg=`'العهدة'!E${first}:E${last}`,vg=`'العهدة'!G${first}:G${last}`;
 used.forEach((c,j)=>{const r=4+j,n=L.filter(x=>x.kind==c).length,a=Math.round(L.filter(x=>x.kind==c).reduce((s,x)=>s+(+x.amt||0),0)*100)/100;
  s2+=`<row r="${r}" ht="20" customHeight="1">${s2c(r,0,c,st({b:1,bg:CKC[c]}))}${s2c(r,1,n,st({}),`COUNTIF(${rg},A${r})`)}${s2c(r,2,a,st({n:4,c:RED}),`SUMIF(${rg},A${r},${vg})`)}${s2c(r,3,tt?a/tt:0,st({n:9}),`IF('العهدة'!G${tot}=0,0,C${r}/'العهدة'!G${tot})`)}</row>`});
 const e=4+used.length;s2+=`<row r="${e}" ht="22" customHeight="1">${s2c(e,0,'الإجمالي',st({b:1,c:NAVY,bg:GOLD}))}${s2c(e,1,N,st({b:1,c:NAVY,bg:GOLD}),`SUM(B4:B${e-1})`)}${s2c(e,2,tt,st({b:1,c:RED,bg:GOLD,n:4}),`SUM(C4:C${e-1})`)}${s2c(e,3,N?1:0,st({b:1,c:NAVY,bg:GOLD,n:9}),`SUM(D4:D${e-1})`)}</row>`;
 const PH={};let shr2=0;L.forEach(x=>{const ns=String(x.ph||'').split(/[^0-9A-Za-z\u0660-\u0669]+/).filter(Boolean),a=+x.amt||0;if(ns.length>1)shr2=1;(ns.length?ns:['—']).forEach(n=>{const o=PH[n]=PH[n]||{n:0,a:0};o.n++;o.a+=a/(ns.length||1)})});
 const pk=Object.keys(PH).sort((a,b)=>a=='—'?1:b=='—'?-1:a.localeCompare(b,undefined,{numeric:true})),p0=e+2;
 if(pk.length){s2+=`<row r="${p0}" ht="24" customHeight="1">${[0,1,2,3].map(i=>s2c(p0,i,i?'':'المصروف حسب الصيدلية',st({sz:12,b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row><row r="${p0+1}">${['رقم الصيدلية','عدد الفواتير','الإجمالي (ر.س)','النسبة'].map((h,i)=>s2c(p0+1,i,h,st({b:1,c:'FFFFFF',bg:NAVY}))).join('')}</row>`;
  pk.forEach((n,j)=>{const r=p0+2+j,a=Math.round(PH[n].a*100)/100;s2+=`<row r="${r}" ht="20" customHeight="1">${s2c(r,0,n=='—'?'بدون رقم صيدلية':n,st({b:1,bg:OPENBG}))}${s2c(r,1,PH[n].n,st({}))}${s2c(r,2,a,st({n:4,c:RED}))}${s2c(r,3,tt?a/tt:0,st({n:9}))}</row>`});
  if(shr2){const r=p0+2+pk.length;s2+=`<row r="${r}">${s2c(r,0,'الفاتورة المشتركة بين أكتر من صيدلية متقسمة عليهم بالتساوي',st({sz:9,c:MUTE,nb:1}))}</row>`}}
 const sheet2=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView rightToLeft="1" workbookViewId="0"/></sheetViews><cols>${[16,14,16,10].map((w,i)=>`<col min="${i+1}" max="${i+1}" width="${w}" customWidth="1"/>`).join('')}</cols><sheetData>${s2}</sheetData><mergeCells count="${pk.length?2+(shr2?1:0):1}"><mergeCell ref="A1:D1"/>${pk.length?`<mergeCell ref="A${p0}:D${p0}"/>`:''}${pk.length&&shr2?`<mergeCell ref="A${p0+2+pk.length}:D${p0+2+pk.length}"/>`:''}</mergeCells></worksheet>`;
 const dx=(c,bg)=>`<dxf><font><b/><color rgb="FF${c}"/></font><fill><patternFill patternType="solid"><fgColor rgb="FF${bg}"/><bgColor rgb="FF${bg}"/></patternFill></fill></dxf>`;
 const styles=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><numFmts count="1"><numFmt numFmtId="164" formatCode="dd\\-mm\\-yyyy"/></numFmts><fonts count="${F.length}">${F.join('')}</fonts><fills count="${P.length}">${P.join('')}</fills><borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border>${['left','right','top','bottom'].map(s=>`<${s} style="thin"><color rgb="FFD5DCE6"/></${s}>`).join('')}<diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="${X.length}">${X.join('')}</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles><dxfs count="3">${dx('B42318','FAD4D4')}${dx('1D4ED8','D6E6FB')}${dx('C00000','FDE2E2')}</dxfs></styleSheet>`;
 const NS='http://schemas.openxmlformats.org';
 return zipBlob([{n:'[Content_Types].xml',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="${NS}/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>`},
  {n:'_rels/.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`},
  {n:'xl/workbook.xml',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="${NS}/spreadsheetml/2006/main" xmlns:r="${NS}/officeDocument/2006/relationships"><bookViews><workbookView/></bookViews><sheets><sheet name="العهدة" sheetId="1" r:id="rId1"/><sheet name="الملخص" sheetId="2" r:id="rId2"/></sheets><definedNames><definedName name="_xlnm.Print_Titles" localSheetId="0">'العهدة'!$6:$6</definedName></definedNames><calcPr calcId="191029" fullCalcOnLoad="1"/></workbook>`},
  {n:'xl/_rels/workbook.xml.rels',d:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${NS}/package/2006/relationships"><Relationship Id="rId1" Type="${NS}/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="${NS}/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/><Relationship Id="rId3" Type="${NS}/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`},
  {n:'xl/styles.xml',d:styles},{n:'xl/worksheets/sheet1.xml',d:sheet1},{n:'xl/worksheets/sheet2.xml',d:sheet2}],'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
// ---- PDF element (same table, A4)
function custPdfEl(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),tt=cTot(M),rm=cRem(M);let bal=cAv(M);const el=document.createElement('div');
 el.innerHTML=`<div class="cpt cy"><b>كشف مصروفات العهدة — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div><div class="cpsub">المشرف: ${esc(C.cfg.sup)} · 966 Motors — صيدليات الدواء · تاريخ الكشف: ${TD().split('-').reverse().join('-')}</div>
 <div class="ckpi">${cKpiOpen(M)}<div><small>إجمالي المصروف</small><b class="c-exp">${f2(tt)}</b></div><div><small>المتبقي في العهدة</small><b class="c-rem">${f2(rm)}</b></div><div><small>عدد الفواتير</small><b>${L.length}</b></div></div>
 <table class="cpdf"><tr><th>م</th><th>التاريخ</th><th>الوقت</th><th class="cdsc">البيان</th><th>النوع</th><th>اسم الشركة</th><th>المصروف</th><th>الرصيد بعد المصروف</th><th>السيارة</th><th>رقم الصيدلية</th><th>رقم الفاتورة / ملاحظات</th></tr>
 <tr class="copen"><td colspan="7">${esc(cDepLab(M))}</td><td class="c-open">${f2(cAv(M))}</td><td colspan="3"></td></tr>
 ${L.map((x,i)=>{bal-= +x.amt||0;const o=cOut(x,k),np=(x.note||'').includes(NOPAPER),rest=[(x.note||'').replace(NOPAPER,'').replace(/^[\s·⚠]+|[\s·]+$/g,''),x.ref].filter(Boolean).join(' · ');return `<tr class="${o?'co-'+o:''}"><td class="cnum">${i+1}</td><td class="cmk cdn">${x.dt.split('-').reverse().join('-')}</td><td>${esc(x.tm||'')}</td><td class="cmk">${esc(x.desc)}</td><td style="background:#${CKC[x.kind]||'EFEFEF'}"><b>${esc(x.kind)}</b></td><td class="cmk">${esc(x.comp)}</td><td><b>${f2(x.amt)}</b></td><td class="cbal">${f2(bal)}</td><td class="ccar">${esc(x.car||'')}</td><td>${esc(x.ph||'')}</td>${np?`<td class="cnpt"><b>⚠ ${esc(NOPAPER)}</b>${rest?`<small class="cref">${esc(rest)}</small>`:''}</td>`:`<td>${esc(rest)}</td>`}</tr>`}).join('')}
 <tr class="ctot"><td colspan="6">الإجمالي</td><td class="c-exp">${f2(tt)}</td><td class="c-rem">${f2(rm)}</td><td colspan="3">← المتبقي في رصيد العهدة</td></tr></table>
 <div class="cnpline">عدد الفواتير بدون فاتورة ورقية: <b>${L.filter(cNp).length}</b>${M.dl?` · تاريخ التسليم: <b>${cDd(M.dl.at)}</b>`:''}${cDepTxt(M)?' · '+esc(cDepTxt(M)):''}</div>
 <div class="csig"><span>توقيع المشرف: ..............</span><span>مراجعة المحاسب: ..............</span><span>اعتماد المدير: ..............</span></div>`;return el}
const cName=(k,e)=>`عهدة ${CU().cfg.region.replace(/[\\/:*?"<>|]/g,'')} - شهر ${k.slice(5,7)}-${k.slice(0,4)} - ${TD()}.${e}`;
async function cExport(kind,mode){if(!cQtOk())return;const k=CU().cur;if(CU().m[k]){CU().m[k].xat=nowIso();svq()}if(!cMo().items.length&&!confirm('الشهر ده مفيهوش فواتير. تكمل؟'))return;
 if(kind=='x'){let bl;try{bl=custXlsx(k)}catch(e){console.error(e);return alert('تعذّر إنشاء ملف Excel')}const n=cName(k,'xlsx');if(CAPN())return nativeSave(n,bl,bl.type,mode=='share');return mode=='share'?shr(n,bl,bl.type):out(n,bl,bl.type)}
 const n=cName(k,'pdf').replace(/\.pdf$/,''),el=custPdfEl(k),ttl='كشف مصروفات العهدة — شهر '+cMoLab(k);
 if(mode=='share')return sharePdf({src:el,name:n,title:ttl});const t=toast('جاري تجهيز ملف PDF…');try{const b=await buildPdf(el,ttl);t.remove();if(CAPN())return nativeSave(n+'.pdf',b,'application/pdf',false);return out(n+'.pdf',b,'application/pdf')}catch(e){t.remove();console.error(e);alert('تعذّر تجهيز ملف PDF')}}
// invoice photos appendix: one block per photo with the same number (م) as the statement
async function cAppEl(k,sel){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),el=document.createElement('div'),no=[],pdfs=[];let h=`<div class="cpt cy"><b>${sel?'فواتير بدون فاتورة ورقية':'ملحق صور فواتير العهدة'} — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div><div class="cpsub">المشرف: ${esc(C.cfg.sup)} · الرقم على كل صورة = رقم «م» في الكشف</div>`;
 for(const[i,x] of L.entries()){if(sel&&!sel.has(x.id))continue;const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}const pk=ks.filter(isPdfK);pk.forEach((key,j)=>pdfs.push({i:i+1,j:pk.length>1?j+1:0,x,key}));for(const[j,key] of ks.filter(y=>!isPdfK(y)).entries()){const b=await idbGet(key);if(!b)continue;const u=URL.createObjectURL(b),d=await shrink(u,1000);URL.revokeObjectURL(u);if(!d)continue;
  h+=`<div class="cax"><div class="caxh"><b class="caxn">م ${i+1}${ks.length>1?' ('+(j+1)+')':''}</b><span>${x.dt.split('-').reverse().join('-')} · ${esc(x.desc)} · ${esc(x.comp)} · <b>${f2(x.amt)}</b></span></div><img src="${d}" alt=""></div>`}}
 if(no.length)h+=`<div class="cpsub">فواتير من غير صورة: ${no.map(n=>'م '+n).join('، ')}</div>`;if(pdfs.length)h+=`<div class="cpsub">فواتير PDF (مبعوتة كملفات منفصلة): ${[...new Set(pdfs.map(y=>'م '+y.i))].join('، ')}</div>`;el.innerHTML=h;return {el,n:L.filter(x=>(!sel||sel.has(x.id))&&(x.imgs||[]).some(y=>!isPdfK(y))).length,pdfs}}
async function cAppx(mode){if(!cQtOk())return;const k=CU().cur;const t=toast('جاري تجهيز صور الفواتير…');let o;try{o=await cAppEl(k)}finally{t.remove()}if(!o.n&&!o.pdfs.length)return alert('مفيش صور ولا ملفات PDF فواتير في الشهر ده على الجهاز ده');if(o.pdfs.length)return cAppxF(k,o,mode);
 const n=cName(k,'pdf').replace(/^عهدة/,'صور فواتير عهدة').replace(/\.pdf$/,''),ttl='ملحق صور فواتير العهدة — شهر '+cMoLab(k);
 if(mode=='share')return sharePdf({src:o.el,name:n,title:ttl});const t2=toast('جاري تجهيز ملف PDF…');try{const b=await buildPdf(o.el,ttl);t2.remove();if(CAPN())return nativeSave(n+'.pdf',b,'application/pdf',false);return out(n+'.pdf',b,'application/pdf')}catch(e){t2.remove();console.error(e);alert('تعذّر تجهيز ملف PDF')}}
// ---- import (file prepared by Claude): {kind:'966cust',items:[...]}
async function cImport(f){let o;try{o=JSON.parse(await f.text())}catch(e){return alert('الملف ده مش ملف فواتير')}const L=Array.isArray(o)?o:o&&o.items;if(!L||!L.length)return alert('مفيش فواتير في الملف');
 if(o&&/^\d{4}-\d{2}$/.test(o.month||'')){const C=CU();if(!C.m[o.month])C.m[o.month]={open:o.open!=null?+o.open:C.cfg.base,why:'',items:[]};C.cur=o.month}
 const M=cMo();let n=0,s=0;for(const y of L){const x=cDraft(Object.assign({},y,{src:'import'}));x.amt=Math.round((+x.amt||0)*100)/100;if(!(x.amt>0)||!/^\d{4}-\d{2}-\d{2}$/.test(x.dt||'')){s++;continue}if(cDup(x)){s++;continue}x.at=nowIso();M.items.push(x);CU().mem[cnk(x.comp)]={desc:x.desc,kind:x.kind};n++}
 cSort(M.items);sv();render();alert(`✓ اتضاف ${n} فاتورة${s?` · اتجاهل ${s} (مكررة أو ناقصة)`:''}`)}
function custClick(d,b){
 if(d.cscan){cScan();return 1}if(d.cscanx){if(CSC)CSC.stop();CSN=0;CLR='';return 1}if(d.ctorch){if(CSC&&CSC.torch)CSC.torch();b.classList.toggle('pr');return 1}if(d.cshot){if(CSC)CSC.shot();return 1}
 if(d.cman){V.cq=[];cOpen(cDraft({}));return 1}
 if(d.ced){const x=cMo().items.find(y=>y.id==d.ced);if(x){V.cq=[];cOpen(JSON.parse(JSON.stringify(x)))}return 1}
 if(d.csave){cSave();return 1}
 if(d.cskip){const nx=(V.cq||[]).shift();if(nx){V.ce=nx;render()}else{V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q})}return 1}
 if(d.ccancel){CSN=0;CLR='';if(V.ce&&!cMo().items.some(x=>x.id==V.ce.id)&&!confirm('الفاتورة دي ما اتحفظتش. تلغيها؟'))return 1;V.ce=null;V.cq=[];goV({v:'cust',op:{},dr:{},q:V.q});return 1}
 if(d.cdel){if(!confirm('تمسح الفاتورة دي؟'))return 1;const M=cMo();M.items=M.items.filter(x=>x.id!=V.ce.id);(M.xd=M.xd||{})[V.ce.id]=nowIso();(V.ce.imgs||[]).forEach(k=>idbDel(k));sv();V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q});toastT('✓ اتمسحت');return 1}
 if(d.calt){const a=V.ce._alt;if(a){V.ce.dt=a.dt;V.ce.tm=a.tm;delete V.ce._alt;if(V.ce.kind=='وجبات')V.ce.desc=descOf('وجبات',V.ce.tm,V.ce.comp);render()}return 1}
 if(d.cpic){const i=$('#cimg1');if(i)i.click();return 1}
 if(d.cimgz){cImgUrl(d.cimgz).then(u=>{if(!u)return;const z=document.createElement('div');z.className='ovl pov';z.innerHTML='<button class="pr" data-ovlx="1">✕ إغلاق</button><img src="'+u+'">';document.body.appendChild(z)});return 1}
 if(d.cimgx){V.ce.imgs=(V.ce.imgs||[]).filter(k=>k!=d.cimgx);render();return 1}
 if(d.capx){cAppx(d.capx);return 1}
 if(d.cxl){cExport('x',d.cxl);return 1}if(d.cpdf){cExport('p',d.cpdf);return 1}
 if(d.cnew!==undefined){V.cnew=d.cnew!=='0';render();return 1}
 if(d.cnewgo){if(!cQtOk())return 1;const C=CU(),v=d.cnewgo=='v'?parseFloat(($('#cnewv')||{}).value):+d.cnewgo;if(!(v>=0))return alert('اكتب المبلغ'),1;const k=cNext(C.cur);if(C.m[k]&&C.m[k].items.length&&!confirm('شهر '+cMoLab(k)+' فيه فواتير. تغيّر رصيد بدايته بس؟'))return 1;
  C.m[k]=C.m[k]||{items:[]};C.m[k].open=Math.round(v*100)/100;C.m[k].why=v==cRem(C.m[C.cur])?'المتبقي من شهر '+cMoLab(C.cur):'';C.cur=k;V.cnew=false;sv();render();toastT('✓ بدأ شهر '+cMoLab(k));return 1}
 return 0}
function custChange(x){
 if(x.id=='cimgs'){const L=[...x.files];x.value='';if(L.length)cFromImages(L);return 1}
 if(x.id=='cimg1'){const L=[...x.files];x.value='';(async()=>{for(const f of L){if(isPdfF(f)&&f.size>CPMAX){alert('⚠ الملف '+f.name+' حجمه '+fsz(f.size)+'، والحد الأقصى 5 ميجا.');continue}const k=isPdfF(f)?await cPdfPut(V.ce,f):await cImgPut(V.ce.id,f);if(k)V.ce.imgs=(V.ce.imgs||[]).concat(k)}render()})();return 1}
 if(x.id=='cjson'){const f=x.files[0];x.value='';if(f)cImport(f);return 1}
 if(x.id=='cmosel'){CU().cur=x.value;V.cnew=false;svq();render();return 1}
 if(x.id=='cnp'&&V.ce){const n=(V.ce.note||'').replace(NOPAPER,'').replace(/^\s*[·⚠]\s*|\s*[·]\s*$/g,'').trim();V.ce.note=x.checked?[NOPAPER,n].filter(Boolean).join(' · '):n;return 1}
 if(x.dataset.cc){const C=CU();C.cfg[x.dataset.cc]=x.type=='number'?(+x.value||0):x.value;svq();return 1}
 if(x.dataset.cmopen){cMo().open=Math.round((+x.value||0)*100)/100;sv();render();return 1}
 if(x.dataset.cf&&V.ce){cField(x);if(x.dataset.cf=='kind'){render();return 1}const q=k=>document.querySelector(`[data-cf=${k}]`);['desc','car'].forEach(k=>{const e=q(k);if(e&&e!==x)e.value=V.ce[k]||''});const kd=q('kind');if(kd)kd.value=V.ce.kind;return 1}
 return 0}
function cField(x){const d=V.ce,k=x.dataset.cf,old=d.kind;if(k=='note'){const np=(d.note||'').includes(NOPAPER);d.note=[np?NOPAPER:'',x.value.trim()].filter(Boolean).join(' · ');return}d[k]=x.value;
 if(k=='comp'&&x.value){const m=CU().mem[cnk(x.value)],auto=!d.desc||d.desc==descOf(old,d.tm,'');if(m){d.kind=m.kind;d.desc=descOf(m.kind,d.tm,x.value)}else{d.kind=kindOf(x.value,'');if(auto)d.desc=descOf(d.kind,d.tm,'')}if((d.kind=='وقود'||d.kind=='سيارة')&&!d.car)d.car=CU().cfg.car}
 if(k=='tm'&&d.kind=='وجبات'){const ml=mealOf(d.tm);if(ml&&/فطار|غداء|عشاء|وجبة/.test(d.desc||''))d.desc=d.desc.replace(/فطار|غداء|عشاء|وجبة/,ml)}
 if(k=='kind'&&old!=d.kind){d.desc=descOf(d.kind,d.tm,d.comp);if((d.kind=='وقود'||d.kind=='سيارة')&&!d.car)d.car=CU().cfg.car}}
document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.cf&&V.ce&&V.v=='ced'&&x.dataset.cf!='kind')cField(x)});

