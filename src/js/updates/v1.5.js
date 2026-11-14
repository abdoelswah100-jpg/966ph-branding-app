// ---------- v1.5: «مقاس قريب» for every type (End cap, End gandola part by part, Floor / Wall Header, Medicated…) ----------
// same type, name, section and material, any shelf type, width and height each from 1 cm smaller to 4 cm bigger; you choose
const nearOK=(a,b)=>{const dw=b[0]-a[0],dh=b[1]-a[1],e=1e-9;if(Math.abs(dw)<e&&Math.abs(dh)<e)return null;if(dw<-1-e||dh<-1-e||dw>4+e||dh>4+e)return null;return {dw,dh,d:Math.max(Math.abs(dw),Math.abs(dh))}};
const nearX=y=>WU().filter(x=>x.ty==y.ty&&!x.old&&!x.rol&&+x.qty>=1&&nk(x.nm||'')==nk(y.nm||'')&&nk(x.sec||'')==nk(y.sec||'')&&nk(x.mat||'')==nk(y.mat||''));
const nearUnit=(t,y)=>y.ep?EGPN[y.ep]:/Header/.test(y.ty)?'هيدر':/Side/.test(y.ty)?'سايد':'قطعة';
ecNear=function(p,t,r){if(!p||p._wh||p._rc||['al','ga','ws'].includes(t.id))return [];const L=whRowPlan(t,r,p.sh);if(!L||!L.M.length)return [];const o=[];
 const add=(y,n0,k)=>{if(!(n0>0))return;const a=ecWH(y.size);if(!a)return;nearX(y).map(x=>{const b=ecWH(x.size),g=b&&nearOK(a,b);return g?{x,...g}:null}).filter(Boolean).sort((u,v)=>u.d-v.d||(+v.x.qty)-(+u.x.qty))
  .forEach(({x,dw,dh,d})=>{const n=Math.min(n0,Math.floor(+x.qty+1e-9));if(n<1)return;o.push({k,id:x.id,ep:y.ep,n,near:1,txt:`📐 مقاس قريب (فرق ${Math.round(d*10)/10} سم): ${n} ${nearUnit(t,y)} ${x.size} بدل ${y.size} (${ecDf(dw)} عرض، ${ecDf(dh)} طول${dw>0||dh>0?' — يتقص':''}) · من مخزن ${x.sh>=0?SH[x.sh]:'مشترك'} (فيه ${wq(x.qty)})`})})};
 if(t.id=='eg'&&L.M.some(y=>y.ep)){const rem=Math.max(0,qn(r)-Math.max(+r.r||0,+r.wf||0));if(!rem)return [];
  L.M.forEach(y=>{if(!y.ep||!(y.f>0))return;const need=Math.max(0,Math.round(y.f*rem-egX(r,y.ep)+1e-9))-((L.ex||{})[y.ep]||0);add(y,need,'ae')});return o}
 if(L.M.length!=1||Math.abs(L.M[0].f-1)>1e-9)return [];const need=Math.max(0,qn(r)-(+r.r||0))-Math.max(0,L.nm||0);add(L.M[0],need,'a');return o};
const _whFrom215=whFrom2;whFrom2=function(tt,j){const o=tt._wf,c=o&&o.O[j];if(!c||c.k!='ae')return _whFrom215(tt,j);
 const p=DB.ph.find(x=>x.id==o.pid),r=p&&(p.rows[o.tid]||[])[o.i],x=WU().find(y=>y.id==c.id);if(!p||!r||!x||+x.qty<c.n)return;
 whAdd(x,-c.n,'out','ph:'+p.no,'سحب لبند في الصيدلية (مقاس تاني · جزء من الجندولة: '+EGPN[c.ep]+')');{const m_=rcvSnap(p,[r]);r['wx'+c.ep]=egRd(egX(r,c.ep)+c.n);egNorm(r);rcvDiff(p,m_,'wh')}
 p.modAt=nowIso();sv();tt.remove();render();toastT('✓ اتسحب من المخزن واتحسب مستلم')};
