#coding:utf-8
import os,os.path as op
import shutil,time
from config import *

src_dir  = Bing_Daily_Dir
dest_dir = Mixed_Dir
sleep_t = 3

def getJPGs(dir):
    return [i for i in os.listdir(dir) if op.isfile(op.join(dir,i)) and i[-4:]=='.jpg']

def move():
    src,dest = getJPGs(src_dir),getJPGs(dest_dir)
    diff = [i for i in src if dest.count(i)==0]
    for i in diff:
        shutil.copy2(src_dir+'/'+i,dest_dir+'/'+i)
    print('{} pictures moved.'.format(len(diff)))

move()
time.sleep(sleep_t)
