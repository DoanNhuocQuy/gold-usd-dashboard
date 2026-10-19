export const OUNCE_GRAMS=31.1034768;
export function theoreticalLuong(spot,fx){return spot*fx*37.5/OUNCE_GRAMS;}
export function cutoff(years,now=new Date()){const d=new Date(now),day=d.getUTCDate(),months=Math.round(years*12);d.setUTCDate(1);d.setUTCMonth(d.getUTCMonth()-months);const last=new Date(Date.UTC(d.getUTCFullYear(),d.getUTCMonth()+1,0)).getUTCDate();d.setUTCDate(Math.min(day,last));return d.toISOString().slice(0,10);}
export function filterHistory(rows,years,now=new Date()){const min=cutoff(years,now),max=now.toISOString().slice(0,10);return rows.filter(r=>r.date>=min&&r.date<=max);}
export function validRows(rows){if(!Array.isArray(rows))throw Error('Định dạng dữ liệu không hợp lệ');return rows.filter(r=>/^\d{4}-\d{2}-\d{2}$/.test(r.date)&&Number.isFinite(r.value)&&r.value>0).sort((a,b)=>a.date.localeCompare(b.date));}
export function change(a,b){return a&&b?(b/a-1)*100:null;}
