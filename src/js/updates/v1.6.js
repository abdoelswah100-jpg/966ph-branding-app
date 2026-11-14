// ---------- v1.6: «مقاس قريب» smaller than needed → a clear warning (e.g. Turkish header 61×22 on the wider Ukraine shelf 62×22) ----------
nearWarn=function(p,dw,dh){const e=1e-9,a=[];if(dw<-e)a.push('أضيق بـ '+(Math.round(-dw*10)/10)+' سم');if(dh<-e)a.push('أقصر بـ '+(Math.round(-dh*10)/10)+' سم');if(!a.length)return '';
 return ' ⚠ '+a.join(' و')+' من مقاس رف '+(p&&p.sh>=0?SH[p.sh]:'الصيدلية')+(dw<-e?' (الرف أعرض)':'')+' — اتأكد إنه ينفع'};
