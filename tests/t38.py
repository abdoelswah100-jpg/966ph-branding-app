# v3.4 part 1: custody — invoices without a paper invoice (count, filter, picker, share/save files), wider description
import json, zipfile, io, re
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new34.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
CJ=W+'cust/عهدة شهر 10-2026 - للاستيراد.json'
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860},accept_downloads=True);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[]
  def dlg(x):DL.append(x.message[:200]);x.accept()
  pg.on('dialog',dlg);FL=[];pg.on('download',lambda d:FL.append(d))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#cjson',CJ);pg.wait_for_timeout(800)
  # mark 3 invoices as no paper, one long description, a photo on two of them and a PDF on one
  pg.evaluate("""(async()=>{const M=cMo(),L=M.items.filter(x=>!x.qt);[2,5,9].forEach(i=>{L[i].note=NOPAPER});L[5].desc='تركيب استيكرات وأكريليك قسم الجمال والعناية في صيدلية 510 شقراء مع نقل المواد من المستودع';
     const c=document.createElement('canvas');c.width=300;c.height=200;const g=c.getContext('2d');g.fillStyle='#c33';g.fillRect(0,0,300,200);const b=await new Promise(r=>c.toBlob(r,'image/png'));
     await idbSet('cimg:t1:a',b);L[2].imgs=['cimg:t1:a'];await idbSet('cimg:t2:a',b);L[0].imgs=['cimg:t2:a'];
     const pdf=new Blob(['%PDF-1.4\\n%test\\n'],{type:'application/pdf'});await idbSet('cimg:t3:a:pdf',pdf);L[9].imgs=['cimg:t3:a:pdf'];sv();render()})()""");pg.wait_for_timeout(500)
  out('tile',pg.evaluate("(e=>e&&e.innerText.replace(/\\s+/g,' '))(document.querySelector('.cnpk'))"))
  n_all=pg.evaluate("document.querySelectorAll('.ctab tr[data-ced]').length")
  pg.click('.cnpk');pg.wait_for_timeout(200)
  out('filter',[n_all,pg.evaluate("[...document.querySelectorAll('.ctab tr[data-ced] td.cnum')].map(t=>t.innerText)"),pg.evaluate("document.querySelector('.cnpk').innerText.includes('اعرض الكل')")])
  pg.click('.cnpk');pg.wait_for_timeout(200);out('unfilter',pg.evaluate("document.querySelectorAll('.ctab tr[data-ced]').length")==n_all)
  # menu
  pg.click('[data-cmenu=save]');pg.wait_for_timeout(200);out('menu',pg.evaluate("[...document.querySelectorAll('.csh button')].map(b=>b.innerText.trim())"))
  pg.click('.csh [data-cnpk="save:np"]');pg.wait_for_timeout(200)
  out('picker',pg.evaluate("[...document.querySelectorAll('.cnpi')].filter(l=>l.querySelector('input').checked).map(l=>l.innerText.replace(/\\s+/g,' ').slice(0,60))"))
  # add invoice 1 (has a photo), remove nothing
  pg.click('.cnpi:nth-child(1) input');pg.wait_for_timeout(100);out('count_btn',pg.evaluate("document.querySelector('[data-cnpgo]').innerText"))
  n0=len(DL)
  pg.click('[data-cnpgo]');pg.wait_for_timeout(4000)
  out('missing_confirm',DL[n0:])
  out('np_files',[f.suggested_filename for f in FL])
  # full: Excel + PDF + invoices
  FL.clear();pg.click('[data-cmenu=save]');pg.wait_for_timeout(200);pg.click('.csh [data-cnpk="save:all"]');pg.wait_for_timeout(200);pg.click('[data-cnpgo]');pg.wait_for_timeout(6000)
  out('all_files',[f.suggested_filename for f in FL])
  x=[f for f in FL if f.suggested_filename.endswith('.xlsx')]
  if x:
    pth=W+'t38.xlsx';x[0].save_as(pth);z=zipfile.ZipFile(pth);sh=z.read('xl/worksheets/sheet1.xml').decode()
    out('xlsx',[re.findall(r'<col min="4"[^>]*>',sh),'عدد الفواتير بدون فاتورة ورقية: 7' in sh,re.findall(r'<row r="(\d+)" ht="(\d+)"',sh)[:12]])
  out('pdf_el',pg.evaluate("(el=>[el.querySelector('.cnpline').innerText,!!el.querySelector('th.cdsc')])(custPdfEl(CU().cur))"))
  # desc preview in the edit screen
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.click('[data-cman]');pg.wait_for_timeout(200)
  pg.fill('[data-cf=desc]','جملة طويلة جدا للبيان علشان نشوفها كاملة تحت الخانة وإحنا بنكتب');pg.wait_for_timeout(100)
  out('desc_prev',pg.evaluate("(e=>[e.hidden,e.innerText.length])(document.querySelector('.cdsp'))"))
  out('ERRS',E)
  br.close()
