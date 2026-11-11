"""v2.6: Pharmacy section (Medicine, blue) in Floor Header and Wall Header for every shelf type, warehouse grouped
(shelf type chips, closed groups by ad type, section colour), pharmacies tab months closed until opened."""
import os, sys, json, base64
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'whGroups' not in s

# ---- Pharmacy section: Medicine
rep("const NM={", "const NM={Pharmacy:['Medicine'],")
rep("{id:'wh',n:'Wall Header',f:[SEC4,", "{id:'wh',n:'Wall Header',f:[sel('sec','القسم',()=>S4.concat(['Pharmacy'])),")
rep("{id:'fh',n:'Floor Header',f:[sel('sec','القسم',()=>S4.concat(['Medicated']))", "{id:'fh',n:'Floor Header',f:[sel('sec','القسم',()=>S4.concat(['Medicated','Pharmacy']))")
# built-in image for the name
BI = os.path.join(R, 'src/bimg.json')
b = json.load(open(BI, encoding='utf-8'))
img = 'data:image/jpeg;base64,' + base64.b64encode(open('/home/claude/work/med.jpg', 'rb').read()).decode()
b['pharmacy|medicine'] = img; b['medicine'] = img
json.dump(b, open(BI, 'w', encoding='utf-8'), ensure_ascii=False)

# ---- pharmacies tab: months closed until opened
rep("open=k==cur||ks.length==1||!!q.mo||!!t;", "open=!!t||!!(V.op&&V.op['mg_'+k]);")
rep("<details class=\"mg\"${open?' open':''}><summary>", "<details class=\"mg\" data-id=\"mg_${k}\"${open?' open':''}><summary>")

# ---- warehouse: shelf chips + closed groups by ad type
i = s.index("<div class=\"c2\"><label>نوع الرفوف<select data-whf=\"sh\">")
j = s.index("</select></label>", i) + len("</select></label>")
s = s[:i] + "${whChips(W0,F)}<div class=\"c2\">" + s[j:]
a = s.index("${L.length?L.map(x=>{const lo=x.min")
e = "'<p class=\"em\">مفيش أصناف. الفائض بيتضاف لوحده لما تنهي صيدلية، أو اضغط «إضافة».</p>'}"
z = s.index(e, a) + len(e)
seg = s[a:z]
body = seg[len("${L.length?L.map(x=>{"):seg.index("}).join(''):'<p")]
s = s[:a] + "${whGroups(L,F)}" + s[z:]
rep("function whHtml(){const W0=WU(),F=V.wf=V.wf||{},q=(F.t||'').trim().toLowerCase();", "function whHtml(){const W0=WU(),F=V.wf=V.wf||{},q=(F.t||'').trim().toLowerCase();if(F.sh===undefined)F.sh=whDefSh(W0);")
card = body.replace('<div class="whc${lo?\' lo\':\'\'}">', '<div class="whc${lo?\' lo\':\'\'}" style="border-inline-start:5px solid ${cl({sec:x.sec})||\'transparent\'}">')
assert card != body
JS = r"""// ---------- v2.6: warehouse grouped ----------
const whShLab=sh=>sh>=0?SH[sh]:'بدون نوع رفوف';
function whDefSh(W){const v=DB.cfg.whfs;if(v!==undefined&&v!==null&&(v===''||W.some(x=>String(x.sh)==String(v))))return v;const c={};W.forEach(x=>c[x.sh]=(c[x.sh]||0)+1);const k=Object.keys(c).sort((a,b)=>c[b]-c[a])[0];return k===undefined?'':+k}
function whChips(W,F){const c={};W.forEach(x=>c[x.sh]=(c[x.sh]||0)+1);const ks=Object.keys(c).map(Number).sort((a,b)=>(a<0)-(b<0)||a-b),on=v=>String(F.sh)===String(v);
 return `<div class="rtchips whch">${ks.map(k=>`<button class="${on(k)?'pr':''}" data-whsh="${k}">${esc(whShLab(k))} <small>${c[k]}</small></button>`).join('')}<button class="${on('')?'pr':''}" data-whsh="all">الكل <small>${W.length}</small></button></div>`}
function whCard(x){""" + card + r"""}
function whGroups(L,F){if(!L.length)return '<p class="em">مفيش أصناف هنا. الفائض بيتضاف لوحده لما تنهي صيدلية، أو اضغط «إضافة».</p>';const all=F.sh===''||F.sh==null,act=!!((F.t||'').trim()||F.low||F.ty||F.sec||F.mat),G=[];
 L.forEach(x=>{const k=(all?whShLab(x.sh)+' · ':'')+x.ty;let g=G.find(y=>y.k==k);if(!g){g={k,a:[]};G.push(g)}g.a.push(x)});G.sort((a,b)=>(a.a[0].sh<0)-(b.a[0].sh<0));
 return G.map(g=>{const id='whg_'+String(g.k).replace(/[^\w؀-ۿ]+/g,'_'),lo=g.a.some(x=>x.min!==''&&x.min!=null&&+x.qty<=+x.min),pc=wq(g.a.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0)),mt=wq(g.a.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0));
  g.a.sort((a,b)=>String(a.sec||'').localeCompare(String(b.sec||''))||String(a.nm||'').localeCompare(String(b.nm||''))||String(a.size||'').localeCompare(String(b.size||''),undefined,{numeric:true}));
  return `<details class="whg" data-id="${id}"${act||V.op[id]?' open':''}><summary><span>${esc(g.k)}</span><small>${g.a.length} صنف${pc?' · '+pc+' قطعة':''}${mt?' · '+mt+' متر':''}${lo?' · <b class="wlo">⚠ رصيد قليل</b>':''}</small></summary>${g.a.map(whCard).join('')}</details>`}).join('')}
function v26Click(d,b){if(d.whsh!==undefined){const v=d.whsh=='all'?'':+d.whsh;V.wf=V.wf||{};V.wf.sh=v;DB.cfg.whfs=v;svq();render();return 1}return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("v21Click(d,b)||v23Click(d,b)||v24Click(d,b)||", "v21Click(d,b)||v23Click(d,b)||v24Click(d,b)||v26Click(d,b)||")
CSS = "\n.whg{margin:8px 0;padding:0;border-radius:var(--rad-sm)}.whg>summary{padding:10px 12px;display:flex;justify-content:space-between;gap:8px}.whg>summary small{color:var(--mu);font-weight:600}.whg .whc{margin:6px 8px}.whg .whimg{width:96px;height:auto;max-height:28px;object-fit:cover}.wlo{color:var(--rd)}.whch button small{opacity:.75}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
rep("VER='v2.5'", "VER='v2.6'")
rep(" changelog:[{version:'v2.5',", " changelog:[{version:'v2.6',date:'2026-11-02',changes:['Floor Header and Wall Header: section Pharmacy (blue) with the name Medicine (الأدوية) and its picture, every shelf type','Warehouse: shelf type chips (remembered), closed groups by ad type with count, totals and low stock mark, section colour on each item','Pharmacies tab: month lists stay closed until opened (open while searching)']},{version:'v2.5',")
EN = {'بدون نوع رفوف':'No shelf type','الكل':'All','رصيد قليل':'Low stock'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
