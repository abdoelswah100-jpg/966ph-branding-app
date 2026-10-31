"""v1.9 part 2: letters max width (tahtit width - 10), Floor Header on Old Turkish (sticker + acrylic / sticker only),
old design (pharmacy + item, photos for the printer), curve note for side acrylic, Acrylic boards status shown as 'تصنيع + تركيب' in light red."""
import os, sys, json, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'FHM' not in s
# helpers (early, next to rsh)
rep("const RSHT=['fh','wh','ec','eg','md'],RSAME=", "const FHM=['ستيكر + تصنيع أكريليك','ستيكر فقط'],fhmOf=r=>FHM.includes(r&&r.fhm)?r.fhm:FHM[0],stD=x=>x=='تصنيع وتركيب'?'تصنيع + تركيب':x||'',ODK=['wh','fh','ec','eg','md'],isOld=(p,r)=>!!(p&&p.dz=='قديم')||!!(r&&r.od=='قديم'),CURVE='الجهة في السايد أكريليك (يمين / يسار) = اتجاه الانحناء';\nconst RSHT=['fh','wh','ec','eg','md'],RSAME=")
# ---- A. letters: tahtit width -> max sentence width
rep("{id:'al',n:'Acrylic letters 8 mm',f:[SECAL,num('h','ارتفاع التخطيط (سم)'),", "{id:'al',n:'Acrylic letters 8 mm',f:[SECAL,num('h','ارتفاع التخطيط (سم)'),Object.assign(num('tw','عرض التخطيط (سم) — بيتاخد من Wall Sticker'),{opt:1}),")
rep("· ${r.sz||'غير محدد'} · ${r.ar||'غير محدد'} · ${SZ('mt.al')}${r.nt?' · '+r.nt:''}`},", "· ${r.sz||'غير محدد'} · ${r.ar||'غير محدد'} · ${SZ('mt.al')}${alMax(r)?' · ⚠ عرض جملة الحروف لا يزيد عن '+alMax(r)+' سم':''}${r.nt?' · '+r.nt:''}`},")
rep("function alPrep(d){", "const alMax=r=>+r.tw>10?Math.round((+r.tw-10)*10)/10:0;\nfunction alTw(p,sec){let m=0;((p&&p.rows.ws)||[]).forEach(r=>{if(r.kd=='تخطيط'&&r.sec==sec&&+r.w>m)m=+r.w});return m||''}\nfunction alPrep(d){if(d.tw===undefined||d.tw===''||d._twa){const v=alTw(curP(),d.sec);if(v!==''){d.tw=v;d._twa=1}else if(d._twa){d.tw='';}}")
rep("document.addEventListener('input',e=>{const x=e.target;\n if(x.dataset.t=='al'&&(x.dataset.k=='lh'||x.dataset.k=='w')){", "document.addEventListener('input',e=>{const x=e.target;\n if(x.dataset.t=='al'&&x.dataset.k=='tw'&&V.dr.al){V.dr.al.tw=x.value;delete V.dr.al._twa;return}\n if(x.dataset.t=='al'&&(x.dataset.k=='lh'||x.dataset.k=='w')){")
rep("if(t.id=='al'){tb+=`<h3>${t.n}</h3><div class=\"sc\"><table><tr><th>القسم</th><th>ارتفاع الحروف (سم)</th><th>مقاس التخطيط (سم)</th><th>الحجم</th><th>الترتيب</th><th>العدد</th><th>ملاحظات</th></tr>`+rs.map(r=>{const c=cl(r)||'#999';return `<tr><td style=\"${bgc(c)};font-weight:700\">${esc(r.sec)}</td><td>${esc(r.lh||'—')}</td><td>${esc(r.h||'—')}×${esc(r.w||'—')}</td><td>${esc(r.sz||'—')}</td><td>${esc(r.ar||'—')}</td><td>${r.q==null?'1':r.q}</td><td>${esc(r.nt||'')}</td></tr>`}).join('')+'</table></div>'+ttot(t,rs);continue;}",
    "if(t.id=='al'){const mx=rs.some(alMax);tb+=`<h3>${t.n}</h3><div class=\"sc\"><table><tr><th>القسم</th><th>ارتفاع الحروف (سم)</th><th>مقاس التخطيط (سم)</th>${mx?'<th>أقصى عرض للحروف (سم)</th>':''}<th>الحجم</th><th>الترتيب</th><th>العدد</th><th>ملاحظات</th></tr>`+rs.map(r=>{const c=cl(r)||'#999';return `<tr><td style=\"${bgc(c)};font-weight:700\">${esc(r.sec)}</td><td>${esc(r.lh||'—')}</td><td>${esc(r.h||'—')}×${esc(r.tw||r.w||'—')}</td>${mx?`<td class=\"almx\">${alMax(r)?alMax(r):'—'}</td>`:''}<td>${esc(r.sz||'—')}</td><td>${esc(r.ar||'—')}</td><td>${r.q==null?'1':r.q}</td><td>${esc(r.nt||'')}</td></tr>`}).join('')+'</table></div>'+rs.filter(alMax).map(r=>`<div class=\"almxs\">⚠ عرض جملة حروف ${esc(r.sec)} لا يزيد عن <b>${alMax(r)} سم</b> (عرض التخطيط ${esc(r.tw)} − 10)</div>`).join('')+ttot(t,rs);continue;}")
