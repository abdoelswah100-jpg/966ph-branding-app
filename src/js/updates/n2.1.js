// ---------- 2.1 (file n2.1.js: the old numbering already has v2.1.js … v3.9.js) ----------
// 1) «📍 مواقع هامة»  2) جدول السير: ابدأ من / ارجع لـ (المخزن = البيت)  3) «الموجود والناقص» لكل صيدليات الشهر
// No place or pharmacy data in the code: places live in DB.cfg.places and come from a «966-places» file or are typed in the app.
MENU.splice(Math.max(0,MENU.findIndex(m=>m[0]=='prep')+1),0,['avl','الموجود والناقص','layers'],['plc','مواقع هامة','pin']);
const PLC=()=>DB.cfg.places||(DB.cfg.places=[]),plcGet=id=>PLC().find(x=>String(x.id)==String(id)),plcHome=()=>plcGet(DB.cfg.rtHome);
const plcUrl=c=>'https://www.google.com/maps?q='+c[0]+','+c[1],plcC=c=>(+c[0]).toFixed(6)+', '+(+c[1]).toFixed(6);
function plcHtml(){const L=PLC(),hm=DB.cfg.rtHome;
 let h=`<div class="wcard"><h2>${ic('pin')}مواقع هامة</h2><p class="sub">دوس على الموقع يفتح في جوجل ماب. الموقع اللي عليه 🏠 هو نقطة البداية والرجوع في «جدول السير».</p></div>`;
 if(!L.length)h+='<p class="em">مفيش مواقع لسه. ضيف موقع من تحت أو استورد ملف المواقع.</p>';
 L.forEach(x=>{h+=`<div class="wcard"><div class="locs"><a class="locb go" href="${plcUrl(x.c)}" target="_blank" rel="noopener">${ic('pin')}${esc(x.ic||'📍')} ${esc(x.n)}</a></div>
  <small class="hint">${plcC(x.c)}${x.ad?' · '+esc(x.ad):''}</small>
  <div class="tt"><button${String(x.id)==String(hm)?' class="pr"':''} data-plch="${x.id}">🏠 ${String(x.id)==String(hm)?'نقطة البداية والرجوع ✓':'خليه نقطة البداية والرجوع'}</button><button data-plce="${x.id}">✏️ تعديل</button><button data-plcd="${x.id}">🗑 حذف</button></div></div>`});
 h+=`<div class="wcard"><h3>➕ موقع جديد</h3><label>الاسم<input id="plcn" placeholder="مثال: مخزن الرياض"></label><label>لينك جوجل ماب أو الإحداثيات<textarea id="plcl" rows="2" placeholder="24.562390, 46.586851"></textarea></label><div class="tt"><button class="pr" data-plca="1">إضافة</button></div></div>`;
 return h}
async function plcParse(t){t=String(t||'').trim();if(!t)return null;let c=locParse(t);if(c)return c;
 if(/goo\.gl|maps\.app/.test(t)){if(!CP('CapacitorHttp')){alert('اللينك المختصر بيتحوّل من تطبيق الموبايل وفيه نت. أو الصق الإحداثيات (مثال: 24.5624, 46.5869).');return null}try{c=await locFetch(t)}catch(e){c=null}}
 if(!c)alert('ما قدرتش أطلّع الإحداثيات من اللي اتكتب. الصق لينك المكان من جوجل ماب أو الإحداثيات (مثال: 24.5624, 46.5869).');return c}
async function plcAdd(){const n=($('#plcn').value||'').trim(),c=await plcParse($('#plcl').value);if(!n)return alert('اكتب اسم الموقع');if(!c)return;
 PLC().push({id:Date.now(),n,ic:'📍',c});if(!plcHome())DB.cfg.rtHome=PLC()[PLC().length-1].id;sv();render();toastT('✓ اتضاف «'+n+'»')}
async function plcEdit(id){const x=plcGet(id);if(!x)return;const n=prompt('اسم الموقع:',x.n);if(n==null)return;const l=prompt('لينك جوجل ماب أو الإحداثيات (سيبه زي ما هو لو مش هتغيره):',plcC(x.c));if(l==null)return;
 const c=l.trim()==plcC(x.c)?x.c:await plcParse(l);if(!c)return;x.n=n.trim()||x.n;x.c=c;sv();render()}
