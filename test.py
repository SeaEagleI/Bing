import requests
from lib import *
from config import *

def PrintList(_list,label):
    print('\n[{}]: {}'.format(label,len(_list)))
    for i,element in enumerate(_list):
        print('[{}]\t{}'.format(i+1,element))

# Connection Test
def SavePic(url):
    print(url)
    try:
        r = requests.get(url,headers=headers,timeout=time_out)
    except:
        print("conn timeout")
        return ["Failed"]
    if r.status_code!=200 or eval(r.headers['content-length'])==0:
        print("status_err {} or empty_file {}".format(r.status_code,r.headers['content-length']))
        return ["Failed"]
    path = url.split('/')[-1]
    with open(path,'wb') as f:
        f.write(r.content)
    if op.isfile(path):
        return ["Success",op.getsize(path)]
    print('write to file failed')
    return ["Failed"]

# url = 'http://bimgs.plmeizi.com/images/bing/2018/TheaterLostSouls_ZH-CN9247537981_1920x1080.jpg'
# SavePic(url)

# Get Statistics
piclist = [f[:-4] for f in os.listdir(pic_folder) if f[-4:]=='.jpg']
suc_cp_lines = [rec_line for rec_line in LoadCheckpoint(cp_path) if rec_line[1]=='Success']
cmm_lines = LoadComments(cmm_path)

# Consistency Check
if len(suc_cp_lines)==len(piclist):
    print('CKPT==PICS')
if len(suc_cp_lines)==len(cmm_lines):
    print('CKPT==CMM')

# Generally, We have CKPT<PICS<CMM (Consider Exe Order)
print('[CKPT]: {}'.format(len(suc_cp_lines)))
print('[PICS]: {}'.format(len(piclist)))
print('[CMM] : {}'.format(len(cmm_lines)))

# Get Extra/Inconsistent List
cp_pics = [rec_line[-1] for rec_line in suc_cp_lines]
cp_dates = [rec_line[-2] for rec_line in suc_cp_lines]
inc_piclist = list(set(piclist).difference(set(cp_pics)))
inc_cmm_lines = [lines for lines in cmm_lines if DateTrans(lines[0]) not in cp_dates]

PrintList(inc_piclist,'INC_PICS')
PrintList(inc_cmm_lines,'INC_CMM')
