from PIL import Image
from PIL import ImageChops
import numpy as np
import os

# frame width
width = 1920
# frame height
height = 1080
# Current P frame (first is 2)
fr_now = 2
# frame image directory
img_folder = '/home/user/mv-get-realtime/frames'
with open('delta.txt', 'w') as fout, open("f_all.txt", "r") as fin:
    for line in fin:
        mv = line.split()
        fr = mv[0]
        x0 = int(mv[4])
        y0 = int(mv[5])
        x1 = int(mv[6])
        y1 = int(mv[7])
        if fr_now != fr:
            filepath_src = os.path.join(img_folder, fr + '.png')
            filepath_dst = os.path.join(img_folder, str(int(fr) - 1) + '.png')
            img_src = Image.open(filepath_src)
            img_dst = Image.open(filepath_dst)
            fr_now = fr

        mb_src_left = x0 - 8  
        mb_src_top = y0 - 8 
        mb_src_right = x0 + 8 
        mb_src_bottom = y0 + 8 

        mb_dst_left = x1 - 8 
        mb_dst_top = y1 - 8 
        mb_dst_right = x1 + 8 
        mb_dst_bottom = y1 + 8 

        img_mb_src = img_src.crop((mb_src_left, mb_src_top, mb_src_right, mb_src_bottom)) 
        img_mb_dst = img_src.crop((mb_dst_left, mb_dst_top, mb_dst_right, mb_dst_bottom)) 
        # print(img_mb_src.size, img_mb_dst.size)
        
        arr_mb_src = np.array(img_mb_src.convert('RGB')).ravel()
        arr_mb_dst = np.array(img_mb_dst.convert('RGB')).ravel()
        SAD = np.sum(np.abs(np.subtract(arr_mb_src, arr_mb_dst, dtype = np.int16)))
        # SAD = np.sum(np.array(ImageChops.difference(img_mb_src, img_mb_dst)).ravel())
        line = line.rstrip('\n') + str(SAD) + "\n"
        fout.write(line)
        # print(line)
        print('READING...' + fr_now, end="\r", flush=True)
fin.close()
fout.close()


