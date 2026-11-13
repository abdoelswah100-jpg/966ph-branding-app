# 1.3: pharmacies import — separate record next to a completed / other-type pharmacy, restore point, undo, undo file for the 1.2 import
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';M=W+'maint/';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
for p in D['ph']:
  if p['no']=='1103' and p['mo']=='2026-11':p['st']='مكتملة';p['mod']='براندنج جديد'
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:300]),x.accept()))
  # the 1.2 import (old merge) on a completed 1103
  pg.goto('file://'+W+'new12.html');pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',JSON.stringify(d))}",D);pg.reload();pg.wait_for_timeout(2500)
  orig=pg.evaluate("JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.mo=='2026-11').rows)")
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);pg.set_input_files('#imp',M+'t_imp.json');pg.wait_for_timeout(1500)
  out('after 1.2 import',pg.evaluate("[DB.ph.length,DB.ph.filter(p=>p.no=='1103'&&p.mo=='2026-11').map(p=>[p.mod,p.st,Object.values(p.rows).flat().length])]"))
  data=pg.evaluate("JSON.stringify(dbOut())")
  # 1.3
  pg.goto('file://'+W+'new13.html');pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",data);pg.reload();pg.wait_for_timeout(2500)
  out('ver',pg.evaluate("VER"))
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);DL.clear()
  pg.set_input_files('#imp',M+'966-تراجع-عن-صيانة-Riyadh2-13-11.json');pg.wait_for_timeout(1500)
  out('undo dlg',DL[0][:400] if DL else None)
  out('after undo',pg.evaluate(f"[DB.ph.length,DB.ph.filter(p=>p.mo=='2026-11'&&p.mod=='صيانة').map(p=>p.no),JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.mo=='2026-11').rows)===arguments[0]||'diff',DB.trash.length,snaps()[0].why]".replace('arguments[0]',json.dumps(orig))))
  # correct import
  DL.clear();pg.set_input_files('#imp',M+'966-صيانة-Riyadh2-26-صيدلية-2026-11 (صحيح 1.3).json');pg.wait_for_timeout(1500)
  out('imp dlg',[x for x in DL[0].split('\n') if '1103' in x or 'دمج' in x] if DL else None)
  out('after imp',pg.evaluate(f"[DB.ph.length,DB.ph.filter(p=>p.no=='1103'&&p.mo=='2026-11').map(p=>[p.mod,p.st,Object.keys(p.rows).join(',')]),JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.st=='مكتملة').rows)==={json.dumps(orig)},DB.ph.filter(p=>p.mo=='2026-11'&&p.mod=='صيانة').length,snaps()[0].why]"))
  # same file again: no duplicate rows (merge into the maintenance records)
  DL.clear();pg.set_input_files('#imp',M+'966-صيانة-Riyadh2-26-صيدلية-2026-11 (صحيح 1.3).json');pg.wait_for_timeout(1500)
  out('again',pg.evaluate("[DB.ph.length,DB.ph.filter(p=>p.no=='1103'&&p.mod=='صيانة').map(p=>Object.values(p.rows).flat().length),(DB.cfg.piLog[0]||{}).rows.length]"))
  # undo button = undo the last one with something (the first correct import, since the 2nd added nothing)
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('undo btn',pg.evaluate("(document.querySelector('[data-phundo]')||{}).innerText"))
  DL.clear();pg.click('[data-phundo]');pg.wait_for_timeout(800);out('undo2 dlg',DL[:1])
  out('after undo2',pg.evaluate(f"[DB.ph.length,DB.ph.filter(p=>p.no=='1103'&&p.mo=='2026-11').length,DB.ph.filter(p=>p.mo=='2026-11'&&p.mod=='صيانة').length,!!document.querySelector('[data-phundo]')]"))
  # replace-mode later (update file): matches the maintenance record, not the completed one
  pg.set_input_files('#imp',M+'966-صيانة-Riyadh2-26-صيدلية-2026-11 (صحيح 1.3).json');pg.wait_for_timeout(1200)
  up={'ph':[dict(no='1103',mo='2026-11',mod='صيانة',sh=2,st='لم تبدأ',rows={'wh':[{'sec':'Beauty','wt':'WALL NORMAL','nm':'Complete skin care','len':'100','q':3,'rsh':'Old Turkish'}]})]}
  open(M+'t_up.json','w').write(json.dumps(up,ensure_ascii=False));DL.clear();pg.set_input_files('#imp',M+'t_up.json');pg.wait_for_timeout(1200)
  out('replace',pg.evaluate(f"[DB.ph.filter(p=>p.no=='1103'&&p.mo=='2026-11').map(p=>[p.mod,p.st,JSON.stringify(p.rows).slice(0,60)]),JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.st=='مكتملة').rows)==={json.dumps(orig)}]"))
  # single pharmacy file of a branding: still replaces the same branding record
  out('ERRS',E);br.close()
