"""v1.4 part 5: users, permissions, per-user data and settings, collecting the supervisors' files."""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function uInit' not in s
JS = open(os.path.join(R, 'src/users.js.part'), encoding='utf-8').read()
rep("// ---------- PDF ----------", JS + "\nconst uAllSt=k=>[DB[k]].concat(Object.keys(DB.uw||{}).filter(id=>id!==STO).map(id=>(DB.uw[id]||{})[k]));\n// ---------- PDF ----------")
# start-up: users are set up once the code above exists; norm() re-applies them when the data is replaced
rep("var PREMIG=null,PRECK=null;", "var PREMIG=null,PRECK=null,UREADY=false;")
rep("DB.cfg.ue=DB.ph.filter(p=>(p.modAt||BASE)>(DB.cfg.lb||'')).length;}\nnorm();", "DB.cfg.ue=DB.ph.filter(p=>(p.modAt||BASE)>(DB.cfg.lb||'')).length;if(UREADY){if(HIDDB!==DB){HID=[];HIDDB=null;STO=null;UBASE=null}uInit()}}\nnorm();")
rep("render();\n(async()=>{const ok=await idbOpen();", "UREADY=true;uInit();\nrender();uStart();\n(async()=>{const ok=await idbOpen();")
# everything that saves or exports the data goes through dbOut()
rep("const j=JSON.stringify(DB);try{localStorage.setItem('ads',j)}", "const j=JSON.stringify(dbOut());try{localStorage.setItem('ads',j)}")
rep("SNAPS.unshift({at:nowIso(),day:TD(),why,db:JSON.stringify(DB)})", "SNAPS.unshift({at:nowIso(),day:TD(),why,db:JSON.stringify(dbOut())})")
rep("Object.assign({},DB,{cfg:Object.assign({},DB.cfg,", "Object.assign({},dbOut(),{cfg:Object.assign({},dbOut().cfg,", 4)
rep("for(const m of Object.values((DB.cust||{}).m||{}))", "for(const m of uAllSt('cust').flatMap(c=>Object.values((c||{}).m||{})))")
rep("for(const x of (DB.mnt||{}).items||[])for(const k of [...(x.imb||[]),...(x.ima||[])])", "for(const x of uAllSt('mnt').flatMap(c=>(c||{}).items||[]))for(const k of [...(x.imb||[]),...(x.ima||[])])")
rep("function dbOut(){if(!DB.users)return DB;const o=Object.assign({},DB),u=U();o.ph=DB.ph.concat(HIDDB===DB?HID:[]);", "function dbOut(){if(!DB.users)return DB;const o=Object.assign({},DB),u=U();o.ph=DB.ph.concat(HIDDB===DB?HID:[]);o.ph.forEach(uSetOwner);")
rep("o.users=DB.users.map(x=>x.id==u.id?Object.assign({},x,{ov:{sz:uDiff(DB.cfg.sz,UBASE.sz),pl:uDiff(DB.pl,UBASE.pl)}}):x);", "const me=DB.users.find(x=>x.id==u.id);if(me)me.ov={sz:uDiff(DB.cfg.sz,UBASE.sz),pl:uDiff(DB.pl,UBASE.pl)};o.users=DB.users;")
rep("const r=mergeSync(inc);DB.cfg.ls=nowIso();", "const r=mergeSync(inc);uApply();DB.cfg.ls=nowIso();")
# device lock: the user PIN replaces it once users have PINs
rep("const lockOn=()=>CAPN()&&!!lkGet().on;", "const lockOn=()=>CAPN()&&!!lkGet().on&&!uPinMode();")
# menu: users + logout, current user shown
rep("const MENU=[['calc','الحاسبة','calc'],", "const MENU=[['usr','المستخدمين والمشرفين','lock'],['calc','الحاسبة','calc'],")
rep("<small>966Ph Branding ${VER}</small></div>`;", "<button data-ulogout=\"1\">${ic('lock')}خروج / تبديل المستخدم</button><small>${esc(U().nm)} · 966Ph Branding ${VER}</small></div>`;")
rep("const TABOF={mnt:'',", "const TABOF={usr:'',ued:'',mnt:'',")
rep("const PARENT={whe:'wh',", "const PARENT={ued:'usr',whe:'wh',")
rep(" if(V.v=='wh'){a.innerHTML=hdr('','المخزن')+`<main>${whHtml()}</main>`;return}", " if(V.v=='usr'){a.innerHTML=hdr(backBtn(),'المستخدمين والمشرفين')+`<main>${usrHtml()}</main>`;return}\n if(V.v=='ued'){a.innerHTML=hdr('<button data-tab=\"usr\">‹ المستخدمين</button>',V.ue&&V.ue.id?'تعديل مستخدم':'مستخدم جديد')+`<main>${uedHtml()}</main>`;return}\n if(V.v=='wh'){a.innerHTML=hdr('','المخزن')+`<main>${uStoreBar()}${whHtml()}</main>`;return}")
rep("+`<main>${mntHtml()}</main>`;return}", "+`<main>${uStoreBar()}${mntHtml()}</main>`;return}")
rep("+`<main>${custHtml()}</main>`;return}", "+`<main>${uStoreBar()}${custHtml()}</main>`;return}")
rep("k==='quotes'?'عروض الأسعار':'الفواتير')+`<main>", "k==='quotes'?'عروض الأسعار':'الفواتير')+`<main>${uStoreBar()}")
# events
rep(" if(custClick(d,b)||mntClick(d)||whClick(d,b))return;", " if(uGuardClick(d,b))return;\n if(usrClick(d,b)||custClick(d,b)||mntClick(d)||whClick(d,b))return;")
rep(" if(custChange(x)||mntChange(x)||whChange(x))return;", " if(uGuardChange(x))return;\n if(usrChange(x)||custChange(x)||mntChange(x)||whChange(x))return;")
rep("function uGuardClick(d,b){const v=V.v;", "function uGuardClick(d,b){const v=V.v;if(d.cpy||d.rm){const q=DB.ph.find(x=>x.id==(d.cpy||d.rm));if(q&&!uEditP(q)){toastT('👁 الصيدلية دي للعرض بس');return 1}}")
rep(" if(d.ust){if(!uAll())return 1;", " if(d.uex){const p=curP();if(!p||!uEditP(p))return 1;const L=p.ex=p.ex||[],i=L.indexOf(d.uex);if(i>=0)L.splice(i,1);else L.push(d.uex);sv();render();return 1}\n if(d.ust){if(!uAll())return 1;")
# pharmacy page: owner, executors, read-only banner, executor picker in the pharmacy data
rep("<div class=\"pc-ln\">الشهر: <b>${mo}</b> · المشرف: <b>${esc(p.sup||'—')}</b></div>${locChips(p)}", "<div class=\"pc-ln\">الشهر: <b>${mo}</b> · المشرف: <b>${esc(uName(p.uid)||p.sup||'—')}</b>${(p.ex||[]).length?' · منفذ: <b>'+esc(p.ex.map(uName).join('، '))+'</b>':''}</div>${uRoBanner(p)}${locChips(p)}")
rep("<div class=\"dts\"><label>الحالة<select id=\"cst\"", "${uExHtml(p)}<div class=\"dts\"><label>الحالة<select id=\"cst\"")
rep("const metaHtml=p=>`<div class=\"meta-panel\"><div class=\"meta-item meta-sup\">المشرف: <b>${esc(p.sup||'عبدالله السواح')}</b></div>", "const metaHtml=p=>`<div class=\"meta-panel\"><div class=\"meta-item meta-sup\">المشرف: <b>${esc(uName(p.uid)||p.sup||'عبدالله السواح')}</b>${(p.ex||[]).length?' · منفذ: <b>'+esc(p.ex.map(uName).join('، '))+'</b>':''}</div>")
# CSS: the login screen uses the lock screen look
css = ''.join(m.group(0).replace('#lock', '#ulog') + '\n' for m in re.finditer(r'#lock[^{}]*\{[^}]*\}', s))
CSS = "\n" + css + r""".ulst{display:grid;gap:8px}.ulst button{display:flex;align-items:center;gap:10px;text-align:start;justify-content:flex-start!important}.ulst i{width:34px;height:34px;border-radius:50%;background:#F2B705;color:#0B1B33;display:grid;place-items:center;font-style:normal;font-weight:900;flex:none}.ulst span{display:grid}.ulst small,#ulog .lks small{display:block;opacity:.75;font-size:11.5px}
.usr{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;border:1px solid var(--ln);border-radius:12px;padding:10px;margin-bottom:8px;background:var(--c)}.usr>div:first-child{display:grid;gap:3px;min-width:0}.usr small{color:var(--mu);font-size:11.5px}.usr .bt{display:grid;gap:6px;flex:none}.usr .pill{font-style:normal;color:#fff;border-radius:6px;padding:0 6px;font-size:10.5px;margin-inline-start:4px}
.ustb{display:flex;gap:8px;align-items:flex-end;background:var(--c2);border:1px solid var(--ln);border-radius:12px;padding:8px 10px;margin-bottom:10px}.ustb label{flex:1}.ustb small{color:#B42318;font-weight:800}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'المستخدمين والمشرفين':'Users and supervisors','خروج / تبديل المستخدم':'Log out / switch user','اختار اسمك':'Choose your name','أو اكتب اسمك':'Or type your name','متابعة':'Continue','الرقم السري':'PIN','دخول':'Log in','فتح بالبصمة':'Open with fingerprint','‹ مستخدم تاني':'‹ Another user','الرقم السري غلط':'Wrong PIN','أهلًا':'Hello','المستخدمين والصلاحيات':'Users and permissions','الفصل ده تنظيمي: كل مستخدم بيشوف شغله، بس البيانات نفسها على الجهاز مش مشفّرة.':'This separation is organisational: each user sees his own work, but the data on the device is not encrypted.','مسؤول البرنامج':'App administrator','مخفي من الدخول':'Hidden from login','يشوف:':'Sees:','كل المناطق':'All regions','شغله':'His work','يعدّل:':'Edits:','منطقته':'His region','العروض والفواتير:':'Quotes and invoices:','بتوعه':'His own','🔒 له رقم سري':'🔒 Has a PIN','⚠ من غير رقم سري':'⚠ No PIN','تعديل في الإعدادات':'settings changes','اعتماد للكل':'Apply for everyone','ملف إعداد جهاز':'Device setup file','إضافة مستخدم':'Add user','أداء المشرفين':'Supervisors performance','المشرف':'Supervisor','الصيدليات':'Pharmacies','مكتملة':'Completed','البنود':'Items','التنفيذ':'Execution','بعد استيراد ملفات المشرفين، الأرقام بتشمل شغلهم كله.':'After importing the supervisors files, the numbers include all their work.','ملفات المشرفين':'Supervisors files','تصدير ملف شغلي':'Export my work file','استيراد ملفات المشرفين':'Import supervisors files','استيراد ملف إعداد جهاز':'Import a device setup file','الاسم':'Name','الوظيفة':'Job title','المناطق':'Regions','يشوف':'Sees','شغله ومنطقته':'His work and region','يعدّل':'Edits','منطقته وشغله':'His region and work','لا (عرض وتصدير)':'No (view and export)','بتوعه بس':'His own only','كل المناطق (يعدّل)':'All regions (edit)','مسؤول البرنامج (المستخدمين والإعدادات الأساسية)':'App administrator (users and base settings)','مخفي من شاشة الدخول':'Hidden from the login screen','يطلب الرقم السري كل ما التطبيق يتفتح':'Ask for the PIN every time the app opens','رقم سري جديد':'New PIN','تأكيد الرقم':'Confirm PIN','مسح الرقم السري':'Remove the PIN','تعديل مستخدم':'Edit user','مستخدم جديد':'New user','‹ المستخدمين':'‹ Users','✓ اتحفظ المستخدم':'✓ User saved','بيانات':'Data of','(أنا)':'(me)','👁 للعرض فقط':'👁 View only','👁 الصيدلية دي للعرض بس':'👁 This pharmacy is view only','👁 بيانات مستخدم تاني — للعرض بس':'👁 Another user data — view only','👁 صلاحيتك عرض وتصدير بس':'👁 You can view and export only','👁 للعرض فقط — صيدلية':'👁 View only — pharmacy of','منفذ:':'Executor:','المشرف المسؤول':'Responsible supervisor','منفذين إضافيين (لو مشرف غطّى الصيدلية)':'Extra executors (if a supervisor covered the pharmacy)','نتيجة الاستيراد:':'Import result:','مدير عام':'General manager','مدير ومحاسب الشركة':'Manager and company accountant','مدير ومشرف المنطقة الشرقية':'Manager and Eastern region supervisor','مشرف المنطقة الوسطى ومسؤول البرنامج':'Central region supervisor and app administrator','مشرف المنطقة الغربية':'Western region supervisor','مشرف المنطقة الجنوبية':'Southern region supervisor','مشرف المنطقة الشمالية':'Northern region supervisor','الرقم السري من 4 لـ 6 أرقام':'The PIN is 4 to 6 digits','الرقمين مش زي بعض':'The two PINs do not match','اكتب الاسم':'Enter the name','الاسم ده مش موجود':'This name does not exist','المشرف يبعت «ملف شغلي»، واللي بيشوف كل المناطق يستورده هنا. التطبيق بياخد نسخة احتياطية قبل الدمج، والأحدث يكسب.':'The supervisor sends «my work file», and whoever sees all regions imports it here. The app takes a backup before merging, and the newest wins.'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a, c in EN.items():
    if a not in D: D[a] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("changes:['Warehouse (المخزن)", "changes:['Users and permissions (المستخدمين والمشرفين): the 7 team members with their regions and rights, login by name + PIN (fingerprint on Android), each user sees his pharmacies / custody / maintenance / warehouse / quotes and invoices, managers see everything and can look at the others (view only), executors for a covered pharmacy, personal settings with «apply for everyone», my-work file and import of the supervisors files with a backup before merging, device setup file, supervisors performance','Warehouse (المخزن)")
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
