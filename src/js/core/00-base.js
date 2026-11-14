const APPSRC='<!doctype html>\n'+document.documentElement.outerHTML;
const SH=['Regular Turkish','New Turkish','Old Turkish','Ukraine','Greece'];SH[-1]='—';
const S7=['Beauty','Baby','Personal','Health','Pharmacy','Mizan','Health Room'],S4=['Beauty','Baby','Personal','Health'];
const L=s=>s.split(';');
// pieces of composite ad types, used by every total, report, checklist and shortage list
const GAP=[['سايد',2,'68×102'],['هيدر',4,'20×65']],GAM='مات فيلم',GAL=['الأساسي','أجواء صيفية'],gaNm=r=>(r&&r.nm)||GAL[0],gaX=r=>gaNm(r)==GAL[0]?'':' · '+gaNm(r),PARTS={eg:[['Header',1],['Side',2]],md:[['Header',1],['Side',1]],ga:GAP};
// an item may sit on a different shelf type than the pharmacy (e.g. vitamins on New Turkish); '' / 'زي الصيدلية' = the pharmacy's
const FHM=['ستيكر + تصنيع أكريليك','ستيكر فقط'],fhmOf=r=>FHM.includes(r&&r.fhm)?r.fhm:FHM[0],whmOf=r=>FHM.includes(r&&r.whm)?r.whm:FHM[0],stD=x=>x=='تصنيع وتركيب'?'تصنيع + تركيب':x||'',ODK=['wh','fh','ec','eg','md'],isOld=(p,r)=>!!(p&&p.dz=='قديم')||!!(r&&r.od=='قديم'),CURVE='الجهة في السايد أكريليك (يمين / يسار) = اتجاه الانحناء';
const RSHT=['fh','wh','ec','eg','md'],RSAME='زي الصيدلية',rsh=(r,s)=>{const i=r&&r.rsh?SH.indexOf(r.rsh):-1;return i>=0?i:s},rshT=(r,s)=>{const i=r&&r.rsh?SH.indexOf(r.rsh):-1;return i>=0&&i!==s?` <small class="rshc">رفوف ${SH[i]}</small>`:''};
// Old Turkish gondola: what is needed (old items = full)
const EGPO=['كامل','باك لايت + ستيكر بس','أكريليك بس'];
const egpOf=(r,s)=>rsh(r,s)!==2?'':(EGPO.includes(r.egp)?r.egp:EGPO[0]),egHS=(r,s)=>egpOf(r,s)!==EGPO[2],egPK=(r,s)=>rsh(r,s)===2&&egpOf(r,s)!==EGPO[1];
// pocket pairs to make; acrylic-only rows: the row count itself; full rows: pq (empty = number of gondolas)
const egAO=(r,s)=>egpOf(r,s)===EGPO[2],egSub=(r,s)=>egPK(r,s),SDS=[['R','يمين'],['L','يسار']],
 egN=(r,s,sd)=>{if(!egPK(r,s))return 0;const v=r['p'+sd];return v!==undefined&&v!==null&&v!==''?Math.max(0,Math.round(+v||0)):(r.q==null?1:(+r.q||0))},egNT=(r,s)=>egN(r,s,'R')+egN(r,s,'L'),pkv=(r,k,sd)=>+r[k+'p'+sd]||0,
 pkZ=(r,q)=>{const c=x=>r[x]!==undefined&&r[x]!==null&&r[x]!=='';if(!c('pR')&&!c('pL'))return '(1L + 1R)';return `(يمين ×${c('pR')?Math.round(+r.pR||0):q} + يسار ×${c('pL')?Math.round(+r.pL||0):q})`};
