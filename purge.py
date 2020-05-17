# -*- coding: utf-8 -*-
from config import *

# Purge Pics consistent with CKPT
ckpt_pics = [line.split('\t')[-1]+'.jpg' for line in LoadTxtToLines(cp_path) if 'Failed' not in line]
ClearPics(ckpt_pics)

# Purge Rest Pics
rest_pics = [f for f in os.listdir(pic_folder) if f[-4:]=='.jpg']
ClearPics(rest_pics)

# Purge CKPT and Comments
os.remove(cp_path)
os.remove(cmm_path)
if not op.exists(cp_path):
    print('Checkpoint Removed.')
if not op.exists(cmm_path):
    print('Comments Removed.')
