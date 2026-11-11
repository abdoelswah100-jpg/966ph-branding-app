// ---------- v3.9: «Big / Small» is the size, not the name ----------
const N39EC={'Baby milk - Small · حليب الطفل':['Baby milk · حليب الطفل','صغير'],'Baby milk - Big · حليب الطفل':['Baby milk · حليب الطفل','كبير'],'Baby Food - small · طعام الطفل':['Baby Food · طعام الطفل','صغير'],'Baby Food - Big · طعام الطفل':['Baby Food · طعام الطفل','كبير'],'Baby Bath Big · مستلزمات حمام الطفل':['Baby Bath · مستلزمات حمام الطفل','كبير'],'Geriatric care Big · العناية بالمسنين':['Geriatric care · العناية بالمسنين','كبير']};
const N39FH={'Healthy food - s':['Healthy food','صغير'],'Healthy food Big 77X11.5':['Healthy food','كبير']};
const n39=(M,nm)=>{if(M[nm])return M[nm];const k=Object.keys(M).find(a=>nk(a)==nk(nm||''));return k?M[k]:null};
function mig39Rows(R,sh){let c=0;if(!R)return 0;
 (R.ec||[]).forEach(r=>{const m=n39(N39EC,r.nm);if(!m)return;r.nm=m[0];if(!String(r.sz||'').startsWith(m[1])){const v=[].concat(SZ('ec.'+rsh(r,sh))||[]).find(x=>String(x).startsWith(m[1]));if(v)r.sz=v}c++});
 ['fh','wh'].forEach(k=>(R[k]||[]).forEach(r=>{const m=n39(N39FH,r.nm);if(!m)return;r.nm=m[0];if(k=='fh'&&two(r)&&rsh(r,sh)!==2)r.sz=m[1];c++}));
 (R.c4||[]).forEach(r=>{if(String(r.sz||'').includes('50×100')){r.sz='صغير 40×100';c++}});return c}
// a warehouse item / transferred entry
function fix39(x){if(!x)return 0;let c=0;
 if(x.ty=='End cap'){const m=n39(N39EC,x.nm);if(m){x.nm=m[0];c=1}}
 if(x.ty=='Floor Header'||x.ty=='Wall Header'){const m=n39(N39FH,x.nm);if(m){x.nm=m[0];c=1}}
 if(x.ty=='Sticker care 4 life'&&String(x.size).replace(/\s+/g,'')=='50×100'){x.size='40×100';c=1}
 if(x.ty==RLTY&&x.nm=='رملي'){x.nm='ثلجي شفاف';c=1}return c}
function whFix39(){const W=DB.wh;let ch=0;W.forEach(x=>{if(x.m39)return;if(fix39(x))ch=1;x.m39=1});
 if(ch)for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));W.splice(i,1)}}}
function v39Fix(){if(!DB.cfg.m39&&DB.ph.some(p=>!p.m39)){try{const pre=JSON.stringify(dbOut());setTimeout(()=>{try{SNAPS.unshift({at:nowIso(),day:TD(),why:'قبل تحديث v3.9 (Big بقى مقاس)',db:pre});SNAPS=SNAPS.slice(0,5);if(IDB.ok)idbSet('snaps',SNAPS);else localStorage.setItem('ads_snaps',JSON.stringify(SNAPS.slice(0,3)))}catch(e){}},5000)}catch(e){}}
 DB.ph.forEach(p=>{if(p.m39)return;mig39Rows(p.rows,p.sh);
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(e&&fix39(e)){const k2=whKey(e);if(o[k2])o[k2].q=wq(+o[k2].q+(+e.q||0));else o[k2]=e}else if(o[k])o[k].q=wq(+o[k].q+(+e.q||0));else o[k]=e});p.whT=o}
  p.m39=1});
 (DB.tp||[]).forEach(t=>{if(t&&!t.m39){mig39Rows(t.rows,t.sh||0);t.m39=1}});
 if(!DB.cfg.m39){const z=DB.cfg.sz;if(z&&Array.isArray(z.c4))z.c4=z.c4.map(v=>String(v).replace('50×100','40×100'));
  try{let ci=0;Object.keys(N39FH).concat(Object.keys(N39EC)).forEach(a=>{const b=(N39FH[a]||N39EC[a])[0];if(IMG[nk(a)]&&!IMG[nk(b)]){IMG[nk(b)]=IMG[nk(a)];ci=1}});if(ci)imgSave()}catch(e){}
  DB.cfg.m39=1}
 svq()}
