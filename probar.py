#coding:utf-8
from math import ceil
import os.path as op
import time
M,T = [1024,'B','KB','MB','GB'],[60,'s','min','h','d']

def s(cells,box,shown=False):
    unit = box[0]
    if shown==False:
        for i in range(4):
            if cells<unit:
                return '{:.1f}'.format(cells)+box[i+1]
            cells = cells/unit
    else:
        tis = 0
        for i in range(4):
            if cells<unit:
                s = '{:.0f}'.format(cells)+box[i+1]+'{:.0f}'.format(tis)+box[i] if tis>1 else '{:.0f}'.format(cells)+box[i+1]
                break
            cells,tis = cells/unit,cells%unit
        return s

def Pro(cur,num,size,tot,start,last_t,shown=False,scale=25,max_len=80):
    cur_t = time.perf_counter()
    count = ceil((num/tot)*scale)
    a = '=' * count
    b = ' ' * (scale-count)
    c = (num/tot)*100
    dur = cur_t-start
    sp = size/float(cur_t-last_t)
    rm = (tot-num)*(cur_t-last_t)
    ratio = "{:.0f}%".format(c) if shown else ''
    if count<=scale-1:
        fi,rm = '>',s(rm,T,True)
    else:
        fi,rm = '=',''
    line = "\rGet:{}/{} All:{} {}[{}{}{}] {} {} {}".format(cur,num,tot,ratio,a,fi,b,s(dur,T,True),s(sp,M)+'/s',rm)
    line += ' '*(max_len-len(line))
    print(line,end="")
    return cur_t
