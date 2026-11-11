"""v2.5: photo limits from the settings (before 8, after 14 by default), second layout attachment, sharing before / after /
both with a text carrying the pharmacy number."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'phMax' not in s

# ---- photo limits
rep("const PHMAX=8,PHU={};", "const PHMAX=8,PHU={};\nconst phMax=sl=>{const v=Math.round(+(sl=='a'?DB.cfg.phA:sl=='b'?DB.cfg.phB:0)||0);return v>0?Math.min(60,v):sl=='a'?14:8};")
rep("<small>${L.length} / ${PHMAX}</small>", "<small>${L.length} / ${phMax(sl)}</small>")
rep("${L.length<PHMAX?`<div class=\"tt\"><button data-phcam=\"${sl}\">", "${L.length<phMax(sl)?`<div class=\"tt\"><button data-phcam=\"${sl}\">")
rep("'<small class=\"hint\">وصلت للحد الأقصى (8 صور).</small>'", "`<small class=\"hint\">وصلت للحد الأقصى (${phMax(sl)} صور).</small>`")
rep("room=PHMAX-L0.length;if(room<=0)return alert('الحد الأقصى 8 صور في كل خانة');const F=[...files];if(F.length>room)alert('هيتضاف أول '+room+' صور بس (الحد الأقصى 8)');",
    "room=phMax(sl)-L0.length;if(room<=0)return alert('الحد الأقصى '+phMax(sl)+' صور في الخانة دي (من الإعدادات العامة)');const F=[...files];if(F.length>room)alert('هيتضاف أول '+room+' صور بس (الحد الأقصى '+phMax(sl)+')');")
rep("<div class=\"wcard\"><h2>${ic('gear')}الإعدادات العامة</h2>", "<div class=\"wcard\"><h2>${ic('gear')}الإعدادات العامة</h2><div class=\"c2\"><label>أقصى عدد صور قبل لكل صيدلية<input type=\"number\" inputmode=\"numeric\" min=\"1\" max=\"60\" id=\"cfphb\" value=\"${phMax('b')}\"></label><label>أقصى عدد صور بعد لكل صيدلية<input type=\"number\" inputmode=\"numeric\" min=\"1\" max=\"60\" id=\"cfpha\" value=\"${phMax('a')}\"></label></div>")
# ---- share before / after / both with a text
rep("${n?`<button data-phshare=\"1\">${ic('share')}مشاركة الصور (واتساب)</button>`:''}",
    "${n?`<div class=\"tt\">${phoList(p,'b').length?`<button data-phshare=\"b\">${ic('share')}صور قبل</button>`:''}${phoList(p,'a').length?`<button data-phshare=\"a\">${ic('share')}صور بعد</button>`:''}${phoList(p,'b').length&&phoList(p,'a').length?`<button class=\"pr\" data-phshare=\"ba\">${ic('share')}قبل + بعد</button>`:''}</div>`:''}")
rep("if(d.phshare){const p=curP();if(p)phoShare(p);return 1}", "if(d.phshare){const p=curP();if(p)phoShare(p,d.phshare);return 1}")
rep("async function phoShare(p){const F=[];for(const[sl,t] of [['b','قبل'],['a','بعد']])for(", "async function phoShare(p,w){w=w&&w!='1'?w:'ba';const F=[];for(const[sl,t] of [['b','قبل'],['a','بعد']].filter(x=>w.includes(x[0])))for(")
rep(" if(!F.length)return alert('مفيش صور على الجهاز ده');const tt=toast('جاري تجهيز الصور…');",
    " if(!F.length)return alert('مفيش صور على الجهاز ده');const msg=`${PL(p)}${p.name?' ('+p.name+')':''} — ${w=='b'?'صور قبل التنفيذ':w=='a'?'صور بعد التنفيذ':'صور قبل وبعد التنفيذ'} (${F.length} صورة)`;try{navigator.clipboard&&navigator.clipboard.writeText(msg)}catch(e){}const tt=toast('جاري تجهيز الصور…');")
rep("await CP('Share').share({title:'صور صيدلية '+p.no,files:U2,dialogTitle:'صور صيدلية '+p.no}).catch(()=>{});return}", "await CP('Share').share({title:msg,text:msg,files:U2,dialogTitle:'صور صيدلية '+p.no}).catch(()=>{});return}")
rep("await navigator.share({files:fl,title:'صور صيدلية '+p.no}).catch(()=>{});return}", "await navigator.share({files:fl,title:msg,text:msg}).catch(()=>{});return}")
# ---- second layout attachment
rep("function attHtml(p){const A=p.att||{},pl=A.plan,xl=A.xls;return `<details class=\"pinfo\" data-id=\"__att\"${V.op.__att?' open':''}><summary>${ic('file')} المخطط والملفات${(pl?1:0)+(xl?1:0)?` (${(pl?1:0)+(xl?1:0)})`:''}</summary><div class=\"atr\"><b>المخطط ${pl&&pl.rev?`<span class=\"xbd\">${esc(pl.rev)}</span>`:''}</b>${pl?`${pl.th?`<img class=\"attimg\" src=\"${pl.th}\" data-attopen=\"plan\">`:`<small>📄 ${esc(pl.n)} · ${fsz(pl.sz)}</small>`}<div class=\"tt\"><button class=\"pr\" data-attopen=\"plan\">${ic('eye')}فتح</button><button data-attpick=\"plan\">تغيير</button><button data-attdel=\"plan\" style=\"color:var(--rd)\">حذف</button></div>`:`<div class=\"tt\"><button data-attpick=\"plan\">${ic('upload')}إرفاق المخطط (صورة أو PDF)</button></div>`}</div>",
    "function attHtml(p){const A=p.att||{},xl=A.xls,nA=(A.plan?1:0)+(A.plan2?1:0)+(xl?1:0),pB=(k,t,u)=>{const pl=A[k];return `<div class=\"atr\"><b>${t} ${pl&&pl.rev?`<span class=\"xbd\">${esc(pl.rev)}</span>`:''}</b>${pl?`${pl.th?`<img class=\"attimg\" src=\"${pl.th}\" data-attopen=\"${k}\">`:`<small>📄 ${esc(pl.n)} · ${fsz(pl.sz)}</small>`}<div class=\"tt\"><button class=\"pr\" data-attopen=\"${k}\">${ic('eye')}فتح</button><button data-attpick=\"${k}\">تغيير</button><button data-attdel=\"${k}\" style=\"color:var(--rd)\">حذف</button></div>`:`<div class=\"tt\"><button data-attpick=\"${k}\">${ic('upload')}${u}</button></div>`}</div>`};return `<details class=\"pinfo\" data-id=\"__att\"${V.op.__att?' open':''}><summary>${ic('file')} المخطط والملفات${nA?` (${nA})`:''}</summary>${pB('plan','المخطط','إرفاق المخطط (صورة أو PDF)')}${A.plan||A.plan2?pB('plan2','مخطط إضافي','إرفاق مخطط إضافي (صورة أو PDF)'):''}")
rep("<input type=\"file\" id=\"attplan\" accept=\"image/*,.pdf,application/pdf\" hidden>", "<input type=\"file\" id=\"attplan\" accept=\"image/*,.pdf,application/pdf\" hidden><input type=\"file\" id=\"attplan2\" accept=\"image/*,.pdf,application/pdf\" hidden>")
rep("if(kind=='plan'&&/^image\\//.test(file.type)){const u=b2u(file,file.type);p.att.plan.th=await shrink(u,900);URL.revokeObjectURL(u)}else if(kind=='plan')delete p.att.plan.th;",
    "if(/^plan/.test(kind)&&/^image\\//.test(file.type)){const u=b2u(file,file.type);p.att[kind].th=await shrink(u,900);URL.revokeObjectURL(u)}else if(/^plan/.test(kind))delete p.att[kind].th;")
rep("if(!confirm(k=='plan'?'حذف المخطط؟':'حذف ملف الـ Excel؟'))return;", "if(!confirm(k=='plan'?'حذف المخطط؟':k=='plan2'?'حذف المخطط الإضافي؟':'حذف ملف الـ Excel؟'))return;")
rep("if(k=='plan'&&/^image\\//.test(b.type||m.t)){const u=b2u(b,b.type);", "if(/^plan/.test(k)&&/^image\\//.test(b.type||m.t)){const u=b2u(b,b.type);")
rep("if(x.id=='attplan'||x.id=='attxls'){const f=x.files[0];x.value='';const q=curP();if(!f||!q)return;const k=x.id=='attplan'?'plan':'xls';if(k=='plan'&&",
    "if(x.id=='attplan'||x.id=='attplan2'||x.id=='attxls'){const f=x.files[0];x.value='';const q=curP();if(!f||!q)return;const k=x.id=='attplan'?'plan':x.id=='attplan2'?'plan2':'xls';if(/^plan/.test(k)&&")
# bulk attach: a layout of the other kind (image vs PDF) goes to the second slot
rep("if(q&&await attPut(q,x.kind,x.f))n++}", "if(q&&await attPut(q,x.kind=='plan'?planSlot(q,x.f):x.kind,x.f))n++}")

JS = r"""// ---------- v2.5: second layout slot, photo limits in settings ----------
const isPdfF=(f,t)=>/pdf/i.test((f&&f.type)||t||'')||/\.pdf$/i.test((f&&f.name)||'');
function planSlot(p,f){const A=p.att||{};if(!A.plan)return 'plan';const a=isPdfF(null,A.plan.t)||/\.pdf$/i.test(A.plan.n||''),b=isPdfF(f);return a!=b?'plan2':'plan'}
function v25Change(x){if(x.id=='cfphb'||x.id=='cfpha'){const v=Math.max(1,Math.min(60,Math.round(+x.value||0)));DB.cfg[x.id=='cfphb'?'phB':'phA']=v;x.value=v;svq();toastT('✓ اتحفظ: أقصى '+v+' صورة '+(x.id=='cfphb'?'قبل':'بعد'));return 1}return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("x15Change(x)||rcvChange(x)||v21Change(x)||v24Change(x)||", "x15Change(x)||rcvChange(x)||v21Change(x)||v24Change(x)||v25Change(x)||")
rep("VER='v2.4'", "VER='v2.5'")
rep(" changelog:[{version:'v2.4',", " changelog:[{version:'v2.5',date:'2026-11-02',changes:['Before / after photos: limits from the general settings (default before 8, after 14; old design stays 8)','Pharmacy attachments: second layout slot (مخطط إضافي), image or PDF; bulk attach puts a layout of the other kind there','Share photos: before / after / both, with a text carrying the pharmacy number (also copied)']},{version:'v2.4',")
EN = {'أقصى عدد صور قبل لكل صيدلية':'Max before photos per pharmacy','أقصى عدد صور بعد لكل صيدلية':'Max after photos per pharmacy','مخطط إضافي':'Extra layout','إرفاق مخطط إضافي (صورة أو PDF)':'Attach an extra layout (image or PDF)','حذف المخطط الإضافي؟':'Delete the extra layout?','قبل + بعد':'Before + after'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
