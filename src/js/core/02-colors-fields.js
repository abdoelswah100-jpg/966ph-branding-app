const RG=['الوسطى (الرياض)','الشرقية','الغربية','الشمالية','الجنوبية'];
const RL=p=>[p.rg,p.ct].filter(Boolean).join(' - ');
const curP=()=>V.v=='wha'?WHP():V.v=='rca'?RCP():DB.ph.find(x=>x.id==V.p);
function goV(o){V=o;render();scrollTo(0,0)}
const metaLines=p=>{const o=[];if(p.sup)o.push('المشرف: '+p.sup);if(p.co)o.push('الشركة المنفذة: '+p.co);if(p.mod||DB.cfg.modTypes[0])o.push('نوع التعديل: '+(p.mod||DB.cfg.modTypes[0]));return o};
const metaHtml=p=>`<div class="meta-panel"><div class="meta-item meta-sup">المشرف: <b>${esc(uName(p.uid)||p.sup||'عبدالله السواح')}</b>${(p.ex||[]).length?' · منفذ: <b>'+esc(p.ex.map(uName).join('، '))+'</b>':''}</div><div class="meta-item meta-co">الشركة المنفذة: <b>${esc(p.co||'عمال الشركة')}</b></div><div class="meta-item meta-mod">نوع التعديل: <b>${esc(p.mod||'براندنج جديد')}</b></div></div>`;
const WSS=S7.concat(['Thank you - نشكركم']);
const SON=['أرباحي','طلباتك','جهاز الخدمة الذاتية','أخرى'],son=r=>r.nm=='أخرى'?(r.nx||'أخرى'):(r.nm||'');
const wood=r=>r.wt&&r.wt!='WALL NORMAL';
const HRI='Health Room – Inside (داخلي)',HRO='Health Room – Outside (خارجي)',STAY='Stay Healthy (خليك صحي)';
const COL={'Thank you - نشكركم':'#FFFFFF',Beauty:'#F6C8BC',Health:'#79B38A',Pharmacy:'#2F6FD0',Personal:'#F57F93',Baby:'#7BAEAF',Medicated:'#E4E7EC',Mizan:'#BE9857','برسلات (Parcelat)':'#A8D86E','Health Room':'#1F6B3B',[HRI]:'#1F6B3B',[HRO]:'#2E7D4F',[STAY]:'#79B38A'};
// width = letter height x (w0/h0), rounded to 0.5 cm. One line per section.
const RATIO={Mizan:[55,270],Personal:[45,190],Baby:[45,185.5],Health:[45,250],Beauty:[45,242],Pharmacy:[50,118],'برسلات (Parcelat)':[21,199],[STAY]:[20,60],[HRI]:[28,200],[HRO]:[35,100]};
const ratW=(sec,lh)=>{const k=RATIO[sec];return k&&+lh>0?Math.round(+lh*k[1]/k[0]*2)/2:null};
const cl=r=>COL[r.sec]||COL[String(r.nm||'').split(' ')[0]];
const SN={Personal:'Personal Care',Baby:'Body care',Health:'Health care',Beauty:'Beauty care'};
const sel=(k,l,o)=>({k,l,o}),num=(k,l)=>({k,l,n:1}),Q=num('q','العدد');
const SEC7=sel('sec','القسم',()=>S7),SECAL=sel('sec','القسم',()=>S7.filter(x=>x!='Health Room').concat([STAY,HRI,HRO,'برسلات (Parcelat)'])),SEC4=sel('sec','القسم',()=>S4),NMF=sel('nm','المسمى',r=>nmOpts(r,r.sec=='Medicated'?MED:(NM[r.sec]||[])));
const two=r=>r.sec=='Health';
const SWO={Personal:'Beauty',Beauty:'Personal'},SWAR={Personal:'العناية',Beauty:'الجمال'};
function nmOpts(r,L){const o=r&&SWO[r.sec];return o&&r.nm&&!L.includes(r.nm)&&(NM[o]||[]).includes(r.nm)?L.concat([r.nm]):L}
const egSwap=n=>String(n||'').replace(/^(Personal|Beauty) · /,(m,a)=>SWO[a]+' · ');
function swapOf(tid,d){if(tid=='eg'){const m=/^(Personal|Beauty) · /.exec(d.nm||'');return m?SWO[m[1]]:null}if(tid=='wh'&&wood(d))return null;return SWO[d.sec]||null}
