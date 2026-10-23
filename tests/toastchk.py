import sys
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=open(W+'out6/966-data-v1.2.json',encoding='utf-8').read()
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  R=[]
  for f in sys.argv[1:]:
    pg=br.new_page();pg.goto('file://'+W+f);pg.wait_for_timeout(300);pg.evaluate("d=>localStorage.setItem('ads',d)",D);pg.reload();pg.wait_for_timeout(1500)
    R.append(pg.evaluate("""(()=>{document.querySelectorAll('.toast').forEach(t=>t.remove());const o=[];DB.cfg.ue=5;bkRemind();o.push(document.querySelector('.toast.rem').outerHTML);document.querySelectorAll('.toast').forEach(t=>t.remove());
     window.CAPN=()=>true;DB.cfg.drn='';DB.cfg.lb='';try{driveRemind()}catch(e){o.push('ERR '+e)};const t=document.querySelector('.toast.rem');o.push(t?t.outerHTML:'none');return o})()"""))
  print('SAME' if R[0]==R[1] else 'DIFF', R[0][0][:150]); print(R[0][1][:200]); print(R[1][1][:200] if R[0]!=R[1] else '')
