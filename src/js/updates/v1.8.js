// ---------- v1.8: WALL WOOD Magnetic UNITS for every section, with any name of the section ----------
// sizes stay the two WALL WOOD sizes (wh.wood: 24×85 / 19×85). Beauty keeps its 3 usual names first.
const WDN=['Hair colorants','Beauty Devices','Lenses'];
const woodNames=r=>{const L=(NM[r.sec]||[]).slice();return r.sec=='Beauty'?WDN.concat(L.filter(n=>!WDN.includes(n))):L};
(function(){const t=T.find(x=>x.id=='wh');if(!t)return;const fw=t.f.find(x=>x.k=='wt'),fn=t.f.find(x=>x.k=='nm');
 if(fw)fw.o=()=>['WALL NORMAL','WALL WOOD Magnetic UNITS'];
 if(fn){const o0=fn.o;fn.o=(r,s)=>wood(r)?nmOpts(r,woodNames(r)):o0(r,s)}})();