const _applyTpl39=applyTpl;applyTpl=function(p,q){_applyTpl39(p,q);mig39Rows(p.rows,p.sh)};

// ---------- v3.9: old-design sides with names and pictures ----------
const OSN={Baby:['Baby accessories','Baby food','Baby milk','Baby toiletries','Baby wipes'],
 Personal:['Bath accessories','Body care','Body lotion','Complete hair & skin care','Deodorant','Feminine care','Hair care','Hair remover','Men care','Oral care','Shaving & Grooming','Shower gel','Soap'],
 Beauty:['Beauty accessories','Complete hair & skin care','Eye care','Hair care','Hair colorants','Skin care','Styling tools'],
 Health:['First aid','Geriatric care','Health & Home care','Healthy food','Medical devices','Medical supports','OTC','Vitamins']};
const osSplit=n=>{const a=String(n||'').split(' · ');return a.length>1?{nm:a.slice(0,-1).join(' · '),sd:a[a.length-1]}:{nm:'',sd:a[0]}},osd=n=>osSplit(n).sd;
const osImgK=(sec,nm,sd)=>BIMG[('os|'+sec+'|'+nm+'|'+sd).toLowerCase()]||null;
const osImg=x=>{const o=osSplit(x&&x.nm);return o.nm?osImgK(x.sec,o.nm,o.sd):null};
const osOk=d=>!!d.nm2&&(OSN[d.sec]||[]).includes(d.nm2),osImgD=d=>['saf','saw','egs'].includes(d.k)&&osOk(d)?osImgK(d.sec,d.nm2,d.sd):null;

// ---------- v3.9: catalog of every item the app knows (import check + export) ----------
const TK3=[0,1,2];let WCK=null;
function whCatalog(){const SKIP=['mw','xi','od','rsh','stt','egp','nt','xn'],O=new Map();
 const types=T.filter(t=>!t.auto&&!WXT.includes(t.id)&&!['ws','al'].includes(t.id));
 for(let s=0;s<SH.length;s++)for(const t of types){if(t.only&&!t.only.includes(s))continue;const sels=t.f.filter(f=>f.o&&!SKIP.includes(f.k));let n=0;
  const go=(i,d)=>{if(n>8000)return;if(i==sels.length){n++;let P=[];try{P=whParts(t,Object.assign({q:1},d),s)}catch(e){}
    P.forEach(y=>{const o={sh:y.sh,ty:y.ty,nm:y.pk?'':(y.nm||''),sec:y.pk?'':(y.sec||''),mat:y.mat||'',size:String(y.size||'')};O.set(whKey(o),o)});return}
   const f=sels[i];try{if(f.hide&&f.hide(d,s))return go(i+1,d)}catch(e){}let op=[];try{op=f.o(d,s)||[]}catch(e){}if(!op.length)return go(i+1,d);
   op.forEach(v=>{const val=typeof v=='object'&&v?(v.v!=null?v.v:v.n):v;if(val===''||String(val).startsWith('➕'))return;go(i+1,Object.assign({},d,{[f.k]:val}))})};
  go(0,{})}
 return [...O.values()]}
function whCatKeys(){if(!WCK)WCK=new Set(whCatalog().map(whKey));return WCK}
function whImpOk(x){if(!x)return false;if(x.old||x.ty=='أخرى')return true;if(x.ty==RLTY)return RLK.includes(x.nm);const o=x.rol?Object.assign({},x,{mat:String(x.mat||'').replace(ROLM,'')}):x;return whCatKeys().has(whKey(o))}
function whCatExport(){WCK=null;const L=whCatalog().sort((a,b)=>(a.ty+a.sec+a.nm+a.size+a.sh).localeCompare(b.ty+b.sec+b.nm+b.size+b.sh));
 RLK.forEach(k=>L.push({sh:-1,ty:RLTY,nm:k,sec:'',mat:'',size:'عرض 1 م'}));
 const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
 const rows=[['sh','نوع الرفوف','ty','nm','sec','mat','size'].map(q).join(',')].concat(L.map(x=>[x.sh,x.sh>=0?SH[x.sh]:'مشترك لكل الرفوف',x.ty,x.nm,x.sec,x.mat,x.size].map(q).join(',')));
 rows.push('','"تصميم قديم: ty = '+Object.values(OLDT).join(' / ')+' · nm = المسمى · يمين أو يسار · old: 1"','"رولات الستيكر: الكمية بالمتر، unit: متر"');
 out('966-كتالوج-أصناف-المخزن-'+VER+'.csv','﻿'+rows.join('\n'),'text/csv');toastT('✓ اتصدّر '+L.length+' صنف')}
