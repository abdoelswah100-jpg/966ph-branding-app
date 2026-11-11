"""v3.9: ISDIN; new End cap names; «Big/Small» is the size, not the name (rows, stock, templates follow);
Old Turkish End gandola names use the section side; New Arrival gondola; Floor Header «Ukraine wide»; Healthy Drinks;
old-design sides with names + pictures (right / left); Care for Life small 40×100; «رملي» = «ثلجي شفاف»;
import check, catalog export, unregistered item label, no warning between Turkish shelf types."""
import os, sys, json, base64, io
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'v39Fix' not in s
JS, EN = [], {}

# ---------------- built-in pictures: Healthy Drinks, Healthy food (one name now), old-design sides
B = json.load(open(os.path.join(R, 'src/bimg.json'), encoding='utf-8'))
O = json.load(open(os.path.join(R, 'tools/osimg_v39.json'), encoding='utf-8'))
for k, v in O.items(): B['os|' + k] = v
B['healthy drinks'] = open(os.path.join(R, 'tools/healthy_drinks_v39.txt'), encoding='utf-8').read().strip()
B.setdefault('healthy food', B.get('healthy food - s'))
json.dump(B, open(os.path.join(R, 'src/bimg.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# ---------------- names
rep("Ivatherm;Laroch posay", "ISDIN;Ivatherm;Laroch posay")
rep("Healthy food - s;Healthy food Big 77X11.5;", "Healthy food;Healthy Drinks;")
rep("Complete hair & skin · العناية المتكاملة'),\nBaby:L('Baby milk - Small · حليب الطفل;Baby milk - Big · حليب الطفل;Baby Food - small · طعام الطفل;Baby Food - Big · طعام الطفل;Baby Accessories · اكسسوارات الطفل;Baby Bath · مستلزمات حمام الطفل;Baby Bath Big · مستلزمات حمام الطفل;Baby wipes · مناديل الطفل'),",
    "Complete hair & skin · العناية المتكاملة;Shower gel · جل الاستحمام'),\nBaby:L('Baby milk · حليب الطفل;Baby Food · طعام الطفل;Baby Accessories · اكسسوارات الطفل;Baby Bath · مستلزمات حمام الطفل;Baby wipes · مناديل الطفل'),")
rep("Geriatric care Big · العناية بالمسنين", "Geriatric care · العناية بالمسنين")
rep("Medical devices · الأجهزة الطبية;Medicated · مديكيتيد')", "Medical devices · الأجهزة الطبية;Medicated · مديكيتيد;Sports Nutrition · المكملات الرياضية;Sport Supplements · المكملات الغذائية الرياضية;Sports tools · الأدوات الرياضية')")
rep("Hair care · عناية بالشعر')};", "Hair care · عناية بالشعر;Feminine care · العناية النسائية;Bath accessories · مستلزمات حمام')};")
rep(";اطفال;صحة;عناية;جمال');", ";Baby · Baby Food · طعام الطفل;New Arrival · وصل حديثاً;اطفال;صحة;عناية;جمال');")
# Old Turkish: every header that is not one of the 4 section gondolas uses the section side
rep("egSN=(r,sh)=>sh==2&&r&&EGS2[r.nm]?{nm:EGS2[r.nm],sec:''}:null,",
    "EGB4=['اطفال','صحة','عناية','جمال'],EGSEC={Personal:'عناية',Beauty:'جمال',Baby:'اطفال',Health:'صحة'},egSN=(r,sh)=>{if(sh!=2||!r||EGB4.includes(r.nm))return null;if(EGS2[r.nm])return {nm:EGS2[r.nm],sec:''};const m=/^(Personal|Beauty|Baby|Health)\\b/.exec(r.nm||'');return m?{nm:EGSEC[m[1]],sec:''}:null},")
JS.append(r"""// New Arrival gondola: 1 header + 2 sides (one Arabic, one English)
(t=>{if(!t)return;const z0=t.z;t.z=(r,s)=>{const v=z0(r,s);return /^New Arrival/.test(r&&r.nm||'')?v+' · (السايد: 1 عربي + 1 إنجليزي لكل جندولة)':v}})(T.find(x=>x.id=='eg'));
""")

# ---------------- Floor Header «Ukraine wide» (second choice)
rep("'fh.s':['11.5×57'", "'fh.ws':'14.5×56.5','fh.wl':'14.5×76.5','fh.s':['11.5×57'")
rep("sel('sz','الحجم',(r,s)=>two(r)&&s!==2?['صغير','كبير']:['قياسي'])",
    "sel('sz','الحجم',(r,s)=>(two(r)&&s!==2?['صغير','كبير']:['قياسي']).concat(rsh(r,s)===3?['عريض صغير','عريض كبير']:[]))")
rep("const d=r.sz=='كبير'&&s!=2?SZ('fh.l'):SZ('fh.s')[s];",
    "const d=/^عريض/.test(r.sz||'')&&s==3?SZ(r.sz=='عريض كبير'?'fh.wl':'fh.ws'):r.sz=='كبير'&&s!=2?SZ('fh.l'):SZ('fh.s')[s];")

# ---------------- Care for Life small = 40×100; rolls: رملي = ثلجي شفاف
rep("'c4':['صغير 50×100','كبير 50×180']", "'c4':['صغير 40×100','كبير 50×180']")
rep("RLK=['تخطيط','ثلجي شفاف','رملي','أخرى']", "RLK=['تخطيط','ثلجي شفاف','أخرى']")

# ---------------- one-time changes of saved data
rep("if(DB.wh.some(x=>!x.m38))whFix38();", "if(DB.wh.some(x=>!x.m38))whFix38();if(DB.wh.some(x=>!x.m39))whFix39();")
rep("v38Fix()}catch(e){console.error(e)}", "v38Fix()}catch(e){console.error(e)}try{if(DB&&DB.ph&&(DB.ph.some(p=>!p.m39)||(DB.ph.length&&!DB.cfg.m39)||(DB.tp||[]).some(t=>t&&!t.m39)))v39Fix()}catch(e){console.error(e)}")
JS.append(r"""// ---------- v3.9: «Big / Small» is the size, not the name ----------
const N39EC={'Baby milk - Small · حليب الطفل':['Baby milk · حليب الطفل','صغير'],'Baby milk - Big · حليب الطفل':['Baby milk · حليب الطفل','كبير'],'Baby Food - small · طعام الطفل':['Baby Food · طعام الطفل','صغير'],'Baby Food - Big · طعام الطفل':['Baby Food · طعام الطفل','كبير'],'Baby Bath Big · مستلزمات حمام الطفل':['Baby Bath · مستلزمات حمام الطفل','كبير'],'Geriatric care Big · العناية بالمسنين':['Geriatric care · العناية بالمسنين','كبير']};
const N39FH={'Healthy food - s':['Healthy food','صغير'],'Healthy food Big 77X11.5':['Healthy food','كبير']};
const n39=(M,nm)=>{if(M[nm])return M[nm];const k=Object.keys(M).find(a=>nk(a)==nk(nm||''));return k?M[k]:null};
function mig39Rows(R,sh){let c=0;if(!R)return 0;
 (R.ec||[]).forEach(r=>{const m=n39(N39EC,r.nm);if(!m)return;r.nm=m[0];if(!String(r.sz||'').startsWith(m[1])){const v=[].concat(SZ('ec.'+rsh(r,sh))||[]).find(x=>String(x).startsWith(m[1]));if(v)r.sz=v}c++});
 ['fh','wh'].forEach(k=>(R[k]||[]).forEach(r=>{const m=n39(N39FH,r.nm);if(!m)return;r.nm=m[0];if(k=='fh'&&two(r)&&rsh(r,sh)!==2)r.sz=m[1];c++}));
 (R.c4||[]).forEach(r=>{if(String(r.sz||'').includes('50×100')){r.sz='صغير 40×100';c++}});return c}
// a warehouse item / transferred entry
function fix39(x){if(!x)return 0;let c=0;
 if(x.ty=='End cap'){const m=n39(N39EC,x.nm);if(m){x.nm=m[0];c=1}}
 if(x.ty=='Floor Header'||x.ty=='Wall Header'){const m=n39(N39FH,x.nm);if(m){x.nm=m[0];c=1}}
 if(x.ty=='Sticker care 4 life'&&String(x.size).replace(/\s+/g,'')=='50×100'){x.size='40×100';c=1}
 if(x.ty==RLTY&&x.nm=='رملي'){x.nm='ثلجي شفاف';c=1}return c}
function whFix39(){const W=DB.wh;let ch=0;W.forEach(x=>{if(x.m39)return;if(fix39(x))ch=1;x.m39=1});
 if(ch)for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));W.splice(i,1)}}}
function v39Fix(){if(!DB.cfg.m39&&DB.ph.some(p=>!p.m39)){try{const pre=JSON.stringify(dbOut());setTimeout(()=>{try{SNAPS.unshift({at:nowIso(),day:TD(),why:'قبل تحديث v3.9 (Big بقى مقاس)',db:pre});SNAPS=SNAPS.slice(0,5);if(IDB.ok)idbSet('snaps',SNAPS);else localStorage.setItem('ads_snaps',JSON.stringify(SNAPS.slice(0,3)))}catch(e){}},5000)}catch(e){}}
 DB.ph.forEach(p=>{if(p.m39)return;mig39Rows(p.rows,p.sh);
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(e&&fix39(e)){const k2=whKey(e);if(o[k2])o[k2].q=wq(+o[k2].q+(+e.q||0));else o[k2]=e}else if(o[k])o[k].q=wq(+o[k].q+(+e.q||0));else o[k]=e});p.whT=o}
  p.m39=1});
 (DB.tp||[]).forEach(t=>{if(t&&!t.m39){mig39Rows(t.rows,t.sh||0);t.m39=1}});
 if(!DB.cfg.m39){const z=DB.cfg.sz;if(z&&Array.isArray(z.c4))z.c4=z.c4.map(v=>String(v).replace('50×100','40×100'));
  try{let ci=0;Object.keys(N39FH).concat(Object.keys(N39EC)).forEach(a=>{const b=(N39FH[a]||N39EC[a])[0];if(IMG[nk(a)]&&!IMG[nk(b)]){IMG[nk(b)]=IMG[nk(a)];ci=1}});if(ci)imgSave()}catch(e){}
  DB.cfg.m39=1}
 svq()}
const _applyTpl39=applyTpl;applyTpl=function(p,q){_applyTpl39(p,q);mig39Rows(p.rows,p.sh)};
""")

# ---------------- old-design sides: name + picture (right / left)
JS.append(r"""// ---------- v3.9: old-design sides with names and pictures ----------
const OSN={Baby:['Baby accessories','Baby food','Baby milk','Baby toiletries','Baby wipes'],
 Personal:['Bath accessories','Body care','Body lotion','Complete hair & skin care','Deodorant','Feminine care','Hair care','Hair remover','Men care','Oral care','Shaving & Grooming','Shower gel','Soap'],
 Beauty:['Beauty accessories','Complete hair & skin care','Eye care','Hair care','Hair colorants','Skin care','Styling tools'],
 Health:['First aid','Geriatric care','Health & Home care','Healthy food','Medical devices','Medical supports','OTC','Vitamins']};
const osSplit=n=>{const a=String(n||'').split(' · ');return a.length>1?{nm:a.slice(0,-1).join(' · '),sd:a[a.length-1]}:{nm:'',sd:a[0]}},osd=n=>osSplit(n).sd;
const osImgK=(sec,nm,sd)=>BIMG[('os|'+sec+'|'+nm+'|'+sd).toLowerCase()]||null;
const osImg=x=>{const o=osSplit(x&&x.nm);return o.nm?osImgK(x.sec,o.nm,o.sd):null};
const osOk=d=>!!d.nm2&&(OSN[d.sec]||[]).includes(d.nm2),osImgD=d=>['saf','saw','egs'].includes(d.k)&&osOk(d)?osImgK(d.sec,d.nm2,d.sd):null;
""")
rep("x.nm==r.sd).forEach", "osd(x.nm)==r.sd).forEach")
rep("${x.nm&&/^(يمين|يسار)$/.test(x.nm)?' · '+x.nm:''}", "${x.nm?' · '+x.nm:''}")
rep("x.old?(x.pic||OLDIMG[", "x.old?(x.pic||osImg(x)||OLDIMG[")
rep("${k=='egs'?'<p class=\"sub\">سايد الجندولة",
    "${['saf','saw','egs'].includes(k)&&(OSN[d.sec]||[]).length?sel('nm2',[['','— بدون مسمى —']].concat(OSN[d.sec]),osOk(d)?d.nm2:'','المسمى (اختياري — بيظهر بصورته)'):''}\n ${k=='egs'?'<p class=\"sub\">سايد الجندولة")
rep("const im=OLDIMG[k+'|'+d.sec];return im?", "const im=osImgD(d)||OLDIMG[k+'|'+d.sec];return im?")
rep("nm:(d.k=='saw'||d.k=='saf'||d.k=='egs')?d.sd:''", "nm:(d.k=='saw'||d.k=='saf'||d.k=='egs')?(osOk(d)?d.nm2+' · '+d.sd:d.sd):''")

# ---------------- import check + catalog export + unregistered item + Turkish shelves
rep("إضافة صنف بمقاس خاص (كتابة يدوي) ›", "صنف غير مسجل أو بمقاس خاص (كتابة يدوي) ›", 2)
rep("WIMP={L,fn:fn||'ملف'};", "WCK=null;WIMP={L,fn:fn||'ملف'};const NB=L.filter(x=>!whImpOk(x)).length;")
rep("الأصناف بتتضاف على الرصيد الحالي، ومفيش حاجة بتتمسح.</small>",
    "الأصناف بتتضاف على الرصيد الحالي، ومفيش حاجة بتتمسح.${NB?'<br><b class=\"wimpbad\">⚠ '+NB+' صنف مش مطابق لأسماء ومقاسات البرنامج: هيتضافوا، بس مش هيتسحبوا لأي صيدلية. راجعهم قبل الإضافة.</b>':''}</small>")
rep("${e?' · الرصيد دلوقتي '+wq(e.qty):' · صنف جديد'}</small>",
    "${e?' · الرصيد دلوقتي '+wq(e.qty):' · صنف جديد'}${whImpOk(x)?'':'<b class=\"wimpbad\"> · ⚠ مش مطابق — مش هيتسحب</b>'}</small>")
rep("<button class=\"lnk\" data-whimp=\"1\">📥 استيراد أصناف مخزن من ملف ›</button>",
    "<button class=\"lnk\" data-whimp=\"1\">📥 استيراد أصناف مخزن من ملف ›</button><button class=\"lnk\" data-whcat=\"1\">📤 تصدير كتالوج الأصناف (لملفات الجرد) ›</button>")
rep("if(d.whaok){whaSave();return 1}", "if(d.whaok){whaSave();return 1}\n if(d.whcat){whCatExport();return 1}")
rep("if(whKey(x)!=ek)o.push(", "if(whKey(x)!=ek&&!(TK3.includes(x.sh)&&TK3.includes(y.sh)))o.push(")
JS.append(r"""// ---------- v3.9: catalog of every item the app knows (import check + export) ----------
const TK3=[0,1,2];let WCK=null;
function whCatalog(){const SKIP=['mw','xi','od','rsh','stt','egp','nt','xn'],O=new Map();
 const types=T.filter(t=>!t.auto&&!WXT.includes(t.id)&&!['ws','al'].includes(t.id));
 for(let s=0;s<SH.length;s++)for(const t of types){if(t.only&&!t.only.includes(s))continue;const sels=t.f.filter(f=>f.o&&!SKIP.includes(f.k));let n=0;
  const go=(i,d)=>{if(n>8000)return;if(i==sels.length){n++;let P=[];try{P=whParts(t,Object.assign({q:1},d),s)}catch(e){}
    P.forEach(y=>{const o={sh:y.sh,ty:y.ty,nm:y.pk?'':(y.nm||''),sec:y.pk?'':(y.sec||''),mat:y.mat||'',size:String(y.size||'')};O.set(whKey(o),o)});return}
   const f=sels[i];try{if(f.hide&&f.hide(d,s))return go(i+1,d)}catch(e){}let op=[];try{op=f.o(d,s)||[]}catch(e){}if(!op.length)return go(i+1,d);
   op.forEach(v=>{const val=typeof v=='object'&&v?(v.v!=null?v.v:v.n):v;if(val===''||String(val).startsWith('➕'))return;go(i+1,Object.assign({},d,{[f.k]:val}))})};
  go(0,{})}
 return [...O.values()]}
function whCatKeys(){if(!WCK)WCK=new Set(whCatalog().map(whKey));return WCK}
function whImpOk(x){if(!x)return false;if(x.old||x.ty=='أخرى')return true;if(x.ty==RLTY)return RLK.includes(x.nm);const o=x.rol?Object.assign({},x,{mat:String(x.mat||'').replace(ROLM,'')}):x;return whCatKeys().has(whKey(o))}
function whCatExport(){WCK=null;const L=whCatalog().sort((a,b)=>(a.ty+a.sec+a.nm+a.size+a.sh).localeCompare(b.ty+b.sec+b.nm+b.size+b.sh));
 RLK.forEach(k=>L.push({sh:-1,ty:RLTY,nm:k,sec:'',mat:'',size:'عرض 1 م'}));
 const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
 const rows=[['sh','نوع الرفوف','ty','nm','sec','mat','size'].map(q).join(',')].concat(L.map(x=>[x.sh,x.sh>=0?SH[x.sh]:'مشترك لكل الرفوف',x.ty,x.nm,x.sec,x.mat,x.size].map(q).join(',')));
 rows.push('','"تصميم قديم: ty = '+Object.values(OLDT).join(' / ')+' · nm = المسمى · يمين أو يسار · old: 1"','"رولات الستيكر: الكمية بالمتر، unit: متر"');
 out('966-كتالوج-أصناف-المخزن-'+VER+'.csv','﻿'+rows.join('\n'),'text/csv');toastT('✓ اتصدّر '+L.length+' صنف')}
""")
rep("return {sh:shi>=0&&!NOSHT().has(ty_)?shi:-1,ty:ty_,nm:String(z.nm||'').trim(),",
    "return {sh:shi>=0&&!NOSHT().has(ty_)?shi:-1,ty:ty_,nm:(ty_==RLTY&&String(z.nm||'').trim()=='رملي')?'ثلجي شفاف':String(z.nm||'').trim(),")

# ---------------- write
EN.update({'عريض صغير':'Wide small','عريض كبير':'Wide large','المسمى (اختياري — بيظهر بصورته)':'Name (optional — shown with its picture)','— بدون مسمى —':'— no name —','📤 تصدير كتالوج الأصناف (لملفات الجرد) ›':'📤 Export item catalog (for stock-take files) ›','صنف غير مسجل أو بمقاس خاص (كتابة يدوي) ›':'Unregistered or custom-size item (typed) ›'})
CSS = ".wimpbad{color:#B45309}"
rep("// ---------- v1.5 extras ----------", '\n'.join(JS) + "// ---------- v1.5 extras ----------")
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
rep("VER='v3.8'", "VER='v3.9'")
rep(" changelog:[{version:'v3.8',", " changelog:[{version:'v3.9',date:'2026-11-11',changes:['Medicated: ISDIN','End cap: Sports Nutrition, Sport Supplements, Sports tools (Health), Feminine care, Bath accessories (Beauty), Shower gel (Personal)','«Big / Small» is the size, not the name: Baby milk, Baby Food, Baby Bath, Geriatric care (End cap) and Healthy food (Floor / Wall Header); pharmacies, templates and stock follow automatically (restore point first)','End gandola: Baby Food and New Arrival (1 header + 2 sides: Arabic + English); Old Turkish headers other than the 4 section gondolas take their section side','Floor Header Ukraine: second choice «wide» small 14.5×56.5 / large 14.5×76.5','Healthy Drinks (Floor / Wall Header, with picture)','Old-design sides: name + picture for right and left','Care for Life small = 40×100; «رملي» merged into «ثلجي شفاف»','Warehouse import marks items that do not match the app; export of the item catalog; no shelf-type warning between Turkish types with the same size']},{version:'v3.8',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
