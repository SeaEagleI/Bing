# -*- coding: utf-8 -*-
from config import *

# Purge Pics consistent with CKPT
ckpt_pics = [line[-1]+'.jpg' for line in LoadCheckpoint(cp_path) if line[1]=='Success']
ClearPics(ckpt_pics)

# # Purge Rest Pics
# rest_pics = [f for f in os.listdir(pic_folder) if f[-4:]=='.jpg']
# ClearPics(rest_pics)

# # Purge CKPT and Comments
# os.remove(cp_path)
# os.remove(cmm_path)
# if not op.exists(cp_path):
#     print('Checkpoint Removed.')
# if not op.exists(cmm_path):
#     print('Comments Removed.')
