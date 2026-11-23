// ---------- 2.8 (file n2.8.js) ----------
// Backup reminder: every N edits (settings, 0 = off, default 10); a successful Google Drive upload (phone or laptop) resets the counter;
// while Drive is linked and working the reminder does not show (it stays when Drive is not linked or failing).
const bkN=()=>{const v=(DB.cfg.c26||{}).bkn;return v==null?10:+v||0};
const gdOk=()=>{try{const s=gdS();return !!((s.on||s.lw)&&!s.need&&!(s.fails>=3))}catch(e){return false}};
function bkDue(){const n=bkN(),u=DB.cfg.ue||0;if(!n||!u||gdOk())return false;return u%n==0}
const _gdU28=gdU;gdU=function(f){const a=gdS(),l0=a.last,w0=a.lw;const r=_gdU28.apply(this,arguments);
 try{if((r.last&&r.last!=l0)||(r.lw&&r.lw!=w0)){if(DB.cfg.ue){DB.cfg.ue=0;svq()}document.querySelectorAll('.toast.rem').forEach(x=>x.remove());document.querySelectorAll('.hmnb').forEach(x=>x.remove())}}catch(e){}return r};
const _bkRemind28=bkRemind;bkRemind=function(){if(!bkN()||gdOk())return;return _bkRemind28.apply(this,arguments)};
const _render0_28=render0;render0=function(){const o=_render0_28.apply(this,arguments);try{if(V.v=='gen'){const m=$('#app main');if(m&&!m.querySelector('[data-c28]'))m.insertAdjacentHTML('beforeend',`<details class="wcard" data-id="__s_bk"${V.op.__s_bk?' open':''}><summary><b>💾 تذكير النسخة الاحتياطية</b></summary><small class="hint">«عملت كذا تعديل من غير نسخة احتياطية». 0 = مقفول. لما Google Drive متربط وبيرفع، التذكير ما بيطلعش والعداد بيتصفر مع كل رفع.</small><label>ذكّرني كل (تعديل)<input type="number" inputmode="decimal" data-c28="bkn" value="${bkN()}"></label><small class="hint">Google Drive: ${gdOk()?'✅ متربط وشغال':'⚠ مش متربط أو فيه مشكلة — التذكير شغال'}</small></details>`)}}catch(e){}return o};
const _v33Change28=v33Change;v33Change=function(x){if(x.dataset&&x.dataset.c28){const v=Math.max(0,Math.round(+x.value||0));DB.cfg.c26=DB.cfg.c26||{};DB.cfg.c26.bkn=v;svq();toastT(v?'✓ التذكير كل '+v+' تعديل':'✓ التذكير اتقفل');return 1}return _v33Change28(x)};
