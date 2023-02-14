#coding:utf-8
from bs4 import BeautifulSoup
import time,requests
from probar import Pro
from lib import Restore,Checkpoint,Crawl

url = 'http://plmeizi.com/'
time_out = 15
sleep_t = 3

def getSize():
    r = requests.get(url,timeout=time_out)
    if r.status_code==200:
        html = r.text
    else:
        print("Failed to GetSize")
        return
    soup = BeautifulSoup(html,'html.parser')
    a = soup('div',attrs={'class':'list'})[0]('a')[0]
    size = eval(a['href'].split('/')[-1].split('-')[1])
    return size

def daily():
    lib_size = getSize()
    suc,num,rest = Restore(lib_size)
    start = time.perf_counter()
    last,old,last_sz = start,suc,0
    url_dict = {}
    for i in rest:
        result, url_dict = Crawl(i, lib_size, url_dict)
        Checkpoint(i,result)
        num += 1
        if result[0]=="Success":
            suc += 1
            last_sz = result[3]
        last = Pro(suc,num,last_sz,lib_size,start,last)
    new = suc-old
    if len(rest)>0:
        print("\n{} pictures added, {} pictures failed.".format(new,len(rest)-new))
    else:
        print("All {} pictures are up-to-date.".format(suc))

daily()
time.sleep(sleep_t)
