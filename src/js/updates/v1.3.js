// ---------- v1.3: pharmacies import — never merges into a completed / different-type record, restore point, undo ----------
// the same pharmacy number + month can exist twice (e.g. a completed branding and a new maintenance):
// a file row matches only a record with the same modification type; a merge never goes into a completed record
const _impIdx13=impIdx;
impIdx=function(z,merge){const n=String(z.no),A=DB.ph.map((y,i)=>[y,i]).filter(([y])=>String(y.no)==n);if(!A.length)return -1;
 if(!z.mod&&!merge)return _impIdx13(z);
 let B=A.filter(([y])=>!z.mod||(y.mod||'براندنج جديد')==z.mod);if(merge)B=B.filter(([y])=>y.st!='مكتملة');
 if(z.mo){B=B.filter(([y])=>y.mo==z.mo);if(!B.length)return -1;const o=B.find(([y])=>y.st!='مكتملة');return (o||B[0])[1]}
 const c=B.filter(([y])=>y.mo==MN());if(c.length)return c[0][1];if(!B.length)return -1;B.sort((a,b)=>String(b[0].mo||'').localeCompare(String(a[0].mo||'')));return B[0][1]};
// why a file pharmacy does not merge into the record with the same number and month
function impSep(z){if(!z.mo)return null;return DB.ph.find(y=>String(y.no)==String(z.no)&&y.mo==z.mo)||null}
impWhere=function(q){const mp=q.mode==='mergePatch',L=(q.ph||[]).map(z=>{const i=impIdx(z,mp);if(i>=0)return z.no+' → '+(mp?'هتتضاف البنود على':'هتستبدل')+' شهر '+(DB.ph[i].mo||'—')+(DB.ph[i].mod?' ('+DB.ph[i].mod+')':'');const s=impSep(z);return z.no+' → '+(s?'سجل جديد'+(z.mod?' '+z.mod:'')+' (الموجودة في '+s.mo+' '+(s.st=='مكتملة'?'مكتملة':s.mod||'')+' مش هتتلمس)':'صيدلية جديدة'+(z.mo?' ('+z.mo+')':''))});
 return L.length?'\n\n'+L.slice(0,40).join('\n')+(L.length>40?'\n… و'+(L.length-40)+' كمان':''):''};
impNewer=function(q){if(q.mode==='mergePatch')return '';const L=(q.ph||[q]).map(z=>{const i=impIdx(z);if(i<0)return null;const y=DB.ph[i],t=z.modAt||q.at||'';return t&&(y.modAt||'')>t?y:null}).filter(Boolean);return L.length?`\n\n⚠ الصيدليات دي اتعدّلت في التطبيق بعد الملف، والاستبدال هيمسح التعديلات دي: ${L.map(y=>y.no+' ('+fd(y.modAt)+')').join('، ')}`:''};
const piLog=()=>DB.cfg.piLog||(DB.cfg.piLog=[]);
const newPhId=()=>{let id=Date.now();while(DB.ph.some(y=>y.id==id)||(DB.del&&DB.del[id])||(DB.trash||[]).some(t=>t.p&&t.p.id==id))id++;return id};
function phImpGo(q,fn){const mp=q.mode==='mergePatch',n=q.ph.length;
 if(!confirm((mp?'دمج '+n+' صيدلية من غير ما يتمسح حاجة؟':'استيراد '+n+' صيدلية؟ الصيدليات بنفس الرقم والشهر ونوع التعديل هتتستبدل')+impWhere(q)+impNewer(q)+'\n\nالبرنامج هياخد نقطة استرجاع قبل الاستيراد، وتقدر تتراجع عنه من «النسخ».'))return;
 snap('قبل استيراد صيدليات · '+(fn||''));const wi='p'+Date.now(),log={wi,at:nowIso(),fn:fn||'ملف',add:[],rows:[],rep:[]};
 q.ph.forEach(z=>{const i=impIdx(z,mp);
  if(mp&&i>=0){const cur=DB.ph[i];cur.rows=cur.rows||{};const pr=z.rows||{};Object.keys(pr).forEach(k=>{if(Array.isArray(pr[k])){cur.rows[k]=Array.isArray(cur.rows[k])?cur.rows[k]:[];pr[k].forEach(r=>{if(!cur.rows[k].some(a=>Object.keys(r).every(f=>f=='_i'||JSON.stringify(a[f])===JSON.stringify(r[f])))){const c={...r};c._i=rid();cur.rows[k].push(c);log.rows.push([cur.id,k,c._i])}})}});
   if(Array.isArray(z.sourceNotes)){cur.sourceNotes=cur.sourceNotes||[];z.sourceNotes.forEach(n=>{if(!cur.sourceNotes.includes(n))cur.sourceNotes.push(n)})}cur.modAt=nowIso()}
  else{mig(z);if(i>=0){z.id=DB.ph[i].id;log.rep.push(z.id);DB.ph[i]=z}else{if(z.id==null||DB.ph.some(y=>y.id==z.id)||(DB.del&&DB.del[z.id]))z.id=newPhId();DB.ph.push(z);log.add.push(z.id)}}});
 (q.tp||[]).forEach(t=>DB.tp.push(t));if(q.qi)['quotes','invoices'].forEach(k=>(q.qi[k]||[]).forEach(x=>{if(!DB.qi[k].some(y=>y.no===x.no))DB.qi[k].push(x)}));if(q.pl)Object.keys(q.pl).forEach(k=>{if(DB.pl[k]==null)DB.pl[k]=q.pl[k]});
 DB.cfg.piLog=[log].concat(piLog()).slice(0,10);norm();sv();render();toastT('✓ اتضاف '+log.add.length+' صيدلية'+(log.rows.length?' و'+log.rows.length+' بند على صيدليات موجودة':'')+(log.rep.length?' واتستبدلت '+log.rep.length:''))}
