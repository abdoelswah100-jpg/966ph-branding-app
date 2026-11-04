"""v3.2: «استيراد ودمج» accepts the laptop / Drive backup files (966-laptop-, 966-day-, 966-full-, 966-month-) and merges them
with the Drive rules (newest pharmacy, most recently edited section, snapshot first); phone Drive screen: «دمج ملف من اللاب توب»."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'gdMergeFile' not in s
rep("rd.onload=()=>{try{const q=JSON.parse(rd.result);if(!q||q.kind!=SKIND)throw 0;doSync(q)}catch(er){alert('هذا ليس ملف مزامنة صالح. استخدم ملف المزامنة المصدَّر من التطبيق.')}};rd.readAsText(f);x.value='';return}",
    "rd.onload=()=>{let q;try{q=JSON.parse(rd.result)}catch(er){return alert('هذا ليس ملف مزامنة صالح. استخدم ملف المزامنة المصدَّر من التطبيق.')}if(q&&q.kind==SKIND){doSync(q);return}if(q&&Array.isArray(q.ph)){gdMergeFile(q,f.name);return}alert('هذا ليس ملف مزامنة صالح. استخدم ملف المزامنة أو ملف 966-laptop / 966-day من فولدر Drive.')};rd.readAsText(f);x.value='';return}")
rep("<label>استيراد ودمج ملف مزامنة<input type=\"file\" id=\"syncin\"", "<label>استيراد ودمج ملف مزامنة أو ملف من اللاب توب (966-laptop / 966-day)<input type=\"file\" id=\"syncin\"")
rep("<div class=\"tt\"><button data-gdls=\"1\">${ic('db')}عرض النسخ على Drive</button></div>${L?gdListHtml(L):''}</div>`;",
    "<div class=\"tt\"><button data-gdls=\"1\">${ic('db')}عرض النسخ على Drive</button><button data-pick=\"gdmfin\">${ic('upload')}دمج ملف من اللاب توب</button></div><input type=\"file\" id=\"gdmfin\" accept=\".json,application/json\" hidden><small class=\"hint\">«دمج ملف من اللاب توب»: اختار Drive ← فولدر ${GDF} ← آخر ملف 966-laptop-… (الموبايل ما بيشوفهوش في القائمة اللي فوق).</small>${L?gdListHtml(L):''}</div>`;")
JS = r"""// ---------- v3.2: merge a laptop / Drive backup file picked by hand ----------
function gdMergeFile(q,name){if(!confirm(`دمج ${name} (${q.ph.length} صيدلية${q.device?' · من '+q.device:''}${q.at?' · '+fd(q.at):''}) مع البيانات اللي هنا؟\nكل صيدلية هتاخد النسخة الأحدث، والأقسام (العهدة، المخزن، الصيانة…) هتاخد اللي اتعدّل آخر واحد.\nهتتاخد نقطة استعادة قبلها.`))return;
 const t=toast('جاري الدمج…');gdApply(q,'merge','قبل دمج '+name).then(m=>{t.remove();render();alert('✓ '+m)}).catch(e=>{t.remove();alert('⚠ الدمج ما نجحش: '+(e.message||e))})}
function v32Change(x){if(x.id=='gdmfin'){const f=x.files[0];x.value='';if(!f)return 1;const rd=new FileReader();rd.onload=()=>{let q;try{q=JSON.parse(rd.result)}catch(e){q=null}if(q&&Array.isArray(q.ph))gdMergeFile(q,f.name);else if(q&&q.kind==SKIND)doSync(q);else alert('الملف ده مش نسخة من التطبيق. اختار ملف 966-laptop-… أو 966-day-…')};rd.readAsText(f);return 1}return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("v29Change(x)||v30Change(x)||", "v29Change(x)||v30Change(x)||v32Change(x)||")
rep("VER='v3.1'", "VER='v3.2'")
rep(" changelog:[{version:'v3.1',", " changelog:[{version:'v3.2',date:'2026-11-05',changes:['Sync import accepts the laptop / Drive backup files (966-laptop, 966-day, full, month) and merges them: newest pharmacy, most recently edited section, snapshot first','Phone Google Drive screen: «دمج ملف من اللاب توب»']},{version:'v3.1',")
EN = {'دمج ملف من اللاب توب':'Merge a file from the laptop','استيراد ودمج ملف مزامنة أو ملف من اللاب توب (966-laptop / 966-day)':'Import and merge a sync file or a laptop file (966-laptop / 966-day)'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
