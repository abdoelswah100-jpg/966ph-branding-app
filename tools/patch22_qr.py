"""v1.5 part 1: QR scanner: centred frame, Google ML Kit in the app, browser reader, cropped jsQR, flash, zoom, continuous scanning."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function cScanN' not in s
a = s.index('// ---- camera QR scan (live)'); b = s.index('// ---- Excel (same layout every time) ----', a)
s = s[:a] + open(os.path.join(R, 'src/qr.js.part'), encoding='utf-8').read() + s[b:]
rep("for(const f of files){const z=await qrFromBlob(f);", "for(const f of files){const z=await qrFromBlobN(f)||await qrFromBlobB(f)||await qrFromBlob(f);")
# continuous scanning: after saving a scanned invoice the camera opens again
rep("['_alt','_qr','_new'].forEach(k=>delete x[k]);", "const seq=d._seq;['_alt','_qr','_new','_seq'].forEach(k=>delete x[k]);")
rep("V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q,from:V.from});toastT('✓ اتحفظت الفاتورة')}",
    "V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q,from:V.from});toastT('✓ اتحفظت الفاتورة');if(seq&&cSeq()){CSN++;setTimeout(cScan,450)}else CSN=0}")
rep("if(d.cscanx){if(CSC)CSC.stop();return 1}", "if(d.cscanx){if(CSC)CSC.stop();CSN=0;CLR='';return 1}if(d.ctorch){if(CSC&&CSC.torch)CSC.torch();b.classList.toggle('pr');return 1}")
rep("if(d.ccancel){", "if(d.ccancel){CSN=0;CLR='';")
rep("function nativeBack(){", "function nativeBack(){if(CSC){CSC.stop();CSN=0;CLR='';return}")
# setting toggle inside the scanner
rep(" if(usrChange(x)||custChange(x)||mntChange(x)||whChange(x))return;", " if(x.id=='cseq'){CU().cfg.seq=x.checked?1:0;sv();return}\n if(usrChange(x)||custChange(x)||mntChange(x)||whChange(x))return;")
# CSS: the frame sits in the middle of the camera picture
old_css = [
 ".cscan video{width:100%;max-width:520px;max-height:70vh;background:#000}",
 ".cscan .cfr{position:absolute;width:min(62vw,300px);height:min(62vw,300px);border:3px solid #F2B705;border-radius:14px;top:calc(50% - min(31vw,150px) - 40px);pointer-events:none}",
]
for c in old_css: rep(c, "")
CSS = """
.cscan{padding:14px 0}.cscan>*:not(.cvw){position:relative;z-index:2}
.cvw{position:relative;width:100%;max-width:520px;direction:ltr;overflow:hidden;border-radius:12px}
.cvw video{display:block;width:100%;max-height:62vh;object-fit:cover;background:#000}
.cfr{position:absolute;inset:0;margin:auto;width:min(66vw,290px);height:min(66vw,290px);max-height:92%;aspect-ratio:1;border:3px solid #F2B705;border-radius:16px;pointer-events:none;box-shadow:0 0 0 2000px rgba(0,0,0,.38)}
.cscan .cmsg{margin:0;text-align:center;padding:0 16px}.cscan .cmsg.w{color:#FFB4B4}.cscan .ccnt{margin:0;color:#7DDA9B;font-weight:800}
.czm{display:flex;align-items:center;gap:8px;width:100%;max-width:520px;padding:0 16px;color:#fff}.czm[hidden]{display:none}.czm input{flex:1}
.cscan .c2b{display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap;margin-bottom:6px}.cscan .chk{color:#fff}
html.bscan,html.bscan body{background:transparent!important}html.bscan body>*:not(.cscan){visibility:hidden!important}
.cscan.nat{background:transparent}.cscan.nat .cvw{height:58vh;overflow:visible;border-radius:0}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
import json
EN = {'وجّه الكاميرا على كود QR الفاتورة جوه المربع':'Point the camera at the invoice QR code inside the frame','مسح متتالي':'Continuous scanning','🔦 فلاش':'🔦 Flash','⚠ الكود ده مش كود فاتورة ضريبية':'⚠ This is not a tax invoice QR code','⚠ قارئ Google مش شغال على الجهاز ده، هيشتغل القارئ العادي':'⚠ The Google reader does not work on this device; using the normal reader','فاتورة في الجلسة دي':'invoices in this session','✓ الفاتورة دي اتسجلت. وجّه على الفاتورة اللي بعدها':'✓ This invoice is saved. Point at the next invoice','✓ اتحفظ':'✓ Saved'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
