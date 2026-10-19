"""Refresh public feeds; never replace valid history with an empty/error response."""
import concurrent.futures, datetime as dt, json, math, pathlib, time, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:
                return json.load(r)
        except Exception:
            if attempt == 2: raise
            time.sleep(1 + attempt)
def valid(rows):
    out={r['date']:r for r in rows if math.isfinite(r['value']) and r['value']>0}
    result=sorted(out.values(),key=lambda r:r['date'])
    if len(result)<2000: raise ValueError('History too short; preserving previous data')
    return result
def usd():
    today=dt.date.today(); start=today.replace(year=today.year-10) if (today.month,today.day)!=(2,29) else today.replace(year=today.year-10,day=28)
    rows=get(f'https://api.frankfurter.dev/v2/rates?base=USD&quotes=VND&from={start}&to={today}')
    return {'source':'Frankfurter · tỷ giá tham khảo tổng hợp theo ngày','unit':'VND/USD','kind':'reference','rows':valid([{'date':r['date'],'value':float(r['rate'])} for r in rows])}
def gold():
    payload=get('https://query2.finance.yahoo.com/v8/finance/chart/GC=F?range=10y&interval=1d')
    item=payload['chart']['result'][0]
    closes=item['indicators']['quote'][0]['close']
    rows=[{'date':dt.datetime.fromtimestamp(t,dt.timezone.utc).date().isoformat(),'value':float(v)} for t,v in zip(item['timestamp'],closes) if v is not None]
    return {'source':'Yahoo Finance · COMEX Gold Futures (GC=F)','unit':'USD/oz','kind':'futures','rows':valid(rows)}
def main():
    failures=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        tasks={pool.submit(fn):name for name,fn in [('usd',usd),('gold',gold)]}
        for task in concurrent.futures.as_completed(tasks):
            name=tasks[task]
            try:
                data=task.result();data['fetchedAt']=dt.datetime.now(dt.timezone.utc).isoformat(); path=ROOT/'data'/f'{name}.json'; tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,separators=(',',':')),encoding='utf-8');tmp.replace(path)
                print(name,len(data['rows']),data['rows'][0]['date'],data['rows'][-1]['date'])
            except Exception as exc: failures.append(name); print(name,'FAILED',str(exc))
    try:
        quote=get('https://api.gold-api.com/price/XAU')
        if quote['price']<=0: raise ValueError('Invalid quote')
        (ROOT/'data'/'spot.json').write_text(json.dumps(quote),encoding='utf-8')
    except Exception as exc: print('spot snapshot unavailable:',str(exc))
    if failures: raise SystemExit('Refresh failed for '+','.join(failures))
if __name__=='__main__': main()
