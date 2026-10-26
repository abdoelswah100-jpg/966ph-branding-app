"""v1.5 part 2: warehouse add = the same item cards as the pharmacy (types, names with images, sizes by shelf type); thumbnails in the list."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function whaHtml' not in s
rep("const curP=()=>DB.ph.find(x=>x.id==V.p);", "const curP=()=>V.v=='wha'?WHP():DB.ph.find(x=>x.id==V.p);")
JS = r"""// add to the warehouse with the same item cards as a pharmacy: the rows wait here, then 'حفظ في المخزن' splits them in their parts
let WHPO=null;
function WHP(){if(!WHPO)WHPO={id:-7,_wh:1,no:'المخزن',sh:+(DB.cfg.whsh||0),rows:{},an:{},st:'جاري',uid:U().id};return WHPO}
const whaN=()=>Object.values(WHP().rows).reduce((a,r)=>a+r.length,0);
function whaHtml(){const p=WHP(),n=whaN();
 return `<div class="wcard"><h2>${ic('box')}إضافة للمخزن</h2><p class="sub">اختار نوع الدعاية والمسمى زي ما بتضيف في الصيدلية. البنود المركّبة (End gandola و Medicated) بتتقسم لوحدها هيدر وسايد.</p><label>نوع الرفوف<select id="whash">${SH.map((x,i)=>`<option value="${i}"${p.sh==i?' selected':''}>${x}</option>`).join('')}</select></label></div>
 ${TY(p).filter(t=>!WXT.includes(t.id)&&!t.auto).map(t=>card(t,p)).join('')}
 <div class="tt what"><button class="pr big" data-whaok="1"${n?'':' disabled'}>${ic('check')}حفظ في المخزن${n?` (${n} بند)`:''}</button><button data-whax="1">إلغاء</button></div><button class="lnk" data-whadd="1">إضافة صنف بمقاس خاص (كتابة يدوي) ›</button>`}
function whaSave(){const p=WHP();let n=0;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const q=qn(r);whParts(t,r,p.sh).forEach(y=>{whAdd({sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:y.mat,size:y.size},wq(q*y.f),'in','manual','إضافة للمخزن');n++})}));
 WHPO=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT(`✓ اتضاف ${n} صنف للمخزن`)}
"""
rep("function whClick(d,b){", JS + "function whClick(d,b){\n if(d.wha){WHPO=null;goV({v:'wha',op:{},dr:{},q:V.q,wf:V.wf});return 1}\n if(d.whaok){whaSave();return 1}\n if(d.whax){if(whaN()&&!confirm('البنود دي ما اتحفظتش في المخزن. تلغيها؟'))return 1;WHPO=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}")
rep("function whChange(x){", "function whChange(x){\n if(x.id=='whash'){WHP().sh=+x.value;DB.cfg.whsh=+x.value;V.dr={};svq();render();return 1}")
rep("<button class=\"pr\" data-whadd=\"1\">${ic('add')}إضافة</button>", "<button class=\"pr\" data-wha=\"1\">${ic('add')}إضافة</button>")
rep(" if(V.v=='wh'){a.innerHTML=hdr('','المخزن')+`<main>${uStoreBar()}${whHtml()}</main>`;return}", " if(V.v=='wh'){a.innerHTML=hdr('','المخزن')+`<main>${uStoreBar()}${whHtml()}</main>`;return}\n if(V.v=='wha'){a.innerHTML=hdr('<button data-whax=\"1\">‹ المخزن</button>','إضافة للمخزن')+`<main>${whaHtml()}</main>`;return}")
rep("function whPullOffer(p,t,r){", "function whPullOffer(p,t,r){if(!p||p._wh)return;")
rep("wh:'wh',whe:'wh',", "wh:'wh',whe:'wh',wha:'wh',")
rep("const PARENT={ued:'usr',whe:'wh',", "const PARENT={ued:'usr',wha:'wh',whe:'wh',")
# list: thumbnail of the name
rep("return `<div class=\"whc${lo?' lo':''}\"><div class=\"whi\">", "const im=x.nm&&imgOf(x.nm,x.sec);return `<div class=\"whc${lo?' lo':''}\">${im?`<img class=\"whimg\" src=\"${im}\" alt=\"\">`:''}<div class=\"whi\">")
# view-only users cannot add
rep("const STEDIT=['csave',", "const STEDIT=['wha','whaok','csave',")
rep(" if(d.newp&&U().edit=='none'){", " if(v=='wha'&&uStoreRO()&&Object.keys(d).some(k=>PHEDIT.includes(k))){toastT('👁 بيانات مستخدم تاني — للعرض بس');return 1}\n if(d.newp&&U().edit=='none'){")
CSS = "\n.whimg{width:52px;height:52px;object-fit:contain;border-radius:8px;background:#fff;border:1px solid var(--ln);flex:none}.whc .whi{flex:1}.what{position:sticky;bottom:calc(env(safe-area-inset-bottom) + 64px);background:var(--bg);padding:8px 0;z-index:5}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'إضافة للمخزن':'Add to warehouse','‹ المخزن':'‹ Warehouse','اختار نوع الدعاية والمسمى زي ما بتضيف في الصيدلية. البنود المركّبة (End gandola و Medicated) بتتقسم لوحدها هيدر وسايد.':'Choose the ad type and name as in a pharmacy. Composite items (End gandola and Medicated) are split into header and side automatically.','حفظ في المخزن':'Save to warehouse','بند':'items','إضافة صنف بمقاس خاص (كتابة يدوي) ›':'Add an item with a special size (typed) ›','البنود دي ما اتحفظتش في المخزن. تلغيها؟':'These items were not saved to the warehouse. Discard them?','صنف للمخزن':'items to the warehouse'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