// file {kind:'966-places', places:[{n, ic, ad, c:[lat,lng], home:1}], ph:[{no, c:[lat,lng]}]}
function plcImpOpen(q){const P=Array.isArray(q.places)?q.places.filter(x=>x&&x.n&&Array.isArray(x.c)):[],H=Array.isArray(q.ph)?q.ph.filter(z=>z&&z.no&&Array.isArray(z.c)):[];
 const hit=H.map(z=>[z,DB.ph.filter(p=>String(p.no)==String(z.no))]),miss=hit.filter(([,a])=>!a.length).map(([z])=>z.no),nP=hit.reduce((a,[,A])=>a+A.length,0);
 if(!confirm(`ملف المواقع:\n• ${P.length} موقع هام${P.length?' ('+P.map(x=>x.n).join('، ')+')':''}\n• إحداثيات ${H.length} صيدلية (${nP} سجل في البرنامج)${miss.length?'\n• مش موجودة عندك: '+miss.join('، '):''}\n\nالإحداثيات بتتحط جنب لينك الصيدلية، واللينك مش بيتغير. تكمل؟`))return;
 P.forEach(x=>{const o=PLC().find(y=>y.n==x.n);if(o){o.c=x.c;if(x.ic)o.ic=x.ic;if(x.ad)o.ad=x.ad}else PLC().push({id:Date.now()+Math.floor(Math.random()*1e3),n:x.n,ic:x.ic||'📍',ad:x.ad||'',c:x.c});if(x.home)DB.cfg.rtHome=PLC().find(y=>y.n==x.n).id});
 hit.forEach(([z,A])=>A.forEach(p=>{if(!p.loc)p.loc=plcUrl(z.c);p.locc=z.c;p.locs=p.loc;p.modAt=nowIso()}));
 sv();snd('ok');toastT(`✓ ${P.length} موقع هام · ${nP} صيدلية بقى ليها إحداثيات`);goV({v:'plc',op:{},dr:{},q:V.q})}
// ---- جدول السير: ابدأ من / ارجع لـ ----
const rtFrom=()=>V.rtsrc==='gps'?null:plcGet(V.rtsrc)||plcHome(),rtBack=()=>V.rtret==='none'?null:plcGet(V.rtret)||plcHome();
const _rteGps21=rteGps;rteGps=function(){const f=rtFrom();if(f){V.rtg=f.c;V.rtgs='plc';if(V.v=='rte')render();return}return _rteGps21()};
const _rteData21=rteData;rteData=function(){const f=rtFrom();if(f){V.rtg=f.c;V.rtgs='plc'}const D=_rteData21(),b=rtBack();D.from=f;D.back=null;
 if(b&&D.rows.length){D.back={p:b,d:hv(D.rows[D.rows.length-1].c,b.c)*1.3};D.tot+=D.back.d}
 if(f||b){const n=8,parts=[];for(let i=0;i<D.rows.length;i+=n)parts.push(D.rows.slice(i,i+n));if(parts.length){if(f)parts[0]=[{c:f.c}].concat(parts[0]);if(b)parts[parts.length-1]=parts[parts.length-1].concat([{c:b.c}])}D.parts=parts}
 return D};
const _rteHtml21=rteHtml;rteHtml=function(){const L=PLC(),f=rtFrom(),b=rtBack();let bar='';
 if(L.length){const D=rteData();bar=`<div class="wcard"><div class="c2"><label>ابدأ من<select id="rtsrc"><option value="gps"${!f?' selected':''}>📍 مكاني الحالي</option>${L.map(x=>`<option value="${x.id}"${f&&f.id==x.id?' selected':''}>${esc(x.ic||'📍')} ${esc(x.n)}</option>`).join('')}</select></label>
  <label>ارجع لـ<select id="rtret"><option value="none"${!b?' selected':''}>— من غير رجوع</option>${L.map(x=>`<option value="${x.id}"${b&&b.id==x.id?' selected':''}>${esc(x.ic||'📍')} ${esc(x.n)}</option>`).join('')}</select></label></div>
  ${D.back?`<small class="hint">↩ الرجوع لـ ${esc(b.n)} ≈ ${km(D.back.d)} (محسوب في الإجمالي)</small>`:''}</div>`}
 else bar=`<div class="wcard"><small class="hint">ضيف «مواقع هامة» (المخزن / الشركة) من المنيو علشان تبدأ منها وترجع لها.</small></div>`;
 return bar+_rteHtml21()};
