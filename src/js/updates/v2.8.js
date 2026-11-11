// ---------- v2.8: visit tracking (background location on the pharmacies' dates) ----------
const VZ={in:0.15,out:0.3,stay:10,h0:7,h1:23},BG=()=>CP('BackgroundGeolocation');
const vOnCfg=()=>DB.cfg.vtrk!==0&&!!BG();
const vIn=(p,d)=>p.ds&&p.de?(p.ds<=d&&d<=p.de):p.ds?p.ds==d:p.de?p.de==d:false;
const VK={br:'تنفيذ دعاية',mn:'صيانة',no:'مش النهارده'};
function vPlan(){return DB.cfg.vplan=DB.cfg.vplan||{it:{}}}
// pharmacies followed today: in their dates (unless "not today"), or kept by the morning answer for more days
function vActive(d){d=d||TD();const it=vPlan().it;return DB.ph.filter(p=>{if(p.st=='مكتملة'||!locC(p))return false;const a=it[p.id];if(a&&a.k=='no'&&a.d==d)return false;return vIn(p,d)||(a&&a.k!='no'&&a.u>=d)})}
const vAskL=d=>{d=d||TD();const it=vPlan().it;return DB.ph.filter(p=>p.st!='مكتملة'&&locC(p)&&vIn(p,d)&&(()=>{const a=it[p.id];return !a||(a.k=='no'?a.d!=d:a.u<d)})())};
function vAskHtml(){if(!vOnCfg())return '';const L=vAskL();if(!L.length)return '';const d=TD(),rem=p=>Math.max(1,p.de?Math.round((new Date(p.de)-new Date(d))/864e5)+1:1);
 return `<div class="wcard vask"><h3>📍 زيارات النهارده</h3><p class="sub">هتروح الصيدليات دي النهارده؟ التطبيق هيتابع وصولك ومشيك، وينبهك لو مشيت والتنفيذ ناقص.</p>${L.map(p=>`<div class="vrow"><b>${esc(p.no)}</b><small>${esc(p.name||'')}</small><select data-vk="${p.id}">${Object.entries(VK).map(([k,t])=>`<option value="${k}"${(isMnt(p)?'mn':'br')==k?' selected':''}>${t}</option>`).join('')}</select><label>أيام<input type="number" inputmode="numeric" min="1" max="30" data-vdn="${p.id}" value="${rem(p)}"></label></div>`).join('')}<div class="tt"><button class="pr" data-vgo="1">ابدأ المتابعة</button></div></div>`}
let VW=null,VWB=0;
async function vStart(){const B=BG();if(!B||VW||VWB||!vOnCfg())return;const h=new Date().getHours();if(h<VZ.h0||h>=VZ.h1||!vActive().length)return;VWB=1;
 try{VW=await B.addWatcher({backgroundTitle:'966Ph: متابعة الزيارات',backgroundMessage:'بيتابع وصولك ومشيك من صيدليات النهارده',requestPermissions:true,stale:false,distanceFilter:40},(loc,err)=>{if(err){if(err.code==='NOT_AUTHORIZED')DB.cfg.vden=1;return}DB.cfg.vden=0;vOn(loc)})}catch(e){console.warn(e);VW=null}VWB=0;if(V&&V.v=='ntf')render()}
async function vStop(){const B=BG(),id=VW;VW=null;if(B&&id){try{await B.removeWatcher({id})}catch(e){}}if(V&&V.v=='ntf')render()}
function vOn(loc){if(!loc)return;const now=Date.now(),h=new Date().getHours(),d=TD(),A=vActive(d);if(h<VZ.h0||h>=VZ.h1||!A.length){vStop();return}
 const c=[loc.latitude,loc.longitude],S=DB.cfg.vst=DB.cfg.vst||{};let ch=0;DB.cfg.vlast={c,at:nowIso()};
 A.forEach(p=>{const km=hv(c,locC(p)),s=S[p.id]=S[p.id]||{};
  if(km<=VZ.in){if(!s.t0){s.t0=now;ch=1}s.last=now;if(!s.arr&&now-s.t0>=VZ.stay*6e4){s.arr=s.t0;(p.vst=p.vst||[]).push({in:new Date(s.t0).toISOString(),out:null});ch=1}}
  else if(km>=VZ.out&&(s.t0||s.arr)){if(s.arr){const v=(p.vst||[]).slice(-1)[0];if(v&&!v.out)v.out=new Date(s.last||now).toISOString();const L=nqLines(p,'x');if(L.length)ntfNowSend('⚠ مشيت من صيدلية '+p.no,'التنفيذ لسه ناقص '+L.length+' بند ما اتعلّمش عليه. ارجع أو كمّل بكرة.',{pid:p.id})}delete S[p.id];ch=1}});
 if(ch)svq()}
