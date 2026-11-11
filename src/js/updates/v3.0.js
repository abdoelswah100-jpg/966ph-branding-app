// ---------- v3.0: custody PDF invoices and quotes ----------
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