const _rteText21=rteText;rteText=function(){const D=rteData();let t=_rteText21();if(D.from)t=t.replace('\n','\nالبداية: '+D.from.n+'\n');if(D.back)t+='\n\nالرجوع لـ '+D.back.p.n+' ≈ '+km(D.back.d);return t};
// ---- الموجود والناقص (same size only, stock shared in pharmacy order) ----
function avlData(mo){const st={};WU().forEach(x=>{const k=x.id+'|'+whKey0(x);st[k]=(st[k]||0)+(+x.qty||0)});
 const take=(y,n)=>{const k0=whKey0(y);let left=n;Object.keys(st).forEach(k=>{if(left<=1e-9||k.split('|').slice(1).join('|')!=k0)return;const u=Math.min(left,st[k]);st[k]-=u;left-=u})};
 const P=DB.ph.filter(p=>p.mo==mo&&p.st!='مكتملة').sort(pSort),out=[];
 P.forEach(p=>{const R=[];prepRows(p).forEach(x=>{const r=x.r,need=r.cx?0:Math.max(0,qn(r)-(+r.r||0));if(!need)return;const P2=(whParts(x.t,r,p.sh)||[]).filter(y=>!y.pk&&y.f>0);
   const z=x.t.z(r,x.s);if(!P2.length){R.push({t:x.t,z,lab:'',need,have:0});return}
   P2.forEach(y=>{const have=Math.min(need,Math.floor((whStQ(st,y)+1e-9)/y.f));if(have)take(y,have*y.f);R.push({t:x.t,z,lab:P2.length>1?y.ty+(y.nm?' · '+y.nm:''):'',size:y.size,need,have})})});
  if(R.length)out.push({p,R,need:R.reduce((a,x)=>a+x.need,0),have:R.reduce((a,x)=>a+x.have,0)})});
 return out}
function avlHtml(){const ms=months().reverse(),mo=V.am2||V.pm||MN(),D=avlData(mo),N=D.reduce((a,x)=>a+x.need,0),H=D.reduce((a,x)=>a+x.have,0),miss={};
 D.forEach(o=>o.R.forEach(x=>{if(x.need>x.have){const k=x.t.n+' · '+(x.lab?x.lab+' · ':'')+x.z;miss[k]=(miss[k]||0)+x.need-x.have}}));
 let h=`<div class="wcard"><h2>${ic('layers')}الموجود والناقص</h2><p class="sub">لكل صيدلية لسه ما اكتملتش: اللي فاضل يتجهز، كام منه <b>موجود في المخزن بنفس المقاس</b>، وكام <b>ناقص</b>. المخزن بيتوزع على الصيدليات بالترتيب، فمفيش قطعة بتتحسب مرتين. «📐 مقاس قريب» مش محسوب هنا. الحساب بس، مفيش سحب من المخزن.</p>
 <label>الشهر<select id="avlm">${ms.map(m=>`<option${m==mo?' selected':''}>${m}</option>`).join('')}</select></label>
 <div class="c2"><div class="sumb"><b>${H}</b><small>موجود في المخزن</small></div><div class="sumb"><b>${N-H}</b><small>ناقص</small></div></div>
 <div class="tt"><button data-avlwa="1">${ic('share')}مشاركة الناقص واتساب</button></div></div>`;
 if(!D.length)return h+'<p class="em">كل صيدليات الشهر ده مكتملة أو مفيهاش حاجة فاضلة.</p>';
 D.forEach(o=>{h+=`<details class="wcard" data-id="av_${o.p.id}"${V.op['av_'+o.p.id]?' open':''}><summary><b>${PL(o.p)}</b><small>موجود ${o.have} · ناقص ${o.need-o.have}</small></summary><div class="sc"><table class="ctab"><tr><th>البند</th><th>فاضل</th><th>في المخزن</th><th>ناقص</th></tr>${o.R.map(x=>`<tr><td><b>${esc(x.t.n)}</b>${x.lab?' <small>'+esc(x.lab)+'</small>':''}<br><small>${esc(x.z)}</small></td><td>${x.need}</td><td class="${x.have?'c-rem':''}">${x.have||'—'}</td><td class="${x.need>x.have?'c-exp':''}"><b>${x.need-x.have||'✓'}</b></td></tr>`).join('')}</table></div></details>`});
 const MK=Object.keys(miss);if(MK.length)h+=`<details class="wcard" data-id="av_all"${V.op.av_all?' open':''}><summary><b>الناقص متجمع لكل الشهر</b><small>${MK.length} بند · ${N-H} قطعة</small></summary><div class="sc"><table class="ctab"><tr><th>البند</th><th>ناقص</th></tr>${MK.sort().map(k=>`<tr><td>${esc(k)}</td><td><b>${miss[k]}</b></td></tr>`).join('')}</table></div></details>`;
 return h}
