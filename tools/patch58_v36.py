"""v3.6: old stock (actual size, «مقاس قديم لوحده», material, side and section for the old gandola side, offered only to old-design
pharmacies / rows, built-in photos of the old sides + 📷 per item), «رملي» sticker roll, item-level merge of custody and
maintenance between devices (+ warning when the warehouse changed on both), backups screen tidy-up, English for the Drive texts."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'gdItemMerge' not in s
JS, CSS, EN = [], [], {}
OLDIMG = json.load(open(os.path.join(R, 'tools/oldimg_v36.json')))

# =====================================================================
# 1. old stock
# =====================================================================
rep("function whoD(){const d=V.wo=V.wo||{k:'saw',sh:2,sec:'Health',sd:'يمين',nm:'',sz:'',q:1};if(d.k=='saw')d.sh=2;if(d.k=='egs'||d.k=='beg')d.sh=0;const S=whoSz(d.k,d.sh);if(!S.includes(d.sz))d.sz=S[0]||'';if(d.k=='egs'&&!EG.includes(d.nm))d.nm=EG[0]||'';return d}",
    "function whoD(){const d=V.wo=V.wo||{k:'saf',sh:0,sec:'Health',sd:'يمين',nm:'',sz:'',q:1,mt:'أكريليك + ستيكر',real:'',solo:''};if(d.k=='saw')d.sh=2;if(d.k=='egs'||d.k=='beg')d.sh=0;const S=whoSz(d.k,d.sh);if(d.sz!=WOSOLO&&!S.includes(d.sz))d.sz=S[0]||'';if(d.k=='egs'&&!S4.includes(d.sec))d.sec='Baby';return d}")
rep(" ${k=='saw'?sel('sec',S4.concat(['Pharmacy']),d.sec,'القسم'):k=='saf'?sel('sec',S4,d.sec,'القسم'):''}\n ${k=='egs'?sel('nm',EG,d.nm,'القسم · المسمى'):''}\n ${sel('sz',S,d.sz,'المقاس (سم)')}\n ${k=='saw'||k=='saf'?sel('sd',['يمين','يسار'],d.sd,'الجهة'):''}",
    " ${k=='saw'?sel('sec',S4.concat(['Pharmacy']),d.sec,'القسم'):k=='saf'||k=='egs'?sel('sec',S4,d.sec,'القسم'):''}\n ${k=='egs'?'<p class=\"sub\">سايد الجندولة بيمشي للجندولة الصغيرة والكبيرة (الفرق في الهيدر بس).</p>':''}\n ${k[0]=='b'?'':sel('mt',['أكريليك + ستيكر','ستيكر فقط'],d.mt,'الخامة')}\n ${sel('sz',S.concat(k[0]=='b'?[]:[[WOSOLO,'مقاس قديم لوحده (اكتبه) — مش بيتعرض على الصيدليات']]),d.sz,'المقاس (سم)')}\n ${d.sz==WOSOLO?`<label>المقاس القديم (سم)<input data-wo=\"solo\" placeholder=\"مثلاً 35×125\" value=\"${esc(d.solo||'')}\"></label>`:`<label>المقاس الفعلي (اختياري)<input data-wo=\"real\" placeholder=\"مثلاً 118.5×30\" value=\"${esc(d.real||'')}\"><small class=\"autot\">لو المقاس الحقيقي مختلف شوية عن المقاس اللي فوق. بيظهر جنبه في المخزن.</small></label>`}\n ${k=='saw'||k=='saf'||k=='egs'?sel('sd',['يمين','يسار'],d.sd,'الجهة (اتجاه الانحناء)'):''}\n ${(()=>{const im=OLDIMG[k+'|'+d.sec];return im?`<div class=\"woim\"><img src=\"${im}\" alt=\"\"><small>صورة التصميم القديم لـ ${esc(d.sec)} (بتظهر على الصنف لحد ما تضيف صورته بـ 📷)</small></div>`:''})()}")
rep(" const o={sh:d.sh,ty:OLDT[d.k],nm:d.k=='egs'?d.nm:(d.k=='saw'||d.k=='saf')?d.sd:'',sec:(d.k=='saw'||d.k=='saf')?d.sec:'',mat:d.k[0]=='b'?'أكريليك فاضي':'أكريليك + ستيكر',size:d.sz,old:1};\n const x=whAdd(o,q,'in','manual','مخزون قديم');x.old=1;",
    " const solo=d.sz==WOSOLO,sz=solo?String(d.solo||'').trim().replace(/\\s*[x×*]\\s*/i,'×'):d.sz;if(!sz)return alert('اكتب المقاس القديم');\n const o={sh:d.sh,ty:OLDT[d.k],nm:(d.k=='saw'||d.k=='saf'||d.k=='egs')?d.sd:'',sec:(d.k=='saw'||d.k=='saf'||d.k=='egs')?d.sec:'',mat:d.k[0]=='b'?'أكريليك فاضي':d.mt||'أكريليك + ستيكر',size:sz,old:1};\n const real=solo?'':String(d.real||'').trim().replace(/\\s*[x×*]\\s*/i,'×');\n const x=whAdd(o,q,'in','manual','مخزون قديم'+(real?' (فعلي '+real+')':''));x.old=1;if(solo)x.solo=1;if(real)x.real=real;d.real='';d.solo='';")
rep("toastT(`✓ اتضاف ${q} · ${OLDL[d.k]} · ${d.sz} (الرصيد ${wq(x.qty)})`)}", "toastT(`✓ اتضاف ${q} · ${OLDL[d.k]} · ${sz}${real?' (فعلي '+real+')':''} (الرصيد ${wq(x.qty)})`)}")
# offered only to old-design pharmacies / rows; gandola side by section; never the «solo» sizes
rep("function whOldOpts(p,t,r){if(!p||p._wh||p._rc)return [];const W=WU().filter(x=>x.old&&+x.qty>=1);",
    "function whOldOpts(p,t,r){if(!p||p._wh||p._rc||!isOld(p,r))return [];const W=WU().filter(x=>x.old&&!x.solo&&+x.qty>=1);")
rep("const add=(x,n,k,lab)=>{n=Math.min(n,Math.floor(+x.qty));if(n>0)O.push({k,id:x.id,n,txt:`🕰 ${n} ${lab} (في المخزن ${wq(x.qty)})`})};",
    "const add=(x,n,k,lab)=>{n=Math.min(n,Math.floor(+x.qty));if(n>0)O.push({k,id:x.id,n,txt:`🕰 ${n} ${lab}${x.mat&&x.mat!='أكريليك فاضي'?' · '+x.mat:''}${x.real?' · فعلي '+x.real:''}${x.nm&&/^(يمين|يسار)$/.test(x.nm)?' · '+x.nm:''} (في المخزن ${wq(x.qty)})`})};")
rep("W.filter(x=>(x.ty==OLDT.egs&&x.nm==r.nm)||x.ty==OLDT.beg)", "W.filter(x=>(x.ty==OLDT.egs&&(x.nm==r.nm||(x.sec&&x.sec==egSec(r.nm))))||x.ty==OLDT.beg)")
# warehouse card: photo (own 📷 or built-in old design picture), actual size
rep("function whCard(x){const lo=x.min!==''&&x.min!=null&&+x.qty<=+x.min;const im=x.nm&&imgOf(x.nm,x.sec);",
    "function whCard(x){const lo=x.min!==''&&x.min!=null&&+x.qty<=+x.min;const im=x.old?(x.pic||OLDIMG[Object.keys(OLDT).find(k=>OLDT[k]==x.ty)+'|'+x.sec]||null):x.nm&&imgOf(x.nm,x.sec);")
rep("<small>${esc(x.size||'—')} · ${esc(x.mat||'—')} ${x.ty==RLTY?", "<small>${esc(x.size||'—')}${x.real?' <span class=\"rshc\">فعلي '+esc(x.real)+'</span>':''}${x.solo?' <span class=\"rshc\">مقاس قديم لوحده</span>':''} · ${esc(x.mat||'—')} ${x.ty==RLTY?")
rep("<button class=\"np\" data-whed=\"${x.id}\">⋮</button></div></div></div>`}",
    "<button class=\"np\" data-whed=\"${x.id}\">⋮</button>${x.old?`<button class=\"np\" data-whpic=\"${x.id}\" title=\"صورة\">📷</button>`:''}</div></div></div>`}")
JS.append("// ---------- v3.6: old stock ----------\nconst WOSOLO='__solo';\nconst OLDIMG=" + json.dumps(OLDIMG) + ";\n" + r"""const egSec=n=>String(n||'').split(' · ')[0].replace(/\s*\(.*\)\s*/,'').trim();
let WPIC=null;
function whPicPick(id){WPIC=id;let i=document.getElementById('whpicin');if(!i){i=document.createElement('input');i.type='file';i.accept='image/*';i.id='whpicin';i.hidden=true;document.body.appendChild(i);
  i.addEventListener('change',async()=>{const f=i.files&&i.files[0];i.value='';if(!f||!WPIC)return;const x=WU().find(y=>y.id==WPIC);if(!x)return;const u=URL.createObjectURL(f);const d=await shrink(u,360);URL.revokeObjectURL(u);if(!d)return alert('ما قدرتش أقرا الصورة');x.pic=d;sv();render();toastT('✓ اتحفظت صورة الصنف')})}
 i.click()}
