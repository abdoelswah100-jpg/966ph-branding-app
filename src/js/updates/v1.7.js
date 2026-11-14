// ---------- v1.7: readable text everywhere — light text on dark backgrounds, dark text on light ones ----------
// after every change of the screen, any text whose contrast with what is behind it is too low gets a colour of the same family
// that reads: on dark → white / sky / yellow / beige / gold / light orange / light green / salmon; on light → navy / brown / dark gold / dark orange / dark red / dark green.
// the original colour is kept in data-cfx and put back before anything is shared (PDF, Excel, print): shared files are always light with dark text.
const CFX_D={red:'#FFA98F',orange:'#FDBA74',yellow:'#FDE68A',gold:'#F2C94C',green:'#86EFAC',teal:'#7EE0D6',blue:'#7DD3FC',purple:'#D8B4FE',pink:'#F9A8D4',gray:'#E9EEF6',beige:'#F5DEB3'};
const CFX_L={red:'#991B1B',orange:'#9A3412',yellow:'#7A5A00',gold:'#7A5A00',green:'#166534',teal:'#115E59',blue:'#12305C',purple:'#5B21B6',pink:'#9D174D',gray:'#1B2430',beige:'#5C4033'};
const cfxP=s=>{const m=String(s).match(/[\d.]+/g);return m?m.map(Number):null};
const cfxL=c=>{c=c/255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4)},cfxY=a=>.2126*cfxL(a[0])+.7152*cfxL(a[1])+.0722*cfxL(a[2]);
const cfxR=(a,b)=>{const x=cfxY(a),y=cfxY(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
function cfxFam(c){const r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),d=mx-mn,l=(mx+mn)/2,s=d?d/(1-Math.abs(2*l-1)):0;if(s<.18||d<.08)return 'gray';
 let h=mx==r?((g-b)/d)%6:mx==g?(b-r)/d+2:(r-g)/d+4;h=(h*60+360)%360;
 return h<15||h>=345?'red':h<38?'orange':h<50?'gold':h<68?'yellow':h<160?'green':h<190?'teal':h<255?'blue':h<290?'purple':'pink'}
function cfxBg(e,M){const o=[];let x=e,r=null;while(x&&x.nodeType==1){if(M.has(x)){r=M.get(x);break}o.push(x);const c=getComputedStyle(x),gi=c.backgroundImage;
  if(gi&&gi.includes('gradient')){const m=cfxP(gi.replace(/^[^(]*\(/,'').replace(/^[^,]*deg,/,''));if(m&&m.length>=3){r=m.slice(0,3);break}}
  if(!/color\(/.test(c.backgroundColor)){const b=cfxP(c.backgroundColor);if(b&&(b.length<4||b[3]>.5)){r=b.slice(0,3);break}}x=x.parentElement}
 r=r||[255,255,255];o.forEach(z=>M.set(z,r));return r}
function cfxRun(root){root=root||document.body;if(!root||!root.querySelectorAll)return;
 root.querySelectorAll('[data-cfx]').forEach(e=>{e.style.color=e.dataset.cfx;delete e.dataset.cfx});
 const M=new Map(),fix=[];
 root.querySelectorAll('*').forEach(e=>{if(e.closest('.pdfpg,svg,#cfxoff'))return;let t=0;for(const n of e.childNodes)if(n.nodeType==3&&n.textContent.trim()){t=1;break}if(!t)return;
  const c=getComputedStyle(e);if(c.display=='none'||c.visibility=='hidden')return;const f=cfxP(c.color);if(!f||(f.length>3&&f[3]<.3))return;const b=cfxBg(e,M);
  const fs=parseFloat(c.fontSize),big=fs>=18.6||(fs>=14&&+c.fontWeight>=700),need=big?3:4.5;if(cfxR(f,b)>=need)return;
  const dk=cfxY(b)<.18,P=dk?CFX_D:CFX_L;let n=P[cfxFam(f)];const nc=cfxP(n.replace('#','').match(/../g).map(h=>parseInt(h,16)).join(','));
  if(cfxR(nc,b)<need){const w=cfxR([255,255,255],b),k=cfxR([17,17,17],b);n=w>=k?'#FFFFFF':'#111111';if(Math.max(w,k)<need&&cfxR(f,b)>=Math.max(w,k)-.5)return}fix.push([e,n])});
 fix.forEach(([e,n])=>{e.dataset.cfx=e.style.getPropertyValue('color')||'';e.style.setProperty('color',n,'important')})}
// shared copies never keep the screen fixes
function cfxStrip(n){if(n&&n.querySelectorAll){const L=[...n.querySelectorAll('[data-cfx]')];if(n.dataset&&n.dataset.cfx!=null)L.push(n);L.forEach(e=>{e.style.color=e.dataset.cfx;delete e.dataset.cfx})}return n}
const _pdfClone17=pdfClone;pdfClone=function(src){return cfxStrip(_pdfClone17(src))};
// Excel is always light: `xls` in core/12-reports.js no longer follows the dark theme
// print (the PDF fallback) is always light
let cfxPr=null;
addEventListener('beforeprint',()=>{const h=document.documentElement;cfxPr=h.getAttribute('data-th');h.setAttribute('data-th','light');cfxStrip(document.body)});
addEventListener('afterprint',()=>{const h=document.documentElement;if(cfxPr)h.setAttribute('data-th',cfxPr);else h.removeAttribute('data-th');cfxPr=null;cfxRun()});
// run after the screen changes (render, sheets, toasts), batched to one pass per frame
let cfxQ=0;const cfxGo=()=>{if(cfxQ)return;cfxQ=requestAnimationFrame(()=>{cfxQ=0;try{cfxRun()}catch(e){console.error(e)}})};
try{new MutationObserver(cfxGo).observe(document.body,{childList:true,subtree:true,characterData:true})}catch(e){}
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',cfxGo)}catch(e){}
const _cfg17=cfg;cfg=function(){const r=_cfg17.apply(this,arguments);cfxGo();return r};
cfxGo();