function avlText(){const mo=V.am2||V.pm||MN(),D=avlData(mo),o=['📋 *الناقص بعد خصم المخزن* — شهر '+mo,''];D.forEach(x=>{const M=x.R.filter(y=>y.need>y.have);if(!M.length)return;o.push('*صيدلية '+x.p.no+'*'+(x.p.name?' ('+x.p.name+')':''));M.forEach(y=>o.push('• '+y.t.n+(y.lab?' · '+y.lab:'')+' · '+y.z+' ← '+(y.need-y.have)));o.push('')});return o.join('\n')}
// ---- wiring ----
const _render0_21=render0;render0=function(){const a=$('#app');
 if(V.v=='plc'){cfg();a.innerHTML=hdr(backBtn(),'📍 مواقع هامة')+`<main>${plcHtml()}</main>`;return}
 if(V.v=='avl'){cfg();a.innerHTML=hdr(backBtn(),'الموجود والناقص')+`<main>${avlHtml()}</main>`;return}
 return _render0_21()};
const _v24Click21=v24Click;v24Click=function(d,b){
 if(d.plca){plcAdd();return 1}if(d.plce){plcEdit(d.plce);return 1}
 if(d.plcd){const x=plcGet(d.plcd);if(x&&confirm('حذف «'+x.n+'» من المواقع الهامة؟')){DB.cfg.places=PLC().filter(y=>y!==x);if(String(DB.cfg.rtHome)==String(x.id))DB.cfg.rtHome=(PLC()[0]||{}).id;sv();render()}return 1}
 if(d.plch){DB.cfg.rtHome=+d.plch||d.plch;sv();render();toastT('✓ بقى نقطة البداية والرجوع');return 1}
 if(d.avlwa){const t=avlText();if(navigator.share)navigator.share({text:t}).catch(()=>{});else{try{navigator.clipboard.writeText(t)}catch(e){}window.open('https://wa.me/?text='+encodeURIComponent(t),'_blank')}return 1}
 return _v24Click21(d,b)};
const _v33Change21=v33Change;v33Change=function(x){if(x.id=='rtsrc'){V.rtsrc=x.value;if(x.value=='gps'){V.rtg=null;V.rtgs='';_rteGps21()}else render();return 1}
 if(x.id=='rtret'){V.rtret=x.value;render();return 1}if(x.id=='avlm'){V.am2=x.value;render();return 1}return _v33Change21(x)};
const _syncRoute21=syncRoute;syncRoute=function(q,fn){if(q&&q.kind=='966-places'){plcImpOpen(q);return 1}return _syncRoute21(q,fn)};
const _whImpOpen21=whImpOpen;whImpOpen=function(q,fn){if(q&&q.kind=='966-places')return plcImpOpen(q);return _whImpOpen21(q,fn)};