// remove pharmacies (to the trash) and rows; used by undo and by an undo file
function phRemove(ids,rows,why){let n=0,m=0;snap(why);
 ids.forEach(id=>{const q=DB.ph.find(x=>x.id==id);if(!q)return;DB.del[q.id]=nowIso();DB.ph=DB.ph.filter(x=>x.id!=q.id);DB.trash.unshift({at:nowIso(),p:q});n++});
 rows.forEach(([pid,k,ri])=>{const p=DB.ph.find(x=>x.id==pid);if(!p||!p.rows||!p.rows[k])return;const j=p.rows[k].findIndex(r=>r._i==ri);if(j<0)return;p.rows[k].splice(j,1);p.modAt=nowIso();m++});
 return [n,m]}
function piLast(){return piLog().find(l=>!l.undone&&(l.add.length||l.rows.length))||null}
function phUndo(){const l=piLast();if(!l)return;if(l.rep.length)return alert('الاستيراد ده استبدل صيدليات موجودة، والتراجع عنه بيكون من نقطة الاسترجاع «قبل استيراد صيدليات» في النسخ.');
 if(!confirm(`تراجع عن استيراد «${l.fn}» (${fd(l.at)})؟\n${l.add.length} صيدلية هتتنقل لسلة المحذوفات، و${l.rows.length} بند هيتشال من صيدليات موجودة.`))return;
 const [n,m]=phRemove(l.add,l.rows,'قبل التراجع عن استيراد صيدليات · '+l.fn);l.undone=nowIso();sv();render();toastT('✓ اتلغى الاستيراد: '+n+' صيدلية و'+m+' بند')}
// a file that removes one earlier import (made before 1.3): {kind:'966-ph-undo', note, ids:[...], strip:[{no,mo,rows:{tid:[row,...]}}]}
function phUndoFile(q){const ids=(q.ids||[]).filter(id=>DB.ph.some(x=>x.id==id)),rows=[],same=(a,b)=>Object.keys(b).every(k=>JSON.stringify(a[k])===JSON.stringify(b[k]));
 (q.strip||[]).forEach(s=>DB.ph.filter(p=>String(p.no)==String(s.no)&&(!s.mo||p.mo==s.mo)).forEach(p=>Object.keys(s.rows||{}).forEach(k=>(s.rows[k]||[]).forEach(r=>{const L=(p.rows&&p.rows[k])||[];for(let j=L.length-1;j>=0;j--){if(same(L[j],r)){if(!L[j]._i)L[j]._i=rid();if(!rows.some(x=>x[2]==L[j]._i)){rows.push([p.id,k,L[j]._i]);break}}}}))));
 const P=ids.map(id=>DB.ph.find(x=>x.id==id).no);
 if(!ids.length&&!rows.length)return alert('مفيش حاجة من الملف ده موجودة في البيانات (يمكن اتشالت قبل كده).');
 if(!confirm(`${q.note||'تراجع عن استيراد'}\n\n${ids.length} صيدلية هتتنقل لسلة المحذوفات: ${P.join('، ')}\n${rows.length} بند هيتشال من: ${[...new Set(rows.map(x=>DB.ph.find(p=>p.id==x[0]).no))].join('، ')||'—'}\n\nالبرنامج هياخد نقطة استرجاع قبلها.`))return;
 const [n,m]=phRemove(ids,rows,'قبل '+(q.note||'تراجع عن استيراد صيدليات'));sv();render();toastT('✓ اتشال '+n+' صيدلية و'+m+' بند')}
const _bkHtml13=bkHtml;bkHtml=function(){const h=_bkHtml13(),l=piLast();if(!l)return h;const k='data-pick="imp">';const i=h.indexOf(k);if(i<0)return h;const j=h.indexOf('</button>',i)+9;
 return h.slice(0,j)+`<button class="lnk" data-phundo="1">↩ تراجع عن آخر استيراد صيدليات: ${esc(l.fn)} · ${esc(fd(l.at))} (${l.add.length} صيدلية${l.rows.length?' + '+l.rows.length+' بند':''}) ›</button>`+h.slice(j)};
const _v37Click13=v37Click;v37Click=function(d,b){if(d.phundo){phUndo();return 1}return _v37Click13(d,b)};
