#coding:utf-8
from bs4 import BeautifulSoup
from chardet import detect
from math import ceil
import os.path as op
import requests
import os,re,time
from config import *

time_out = 5
deli = [r' ',r'<br/>',r'<br>']
rest,date = [],[]
T = [60,'s','min','h','d']
Sensitive_Words = '''"/\|<>*?:'''
CR_Deli = ' (© '

def Sep(s,deli):
    list,sep = [],''
    for i in deli:
        if s.find(i)!=-1:
            sp = s.split(i,1)
            list.append(sp[0])
            s,sep = sp[1],i
    list.append(s)
    if len(list)==2 and CR_Deli in list[1]:
        b,a = list[1].split(CR_Deli)
        list = [list[0]+sep+b,CR_Deli[1:]+a]+list[2:]
    return list

def Date(s):
    return eval(re.findall(r'[\d]+-[\d]+-[\d]+',s)[0].replace('-',''))

def Strip(lista):
    listb = []
    for i in lista:
        if listb.count(i)==0:
            listb.append(i)
    return listb

def Rename(f):
    for ch in Sensitive_Words:
        f = f.replace(ch,'')
    flist = [i for i in os.listdir(pic_folder) if len(re.findall(r'^{}(|\d+).jpg$'.format(f),i))>0]
    f = f+str(len(flist)+1) if len(flist)>0 else f
    return f

def SavePic(refer,url,fname,rdate,dir_path):
    headers['Referer'] = refer
    try:
        r = requests.get(url,headers=headers,timeout=time_out)
    except:
        print('\r{}\tConnection Time Out'.format(url))
        return ['Failed']
    if r.status_code!=200:
        print('\r{}\tStatus Error Code {}'.format(url,r.status_code))
    elif eval(r.headers['content-length'])<=1024:
        print('\r{}\tEmpty File Size {}bytes'.format(url,r.headers['content-length']))
    else:
        path = dir_path+'/'+fname+'.jpg'
        with open(path,'wb') as f:
            f.write(r.content)
        if op.isfile(path):
            return ['Success',rdate,fname,op.getsize(path)]
        print('\r{}\tWrite to File Failed'.format(url))
    return ['Failed']

def WrtTxt(txt,d):
    pos = -1
    for i in date:
        if d>i[0]:
            pos = date.index(i)
            break
    if pos==-1:
        date.append([d,txt])
    else:
        date.insert(pos,[d,txt])
    txt = '\n\n'.join([header]+[i[1] for i in date]+[''])
    open(cmm_path, 'wb').write(txt.encode('utf-8'))
    return "Success"

def Crawl(n):
    url = main_url+str(n)
    try:
        r = requests.get(url,timeout=5)
        r.encoding = 'utf-8'
    except:
        return ["Failed"]
    if r.status_code==200:
        html = r.text
    else:
        return ["Failed"]
    soup = BeautifulSoup(html,'html.parser')
    h1 = soup.find_all('h1')[0]
    rdate = h1.find_all('strong')[0].string
    date = rdate[:4]+'-'+rdate[4:6]+'-'+rdate[6:]
    span_str = str(soup.find_all('span',id="title")[0])
    span = re.findall(r'<span id="title">(.*?)</span>',span_str)[0]
    titles = [date]+Sep(span,deli)
    if len(titles)==3:
        titles += ['No Comments']
    if len(titles)!=4 or WrtTxt('\n'.join(titles),eval(rdate))=="Failed":
        return ["Failed"]
    pic_url = 'http:'+soup.find_all('a',id="picurl")[0]['href']
    return SavePic(url,pic_url,Rename(titles[1]),eval(rdate),pic_folder)

def Checkpoint(n,result):
    if result[0]=="Success":
        cp = "{}\t{}\t{}\t{}\n".format(n,"Success",result[1],result[2])
    else:
        cp = "{}\t{}\n".format(n,result[0])
    open(cp_path,'ab').write(cp.encode('utf-8'))

def Restore(lib_size):
    global rest,date
    suc,num = 0,0
    all = [i for i in range(1,lib_size+1)][::-1]
    if op.exists(cp_path):
        cp_lines = LoadCheckpoint(cp_path)
        suc,num = len([eval(li[0]) for li in cp_lines if li[1]=="Success"]),len(cp_lines)
        done = [eval(li[0]) for li in cp_lines]
        rest = [i for i in all if done.count(i)==0]
        comments = open(cmm_path, 'rb').read().decode('utf-8').split('\n\n')[1:-1]
        date = Strip([[Date(i),i] for i in comments])
        date.sort(key=lambda x:x[0],reverse=True)
        cmm_txt = '\n\n'.join([header]+[i[1] for i in date]+[''])
        open(cmm_path, 'wb').write(cmm_txt.encode('utf-8'))
    else:
        open(cmm_path, 'w+').write(header)
        rest = all
    return [suc,num,rest]
