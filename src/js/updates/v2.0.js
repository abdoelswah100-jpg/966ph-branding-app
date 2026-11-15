// ---------- v2.0: «ستيكر خارجي» (Sticker outdoor) is kept in the warehouse like every other kind ----------
// before 2.0 it was the only kind not stored (WXT). Now: no shelf type (like Door sticker / Die Cut),
// name = المسمى (+ arrow direction when set), size = height×width, material = the outdoor sticker material.
(function(){const i=WXT.indexOf('so');if(i>=0)WXT.splice(i,1);if(!NOSH.includes('so'))NOSH.push('so')})();
const SODIR=['بدون','يمين','يسار'],soDir=r=>r&&SODIR.includes(r.dir)&&r.dir!='بدون'?r.dir:'';
const soWNm=r=>son(r)+(soDir(r)?' · سهم '+soDir(r):'');
(function(){const t=T.find(x=>x.id=='so');if(!t)return;
 if(!t.f.some(f=>f.k=='dir')){const at=t.f.findIndex(f=>f.k=='q');t.f.splice(at<0?t.f.length:at,0,sel('dir','اتجاه السهم',()=>SODIR))}
 const z0=t.z;t.z=(r,s)=>{const z=z0(r,s),d=soDir(r);return d?z.replace(son(r),son(r)+' · سهم '+d):z}})();
const _whParts20=whParts;whParts=function(t,r,s){if(t&&t.id=='so')return [{ty:t.n,nm:soWNm(r),sec:'',size:`${r.h||''}×${r.w||''}`,mat:SZ('mt.so'),f:1,sh:-1}];return _whParts20(t,r,s)};
// import check: an outdoor sticker item is valid with a known name (+ arrow) and a height×width size
const _whImpOk20=whImpOk;whImpOk=function(x){if(x&&x.ty==(T.find(t=>t.id=='so')||{}).n){const m=String(x.nm||'').split(' · سهم ');return (SON.includes(m[0])||!!m[0])&&(!m[1]||SODIR.includes(m[1]))&&/^\d+(\.\d+)?×\d+(\.\d+)?$/.test(String(x.size||'').replace(/\s+/g,''))&&x.sh==-1}return _whImpOk20(x)};
// WALL WOOD Magnetic units are the same on every shelf type → one shared stock (no shelf type), no «different shelf» warning
const _whParts20w=whParts;whParts=function(t,r,s){const L=_whParts20w(t,r,s);return t&&t.id=='wh'&&wood(r)?L.map(y=>Object.assign({},y,{sh:-1})):L};