""")
rep("function v34WhClick(d,b){", "function v34WhClick(d,b){\n if(d.whpic){const x=WU().find(y=>y.id==d.whpic);if(x&&x.pic&&!confirm('الصنف ليه صورة. تغيّرها؟ (إلغاء = تمسحها)')){delete x.pic;sv();render();return 1}whPicPick(d.whpic);return 1}")
CSS.append(".woim{display:flex;gap:10px;align-items:center;background:var(--c2);border:1px solid var(--ln);border-radius:12px;padding:8px}.woim img{width:56px;border-radius:6px;box-shadow:var(--sh)}.woim small{color:var(--mu)}.whc .whimg{object-fit:cover}")
# sticker roll: «رملي»
rep("RLK=['تخطيط','ثلجي شفاف','أخرى']", "RLK=['تخطيط','ثلجي شفاف','رملي','أخرى']")
EN.update({'رملي':'Sandblast (frosted)','الخامة':'Material','ستيكر فقط':'Sticker only','المقاس الفعلي (اختياري)':'Actual size (optional)','المقاس القديم (سم)':'Old size (cm)','مقاس قديم لوحده':'Separate old size','فعلي':'actual','الجهة (اتجاه الانحناء)':'Side (curve direction)'})

# =====================================================================
# 2. merge custody and maintenance by item between devices; warning for the warehouse
# =====================================================================
rep("if(d.cdel){if(!confirm('تمسح الفاتورة دي؟'))return 1;const M=cMo();M.items=M.items.filter(x=>x.id!=V.ce.id);",
    "if(d.cdel){if(!confirm('تمسح الفاتورة دي؟'))return 1;const M=cMo();M.items=M.items.filter(x=>x.id!=V.ce.id);(M.xd=M.xd||{})[V.ce.id]=nowIso();")
rep("if(d.mdel){if(!confirm('تمسح البند ده؟'))return 1;const C=MU();C.items=C.items.filter(x=>x.id!=V.me.id);",
    "if(d.mdel){if(!confirm('تمسح البند ده؟'))return 1;const C=MU();C.items=C.items.filter(x=>x.id!=V.me.id);(C.xd=C.xd||{})[V.me.id]=nowIso();")
rep("confirm('حذف المبلغ المستلم '+f2(M.dep[i].amt)+'؟')){M.dep.splice(i,1);", "confirm('حذف المبلغ المستلم '+f2(M.dep[i].amt)+'؟')){(M.dd=M.dd||{})[M.dep[i].id]=nowIso();M.dep.splice(i,1);")
rep("UST.forEach(k=>{const inc=src(k);if(inc===undefined||gdEmpty(inc))return;if(gdEmpty(DB[k])||(qa[k]||'')>(la[k]||'')){",
    "const lp=gdS().pt||'';UST.forEach(k=>{const inc=src(k);if(inc===undefined||gdEmpty(inc))return;\n  if((k=='cust'||k=='mnt')&&!gdEmpty(DB[k])){const nw=(qa[k]||'')>(la[k]||''),b0=JSON.stringify(DB[k]);gdItemMerge(k,DB[k],JSON.parse(JSON.stringify(inc)),nw);if(JSON.stringify(DB[k])!=b0)res.sec.push(k);if(nw)la[k]=qa[k];return}\n  if((k=='wh'||k=='wlog')&&lp&&(qa[k]||'')>(la[k]||'')&&(la[k]||'')>lp&&!syncEq(DB[k],inc))res.whc=1;\n  if(gdEmpty(DB[k])||(qa[k]||'')>(la[k]||'')){")
rep("const r=gdMerge(q,why);if(EXR.imgs||EXR.files||EXR.photos)await restoreExtras(EXR);render();return gdResTxt(r)}",
    "const r=gdMerge(q,why);if(EXR.imgs||EXR.files||EXR.photos)await restoreExtras(EXR);render();if(r.whc)setTimeout(()=>alert('⚠ المخزن اتعدّل على الجهازين قبل ما يتزامنوا، واتاخدت نسخة الجهاز التاني (الأحدث). راجع أرصدة المخزن، ولو فيه حركة ناقصة سجلها تاني أو رجّع من «نقاط الاستعادة».'),300);return gdResTxt(r)}")
JS.append(r"""// ---------- v3.6: item-level merge (custody months / maintenance) ----------
function gdUnion(L,I,nw,del){const m=new Map();(L||[]).forEach(x=>{if(!del[x.id])m.set(String(x.id),x)});(I||[]).forEach(x=>{if(del[x.id])return;const k=String(x.id);if(!m.has(k)||nw)m.set(k,x)});return [...m.values()]}
function gdDel(a,b){const o=Object.assign({},a||{});Object.keys(b||{}).forEach(k=>{if(!(o[k]>b[k]))o[k]=b[k]});return o}
function gdItemMerge(k,L,I,nw){
 if(k=='cust'){L.m=L.m||{};const IM=I.m||{};Object.keys(IM).forEach(mk=>{const a=L.m[mk],b=IM[mk];if(!a){L.m[mk]=b;return}
   const xd=gdDel(a.xd,b.xd),dd=gdDel(a.dd,b.dd);const it=gdUnion(a.items,b.items,nw,xd),dp=gdUnion(a.dep,b.dep,nw,dd);
   if(nw)['open','why','dl','reo','xat'].forEach(f=>{if(b[f]===undefined)delete a[f];else a[f]=b[f]});
   a.items=cSort(it);if(dp.length)a.dep=dp.sort((x,y)=>String(x.dt).localeCompare(String(y.dt)));else delete a.dep;if(Object.keys(xd).length)a.xd=xd;if(Object.keys(dd).length)a.dd=dd});
  Object.keys(L.m).forEach(mk=>{const a=L.m[mk];if(a.xd)a.items=(a.items||[]).filter(x=>!a.xd[x.id])});
  if(nw){if(I.cfg)L.cfg=I.cfg;if(I.mem)L.mem=Object.assign({},L.mem||{},I.mem)}return}
 if(k=='mnt'){const xd=gdDel(L.xd,I.xd);L.items=gdUnion(L.items,I.items,nw,xd);if(Object.keys(xd).length)L.xd=xd;if(nw&&I.cfg)L.cfg=I.cfg}}
