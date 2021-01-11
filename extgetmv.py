import sys
import cv2
from ctypes import *
import time

vidpath = "./" + sys.argv[1]
# convert string to byte objects
b_vidpath = vidpath.encode('utf-8')

vid = cv2.VideoCapture(vidpath)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
total_fr = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

mb_size = 16 * 16
num_mv = (height * width) / mb_size
# 1 frame number + 4 fields (src_x, src_y, dst_x, dst_y )
mv_data_size = int(1 + 4 * num_mv)

class MvDumper(object):
    def __init__(self, filepath):
        self.lib = CDLL(filepath)
        self.lib.setup.argtypes = [c_char_p]
        self.lib.setup(b_vidpath)
        self.lib.call_dec.argtypes = [POINTER(c_int)]
        self.ptr = (c_int * mv_data_size)()
    def readFrame(self):
        return self.lib.call_readframe()
    def decode(self):
        return self.lib.call_dec(self.ptr)
    def release(self):
        self.lib.release()

# example
tmv = 0
tpx = 0
count = 0
mvObj = MvDumper('./lextractmvs.so')
while (mvObj.readFrame() >= 0):
    t0 = time.time()
    ret = mvObj.decode()
    # at the moment, buffer size = 1 frame
    buffer = list(mvObj.ptr)
    t1 = time.time()
    # print(buffer[0])
    
    # vid.set(cv2.CAP_PROP_POS_FRAMES, buffer[0])
    if count <= buffer[0]:
        t2 = time.time()
        res, image = vid.read()
        t3 = time.time()
    tmv = tmv + t1 - t0
    tpx = tpx + t3 - t2
    count = count + res
    # print(count)
    print(count,"/", total_fr, end = "\r", flush = True)
    if (ret < 0):
        break
# cv2.namedWindow("Win")
# cv2.imshow("Win", image)
# cv2.waitKey(0)
vid.release() 
mvObj.release()
print(count, tmv, tpx)
