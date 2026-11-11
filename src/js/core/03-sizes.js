const SZD={
'wh.h':['20','20','17.5','20','17'],'wh.len':['100','80','50'],'wh.wood':['24×85','19×85'],
'fh.ws':'14.5×56.5','fh.wl':'14.5×76.5','fh.s':['11.5×57','14×59','17.5×100','12×53.5','11.5×57'],'fh.l':'11.5×76',
'ec.0':['صغير 64×111','كبير 81×123'],'ec.1':['صغير 64×111','كبير 81×123'],'ec.2':['صغير 64×111','كبير 81×123'],'ec.3':['صغير 67×117','كبير 88×132'],'ec.4':['صغير 70.5×116','كبير 80×122','كبير 91.5×122'],
'eg.hs':['61×22','61×22','50×66','62×22','63.8×28.3'],'eg.hl':['77×22','77×22','50×66','86×22','89×28'],
'eg.ss':['25×101','25×101','30×120','124×32','90×22'],'eg.sl':['25×101','25×101','30×120','135×32','103×33'],
'md.h':'12×83','md.s':['30×75','30×75','30×75','33×72','43×85'],
'saw':['215×35','215×40','215×45'],
'saf.0':['صغير 30×120','كبير 40×136','كبير 30×140','كبير 30×130'],'saf.1':['صغير 30×120','كبير 40×136','كبير 30×140','كبير 30×130'],
'saf.2':['صغير 30×120','كبير 40×130','كبير 30×135'],'saf.3':['صغير 30×120','كبير 40×136','كبير 30×140','كبير 30×130'],
'saf.4':['صغير 30×120','صغير 40×130','كبير 40×136','كبير 30×140'],
'ds':['صغير 100×5','كبير 200×5'],'c4':['صغير 40×100','كبير 50×180'],'fr':'30×60','dc':'40×45',
'abs.Decorative nail':'—|مسمار','abs.Acrylic board A3':'A3|أكريليك','abs.Acrylic board pockets 5':'50×111|أكريليك','abs.Acrylic board pockets 4':'55×80|أكريليك','abs.No smoking acrylic':'15×15|أكريليك',
'mt.fhx':['ستيكر + تصنيع أكريليك','ستيكر فقط'],'mt.ws':'ستيكر','mt.so':'Sticker outdoor + Laminate','mt.wh':'ستيكر','mt.fh':['باك لايت','باك لايت','ستيكر','باك لايت','باك لايت'],'mt.ec':'باك لايت','mt.egh':['باك لايت','باك لايت','ستيكر','باك لايت','باك لايت'],'mt.egs':['ستيكر','ستيكر','باك لايت','ستيكر','ستيكر'],'mt.md':'باك لايت','mt.sa':'أكريليك','mt.al':'أكريليك 8 مم','mt.st':'ستيكر'};
const SZ=k=>{const o=DB&&DB.cfg&&DB.cfg.sz&&DB.cfg.sz[k];return o!=null?o:SZD[k]};
const ABV=i=>{const v=String(SZ('abs.'+i)||'—|—').split('|');return[(v[0]||'—').trim(),(v[1]||'—').trim()]};
const ALLM=()=>{const m=new Set();Object.keys(SZD).forEach(k=>{if(k.startsWith('mt.'))[].concat(SZ(k)).forEach(x=>m.add(String(x).trim()));if(k.startsWith('abs.'))m.add(ABV(k.slice(4))[1])});m.delete('—');m.delete('');return[...m].sort((a,b)=>b.length-a.length)};
function noCk(R){Object.values(R||{}).forEach(a=>{if(Array.isArray(a))a.forEach(r=>{delete r.ck;delete r.r;delete r.x})});return R}
const ABN=['انسى الانتظار','ارباحي','اترك لهم الباقي','يحظر صرف دواء','الضمان الصحي','نقاتي stc'],ABA3='Acrylic board A3',abNm=r=>r?(r.it==ABA3&&r.an&&ABN.includes(r.an)?r.it+' · '+r.an:r.it||''):'';
const FRK=['ثلاجة عصير','ثلاجة أدوية'],frAd=k=>'Fridge sticker - '+(k||FRK[0]);
const EGS2={'Personal · Premium Deo · مزيلات عرق طبية':'عناية'},EGB4=['اطفال','صحة','عناية','جمال'],EGSEC={Personal:'عناية',Beauty:'جمال',Baby:'اطفال',Health:'صحة'},egSN=(r,sh)=>{if(sh!=2||!r||EGB4.includes(r.nm))return null;if(EGS2[r.nm])return {nm:EGS2[r.nm],sec:''};const m=/^(Personal|Beauty|Baby|Health)\b/.exec(r.nm||'');return m?{nm:EGSEC[m[1]],sec:''}:null},egX=(r,ep)=>+(r&&r['wx'+ep])||0,egXs=r=>egX(r,'h')+egX(r,'s')+egX(r,'a');
const ABI=['Decorative nail','Acrylic board A3','Acrylic board pockets 5','Acrylic board pockets 4','No smoking acrylic'];
const ABD0=()=>['Acrylic board pockets 5','Acrylic board pockets 4','No smoking acrylic'].map(i=>({it:i,q:1,stt:'تصنيع وتركيب'}));
// automatic boards of a new pharmacy: Branding modification = install only (No smoking made + installed), new Branding = made + installed, maintenance = none
const ABD=mod=>{if(mod===undefined)return ABD0();if(mod=='صيانة')return [];const m=mod=='تعديل براندنج'?'تركيب فقط':'تصنيع وتركيب';return ABN.slice(0,5).map(n=>({it:ABA3,an:n,q:1,stt:m})).concat([{it:'Acrylic board pockets 4',q:1,stt:m},{it:'Acrylic board pockets 5',q:1,stt:m},{it:'No smoking acrylic',q:1,stt:'تصنيع وتركيب'}])};
