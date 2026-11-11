// ---------- v2.4: route table, short links -> coordinates ----------
const locC=p=>p?(coordsOf(p.loc)||(p.locc&&p.locs===p.loc?p.locc:null)):null;
const needLoc=p=>!!(p&&p.loc&&!coordsOf(p.loc)&&!(p.locc&&p.locs===p.loc));
const inSA=(a,b)=>a>15&&a<33&&b>34&&b<57;
function locParse(t){let x=String(t||'');try{x=decodeURIComponent(x)}catch(e){}const R=[/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/g,/\/(?:search|place|dir)\/(-?\d{1,2}\.\d{3,}),\s*\+?\s*(-?\d{1,3}\.\d{3,})/g,/@(-?\d{1,2}\.\d{3,}),(-?\d{1,3}\.\d{3,})/g,/[?&](?:q|ll|query|destination|center|daddr)=(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)/g,/center=(-?\d+\.\d+)%2C(-?\d+\.\d+)/g],F=[];
 for(const r of R){let m;while((m=r.exec(x))){const a=+m[1],b=+m[2];if(Math.abs(a)<=90&&Math.abs(b)<=180){if(inSA(a,b))return [a,b];F.push([a,b])}}}
 const m=x.match(/APP_INITIALIZATION_STATE=\[\[\[(-?\d+\.?\d*),(-?\d+\.\d+),(-?\d+\.\d+)\]/);if(m&&Math.abs(+m[3])<=90)return [+m[3],+m[2]];return F[0]||null}
async function locFetch(u){const H=CP('CapacitorHttp');if(!H)throw new Error('web');const r=await H.request({url:u,method:'GET',headers:{'User-Agent':'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Mobile Safari/537.36','Accept-Language':'ar,en;q=0.8'}});return locParse(String(r.url||'')+' '+(typeof r.data=='string'?r.data:JSON.stringify(r.data||'')))}
let LOCBUSY=0,LOCAUTO=0;
async function locUpdate(list,quiet){if(LOCBUSY)return;const L=(list||DB.ph).filter(needLoc);if(!L.length){if(!quiet)toastT('✓ كل المواقع جاهزة');return}
 if(!CP('CapacitorHttp')){if(!quiet)alert('تحويل اللينكات المختصرة لإحداثيات بيشتغل من تطبيق الموبايل وفيه نت. على اللاب توب: خد المواقع من الموبايل بالمزامنة أو النسخة الاحتياطية، أو الصق الإحداثيات بنفسك في خانة الموقع.');return}
 if(navigator.onLine===false){if(!quiet)toastT('⚠ محتاج نت علشان أحوّل المواقع');return}
 LOCBUSY=1;const t=toast('📍 جاري تحديث المواقع… 0 / '+L.length);let ok=0;const bad=[];
 for(let i=0;i<L.length;i++){const p=L[i];try{const c=await locFetch(p.loc);if(c){p.locc=c;p.locs=p.loc;p.modAt=nowIso();ok++}else bad.push(p.no)}catch(e){console.warn(e);bad.push(p.no)}t.innerHTML='📍 جاري تحديث المواقع… '+(i+1)+' / '+L.length}
 t.remove();LOCBUSY=0;if(ok)svq();if(['rte','month','home','ph'].includes(V.v))render();if(ok||!quiet)toastT('📍 اتحدّث '+ok+' موقع'+(bad.length?' · ما اتعرفش: '+bad.join('، '):''))}
function locAuto(){if(LOCAUTO||!['rte','month'].includes(V&&V.v)||!CP('CapacitorHttp')||navigator.onLine===false||!DB||!DB.ph.some(needLoc))return;LOCAUTO=1;setTimeout(()=>locUpdate(null,1),400)}
// distance in km (straight line)
const hv=(a,b)=>{const R=6371,r=x=>x*Math.PI/180,dl=r(b[0]-a[0]),dn=r(b[1]-a[1]),h=Math.sin(dl/2)**2+Math.cos(r(a[0]))*Math.cos(r(b[0]))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(h))};
const km=x=>x==null?'—':(x<10?x.toFixed(1):Math.round(x))+' كم';
function rteOrder(L,st){const R=L.slice(),o=[];let c=st?{c:st}:null;if(!c){c=R.shift();o.push(c)}while(R.length){let bi=0,bd=1e18;R.forEach((q,i)=>{const d=hv(c.c,q.c);if(d<bd){bd=d;bi=i}});c=R.splice(bi,1)[0];o.push(c)}return o}
function rteData(){const S=(V.rts||[]).map(id=>DB.ph.find(p=>p.id==id)).filter(Boolean),W=S.map(p=>({p,c:locC(p)})),ok=W.filter(x=>x.c),no=W.filter(x=>!x.c).map(x=>x.p),O=ok.length?rteOrder(ok,V.rtg):[];let prev=V.rtg||null,tot=0;
 const rows=O.map((x,i)=>{const d=prev?hv(prev,x.c)*1.3:null;if(d!=null)tot+=d;prev=x.c;return{p:x.p,c:x.c,d}});const parts=[];for(let i=0;i<rows.length;i+=9)parts.push(rows.slice(i,i+9));return{S,rows,no,tot,parts}}
const rteUrl=g=>'https://www.google.com/maps/dir//'+g.map(x=>x.c[0]+','+x.c[1]).join('/');
const phLink=p=>p.loc||(locC(p)?'https://www.google.com/maps?q='+locC(p).join(','):'');
function rteHtml(){const D=rteData(),m=MN(),M=DB.ph.filter(p=>p.mo==m).sort(pSort),sel=new Set((V.rts||[]).map(String)),g=V.rtgs;
 let h=`<div class="wcard"><h2>${ic('pin')}جدول السير</h2><p class="sub">اكتب أرقام الصيدليات (مسافة أو فاصلة بينهم) أو اختارهم من صيدليات الشهر. الترتيب أقرب فأقرب من مكانك الحالي، والمسافة تقريبية.</p>
 <label>أرقام الصيدليات<textarea id="rtn" rows="2" inputmode="numeric" placeholder="مثال: 1184 843 1136">${esc(D.S.map(p=>p.no).join(' '))}</textarea></label>
 ${M.length?`<div class="rtchips">${M.map(p=>`<button class="${sel.has(String(p.id))?'pr':''}" data-rtt="${p.id}">${esc(p.no)}${isMnt(p)?' 🔧':''}${p.st=='مكتملة'?' ✓':''}</button>`).join('')}</div>`:''}
 <div class="tt"><button data-rtgps="1">${ic('pin')}${g=='ok'?'✓ مكانك الحالي':g=='…'?'جاري تحديد مكانك…':'تحديد مكاني الحالي'}</button>${D.S.length?'<button data-rtclr="1">✕ مسح الكل</button>':''}${DB.ph.some(needLoc)?'<button data-locup="1">📍 تحديث المواقع</button>':''}</div>${g=='no'?'<small class="ywarn">⚠ مقدرتش أحدد مكانك (فعّل الموقع واسمح للتطبيق). الترتيب هيبدأ من أول صيدلية، وجوجل ماب هيبدأ المسار من مكانك.</small>':''}</div>`;
 if(!D.S.length)return h+'<p class="em">ضيف أرقام الصيدليات علشان يطلع الجدول.</p>';
 h+=`<div class="wcard"><div class="sc"><table class="rtt"><tr><th>#</th><th>الصيدلية</th><th>الحي / المدينة</th><th>المسافة</th><th>📍</th></tr>${D.rows.map((x,i)=>`<tr><td><b>${i+1}</b></td><td><b>${esc(x.p.no)}</b>${isMnt(x.p)?' <small class="rshc cxt">🔧 صيانة</small>':''}${x.p.st=='مكتملة'?' <small>✓</small>':''}</td><td>${esc(x.p.name||x.p.ct||'—')}</td><td>${km(x.d)}</td><td><a class="locb" href="${esc(phLink(x.p))}" target="_blank" rel="noopener">فتح</a></td></tr>`).join('')}${D.rows.length?`<tr class="tot"><td colspan="3">الإجمالي التقريبي${V.rtg?'':' (من أول صيدلية)'}</td><td>${km(D.tot)}</td><td></td></tr>`:''}</table></div>
 ${D.no.length?`<small class="ywarn">⚠ من غير موقع${DB.ph.some(needLoc)?' (أو لينك لسه ما اتحوّلش)':''}: ${D.no.map(p=>esc(p.no)).join('، ')}</small>`:''}
 <div class="locs">${D.parts.map((g2,i)=>`<a class="locb go" href="${rteUrl(g2)}" target="_blank" rel="noopener">${ic('pin')}${D.parts.length>1?'المسار — الجزء '+(i+1)+' ('+g2.length+')':'افتح المسار في جوجل ماب ('+g2.length+')'}</a>`).join('')}</div>
 <div class="tt"><button class="pr" data-rtwa="1">${ic('share')}مشاركة الجدول واتساب</button></div></div>`;
 return h}
function rteText(){const D=rteData(),o=['🗺️ *جدول السير* '+TD().split('-').reverse().join('-'),''];D.rows.forEach((x,i)=>{o.push(`${i+1}. صيدلية ${x.p.no}${x.p.name?' ('+x.p.name+')':''}${isMnt(x.p)?' — صيانة':''}${x.d!=null?' — '+km(x.d):''}`);const l=phLink(x.p);if(l)o.push(l)});
 if(D.rows.length)o.push('','الإجمالي التقريبي: '+km(D.tot));if(D.no.length)o.push('','من غير موقع: '+D.no.map(p=>p.no).join('، '));D.parts.forEach((g,i)=>o.push('',(D.parts.length>1?'المسار '+(i+1)+': ':'المسار: ')+rteUrl(g)));return o.join('\n')}
function rteGps(){if(!navigator.geolocation){V.rtgs='no';if(V.v=='rte')render();return}V.rtgs='…';if(V.v=='rte')render();navigator.geolocation.getCurrentPosition(g=>{V.rtg=[g.coords.latitude,g.coords.longitude];V.rtgs='ok';if(V.v=='rte')render()},()=>{V.rtgs='no';if(V.v=='rte')render()},{enableHighAccuracy:true,timeout:12000,maximumAge:120000})}
function rtePick(txt){const ns=String(txt||'').split(/[^\d]+/).filter(Boolean),ids=[];ns.forEach(n=>{const p=rcvPh(n);if(p&&!ids.includes(p.id))ids.push(p.id)});return{ids,miss:ns.filter(n=>!rcvPh(n))}}
function v24Click(d,b){
 if(d.rtgo!==undefined){const ids=String(d.rtgo||'').split(',').filter(Boolean).map(Number);goV({v:'rte',rts:ids,bk:V.v,bmo:V.mo,op:{},dr:{},q:V.q});rteGps();return 1}
 if(d.rtx){const k=V.bk||'home';goV({v:k=='month'?'month':'home',mo:V.bmo,op:{},dr:{},q:V.q});return 1}
 if(d.rtgps){rteGps();return 1}
 if(d.rtt){const id=+d.rtt,a=V.rts=V.rts||[];const i=a.indexOf(id);if(i>=0)a.splice(i,1);else a.push(id);render();return 1}
 if(d.rtclr){V.rts=[];render();return 1}
 if(d.rtwa){shareText(rteText());return 1}
 if(d.locup){locUpdate(null,0);return 1}
 return 0}
function v24Change(x){if(x.id=='rtn'){const r=rtePick(x.value);V.rts=r.ids;render();if(r.miss.length)toastT('⚠ مش لاقي صيدلية رقم: '+r.miss.join('، '));return 1}return 0}
