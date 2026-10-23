# Compare out() / shr() / sav() between two builds under mocked picker / share APIs.
import sys, json
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'
SC = """async (sc)=>{const L=[];window.alert=m=>L.push('alert:'+m);window.dl=(n,t,ty)=>L.push('dl:'+n+':'+ty);
 const mk=k=>k=='ok'?async o=>{L.push('pick:'+JSON.stringify(o));return{createWritable:async()=>({write:async b=>L.push('write:'+b.size+':'+b.type),close:async()=>L.push('close')})}}:k=='abort'?async()=>{const e=new Error('a');e.name='AbortError';throw e}:k=='err'?async()=>{throw new Error('x')}:undefined;
 if(sc.p===undefined)delete window.showSaveFilePicker;else window.showSaveFilePicker=mk(sc.p);
 navigator.canShare=sc.s===undefined?undefined:(o=>{L.push('can:'+o.files[0].type);return sc.s!='no'});
 navigator.share=async o=>{L.push('share:'+o.title);if(sc.s=='abort'){const e=new Error('a');e.name='AbortError';throw e}if(sc.s=='err')throw new Error('x')};
 const r=[];r.push(String(await out('a.xlsx','DATA','application/x')));r.push(String(await shr('b.pdf','DATA','application/pdf')));r.push(String(await sav('c.json','DATA','application/json')));return r.concat(L)}"""
CASES = [dict(p=p, s=x) for p in (None, 'ok', 'abort', 'err') for x in (None, 'ok', 'no', 'abort', 'err')]
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for f in sys.argv[1:3]:
        pg = br.new_page(); pg.goto('file://' + W + f); pg.wait_for_timeout(1200)
        res[f] = [pg.evaluate(SC, {k: v for k, v in c.items() if v is not None}) for c in CASES]
    br.close()
a, b = res[sys.argv[1]], res[sys.argv[2]]
bad = [(CASES[i], a[i], b[i]) for i in range(len(CASES)) if a[i] != b[i]]
print('save/share cases', len(CASES), 'same' if not bad else 'DIFF'); [print(x) for x in bad[:5]]
print(a[6])