# ---- B. Floor Header on Old Turkish
rep("{id:'fh',n:'Floor Header',f:[sel('sec','القسم',()=>S4.concat(['Medicated'])),NMF,sel('sz','الحجم',r=>two(r)?['صغير','كبير']:['قياسي']),Q],\n z:(r,s)=>{const d=r.sz=='كبير'?SZ('fh.l'):SZ('fh.s')[s];return `${r.sec} · ${r.nm} · ${d} سم · ${SZ('mt.fh')[s]}`}},",
    "{id:'fh',n:'Floor Header',f:[sel('sec','القسم',()=>S4.concat(['Medicated'])),NMF,sel('sz','الحجم',r=>two(r)?['صغير','كبير']:['قياسي']),Object.assign(sel('fhm','المطلوب',()=>FHM),{hide:(d,s)=>rsh(d,s)!==2}),Q],\n z:(r,s)=>{const d=r.sz=='كبير'?SZ('fh.l'):SZ('fh.s')[s];return `${r.sec} · ${r.nm} · ${d} سم · ${s==2?fhmOf(r):SZ('mt.fh')[s]}`}},")
rep("'mt.ws':'ستيكر','mt.so':", "'mt.fhx':['ستيكر + تصنيع أكريليك','ستيكر فقط'],'mt.ws':'ستيكر','mt.so':")
rep("material=SZ('mt.fh')[rsh(r,s)]", "material=rsh(r,s)===2?fhmOf(r):SZ('mt.fh')[rsh(r,s)]")
rep("const fm=' · '+SZ('mt.fh')[rsh(r,s)];", "const fm=' · '+(rsh(r,s)===2?fhmOf(r):SZ('mt.fh')[rsh(r,s)]);")
rep("function WU(){DB.wh=DB.wh||[];DB.wlog=DB.wlog||[];return DB.wh}", "function WU(){DB.wh=DB.wh||[];DB.wlog=DB.wlog||[];DB.wh.forEach(x=>{if(!x.m19){if(x.ty=='Floor Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19=1}});return DB.wh}")
# execution: what to do for the Old Turkish Floor Header
rep("<td>${esc(dt)}${rshT(x.r,x.s)}</td><td><b>${q}</b></td>", "<td>${esc(dt)}${rshT(x.r,x.s)}${x.t.id=='fh'&&rsh(x.r,x.s)===2?`<small class=\"rshc fhx\">${k=='x'?(fhmOf(x.r)==FHM[1]?'تركيب ستيكر فقط':'تصنيع أكريليك + تركيب ستيكر'):fhmOf(x.r)}</small>`:''}${isOld(x.r&&p,x.r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}</td><td><b>${q}</b></td>")
# ---- C. old design: pharmacy + item
for t in ['wh','ec','md']:
    pass
