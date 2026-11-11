"""v1.8 part 1: Pharmacy on Side Acrylic Shelves Wall (no name), wall sticker totals per section · kind,
new type ستيكر خارجي / Sticker outdoor (name, size, count, margin sentence, material Sticker outdoor + Laminate)."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert "id:'so'" not in s
# Pharmacy on wall shelves
rep("{id:'saw',n:'Side Acrylic Shelves Wall',only:[2],f:[SEC4,", "{id:'saw',n:'Side Acrylic Shelves Wall',only:[2],f:[sel('sec','القسم',()=>S4.concat(['Pharmacy'])),")
rep(" z:r=>`${r.sec} · ${SN[r.sec]} · ${r.sz} سم · ${r.sd} · ${SZ('mt.sa')}`},\n{id:'saf'", " z:r=>`${r.sec}${SN[r.sec]?' · '+SN[r.sec]:''} · ${r.sz} سم · ${r.sd} · ${SZ('mt.sa')}`},\n{id:'saf'")
# Sticker outdoor
rep("{id:'c4',n:'Sticker care 4 life',", "{id:'so',n:'ستيكر خارجي',f:[sel('nm','المسمى',()=>SON),Object.assign({k:'nx',l:'اكتب المسمى'},{hide:d=>d.nm!='أخرى'}),num('h','الطول (سم)'),num('w','العرض (سم)'),Q,Object.assign(num('mg','المسافة من الأطراف (سم) — اختياري'),{opt:1})],\n z:r=>`${son(r)} · ${r.h}×${r.w} سم · ${SZ('mt.so')} · ⚠ مراعاة ${r.mg?'مسافة '+r.mg+' سم':'المسافة المناسبة'} بين الكلام والشعارات والأطراف${r.nt?' · '+r.nt:''}`},\n{id:'c4',n:'Sticker care 4 life',")
rep("const WSS=S7.concat(['Thank you - نشكركم']);", "const WSS=S7.concat(['Thank you - نشكركم']);\nconst SON=['أرباحي','طلباتك','جهاز الخدمة الذاتية','أخرى'],son=r=>r.nm=='أخرى'?(r.nx||'أخرى'):(r.nm||'');")
rep("'mt.ws':'ستيكر','mt.wh':'ستيكر',", "'mt.ws':'ستيكر','mt.so':'Sticker outdoor + Laminate','mt.wh':'ستيكر',")
rep("h('الخامات');[['mt.ws','Wall Sticker'],", "h('الخامات');[['mt.ws','Wall Sticker'],['mt.so','ستيكر خارجي (Sticker outdoor)'],")
rep("const WXT=['ws','al','ab','dc'];", "const WXT=['ws','al','ab','dc','so'];")
rep("const nm=r.nm||r.it||r.kd||'',sz=t.id=='ws'", "const nm=t.id=='so'?son(r):r.nm||r.it||r.kd||'',sz=t.id=='ws'")
# wall sticker: totals per section · kind (summary table + chips under the items)
rep("function totRows(rs,t){", "function totRowsK(rs,t){const g={};let tot=0;rs.forEach(r=>{const v=t.m(r),k=t.id=='ws'&&r.kd?r.sec+' · '+r.kd:r.sec;g[k]=(g[k]||0)+v;tot+=v});return{g,tot}}\nconst colK=k=>COL[k]||COL[String(k).split(' · ')[0]]||'#999';\nfunction totRows(rs,t){")
rep("function totBox(rs,t){if(!rs.length)return'';const x=totRows(rs,t);return `<div class=\"tt\">`+Object.keys(x.g).map(k=>`<span style=\"${bgc(COL[k]||'#999')}\">",
    "function totBox(rs,t){if(!rs.length)return'';const x=totRowsK(rs,t);return `<div class=\"tt\">`+Object.keys(x.g).map(k=>`<span style=\"${bgc(colK(k))}\">")
rep("if(t.m){const x=totRows(rs,t);tot+=x.tot;tb+=`<div class=\"sc\"><table><tr><th>القسم</th><th>إجمالي الأمتار (م²)</th></tr>`+Object.keys(x.g).map(k=>`<tr><td style=\"${bgc(COL[k]||'#999')};font-weight:700\">",
    "if(t.m){const x=totRowsK(rs,t);tot+=x.tot;tb+=`<div class=\"sc\"><table><tr><th>القسم</th><th>إجمالي الأمتار (م²)</th></tr>`+Object.keys(x.g).map(k=>`<tr><td style=\"${bgc(colK(k))};font-weight:700\">")
EN = {'ستيكر خارجي':'Sticker outdoor','أرباحي':'Arbahi','طلباتك':'Talabatak','جهاز الخدمة الذاتية':'Self-service kiosk','أخرى':'Other','اكتب المسمى':'Type the name','المسافة من الأطراف (سم) — اختياري':'Margin from the edges (cm) — optional','مراعاة':'Keep','المسافة المناسبة':'a suitable margin','بين الكلام والشعارات والأطراف':'between the text / logos and the edges','ستيكر خارجي (Sticker outdoor)':'Sticker outdoor'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
