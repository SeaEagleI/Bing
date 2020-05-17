import os.path as op
from lib import *
from config import *
import time

# Get Statistics
cp_lines = LoadCheckpoint(cp_path)
cmm_lines = LoadComments(cmm_path)
date_fnames = dict([rec_line[-2:] for rec_line in cp_lines if rec_line[1]=='Success'])
err_cmm_lines,err_dates = [],[]
for lines in cmm_lines:
    if lines[0]>='2019-03-01' and CR_Deli in lines[2]:
        err_cmm_lines.append(lines)
        err_dates.append(DateTrans(lines[0]))
piclist = [fname.replace('.jpg','') for fname in os.listdir(pic_folder)]

# Clear Checkpoint
cp_txt_lines = []
for rec_line in cp_lines:
    if rec_line[-1] == 'Failed':
        continue
    date,picName = rec_line[-2:]
    if date not in err_dates and picName in piclist:
        cp_txt_lines.append('\t'.join(rec_line))
cp_txt = '\n'.join(cp_txt_lines)
open(cp_path,'wb').write(cp_txt.encode('utf-8'))
new_cp_lines = LoadCheckpoint(cp_path)
print('[Checkpoint]:\tCleared {} Err_Msgs.'.format(len(cp_lines)-len(new_cp_lines)))
# Clear Comments
crt_cmm_lines = ['\n'.join(lines) for lines in cmm_lines if DateTrans(lines[0]) not in err_dates]
cmm_txt = '\n\n'.join([header]+crt_cmm_lines+[''])
open(cmm_path, 'wb').write(cmm_txt.encode('utf-8'))
new_cmm_lines = LoadComments(cmm_path)
print('[Comments]:\tCleared {} Err_Msgs.'.format(len(cmm_lines)-len(new_cmm_lines)))
# Clear Pictures
clr_pics = [date_fnames[DateTrans(lines[0])]+'.jpg' for lines in err_cmm_lines]
ClearPics(clr_pics)

print('Files Refreshed Successfully.')
print('Exiting...')
time.sleep(1)