rep("T.forEach(t=>{if(RSHT.includes(t.id)){", "T.forEach(t=>{if(ODK.includes(t.id)&&t.f)t.f.push(Object.assign(sel('od','التصميم',()=>['جديد','قديم']),{hide:()=>{const p=curP();return !!(p&&(p.dz=='قديم'||p._wh))}}));if(RSHT.includes(t.id)){")
s = s.replace("${r.nm&&imgOf(r.nm,r.sec)?`<img class=\"rwimg\" src=\"${imgOf(r.nm,r.sec)}\" alt=\"\">`:''}${esc(t.z(r,s))}${rshT(r,s)}", "${r.nm&&!isOld(p,r)&&imgOf(r.nm,r.sec)?`<img class=\"rwimg\" src=\"${imgOf(r.nm,r.sec)}\" alt=\"\">`:''}${esc(t.z(r,s))}${rshT(r,s)}${isOld(p,r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}")
i = s.index('function sumHtml(p){'); j = s.index('\nfunction ', i + 5); b = s[i:j]
n = b.count("imgOf(r.nm,r.sec)")
b = b.replace("imgOf(r.nm,r.sec)", "(isOld(p,r)?null:imgOf(r.nm,r.sec))")
b = b.replace("${rshT(r,s)}${tg(r)}</td><td>${+r.q||0}</td><td>${2*(+r.q||0)}</td>", "${rshT(r,s)}${tg(r)}${isOld(p,r)?' <small class=\"rshc odt\">تصميم قديم</small>':''}</td><td>${+r.q||0}</td><td>${2*(+r.q||0)}</td>")
s = s[:i] + b + s[j:]
print('summary images guarded', n)
rep("<label>اسم المشرف<input id=\"csup\" value=", "<label>التصميم<select id=\"cdz\">${['جديد','قديم'].map(x=>`<option${(p.dz||'جديد')==x?' selected':''}>${x}</option>`).join('')}</select></label><label>اسم المشرف<input id=\"csup\" value=")
rep("const phoList=(p,sl)=>((p&&p.pho||{})[sl]||[]);", "const phoList=(p,sl)=>((p&&p.pho||{})[sl]||[]);\nconst odNeed=p=>!!(p&&(p.dz=='قديم'||ODK.some(k=>((p.rows||{})[k]||[]).some(r=>r.od=='قديم'))));")
rep("return `<details class=\"pinfo\" data-id=\"__pho\"${V.op.__pho?' open':''}><summary>${ic('img')} صور قبل / بعد${n?` (${n})`:''}</summary>${blk('b','صور قبل')}${blk('a','صور بعد')}",
    "return `<details class=\"pinfo\" data-id=\"__pho\"${V.op.__pho?' open':''}><summary>${ic('img')} صور قبل / بعد${n?` (${n})`:''}</summary>${odNeed(p)||phoList(p,'o').length?blk('o','صور التصميم القديم (بتظهر في ملخص الطباعة)'):''}${blk('b','صور قبل')}${blk('a','صور بعد')}")
