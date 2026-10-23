# Compare the output of the totals/report functions between two builds on the same data (with gandola, Add-to-cart and Medicated rows).
import sys, json
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'
D = json.load(open(W + 'out6/966-data-v1.2.json', encoding='utf-8'))
for i, p in enumerate(D['ph']):
    p['rows'].setdefault('ga', []).append({'q': 2 + i})
    p['rows'].setdefault('md', []).append({'nm': 'AVENE', 'q': 1 + i % 3})
    for r in list(p['rows'].get('eg', []))[:2]: r['r'] = 1; r['x'] = 0
DATA = json.dumps(D, ensure_ascii=False)
JS = """()=>{const o={};const P=DB.ph;o.tTot=P.map(p=>TY(p).map(t=>tTot(t,p.rows[t.id]||[])));o.z=P.map(p=>TY(p).map(t=>(p.rows[t.id]||[]).map(r=>t.z(r,p.sh))));
o.size=sizeRows(P);o.mgmt=managementReportRows(P);o.aggr=(V.q={t:'',st:'',mo:''},aggr());o.mst=JSON.stringify(mStats(P),(k,v)=>k=='al'?v.map(p=>p.no):v);
o.nq=P.map(p=>['x','r'].map(k=>nqLines(p,k).map(x=>[x.t.id,x.nm,x.pt,x.sz,x.mat,x.q,x.v,x.d])));o.pcs=T.map(t=>pcs(t));o.prog=P.map(p=>[tkProg(p,'r'),tkProg(p,'x')]);
const H=[];for(const p of P){for(const v of [{v:'sum',sm:'sum'},{v:'sum',sm:'print'},{v:'sum',sm:'mgmt'},{v:'sum',sm:'ck'},{v:'exec'},{v:'nq',nk:'x',ns:'ph',mo:p.mo},{v:'nq',nk:'r',ns:'mo',mo:p.mo}]){V=Object.assign({p:p.id,op:{},dr:{},q:{t:'',st:'',mo:''}},v);render();H.push(document.querySelector('main').innerHTML.replace(/\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}/g,'T'))}}
for(const v of [{v:'all',am:'sec'},{v:'all',am:'mg'},{v:'all',am:'ph'},{v:'month'},{v:'home'}]){V=Object.assign({op:{},dr:{},q:{t:'',st:'',mo:''}},v);render();H.push(document.querySelector('main').innerHTML.replace(/\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}/g,'T'))}
o.html=H;o.csv=csvAll();o.looker=lookerCsv();return JSON.stringify(o)}"""
R = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for f in sys.argv[1:3]:
        pg = br.new_page(viewport={'width': 400, 'height': 860}); E = []; pg.on('pageerror', lambda e: E.append(str(e)))
        pg.add_init_script("(()=>{const T=new Date('2026-10-22T09:00:00').getTime(),D=Date;class F extends D{constructor(...a){super(...(a.length?a:[T]))}static now(){return T}};window.Date=F})()")
        pg.goto('file://' + W + f); pg.wait_for_timeout(300); pg.evaluate("d=>localStorage.setItem('ads',d)", DATA); pg.reload(); pg.wait_for_timeout(1500)
        R[f] = json.loads(pg.evaluate(JS)); print(f, 'errors', E)
    br.close()
a, b = R[sys.argv[1]], R[sys.argv[2]]
for k in a:
    if a[k] == b[k]: print('same', k, len(json.dumps(a[k])))
    else:
        print('DIFF', k)
        if isinstance(a[k], list):
            for i, (x, y) in enumerate(zip(a[k], b[k])):
                if x != y: print('  first diff at', i, str(x)[:300], '|||', str(y)[:300]); break
