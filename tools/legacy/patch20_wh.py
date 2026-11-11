"""v1.4 part 4: warehouse (المخزن): stock, inventory count, surplus from pharmacies, pull into pharmacy items, maintenance asks first."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function whHtml' not in s
JS = open(os.path.join(R, 'src/wh.js.part'), encoding='utf-8').read()
rep("// ---------- PDF ----------", JS + "\n// ---------- PDF ----------")
rep("const ICN={", "const ICN={box:'<path d=\"M21 8l-9-5-9 5 9 5 9-5z\"/><path d=\"M3 8v8l9 5 9-5V8\"/><path d=\"M12 13v8\"/>',")
# bottom bar: المخزن takes the place of الحاسبة, which moves to the menu
rep("['calc','الحاسبة','calc','t-calc'],", "['wh','المخزن','box',''],")
rep("const MENU=[['cust','العهدة','sheet'],", "const MENU=[['calc','الحاسبة','calc'],['cust','العهدة','sheet'],")
rep("calc:'calc',prc:'calc',docs:'calc',", "calc:'',prc:'',docs:'',wh:'wh',whe:'wh',inv:'wh',wlog:'wh',wht:'home',")
rep("${t[0]=='bk'&&nb?`<i class=\"nb\">${nb}</i>`:''}", "${t[0]=='bk'&&nb?`<i class=\"nb\">${nb}</i>`:''}${t[0]=='wh'&&whLow()?`<i class=\"nb\" style=\"background:#C7313B\">${whLow()}</i>`:''}")
rep("const PARENT={med:'mnt',", "const PARENT={whe:'wh',inv:'wh',wlog:'wh',wht:'ph',med:'mnt',")
rep(" if(V.v=='mnt'){a.innerHTML=", " if(V.v=='wh'){a.innerHTML=hdr('','المخزن')+`<main>${whHtml()}</main>`;return}\n if(V.v=='whe'){a.innerHTML=hdr('<button data-tab=\"wh\">‹ المخزن</button>',V.we&&V.we._old?'تعديل صنف':'إضافة صنف')+`<main>${wheHtml()}</main>`;return}\n if(V.v=='inv'){a.innerHTML=hdr('<button data-invx=\"1\">‹ المخزن</button>','جرد المخزن')+`<main>${invHtml()}</main>`;return}\n if(V.v=='wlog'){a.innerHTML=hdr('<button data-tab=\"wh\">‹ المخزن</button>','سجل الحركات')+`<main>${wlogHtml()}</main>`;return}\n if(V.v=='wht'){a.innerHTML=hdr('<button data-whno=\"1\">‹ الصيدلية</button>','ترحيل للمخزن')+`<main>${whtHtml()}</main>`;return}\n if(V.v=='mnt'){a.innerHTML=")
rep(" if(custClick(d,b)||mntClick(d))return;", " if(custClick(d,b)||mntClick(d)||whClick(d,b))return;")
rep(" if(custChange(x)||mntChange(x))return;", " if(custChange(x)||mntChange(x)||whChange(x))return;")
rep("document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.wef&&V.we&&V.v=='whe'&&x.tagName=='INPUT')V.we[x.dataset.wef]=x.value});",
    "document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.wef&&V.we&&V.v=='whe'&&x.tagName=='INPUT')V.we[x.dataset.wef]=x.value;if(x.id=='whq')whChange(x)});")
# finish pharmacy: button next to the receipt / execution bar, and in the execution screen
rep("<button data-exg=\"${p.id}\">${ic('check')}التنفيذ</button></div>`}", "<button data-exg=\"${p.id}\">${ic('check')}التنفيذ</button><button data-whdone=\"${p.id}\">${ic('box')}إنهاء الصيدلية</button></div>`}")
rep("<button data-nq=\"r:ph\">ملخص نواقص الطباعة</button></div></main>`;fixT();return}", "<button data-nq=\"r:ph\">ملخص نواقص الطباعة</button><button data-whdone=\"${q.id}\">${ic('box')}إنهاء الصيدلية ونقل الفائض للمخزن</button></div></main>`;fixT();return}")
# status set to مكتملة -> offer the transfer
rep("if(x.id=='rvst'){const q=curP();if(q){q.st=x.value;sv();render()}return}", "if(x.id=='rvst'){const q=curP();if(q){q.st=x.value;sv();render();if(q.st=='مكتملة')setTimeout(()=>whOffer(q,true),50)}return}")
rep("else if(x.id=='cst'){curP().st=x.value;sv()}", "else if(x.id=='cst'){const q=curP();q.st=x.value;sv();if(q.st=='مكتملة')setTimeout(()=>whOffer(q,true),50);else if(q.whAt)toastT('⚠ الصيدلية دي اترحّل فائضها للمخزن قبل كده. لو اتعدلت، اضغط «إنهاء الصيدلية» تاني علشان يترحّل الفرق بس.')}")
# pull from stock for a new pharmacy item
rep("}else{(p.rows[t.id]=p.rows[t.id]||[]).push(r);", "}else{(p.rows[t.id]=p.rows[t.id]||[]).push(r);setTimeout(()=>whPullOffer(p,t,r),60);")
rep("const FPX=['ck','nt','r','x'];", "const FPX=['ck','nt','r','x','wf'];")
# maintenance asks before taking from stock (new jobs only)
rep("const C=MU(),i=C.items.findIndex(y=>y.id==x.id);if(i>=0)C.items[i]=x;else C.items.push(x);C.cur=mQ(x.dt);sv();snd('ok');",
    "const C=MU(),i=C.items.findIndex(y=>y.id==x.id);if(i>=0)C.items[i]=x;else C.items.push(x);C.cur=mQ(x.dt);sv();snd('ok');if(i<0)whMntOffer(x);")
CSS = r"""
.whc{display:flex;justify-content:space-between;gap:10px;align-items:center;background:var(--c);border:1px solid var(--ln);border-radius:12px;padding:10px;margin-bottom:8px}.whc.lo{border-color:#E8A0A0;background:#FFF5F5}:root[data-th=dark] .whc.lo{background:#3A1A1C}
.whi{display:grid;gap:2px;min-width:0}.whi small{color:var(--mu);font-size:11.5px}.whi small.mu{font-size:10.5px}
.whq{display:grid;justify-items:center;gap:2px;flex:none}.whq>b{font-size:22px;color:var(--pb)}.whq>small{color:var(--mu);font-size:11px}.whq div{display:flex;gap:4px}.whq button{min-width:34px;min-height:32px;padding:2px 8px}
.whc.lo .whq>b{color:#8B0000}
.whsum{position:sticky;bottom:calc(env(safe-area-inset-bottom) + 64px);background:var(--pb);color:#fff;border-radius:10px;padding:8px 12px;text-align:center;margin:8px 0;z-index:5}
.invc{width:80px;text-align:center}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'المخزن':'Warehouse','‹ المخزن':'‹ Warehouse','عدد الأصناف':'Items','إجمالي القطع':'Total pieces','إجمالي الأمتار':'Total metres','آخر حركة':'Last movement','جرد جديد':'New stock count','سجل الحركات':'Movements log','رصيد قليل بس':'Low stock only','كل الأنواع':'All types','الكل':'All','المسمى':'Name','الخامة':'Material','الحد الأدنى':'Minimum','المعروض:':'Shown:','صنف':'items','متر':'m','إضافة صنف':'Add item','تعديل صنف':'Edit item','الكمية':'Quantity','الحد الأدنى (اختياري)':'Minimum (optional)','مسح الصنف':'Delete item','✓ اتحفظ الصنف':'✓ Item saved','جرد المخزن':'Stock count','اتعدّ':'counted','اللي ما اتعدّش بس':'Not counted only','الرصيد':'Balance','العدّ الفعلي':'Counted','الفرق':'Difference','اعتماد الجرد':'Approve count','إلغاء الجرد':'Cancel count','لسه مفيش حركات.':'No movements yet.','إضافة':'Add','سحب':'Take out','تسوية':'Adjustment','جرد':'Count','يدوي':'Manual','إنهاء الصيدلية':'Finish pharmacy','إنهاء الصيدلية ونقل الفائض للمخزن':'Finish pharmacy and move surplus to the warehouse','ترحيل للمخزن':'Move to warehouse','ترحيل الفائض للمخزن':'Move surplus to the warehouse','الفائض = المستلم − المتنفذ لكل بند، بنوع رفوف البند.':'Surplus = received − executed for each item, with the item shelf type.','تجاهل':'Ignore','هيتضاف':'Will be added','الصنف':'Item','الرفوف':'Shelves','رصيد المخزن':'Warehouse stock','تقرير جرد المخزن':'Stock count report','الحاسبة':'Calculator','مفيش أصناف. الفائض بيتضاف لوحده لما تنهي صيدلية، أو اضغط «إضافة».':'No items. Surplus is added automatically when you finish a pharmacy, or tap «Add».','الوحدة':'Unit','الرصيد قبل':'Balance before','العدّ':'Count','إجمالي الفروق':'Total difference','تقرير آخر جرد Excel':'Last count report Excel','آخر جرد:':'Last count:','قطعة':'pieces','مفيش فائض جديد يترحّل للمخزن من الصيدلية دي':'No new surplus to move from this pharmacy','تحويل حالة الصيدلية إلى «مكتملة»؟':'Set the pharmacy status to «Completed»?','تمسح الصنف ده من المخزن؟':'Delete this item from the warehouse?','اعتماد الجرد هيعدّل أرصدة الأصناف اللي اتعدّت. تكمل؟':'Approving will change the balances of the counted items. Continue?','إلغاء الجرد؟ مفيش أي رصيد هيتغير.':'Cancel the count? No balance will change.','ما اتعدّش أي صنف':'No item counted','اكتب الكمية':'Enter the quantity','اختار نوع الدعاية':'Choose the ad type','فيه صنف بنفس البيانات. أدمجهم في صنف واحد؟':'An item with the same data exists. Merge them?'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a, c in EN.items():
    if a not in D: D[a] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("changes:['Shelf type per item", "changes:['Warehouse (المخزن) in the bottom bar (Calculator moved to the menu): stock by shelf type / ad type / name / material / size, filters, + / −, low-stock badge, stock count with differences and report, movements log, Excel/PDF; finishing a pharmacy moves its surplus (received − executed) with a confirmation and only the difference later; adding an item offers stock; maintenance asks before taking from stock','Shelf type per item")
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