const hm=t=>{const x=new Date(t);return z2n(x.getHours())+':'+z2n(x.getMinutes())};
function vstHtml(p){const L=(p.vst||[]).slice(-6);if(!L.length)return '';return `<div class="ph vst"><small>🕒 الزيارات: ${L.map(v=>{const d=new Date(v.in),m=v.out?Math.round((new Date(v.out)-d)/6e4):null;return `${z2n(d.getDate())}-${z2n(d.getMonth()+1)} ${hm(v.in)} ← ${v.out?hm(v.out)+' ('+Math.floor(m/60)+':'+z2n(m%60)+')':'لسه هناك'}`}).join(' · ')}</small></div>`}
function vCfgHtml(){const nat=!!BG(),on=DB.cfg.vtrk!==0,A=vActive();return `<div class="wcard"><h3>📍 متابعة الزيارات بالموقع</h3><label class="chk"><input type="checkbox" id="vtrk"${on?' checked':''}${nat?'':' disabled'}> تنبيه لو مشيت من الصيدلية والتنفيذ ناقص</label><small class="hint">بتشتغل في الخلفية في أيام تواريخ الصيدليات بس (من ${VZ.h0} الصبح لـ ${VZ.h1-12} بالليل). الوصول بيتسجل لو فضلت ${VZ.stay} دقايق على بعد أقل من ${VZ.in*1000} متر، والتنبيه لما تبعد ${VZ.out*1000} متر. الصيدليات من غير موقع مش بتتابع.</small>${nat?`<div class="stb"><small>الحالة:</small><b class="${VW?'ok':''}">${VW?'شغالة ('+A.length+' صيدلية النهارده)':A.length?'واقفة':'مفيش صيدليات النهارده'}</b></div>${DB.cfg.vden?'<div class="ywarn">⚠ إذن الموقع مرفوض. اسمح للتطبيق بالموقع من إعدادات الموبايل.</div>':''}<div class="tt">${VW?'<button data-vstop="1">إيقاف النهارده</button>':A.length&&on?'<button class="pr" data-vstart="1">تشغيل دلوقتي</button>':''}</div>`:'<div class="ywarn">بتشتغل من تطبيق الموبايل بس.</div>'}</div>`}
function v28Click(d,b){
 if(d.vgo){const it=vPlan().it,td=TD();document.querySelectorAll('[data-vk]').forEach(sx=>{const id=sx.dataset.vk,k=sx.value,n=Math.max(1,Math.min(30,+((document.querySelector(`[data-vdn="${id}"]`)||{}).value||1))),u=new Date(+new Date(td)+(n-1)*864e5).toISOString().slice(0,10);it[id]={k,d:td,u}});svq();render();if(vActive().length){vStart();toastT('📍 المتابعة شغالة لـ '+vActive().length+' صيدلية')}else toastT('تمام، مفيش متابعة النهارده');return 1}
 if(d.vstart){vStart();return 1}
 if(d.vstop){const it=vPlan().it,td=TD();vActive().forEach(p=>{it[p.id]={k:'no',d:td,u:td}});svq();vStop();toastT('اتوقفت متابعة النهارده');return 1}
 return 0}
function v28Change(x){if(x.id=='vtrk'){DB.cfg.vtrk=x.checked?1:0;svq();if(x.checked)vStart();else vStop();ntfLater();render();return 1}if(x.dataset&&(x.dataset.vk||x.dataset.vdn))return 1;return 0}
