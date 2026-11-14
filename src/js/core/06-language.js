const ORD=['ws','al','wh','fh','ec','eg','ga','md'];T.sort((a,b)=>{const x=ORD.indexOf(a.id),y=ORD.indexOf(b.id);return(x<0?99:x)-(y<0?99:y)});
T.forEach(t=>{if(ODK.includes(t.id)&&t.f)t.f.push(Object.assign(sel('od','التصميم',()=>['جديد','قديم']),{hide:()=>{const p=curP();return !!(p&&(p.dz=='قديم'||p._wh||p._rc))}}));if(RSHT.includes(t.id)){t.f.push(sel('rsh','نوع الرفوف',()=>[RSAME].concat(SH)));const z0=t.z;t.z=(r,x)=>z0(r,rsh(r,x))}if(t.f){t.f.push(Object.assign(sel('mw','نوع العمل (الصيانة)',()=>MWL()),{hide:()=>{const p=curP();return !isMnt(p)}}));t.f.push(Object.assign(sel('xi','بند إضافي (طلب العميل)',()=>['لا','نعم']),{hide:()=>{const p=curP();return !!(p&&(p._wh||p._rc))}}));t.f.push({k:'xn',l:'سبب البند الإضافي (بيظهر في تقرير الإدارة)',hide:d=>d.xi!='نعم'||(()=>{const p=curP();return !!(p&&(p._wh||p._rc))})()})}if(t.f)t.f.push({k:'nt',l:'ملاحظات (اختياري)'})});
const TY=p=>{DB.cfg.adTypes=DB.cfg.adTypes||[];DB.cfg.adTypes.forEach((n,i)=>{if(!n)return;const id='custom_'+i,old=T.find(t=>t.id===id);if(old){old.n=n;old.z=r=>DB.cfg.adTypes[i]}else T.push({id,n,f:[Q,{k:'nt',l:'ملاحظات (اختياري)'}],z:r=>DB.cfg.adTypes[i]})});return T.filter(t=>{if(t.id&&t.id.startsWith('custom_')&&!DB.cfg.adTypes[+t.id.slice(7)])return false;return !t.only||t.only.includes(p.sh)})};
const ST=['لم تبدأ','جاري','مكتملة'],SC={'لم تبدأ':'#5F6B7E','جاري':'#B45309','مكتملة':'#23774A'};
const z2=n=>String(n).padStart(2,'0'),MN=()=>{const d=new Date();return d.getFullYear()+'-'+z2(d.getMonth()+1)},TD=()=>MN()+'-'+z2(new Date().getDate()),VER='v1.7';
const EN_D=/*@EN*/{};let TRX=null;
const isEN=()=>!!(DB&&DB.cfg&&DB.cfg.lang=='en');
const AW='\\u0621-\\u065F\\u066E-\\u06D3';
function trRx(){if(!TRX){const ks=Object.keys(EN_D).sort((a,b)=>b.length-a.length).map(k=>k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));TRX=new RegExp('(?<!['+AW+'])(?:'+ks.join('|')+')(?!['+AW+'])','g')}return TRX}
function tr(x){if(!isEN()||x==null||typeof x=='number')return x;const s=String(x);if(!/[؀-ۿ]/.test(s))return x;return s.replace(trRx(),m=>EN_D[m]).replace(/ {2,}/g,' ').replace(/\b(\d+) Pharmacy\b(?! \d)/g,(m,n)=>n=='1'?m:n+' pharmacies')}
const TRSKIP={SCRIPT:1,STYLE:1,TEXTAREA:1};
function trNode(n){if(!isEN()||!n)return;
 if(n.nodeType==3){const p=n.parentNode;if(!p||TRSKIP[p.nodeName]||(p.closest&&p.closest('[contenteditable="true"]')))return;if(p.nodeName=='OPTION'&&!p.hasAttribute('value'))p.setAttribute('value',p.textContent);const t=tr(n.nodeValue);if(t!==n.nodeValue)n.nodeValue=t;return}
 if(n.nodeType!=1&&n.nodeType!=11)return;if(TRSKIP[n.nodeName])return;
 const els=n.nodeType==1?[n,...n.querySelectorAll('*')]:[...n.querySelectorAll('*')];
 for(const e of els){if(e.nodeName=='OPTION'&&!e.hasAttribute('value'))e.setAttribute('value',e.textContent);for(const a of ['placeholder','title','aria-label'])if(e.hasAttribute(a)){const v=e.getAttribute(a),t=tr(v);if(t!==v)e.setAttribute(a,t)}}
 const w=document.createTreeWalker(n,4);const L=[];let x;while(x=w.nextNode())L.push(x);L.forEach(trNode)}
new MutationObserver(ms=>{if(!isEN())return;for(const m of ms)m.addedNodes.forEach(trNode)}).observe(document.documentElement,{childList:true,subtree:true});
{const _al=window.alert.bind(window),_cf=window.confirm.bind(window),_pr=window.prompt.bind(window);window.alert=m=>_al(tr(m));window.confirm=m=>_cf(tr(m));window.prompt=(m,d)=>_pr(tr(m),d)}

