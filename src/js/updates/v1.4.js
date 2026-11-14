// ---------- v1.4: «ضفها للسلة» names — the stock without a name becomes «الأساسي» (restore point first) ----------
const GAR=/^ضفها للسلة - /;
function gaFix14(){const W=DB.wh||[];if(!W.some(x=>GAR.test(x.ty)&&!x.nm)&&!(DB.ph||[]).some(p=>((p.rows||{}).ga||[]).some(r=>r&&!r.nm)))return;
 if(!DB.cfg.m14ga){try{snapLater('قبل تحديث 1.4 (مسميات ضفها للسلة)',JSON.stringify(dbOut()))}catch(e){}DB.cfg.m14ga=nowIso()}
 let ch=0;W.forEach(x=>{if(GAR.test(x.ty)&&!x.nm){x.nm=GAL[0];ch=1}});
 if(ch){for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));if(W[i].min!==''&&W[i].min!=null&&(W[j].min===''||W[j].min==null))W[j].min=W[i].min;W.splice(i,1)}}}
 (DB.ph||[]).forEach(p=>{((p.rows||{}).ga||[]).forEach(r=>{if(r&&!r.nm)r.nm=GAL[0]});
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(!e)return;let k2=k;if(GAR.test(e.ty||'')&&!e.nm){e.nm=GAL[0];k2=whKey(e)}if(o[k2])o[k2].q=wq(+o[k2].q+(+e.q||0));else o[k2]=e});p.whT=o}});
 svq()}
const _WU14=WU;WU=function(){const W=_WU14();if(W.some(x=>!x.nm&&GAR.test(x.ty)))gaFix14();return DB.wh};
const _render14=render;render=function(){try{if(DB&&DB.ph&&DB.ph.some(p=>((p.rows||{}).ga||[]).some(r=>r&&!r.nm)))gaFix14()}catch(e){console.error(e)}return _render14.apply(this,arguments)};

// ---------- v1.4: warehouse import — size without «صغير / كبير», «ضفها للسلة» without a name = «الأساسي» ----------
const _whImpNorm14=whImpNorm;whImpNorm=function(z){const o=_whImpNorm14(z);o.size=String(o.size||'').replace(/^(عريض\s+)?(صغير|كبير)\s+(?=\d)/,'');if(GAR.test(o.ty)&&!o.nm)o.nm=GAL[0];return o};

// ---------- v1.4: End cap «مقاس قريب» — same name, section and material, any shelf type: up to 1 cm smaller or 4 cm bigger ----------
const ecWH=s=>{const m=/(\d+(?:\.\d+)?)×(\d+(?:\.\d+)?)/.exec(String(s||'').replace(/\s*[x×*]\s*/i,'×'));return m?[+m[1],+m[2]]:null};
const ecDf=v=>(v>0?'+':'')+(Math.round(v*10)/10);
function ecNear(p,t,r){if(!p||p._wh||p._rc||t.id!='ec')return [];const need=Math.max(0,qn(r)-(+r.r||0));if(!need)return [];
 const L=whRowPlan(t,r,p.sh),y=L&&L.M[0];if(!y)return [];const rem=need-Math.min(need,L.nm||0);if(rem<=0)return [];const a=ecWH(y.size);if(!a)return [];
 return WU().filter(x=>x.ty=='End cap'&&!x.old&&+x.qty>=1&&nk(x.nm||'')==nk(y.nm||'')&&nk(x.sec||'')==nk(y.sec||'')&&nk(x.mat||'')==nk(y.mat||'')).map(x=>{const b=ecWH(x.size);if(!b)return null;const dw=b[0]-a[0],dh=b[1]-a[1];
   if(Math.abs(dw)<1e-9&&Math.abs(dh)<1e-9)return null;if(dw<-1-1e-9||dh<-1-1e-9||dw>4+1e-9||dh>4+1e-9)return null;return {x,dw,dh,d:Math.max(Math.abs(dw),Math.abs(dh))}}).filter(Boolean).sort((u,v)=>u.d-v.d||(+v.x.qty)-(+u.x.qty))
  .map(({x,dw,dh,d})=>{const n=Math.min(rem,Math.floor(+x.qty));return {k:'a',id:x.id,n,near:1,txt:`📐 مقاس قريب (فرق ${Math.round(d*10)/10} سم): ${n} قطعة ${x.size} بدل ${y.size} (${ecDf(dw)} عرض، ${ecDf(dh)} طول${dw>0||dh>0?' — تتقص':''}) · من مخزن ${x.sh>=0?SH[x.sh]:'مشترك'} (فيه ${wq(x.qty)})`}})}
const _whFromOpts14=whFromOpts;whFromOpts=function(p,t,r){const o=_whFromOpts14(p,t,r);let e=[];try{e=ecNear(p,t,r)}catch(er){console.error(er)}return e.length?o.concat(e.filter(c=>!o.some(z=>z.k=='a'&&z.id==c.id))):o};

// ---------- v1.4: the sync button with a pharmacies / warehouse / undo file: goes to the right import (never «newest pharmacy wins») ----------
// a laptop / Drive backup always has the settings (cfg); a pharmacies file from Claude or from «استيراد ملف صيدلية» does not
const isPhFile=q=>!!(q&&Array.isArray(q.ph)&&(q.mode==='mergePatch'||q.mode==='replace'||!q.cfg));
function syncRoute(q,fn){if(!q)return 0;
 if(q.kind=='966-warehouse'){alert('الملف ده ملف مخزن، مش ملف مزامنة.\nهيتفتح في «استيراد للمخزن» (بيضيف على الرصيد ومش بيمسح حاجة).');whImpOpen(q,fn);return 1}
 if(q.kind=='966-ph-undo'){alert('الملف ده ملف تراجع عن استيراد صيدليات، مش ملف مزامنة.\nهيتفتح في «استيراد ملف صيدلية».');phUndoFile(q);return 1}
 if(isPhFile(q)){if(!confirm('⚠ الملف ده ملف صيدليات («'+fn+'»)، مش نسخة مزامنة من جهاز تاني.\nزرار المزامنة بياخد «الصيدلية الأحدث» وممكن يستبدل صيدلية موجودة بنفس الرقم (زي اللي حصل في 1103).\n\nهيتستورد بطريقة «استيراد ملف صيدلية أو دمج نسخة» (صيدلية مكتملة أو نوع تعديل مختلف بيتعمل لها سجل منفصل، ونقطة استرجاع قبلها). تكمل؟'))return 1;phImpGo(q,fn);return 1}
 return 0}