rep("for(const sl of ['b','a'])", "for(const sl of ['b','a','o'])")
# summary: banner + photos (data URLs so the PDF has them)
rep("+metaHtml(p)+tSum(p)+rlReqHtml(p)+tb", "+metaHtml(p)+odBanner(p)+tSum(p)+rlReqHtml(p)+tb+curveNote(p)+odPhotos(p)")
JS = r"""// old design: banner + photos in the print summary; curve note for side acrylic
const odBanner=p=>p.dz=='قديم'?'<div class="sxn odz">⚠ الصيدلية دي تصميم قديم — يطبع حسب الطلب (شوف صور التصميم القديم في الآخر)</div>':odNeed(p)?'<div class="sxn odz">⚠ فيه بنود تصميم قديم (مكتوب جنبها) — تطبع حسب الطلب</div>':'';
const odPhotos=p=>{const L=phoList(p,'o');return L.length?`<h3>صور التصميم القديم</h3><div class="odg">${L.map(x=>`<img data-phod="${phoKey(p.id,'o',x.k)}" alt="">`).join('')}</div>`:''};
async function odFill(){for(const im of document.querySelectorAll('img[data-phod]')){if(im.getAttribute('src'))continue;const b=await idbGet(im.dataset.phod);if(!b)continue;const u=URL.createObjectURL(b),d=await shrink(u,900);URL.revokeObjectURL(u);if(d)im.src=d}}
const hasCurve=p=>((p.rows.saw||[]).length+(p.rows.saf||[]).length)>0||((p.rows.eg||[]).some(r=>egPK(r,p.sh)));
const curveNote=p=>hasCurve(p)?`<div class="ph curve"><small>ℹ ${CURVE}</small></div>`:'';
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("${!c&&!m?rlBox(p)+sxBox(p,whNet(p)):''}", "${!c&&!m?rlBox(p)+sxBox(p,whNet(p)):''}")
i = s.index("${!c&&!m?rlBox(p)+sxBox(p,whNet(p)):''}"); j = s.index(";fixT();return}", i)
s = s[:j] + ";fixT();odFill();return}" + s[j+len(";fixT();return}"):]
rep(" o.push(...rlReqTxt(p));return o.join('\\n')}", " o.push(...rlReqTxt(p));if(p.dz=='قديم')o.splice(1,0,'⚠ تصميم قديم — يطبع حسب الطلب');if(hasCurve(p))o.push('','ℹ '+CURVE);return o.join('\\n')}")
# ---- D. curve hints in the form
rep("value=\"${esc(d[f.k]??'')}\">`)+`</label>`).join('')}", "value=\"${esc(d[f.k]??'')}\">`)+`</label>`+(f.hint?`<small class=\"hint fhint\">${f.hint}</small>`:'')).join('')}")
HINT = "يمين = الانحناء ناحية اليمين · يسار = الانحناء ناحية الشمال"
rep("sel('sd','الجهة',()=>['يمين','يسار']),Q],\n z:r=>`${r.sec}${SN[r.sec]?", "Object.assign(sel('sd','الجهة',()=>['يمين','يسار']),{hint:'" + HINT + "'}),Q],\n z:r=>`${r.sec}${SN[r.sec]?")
rep("{id:'saf',n:'Side Acrylic Shelves Floor',f:[SEC4,sel('sz','المقاس',(r,s)=>SZ('saf.'+s)),sel('sd','الجهة',()=>['يمين','يسار']),Q],", "{id:'saf',n:'Side Acrylic Shelves Floor',f:[SEC4,sel('sz','المقاس',(r,s)=>SZ('saf.'+s)),Object.assign(sel('sd','الجهة',()=>['يمين','يسار']),{hint:'" + HINT + "'}),Q],")
rep("{opt:1,z0:1,hide:(d,s)=>rsh(d,s)!==2||(EGPO.includes(d.egp)?d.egp:EGPO[0])===EGPO[1]}))", "{opt:1,z0:1,hint:sd=='L'?'" + HINT + "':'',hide:(d,s)=>rsh(d,s)!==2||(EGPO.includes(d.egp)?d.egp:EGPO[0])===EGPO[1]}))")
rep("function x15Change(x){", "function x15Change(x){\n if(x.id=='cdz'){const q=curP();if(q){if(x.value=='قديم')q.dz='قديم';else delete q.dz;q.modAt=nowIso();sv();render()}return 1}")
rep("const PHEDIT=[", "const PHEDIT=['cdz',")
rep("const sg=y=>JSON.stringify(t.f.filter(f=>f.k!='q'&&f.k!='nt').map(f=>f.k=='rsh'&&(!y[f.k]||y[f.k]==RSAME)?'':y[f.k]));", "const sg=y=>JSON.stringify(t.f.filter(f=>f.k!='q'&&f.k!='nt').map(f=>f.k=='rsh'&&(!y[f.k]||y[f.k]==RSAME)?'':f.k=='od'?(y.od=='قديم'?'قديم':''):f.k=='fhm'?(rsh(y,p.sh)===2?fhmOf(y):''):f.k=='tw'||f.k=='pR'||f.k=='pL'?String(y[f.k]??''):y[f.k]));")
# shortages: curve note, Acrylic boards status
rep("  o.push({...b,nm,pt:'',sz,mat,sd:r.sd||'',q,v,d})});return o}", "  o.push({...b,nm,pt:'',sz,mat,sd:r.sd||'',stt:t.id=='ab'?stD(r.stt):'',q,v,d})});return o}")
rep("const hn=g.a.some(nqHasNm),hs=g.a.some(x=>x.sd);", "const hn=g.a.some(nqHasNm),hs=g.a.some(x=>x.sd),ht=g.a.some(x=>x.stt);")
rep("${hs?'<th>الجهة</th>':''}<th>الخامة</th>", "${hs?'<th>الجهة</th>':''}${ht?'<th>الحالة</th>':''}<th>الخامة</th>")
rep("${hs?`<td><b>${esc(x.sd||'—')}</b></td>`:''}", "${hs?`<td><b>${esc(x.sd||'—')}</b></td>`:''}${ht?`<td style=\"background:${x.stt=='تركيب فقط'?'#DCEBFA':'#FAD4D4'};color:#111;font-weight:700\">${esc(x.stt||'—')}</td>`:''}")
i = s.index('function nqHtml'); j = s.index('\n return h}', i)
s = s[:j] + "\n if(A.some(x=>x.L.some(y=>y.sd)))h+=`<div class=\"ph curve\"><small>ℹ ${CURVE}</small></div>`;" + s[j:]
rep("x.sd,x.mat&&x.mat!='—'?x.mat:''].filter(Boolean).join(' · ')+' ×'+x.d);tot+=x.d", "x.sd,x.stt,x.mat&&x.mat!='—'?x.mat:''].filter(Boolean).join(' · ')+' ×'+x.d);tot+=x.d")
rep("o.push('',tot?'الإجمالي: '+tot+' قطعة':'✅ مفيش نواقص');", "if(P.some(p=>nqLines(p,k).some(y=>y.sd)))o.push('','ℹ '+CURVE);o.push('',tot?'الإجمالي: '+tot+' قطعة':'✅ مفيش نواقص');")
# Acrylic boards: shown as 'تصنيع + تركيب', light red
rep("z:r=>`${r.it} · ${ABV(r.it).join(' · ')} · ${r.stt}`}];", "z:r=>`${r.it} · ${ABV(r.it).join(' · ')} · ${stD(r.stt)}`}];")
rep("<td style=\"background:${r.stt=='تركيب فقط'?'#DCEBFA':'#FDE9C9'};color:#111;font-weight:700\">${esc(r.stt||'')}</td>", "<td style=\"background:${r.stt=='تركيب فقط'?'#DCEBFA':'#FAD4D4'};color:#111;font-weight:700\">${esc(stD(r.stt))}</td>")
CSS = "\n.almx{font-weight:800;color:#8B0000}.almxs{background:#FFF4D6;border:1px solid #F2B705;color:#5A4300;border-radius:8px;padding:5px 8px;margin:4px 0;font-weight:700}.odz{background:#FDE2E2;border-color:#C7313B;color:#8B0000}.rshc.odt{background:#FDE2E2;color:#8B0000;border-color:#E8A0A0}.rshc.fhx{background:#E6F4EA;color:#1E7B45;border-color:#A8D5B5}.odg{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}.odg img{width:100%;border-radius:6px;border:1px solid var(--ln)}.ph.curve small{color:var(--tx);font-weight:700}.fhint{display:block;margin:-6px 0 8px;color:var(--mu);font-size:11.5px}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'عرض التخطيط (سم) — بيتاخد من Wall Sticker':'Tahtit width (cm) — taken from Wall Sticker','أقصى عرض للحروف (سم)':'Max letters width (cm)','عرض جملة الحروف لا يزيد عن':'Letters sentence width not more than','عرض جملة حروف':'Letters sentence width of','لا يزيد عن':'not more than','عرض التخطيط':'tahtit width','ستيكر + تصنيع أكريليك':'Sticker + acrylic','ستيكر فقط':'Sticker only','تركيب ستيكر فقط':'Install sticker only','تصنيع أكريليك + تركيب ستيكر':'Make acrylic + install sticker','التصميم':'Design','جديد':'New','قديم':'Old','تصميم قديم':'Old design','صور التصميم القديم (بتظهر في ملخص الطباعة)':'Old design photos (shown in the print summary)','صور التصميم القديم':'Old design photos','⚠ الصيدلية دي تصميم قديم — يطبع حسب الطلب (شوف صور التصميم القديم في الآخر)':'⚠ This pharmacy is an old design — print as requested (see the old design photos at the end)','⚠ فيه بنود تصميم قديم (مكتوب جنبها) — تطبع حسب الطلب':'⚠ Some items are old design (marked) — print as requested','الجهة في السايد أكريليك (يمين / يسار) = اتجاه الانحناء':'Side acrylic direction (right / left) = direction of the curve','يمين = الانحناء ناحية اليمين · يسار = الانحناء ناحية الشمال':'Right = curve to the right · Left = curve to the left','تصنيع + تركيب':'Make + install','الحالة':'Status'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
