import os,os.path as op
from os.path import join as Join
from tqdm import tqdm

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
"Referer": "",
"Sec-Fetch-Mode": "no-cors",
"Connection": "keep-alive"
}

#Daily-Config
main_url  = 'http://bing.plmeizi.com/show/'
header    = '今日美图首页'
User_Name = '57460'

#Desktop_Dir    =  'C:/Users/'+User_Name+'/Desktop/'
#Desktop_Dir    =  'D:/'
Python_Dir     =  'D:/Python'
Pictures_Dir   =  'D:/Pictures'
Bing_Daily_Dir =  Join(Pictures_Dir,'Bing/Date')
Bing_Codes_Dir =  Join(Python_Dir,'Bing/Date')
Mixed_Dir      =  Join(Pictures_Dir,'Mixed')

cur_folder     =  Join(Python_Dir,'Web/CrawlMasPic/Bing')
pic_folder     =  Join(Pictures_Dir,'Bing/Date')
cmm_path       =  Join(pic_folder, 'Comments')
cp_path        =  Join(cur_folder,'.checkpoint')
mv_dest_dir    =  Mixed_Dir

# Load Files
# def GetTxt(path):
#     return open(path,'rb').read().decode('utf-8')
# def LoadTxtToLines(path,sep='\n'):
#     return [line for line in open(path,'rb').read().decode('utf-8').split(sep) if len(line)>0]
def LoadCheckpoint(cp_path):
    return [rec_line.split('\t') for rec_line in open(cp_path,'rb').read().decode('utf-8').split('\n') if len(rec_line)>0]
def LoadComments(cmm_path):
    return [lines.split('\n') for lines in open(cmm_path,'rb').read().decode('utf-8').split('\n\n')[1:-1]]
# Purge Files
def ClearFile(fpath):
    if op.exists(fpath):
        os.remove(fpath)
    else:
        return 'Empty'
    return 'Failed' if op.exists(fpath) else 'Success'
def ClearPics(piclist):
    suc = 0
    for picName in tqdm(piclist):
        picPath1,picPath2 = op.join(pic_folder,picName),op.join(mv_dest_dir,picName)
        results = [ClearFile(picPath1),ClearFile(picPath2)]
        if 'Failed' in results:
            print('Failed to remove {}'.format(picName))
        suc += results.count('Success')
    print('[Pictures]:\tCleared {} Err_Pics.'.format(suc))
    # print('[Pictures]:\tCleared {} Err_Pics.'.format(2*len(piclist)))
# Utils
def DateTrans(cmm_date):
    return cmm_date.replace('-','')

#Cat-Config
