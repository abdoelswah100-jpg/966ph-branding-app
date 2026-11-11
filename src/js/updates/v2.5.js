// ---------- v2.5: second layout slot, photo limits in settings ----------
const isPdfF=(f,t)=>/pdf/i.test((f&&f.type)||t||'')||/\.pdf$/i.test((f&&f.name)||'');
function planSlot(p,f){const A=p.att||{};if(!A.plan)return 'plan';const a=isPdfF(null,A.plan.t)||/\.pdf$/i.test(A.plan.n||''),b=isPdfF(f);return a!=b?'plan2':'plan'}
function v25Change(x){if(x.id=='cfphb'||x.id=='cfpha'){const v=Math.max(1,Math.min(60,Math.round(+x.value||0)));DB.cfg[x.id=='cfphb'?'phB':'phA']=v;x.value=v;svq();toastT('✓ اتحفظ: أقصى '+v+' صورة '+(x.id=='cfphb'?'قبل':'بعد'));return 1}return 0}
