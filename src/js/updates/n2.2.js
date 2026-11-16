// ---------- 2.2: invoice QR codes of ZATCA phase 2 (dense codes on thermal paper) ----------
// 1) camera: Google code scanner (Play services, full camera resolution) first; the old in-app scanner stays as a fallback + its own button
// 2) photo / PDF: ML Kit also on enlarged, contrasted crops of the photo
// 3) parser: spaces, URL-safe base64, missing padding, long TLV lengths (0x81 / 0x82), amounts with commas
const _zatca22=zatca;zatca=function(s){let r=null;try{r=_zatca22(s)}catch(e){}
 try{let t=String(s||'').replace(/\s+/g,'').replace(/-/g,'+').replace(/_/g,'/');while(t.length%4)t+='=';const b=Uint8Array.from(atob(t),c=>c.charCodeAt(0)),o={};let i=0;
  while(i+2<=b.length){const tg=b[i];let l=b[i+1],h=2;if(l==0x81){l=b[i+2];h=3}else if(l==0x82){l=(b[i+2]<<8)|b[i+3];h=4}if(i+h+l>b.length)break;if(tg>=1&&tg<=5&&o[tg]==null)o[tg]=b.slice(i+h,i+h+l);i+=h+l}
  if(!o[1]||!o[4])return r;const dec=x=>new TextDecoder().decode(x),enc=new TextEncoder(),P=[];
  [1,2,3,4,5].forEach(k=>{if(!o[k])return;let v=k==4||k==5?enc.encode(dec(o[k]).replace(/,/g,'').trim()):o[k];if(v.length>255)v=v.slice(0,255);P.push(k,v.length,...v)});
  const z=_zatca22(btoa(String.fromCharCode(...P)));return z||r}catch(e){return r}};
async function cScanG(){const B=MLK();if(!B||!B.scan)return false;
 try{const a=await B.isGoogleBarcodeScannerModuleAvailable();if(a&&a.available===false){const t=toast('<span>جاري تحميل قارئ Google لأول مرة… (محتاج نت)</span>');let ok=false;
   try{await B.installGoogleBarcodeScannerModule();for(let i=0;i<45&&!ok;i++){await new Promise(r=>setTimeout(r,2000));try{ok=!!(await B.isGoogleBarcodeScannerModuleAvailable()).available}catch(e){}}}catch(e){console.warn('gms install',e)}finally{t.remove()}
   if(!ok){toastT('⚠ قارئ Google ما اتحمّلش، هيشتغل القارئ العادي');return false}}}catch(e){}
 let R;try{R=await B.scan({formats:['QR_CODE']})}catch(e){const m=String(e&&e.message||e);if(/cancel/i.test(m))return true;console.warn('gms scan',e);return false}
 const L=(R&&R.barcodes)||[];for(const b of L){const raw=b.rawValue||b.displayValue||'',z=zatca(raw);if(z){CLR=raw;cAfterScan(z,null);return true}}
 if(L.length){if(confirm('⚠ الكود اللي اتقرا مش كود فاتورة ضريبية.\nتجرّب تاني؟'))return cScanG();return true}
 return true}
const _cScan22=cScan;cScan=async function(){if(CSC)return;if(MLK()){try{if(await cScanG())return}catch(e){console.warn('gms',e)}}return _cScan22()};
// enlarged crops of a photo, for ML Kit (dense codes read better when they fill the image)
async function qrCrops(blob){const u=URL.createObjectURL(blob),out=[];try{const im=await new Promise((ok,no)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=no;i.src=u}),W=im.naturalWidth,H=im.naturalHeight,cv=document.createElement('canvas'),x=cv.getContext('2d');
 for(const[a,b,c,d] of [[0.15,0.15,0.7,0.7],[0.1,0.25,0.8,0.5],[0.25,0.1,0.5,0.8],[0,0,0.65,0.65],[0.35,0,0.65,0.65],[0,0.35,0.65,0.65],[0.35,0.35,0.65,0.65]]){const sw=W*c,sh=H*d,sc=Math.min(2.5,3200/Math.max(sw,sh));
  cv.width=Math.round(sw*sc);cv.height=Math.round(sh*sc);x.imageSmoothingQuality='high';x.filter='grayscale(1) contrast(1.6)';x.drawImage(im,W*a,H*b,sw,sh,0,0,cv.width,cv.height);x.filter='none';const bl=await new Promise(ok=>cv.toBlob(ok,'image/jpeg',0.95));if(bl)out.push(bl)}}catch(e){console.warn('crops',e)}finally{URL.revokeObjectURL(u)}return out}
const _qrN22=qrFromBlobN;qrFromBlobN=async function(blob){const z=await _qrN22(blob);if(z||!MLK())return z;for(const b of await qrCrops(blob)){const r=await _qrN22(b);if(r)return r}return null};
// the old in-app scanner on its own button (inside the app only)
const _render0_22=render0;render0=function(){const r=_render0_22.apply(this,arguments);try{if(MLK()){const b=document.querySelector('[data-cscan]');if(b&&!document.querySelector('[data-cscano]'))b.insertAdjacentHTML('afterend','<button data-cscano="1">📷 الماسح القديم</button>')}}catch(e){}return r};
const _v24Click22=v24Click;v24Click=function(d,b){if(d.cscano){if(!CSC)_cScan22();return 1}return _v24Click22(d,b)};
