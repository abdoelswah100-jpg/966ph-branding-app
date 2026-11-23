// ---------- 2.7 (file n2.7.js) ----------
// 1) contacts in groups (الإدارة · مشرفين المناطق · الدواء · الطباعة والتصنيع), add / rename / delete groups, group per contact
// 2) Wall Sticker kind «ثلجي» → deducted from the roll «ثلجي شفاف» at execution
const CG0=['الإدارة','مشرفين المناطق','الدواء','الطباعة والتصنيع'],CGI={'الإدارة':'🏢','مشرفين المناطق':'🗺️','الدواء':'💊','الطباعة والتصنيع':'🖨️'};
const CG=()=>D26().cntg=D26().cntg||CG0.slice();
// ---- 2) «ثلجي»
(function(){const t=T.find(x=>x.id=='ws');if(t){const f=t.f.find(y=>y.k=='kd');if(f){const o=f.o;f.o=function(){const L=(o?o.apply(this,arguments):['لوجو','تخطيط','سي ثرو']).slice();if(!L.includes('ثلجي'))L.push('ثلجي');return L}}}})();
// ---- 1) contact groups
cntHtml=function(){const L=CNT(),G=CG(),other=L.filter(x=>!G.includes(x.g)),card=(x,i)=>`<div class="wcard"><div class="cnt26"><b>${esc(x.n)}</b>${x.t?`<small>${esc(x.t)}</small>`:''}<small dir="ltr">${esc(x.tel||'')}</small></div><div class="locs">${ctB(x.tel,x.wa)}</div>
  <div class="tt"><button data-cnte="${i}">✏️ تعديل</button><button data-cntd="${i}">🗑 حذف</button></div></div>`;
 let h=`<div class="wcard"><h2>📞 أرقام هامة</h2><p class="sub">اتصال أو واتساب بضغطة. كل رقم في مجموعته، وتقدر تنقله من «تعديل».</p></div>`;if(!L.length)h+='<p class="em">مفيش أرقام لسه. ضيف من تحت أو استورد ملف المواقع والأرقام.</p>';
 G.concat(other.length?['__o']:[]).forEach((g,gi)=>{const M=L.map((x,i)=>[x,i]).filter(([x])=>g=='__o'?!G.includes(x.g):x.g==g),id='cg_'+gi;
  h+=`<details class="mg lst" data-id="${id}"${V.op[id]?' open':''}><summary><span>${g=='__o'?'📇 من غير مجموعة':(CGI[g]||'📇')+' '+esc(g)}</span><i>${M.length}</i></summary><div class="mgb">${M.map(([x,i])=>card(x,i)).join('')||'<p class="em">فاضية</p>'}
  ${g=='__o'?'':`<div class="tt"><button class="lnk" data-cgr="${gi}">✏️ اسم المجموعة</button>${gi?`<button class="lnk" data-cgu="${gi}">↑</button>`:''}${!M.length?`<button class="lnk" data-cgd="${gi}">🗑 حذف المجموعة</button>`:''}</div>`}</div></details>`});
 return h+`<div class="wcard"><h3>➕ رقم جديد</h3><label>الاسم<input id="cntn"></label><label>الصفة<input id="cntt" placeholder="مثال: الطباعة"></label><label>المجموعة<select id="cntg">${G.map(g=>`<option>${esc(g)}</option>`).join('')}</select></label><label>الرقم<input id="cntp" inputmode="tel" placeholder="05xxxxxxxx"></label><label>رقم الواتساب (فاضي = نفس الرقم)<input id="cntw" inputmode="tel"></label><div class="tt"><button class="pr" data-cnta="1">إضافة</button><button data-cga="1">➕ مجموعة جديدة</button></div></div>`};
const cgPick=(cur)=>{const G=CG(),v=prompt('المجموعة — اكتب رقمها:\n'+G.map((g,i)=>(i+1)+') '+g).join('\n'),String(Math.max(1,G.indexOf(cur)+1)));if(v==null)return null;const i=+String(v).trim()-1;return G[i]!=null?G[i]:cur};
// imports: keep the group from the file
const _plcImpOpen27=plcImpOpen;plcImpOpen=function(q){const C=Array.isArray(q.contacts)?q.contacts:[];const r=_plcImpOpen27.apply(this,arguments);let ch=0;C.forEach(x=>{const o=CNT().find(y=>y.n==x.n);if(o&&x.g&&o.g!=x.g){o.g=x.g;ch=1}if(x.g&&!CG().includes(x.g)){CG().push(x.g);ch=1}});if(ch){sv();render()}return r};
const _v24Click27=v24Click;v24Click=function(d,b){
 if(d.cnta){const n=($('#cntn').value||'').trim();if(!n)return alert('اكتب الاسم'),1;CNT().push({n,t:($('#cntt').value||'').trim(),g:($('#cntg')||{}).value||CG()[0],tel:($('#cntp').value||'').trim(),wa:($('#cntw').value||'').trim()});sv();render();toastT('✓ اتضاف «'+n+'»');return 1}
 if(d.cnte){const x=CNT()[+d.cnte];if(!x)return 1;const n=prompt('الاسم:',x.n);if(n==null)return 1;const t=prompt('الصفة:',x.t||'');if(t==null)return 1;const g=cgPick(x.g);if(g==null)return 1;const p=prompt('الرقم:',x.tel||'');if(p==null)return 1;const w=prompt('رقم الواتساب (فاضي = نفس الرقم):',x.wa||'');if(w==null)return 1;Object.assign(x,{n:n.trim()||x.n,t:t.trim(),g,tel:p.trim(),wa:w.trim()});sv();render();return 1}
 if(d.cga){const n=(prompt('اسم المجموعة الجديدة:','')||'').trim();if(n&&!CG().includes(n)){CG().push(n);sv();render()}return 1}
 if(d.cgr){const G=CG(),i=+d.cgr,o=G[i],n=(prompt('اسم المجموعة:',o)||'').trim();if(!n||n==o)return 1;if(G.includes(n))return alert('الاسم ده موجود'),1;G[i]=n;CNT().forEach(x=>{if(x.g==o)x.g=n});sv();render();return 1}
 if(d.cgu){mv(CG(),+d.cgu,-1);sv();render();return 1}
 if(d.cgd){const G=CG(),i=+d.cgd;if(confirm('حذف مجموعة «'+G[i]+'»؟')){G.splice(i,1);sv();render()}return 1}
 return _v24Click27(d,b)};
