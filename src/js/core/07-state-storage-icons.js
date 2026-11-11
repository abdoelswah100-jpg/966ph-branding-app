const LOGO='__LOGO_DATA_URI__';
const logoChip=(h)=>`<span style="display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--pb),var(--pb2));border-radius:8px;padding:4px 8px;line-height:0;flex:none"><img src="${LOGO}" alt="Al-Dawaa" style="height:${h}px;display:block"></span>`;
const logoImg=(h)=>`<img src="${LOGO}" alt="Al-Dawaa" style="height:${h}px;display:block;filter:drop-shadow(0 1px 3px rgba(0,0,0,.35))">`;
let V={v:'home',p:null,op:{},dr:{},q:{t:'',st:'',mo:''}},DB=null;
const FPX=['ck','nt','r','x','wf','rpR','rpL','xpR','xpL','wfpR','wfpL','rp','xp','wfp'];
function fp(p){const R={};Object.keys(p.rows||{}).sort().forEach(k=>{const a=p.rows[k];if(Array.isArray(a)&&a.length)R[k]=a.map(r=>{const o={};Object.keys(r).sort().forEach(x=>{if(!FPX.includes(x))o[x]=r[x]});return o})});const s=JSON.stringify([p.sh,p.mod||'',R]);let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))|0;return (h>>>0).toString(36)+'.'+s.length}
const revSt=p=>!p.rev?'':(p.revFp&&p.revFp!==fp(p)?'old':'ok');
try{DB=JSON.parse(localStorage.getItem('ads')||'null')}catch(e){}
const BASE='2026-10-16T00:00:00.000Z';
var PREMIG=null,PRECK=null,UREADY=false;
function norm(){DB=DB||{ph:[]};if(!PRECK&&(DB.ph||[]).some(p=>Object.values(p.rows||{}).some(a=>Array.isArray(a)&&a.some(r=>r&&r.ck!=null))))PRECK=JSON.stringify(DB);if((DB.ph||[]).some(p=>((p.rows||{}).al||[]).some(r=>r&&r.sec=='Health Room')))PREMIG=JSON.stringify(DB);if(DB.cfg&&DB.cfg.sz&&DB.cfg.sz['mt.al']=='أكريليك 8 ml')delete DB.cfg.sz['mt.al'];DB.tp=DB.tp||[];DB.cfg=DB.cfg||{};DB.cfg.adTypes=(DB.cfg.adTypes||[]).filter(x=>x&&(typeof x!='string'||x.trim()));DB.cfg.modTypes=DB.cfg.modTypes||['تعديل براندنج','براندنج جديد','صيانة'];DB.dt=DB.dt||{};DB.del=DB.del||{};DB.cfg.sz=DB.cfg.sz||{};DB.pl=DB.pl||{};DB.qi=DB.qi||{quotes:[],invoices:[]};DB.qi.quotes=DB.qi.quotes||[];DB.qi.invoices=DB.qi.invoices||[];DB.ph.forEach(p=>{p.st=p.st||'لم تبدأ';if(!(p.sh>=0&&p.sh<SH.length))p.sh=0;p.mo=p.mo||MN();p.sup=p.sup||'عبدالله السواح';if(p.sup.trim()==='عبدالله')p.sup='عبدالله السواح';p.co=p.co||'عمال الشركة';p.mod=p.mod||'براندنج جديد';p.modAt=p.modAt||BASE;if(p.rev==null)p.rev=false;mig(p);if(p.rev&&!p.revFp)p.revFp=fp(p)});if(!DB.cfg.dsup||DB.cfg.dsup.trim()==='عبدالله')DB.cfg.dsup='عبدالله السواح';DB.trash=(DB.trash||[]).filter(x=>x&&x.p&&Date.now()-new Date(x.at).getTime()<30*864e5);if(DB.cfg.ue==null)DB.cfg.ue=DB.ph.filter(p=>(p.modAt||BASE)>(DB.cfg.lb||'')).length;if(UREADY){if(HIDDB!==DB){HID=[];HIDDB=null;STO=null;UBASE=null}uInit()}}
norm();
const nowIso=()=>new Date().toISOString();
const IDB={db:null,ok:false};let SNAPS=[],PERS=false,NOC=0,LASTE=0,IDBT=null,EDTD=false;
function idbOpen(){return new Promise(r=>{try{const q=indexedDB.open('ads966',1);q.onupgradeneeded=()=>{const d=q.result;if(!d.objectStoreNames.contains('kv'))d.createObjectStore('kv')};q.onsuccess=()=>{IDB.db=q.result;IDB.ok=true;r(true)};q.onerror=()=>r(false)}catch(e){r(false)}})}
function idbGet(k){return new Promise(r=>{if(!IDB.ok)return r(null);try{const q=IDB.db.transaction('kv').objectStore('kv').get(k);q.onsuccess=()=>r(q.result==null?null:q.result);q.onerror=()=>r(null)}catch(e){r(null)}})}
function idbSet(k,v){if(!IDB.ok)return Promise.resolve(false);return new Promise(r=>{try{const t=IDB.db.transaction('kv','readwrite');t.objectStore('kv').put(v,k);t.oncomplete=()=>r(true);t.onerror=()=>r(false)}catch(e){r(false)}})}
const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}try{reqAuto()}catch(e){console.error(e)}try{ntfLater()}catch(e){}try{capAuto()}catch(e){console.error(e)}const p=(V&&V.p&&(V.v=='ph'||V.v=='sum'||V.v=='rev'||V.v=='qe'||(V.v=='all'&&V.am=='ph')))?curP():null;if(p)p.modAt=nowIso();if(!NOC){const n=Date.now();if(n-LASTE>4000){DB.cfg.ue=(DB.cfg.ue||0)+1;LASTE=n;try{gdEdit()}catch(e){}if(DB.cfg.ue%10==0)setTimeout(bkRemind,80)}}try{secLater()}catch(e){}const j=JSON.stringify(dbOut());try{localStorage.setItem('ads',j)}catch(e){}clearTimeout(IDBT);IDBT=setTimeout(()=>idbSet('ads',j),300)}catch(e){}};
const svq=()=>{NOC=1;try{sv()}finally{NOC=0}};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ICN={bell:'<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',inbox:'<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',box:'<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',t_ga:'<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11.5l2-8H6.5"/>',cam:'<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',lock:'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',finger:'<path d="M12 11v4"/><path d="M8 15a4 4 0 0 0 8 0v-4a4 4 0 0 0-8 0"/><path d="M5 13v-2a7 7 0 0 1 14 0v4a7 7 0 0 1-3 5.7"/>',img:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',check:'<polyline points="20 6 9 17 4 12"/>',pin:'<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',globe:'<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',add:'<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
trash:'<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
edit:'<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>',
print:'<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
copy:'<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
share:'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>',
chat:'<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
layers:'<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
bld:'<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 21v-4h6v4"/><path d="M8 7h.01M12 7h.01M16 7h.01M8 11h.01M12 11h.01M16 11h.01"/>',
bars:'<path d="M3 3v18h18"/><path d="M8 17v-5M12 17V8M16 17V9M20 17v-3"/>',
calc:'<rect x="5" y="2" width="14" height="20" rx="2"/><rect x="8" y="5" width="8" height="4" rx="1"/><path d="M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01"/>',
eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
db:'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
chev:'<polyline points="15 18 9 12 15 6"/>',chevr:'<polyline points="9 18 15 12 9 6"/>',
menu:'<line x1="5" y1="7" x2="19" y2="7"/><line x1="5" y1="12" x2="19" y2="12"/><line x1="5" y1="17" x2="19" y2="17"/>',
gear:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
list:'<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
ruler:'<rect x="2" y="8" width="20" height="8" rx="1"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/>',
look:'<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/>',
upload:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
file:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="14" y2="17"/>',
sheet:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M8 12h8v6H8zM12 12v6M8 15h8"/>',
phone:'<rect x="6" y="2" width="12" height="20" rx="2"/><line x1="11" y1="18" x2="13" y2="18"/>',
check:'<circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16 9.5"/>',
filter:'<polygon points="22 3 2 3 10 12.5 10 19 14 21 14 12.5 22 3"/>',
t_ws:'<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 17l-5-5-9 8"/>',
t_al:'<path d="M4 20l6-16 6 16M6.5 14h7"/><path d="M19 10v10"/>',
t_wh:'<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
t_fh:'<rect x="2" y="8" width="20" height="8" rx="1"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/>',
t_ec:'<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
t_eg:'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M4 9h16M4 15h16"/>',
t_md:'<path d="M10.5 3.5a5 5 0 0 1 7 7l-7 7a5 5 0 0 1-7-7z"/><path d="M7 7l7 7"/>',
t_dc:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',
t_saw:'<rect x="3" y="3" width="7" height="18" rx="1"/><rect x="14" y="3" width="7" height="18" rx="1"/>',
t_saf:'<path d="M3 21V3M21 21V3M3 8h18M3 14h18M3 20h18"/>',
t_ds:'<path d="M5 21V3h12v18M3 21h18"/><circle cx="14" cy="12" r="1"/>',
t_c4:'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
t_fr:'<path d="M12 2v20M3.5 7l17 10M3.5 17l17-10"/>',
t_cm:'<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
t_ab:'<rect x="3" y="4" width="18" height="13" rx="1"/><path d="M8 21l4-4 4 4"/>'};
const tIc=id=>ic(ICN['t_'+id]?'t_'+id:'t_wh');
const ic=n=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICN[n]||''}</svg>`;
const $=s=>document.querySelector(s);
function dl(n,t,ty){if(CAPN()){nativeSave(n,t,ty);return}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:ty}));a.download=n;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},800)}
const PL=p=>`Ph Al-Dawaa ${esc(p.no||'')}`;
const opts=(f,r,s)=>f.o(r,f.k=='rsh'?s:rsh(r,s));