""")

# =====================================================================
# 3. backups screen: Drive status once; English for the Drive texts
# =====================================================================
rep("<summary>☁️ Google Drive ${gdLine()}</summary>${gdHtml()}</details>", "<summary>☁️ Google Drive <small class=\"gdsm\">${esc(gdStat()||'')}</small></summary>${gdHtml()}</details>")
CSS.append(".gdbk>summary .gdsm{flex-basis:100%;color:var(--mu);font-weight:600;font-size:12px}")
EN.update({'اتأكد إن الإعداد ده':'make sure this setting','احفظ':'Save','افتح التطبيق':'Open the app','التطبيق بشكل دائم، فممكن يمسحها':'the app permanently, so it may delete it','التطبيق بيقرا':'The app reads','اللينك':'the link','المتصفح ما وافقش يحفظ':'The browser did not agree to keep','الموبايل':'the phone','الموبايل أول ما تفتحه ويدمجه، وبيكتب':'the phone as soon as you open it and merges it, and writes','الموبايل مابيشوفش':'The phone does not see','الموبايل هيظهر':'The phone will show','بعد أول رفع':'after the first upload','بيانات الموبايل':'phone data','بيانات اللاب توب':'laptop data','اقرا آخر بيانات':'Read the latest data of','دلوقتي':'now','آخر دمج تلقائي:':'Last automatic merge:','الطريقة القديمة: فولدر Drive for desktop':'Old way: Drive for desktop folder','فاتح التطبيق من اللينك.':'The app is open from the link.','ربط حساب Google':'Connect Google account','ارفع دلوقتي':'Upload now','متزامن':'In sync','آخر قراءة من':'last read from'})

# =====================================================================
# write
# =====================================================================
rep("// ---------- v1.5 extras ----------", '\n'.join(JS) + "// ---------- v1.5 extras ----------")
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}\n" + ''.join(CSS) + "\n")
rep("VER='v3.5'", "VER='v3.6'")
rep(" changelog:[{version:'v3.5',", " changelog:[{version:'v3.6',date:'2026-11-10',changes:['Old stock: material (acrylic + sticker / sticker only), optional actual size, «separate old size» that is never offered, side and section for the old gandola side (fits small and big gandolas), offered only to old-design pharmacies/rows, built-in photos of the old sides and 📷 per item','Sticker roll type «رملي»','Sync: custody (invoices, received amounts) and maintenance merge item by item between the devices with deletions kept; warning when the warehouse changed on both devices','Backups screen shows the Drive status once; English for the Drive texts']},{version:'v3.5',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
