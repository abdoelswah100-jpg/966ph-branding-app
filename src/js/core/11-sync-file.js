const cntRows=p=>Object.values(p.rows||{}).reduce((a,v)=>a+(Array.isArray(v)?v.length:0),0);
const SKIND='966-sync';
const syncPayload=()=>({kind:SKIND,v:1,ver:VER,at:nowIso(),device:DB.cfg.dev||'',ph:DB.ph,del:DB.del||{}});
const pendingN=()=>DB.ph.filter(p=>(p.modAt||BASE)>(DB.cfg.lx||BASE)).length;
const syncName=()=>{const n=nowIso();return '966-sync-'+n.slice(0,10)+'-'+n.slice(11,16).replace(':','')+'-'+(DB.cfg.dev||'device').replace(/[^\w\u0600-\u06FF-]+/g,'')+'.json'};
function snap(why){try{SNAPS.unshift({at:nowIso(),day:TD(),why,db:JSON.stringify(dbOut())});SNAPS=SNAPS.slice(0,5);if(IDB.ok)idbSet('snaps',SNAPS);else localStorage.setItem('ads_snaps',JSON.stringify(SNAPS.slice(0,3)))}catch(e){}}
function snaps(){return SNAPS}
// same content? (ignores key order and the empty lists a screen creates)
const syncN=v=>Array.isArray(v)?v.map(syncN):v&&typeof v=='object'?Object.keys(v).sort().reduce((o,k)=>{const x=v[k];if(!(Array.isArray(x)&&!x.length))o[k]=syncN(x);return o},{}):v;
const syncEq=(a,b)=>JSON.stringify(syncN(a))===JSON.stringify(syncN(b));
function mergeSync(inc){const res={added:0,updated:0,same:0,deleted:0,conflicts:[]},since=[DB.cfg.ls||BASE,DB.cfg.lx||BASE].sort().pop();
 const find=z=>DB.ph.find(x=>x.id==z.id)||DB.ph.find(x=>String(x.no)==String(z.no)&&x.mo==z.mo);
 Object.keys(inc.del||{}).forEach(id=>{const t=inc.del[id],l=DB.ph.find(x=>x.id==id);if(l&&(l.modAt||BASE)<=t){DB.ph=DB.ph.filter(x=>x!==l);res.deleted++}if(!(DB.del[id]>t))DB.del[id]=t});
 (inc.ph||[]).forEach(z=>{z=JSON.parse(JSON.stringify(z));mig(z);z.modAt=z.modAt||BASE;const td=DB.del[z.id];if(td&&td>=z.modAt)return;
  const l=find(z);if(!l){delete DB.del[z.id];DB.ph.push(z);res.added++;return}
  if(syncEq(l,z)){res.same++;return}
  const lm=l.modAt||BASE,zm=z.modAt,lc=lm>since,zc=zm>since;
  if(lc&&zc||lm===zm){res.conflicts.push({l,z});return}
  if(zc||(!lc&&zm>lm)){z.id=l.id;DB.ph[DB.ph.indexOf(l)]=z;res.updated++}else res.same++});
 return res}
