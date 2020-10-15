import sys
import cv2
from ctypes import *

vidpath = "./" + sys.argv[1]
# convert string to byte objects
b_vidpath = vidpath.encode('utf-8')

vid = cv2.VideoCapture(vidpath)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
vid.release() 
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
mvObj = MvDumper('./lextractmvs.so')
while (mvObj.readFrame() >= 0):
    ret = mvObj.decode()
    # at the moment, buffer size = 1 frame
    buffer = list(mvObj.ptr)
    if (ret < 0):
        break
mvObj.release()
