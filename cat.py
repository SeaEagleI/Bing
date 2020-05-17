#coding:utf-8
import os,re
import requests

turns = 20
time_out = 5
dir = '/home/andrew/Pictures/Bing/Cat'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
random = 'https://api.i-meto.com/bing'
latest = 'https://api.i-meto.com/bing?new'
color = 'https://api.i-meto.com/bing?color='
cat = 'https://api.i-meto.com/bing?cat='
colors = ['Blue','Brown','Green','Multi','Orange','Pink','Purple','Red','White','Yellow']
cats = ['A','C','N','S','T']
dict = {'A':"Animal",'C':'Culture','N':"Nature","S":"Space",'T':"Travel"}
suc = 0

def Rename(f):
    flist = [i for i in os.listdir(dir) if len(re.findall(r'^{}(|\d+).jpg$'.format(f),i))>0]
    f = f+str(len(flist)+1) if len(flist)>0 else f
    return f

def down(url,fname):  
    global suc
    try:
        r = requests.get(url,headers=headers,timeout=time_out)
        path = dir+'/'+Rename(fname)+'.jpg'
        open(path,'wb').write(r.content)
        suc += 1
        print('\rNow Get {}/{} Images.'.format(suc,len(os.listdir(dir))),end='')
    except:
        pass

def Get():
    down(random,'random')
    #down(latest,'new')
    for i in colors:
        down(color+i,i)
    for i in cats:
        down(cat+i,dict[i])

def main():
    print('\rNow Get {}/{} Images.'.format(suc,len(os.listdir(dir))),end='')
    for i in range(1,turns+1):
        Get()

main()
