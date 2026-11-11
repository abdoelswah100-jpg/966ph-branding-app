"""v1.5: version, changelog, trial-app badge (the trial APK sets window.T966)."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
rep("VER='v1.4'", "VER='v1.5'")
rep(" changelog:[{version:'v1.4',", " changelog:[{version:'v1.5',date:'2026-10-26',changes:['QR scanner: frame centred on the camera picture; inside the app Google ML Kit (fast, offline), in the browser the built-in reader or jsQR on the frame area at full resolution; flash and zoom; continuous scanning (camera opens again after each saved invoice); photos read with ML Kit inside the app','Warehouse add uses the same item cards as a pharmacy (types, names with images, sizes by shelf type; composite items split in header / side); thumbnails in the stock list','End gandola on Old Turkish: needed = full / backlight + sticker only / acrylic only; Side Acrylic Pocket is its own table in the print summary, its own row in the management report, sizes report and warehouse','Print only what is missing: the print summary can deduct what is in the warehouse, and take it from stock for the pharmacy','Custody alert when the remaining is below 2000 (changeable, 0 = off), on the custody screen and the home screen','Maintenance search; share before / after photos (WhatsApp)','Trial app (966Ph تجريبي) installs next to the main app with separate data']},{version:'v1.4',")
JS = "if(window.T966){try{const t=document.createElement('button');t.className='t966';t.dataset.tab='bk';t.textContent='🧪 نسخة تجريبية · بياناتها منفصلة';document.body.appendChild(t);document.title='966Ph تجريبي'}catch(e){}}\n"
rep("(function(){try{var s=document.createElement('div');s.id='splash';", JS + "(function(){try{var s=document.createElement('div');s.id='splash';")
CSS = "\n.t966{position:fixed;top:calc(env(safe-area-inset-top) + 2px);left:50%;transform:translateX(-50%);z-index:9000;background:#F28C05;color:#fff;border:0;border-radius:20px;padding:1px 12px;font-size:10.5px;font-weight:800;min-height:0;box-shadow:0 2px 6px rgba(0,0,0,.25)}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
open(P, 'w', encoding='utf-8').write(s)
print('ok')
