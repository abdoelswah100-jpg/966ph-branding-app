// ---------- v3.1: layout heights filled automatically ----------
function wsLastH(p){const L=((p&&p.rows.ws)||[]).filter(r=>r.kd=='تخطيط'&&+r.h>0),a=L.filter(r=>r.sec!='Pharmacy');if(a.length)return +a[a.length-1].h;const b=L.filter(r=>r.sec=='Pharmacy');return b.length&&+b[b.length-1].h>10?+b[b.length-1].h-10:''}
function wsPrep(d){if(d.kd!='تخطيط'){if(d._hA){d.h='';delete d._hA}return}if(d.h===undefined||d.h===''||d._hA){const b=wsLastH(curP());if(b!==''){d.h=d.sec=='Pharmacy'?b+10:b;d._hA=1}else if(d._hA){d.h='';delete d._hA}}}
function alTh(p,sec){const L=((p&&p.rows.ws)||[]).filter(r=>r.kd=='تخطيط'&&r.sec==sec&&+r.h>0);if(!L.length)return '';const v=+L[L.length-1].h-10;return v>0?v:''}
