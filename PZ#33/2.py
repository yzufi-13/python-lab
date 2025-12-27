import requests
from datetime import date,timedelta
import matplotlib.pyplot as plt
import time
def get_week_range(valcode):
    end=date.today()-timedelta(days=1)
    start=end-timedelta(days=6)
    url="https://bank.gov.ua/NBU_Exchange/exchange_site"
    params={"start":start.strftime("%Y%m%d"),"end":end.strftime("%Y%m%d"),"valcode":valcode.lower(),"sort":"exchangedate","order":"asc","json":""}
    r=requests.get(url,params=params,timeout=20)
    r.raise_for_status()
    return r.json(),start,end
def get_day(d):
    url="https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    r=requests.get(url,params={"date":d.strftime("%Y%m%d"),"json":""},timeout=20)
    r.raise_for_status()
    return r.json()
def get_week_fallback(valcode):
    end=date.today()-timedelta(days=1)
    start=end-timedelta(days=6)
    out=[]
    for i in range(7):
        d=start+timedelta(days=i)
        day=get_day(d)
        m={x["cc"]:x["rate"] for x in day}
        out.append({"exchangedate":d.strftime("%d.%m.%Y"),"cc":valcode.upper(),"rate":m.get(valcode.upper())})
    return out,start,end
def get_week(valcode):
    for _ in range(3):
        try:
            return get_week_range(valcode)
        except Exception:
            time.sleep(1)
    return get_week_fallback(valcode)
def show_data(data):
    for x in data:
        print(x["exchangedate"],x["cc"],x["rate"])
def plot_data(all_data):
    for code,data in all_data.items():
        x=[]
        y=[]
        for a in data:
            x.append(a["exchangedate"])
            y.append(a["rate"])
        plt.plot(x,y,label=code.upper())
    plt.title("Курс НБУ за попередній тиждень")
    plt.xlabel("Дата")
    plt.ylabel("UAH")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
if __name__=="__main__":
    codes=["usd","eur"]
    all_data={}
    for c in codes:
        data,start,end=get_week(c)
        print("period",start,end,c.upper())
        show_data(data)
        all_data[c]=data
        print()
    ans=input("побудувати графік? (y/n): ").strip().lower()
    if ans=="y":
        plot_data(all_data)
    else:
        print("графік не побудовано")