// versions restarted at 1.1 after 3.9 (2026-11-11): the new 1.x line counts after every 2.x / 3.x (old 1.x files are long gone)
const verN=v=>{const a=String(v||'v0').replace(/^v/,'').split('.').map(Number),n=a.reduce((s,x,i)=>s+(x||0)/Math.pow(100,i),0);return a[0]==1?100+n:n};
function doSync(inc){if(verN(inc.ver)<verN(VER))alert('⚠ ملف المزامنة ده من إصدار أقدم ('+(inc.ver||'قبل v1.3')+'). الجهاز التاني لازم يتحدّث لـ '+VER+' علشان البيانات تفضل متطابقة والمراجعة ما تبانش قديمة.');snap('قبل دمج ملف مزامنة من '+(inc.device||'جهاز غير مسمى'));const r=mergeSync(inc);uApply();DB.cfg.ls=nowIso();DB.cfg.lsd=inc.device||'';sv();V={v:'sync',op:{},dr:{},q:V.q,sy:{res:r,conf:r.conflicts.slice(),dev:inc.device||''}};render()}
const fd=x=>{if(!x)return '';const d=new Date(x);if(isNaN(d))return esc(String(x).slice(0,16));return d.getFullYear()+'-'+z2(d.getMonth()+1)+'-'+z2(d.getDate())+' '+z2(d.getHours())+':'+z2(d.getMinutes())};
function syncHtml(){const S=V.sy,sn=snaps();
 let h=`<label>اسم هذا الجهاز (مثال: لاب توب / موبايل)<input id="sydev" value="${esc(DB.cfg.dev||'')}"></label><div class="ph"><small>آخر استيراد: ${DB.cfg.ls?fd(DB.cfg.ls)+(DB.cfg.lsd?' من '+esc(DB.cfg.lsd):''):'لم يتم بعد'}<br>آخر تصدير: ${DB.cfg.lx?fd(DB.cfg.lx):'لم يتم بعد'}<br>صيدليات معدلة منذ آخر تصدير: ${pendingN()}</small></div><div class="tt"><button class="pr" id="syex">تصدير ملف المزامنة</button></div><label>استيراد ودمج ملف مزامنة أو ملف من اللاب توب (966-laptop / 966-day)<input type="file" id="syncin" accept=".json,application/json"></label>`;
 if(S){const r=S.res;h+=`<div class="ph"><b>نتيجة الدمج${S.dev?' (ملف من '+esc(S.dev)+')':''}</b><small>أضيفت ${r.added} · حُدّثت ${r.updated} · بدون تغيير ${r.same} · محذوفة ${r.deleted} · تعارضات ${r.conflicts.length}</small></div>`;
  h+=S.conf.map((c,i)=>`<div class="alr"><b>تعارض: ${PL(c.l)}${c.l.name?' · '+esc(c.l.name):''}</b><div class="sc"><table><tr><th></th><th>عندك</th><th>الواردة</th></tr><tr><td>آخر تعديل</td><td>${fd(c.l.modAt)}</td><td>${fd(c.z.modAt)}</td></tr><tr><td>الحالة</td><td>${esc(c.l.st)}</td><td>${esc(c.z.st)}</td></tr><tr><td>عدد البنود</td><td>${cntRows(c.l)}</td><td>${cntRows(c.z)}</td></tr><tr><td>تمت مراجعتها</td><td>${c.l.rev?'نعم':'لا'}</td><td>${c.z.rev?'نعم':'لا'}</td></tr></table></div><div class="tt"><button data-cfk="${i}:m">احتفظ بنسختي</button><button data-cfk="${i}:i">استخدم الواردة</button><button data-cfk="${i}:b">احتفظ بالاثنين</button></div></div>`).join('')}
 h+=`<div class="ph"><small><b>الخطوات:</b><br>1) قبل ما تبدأ شغل على جهاز: استورد آخر ملف مزامنة من الجهاز الآخر.<br>2) بعد ما تخلص: اضغط تصدير ملف المزامنة واحفظه في Drive أو OneDrive أو أرسله لنفسك.<br>3) ملف المزامنة يحمل الصيدليات وحذفها فقط. الأسعار والإعدادات والعروض والفواتير تنتقل بالنسخة الاحتياطية الكاملة.<br>4) تجنّب تعديل نفس الصيدلية على الجهازين قبل المزامنة. وقبل أي دمج بتتحفظ نسخة تلقائية تقدر ترجع لها.</small></div>`;
 if(sn.length)h+='<h3>نسخ تلقائية قبل الاستيراد</h3>'+sn.map((x,i)=>`<div class="ph"><small>${fd(x.at)} — ${esc(x.why)}</small><button data-snr="${i}">استرجاع</button></div>`).join('');
 return h}
function syncBanner(){if(!DB.ph.length)return'';const n=pendingN(),d=dayDiff(DB.cfg.ls),x=dayDiff(DB.cfg.lx),stale=n>0&&(!DB.cfg.lx||x>=1),old=DB.cfg.ls&&d>=3,warn=stale||old;
 return `<div class="${warn?'alr':'ph'}"><small>المزامنة: آخر استيراد ${DB.cfg.ls?fd(DB.cfg.ls)+(DB.cfg.lsd?' من '+esc(DB.cfg.lsd):''):'لم يتم بعد'} · ${n} صيدلية معدلة ولم تُصدَّر</small>${stale?'<div><b>فيه صيدليات معدلة لم تُصدَّر '+(DB.cfg.lx?'منذ '+x+' يوم':'لسه')+'. صدّر ملف المزامنة للجهاز التاني.</b></div>':''}${old?'<div><b>آخر استيراد من الجهاز الآخر منذ '+d+' يوم. تأكد إنك شغال على آخر نسخة.</b></div>':''}<div class="tt"><button data-sync="1">المزامنة بين الأجهزة</button></div></div>`}
