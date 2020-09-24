from ctypes import *

class MvDumper(object):
    def __init__(self, filepath):
        self.lib = CDLL(filepath)
        self.lib.setup()
        # self.lib.call_dec.argtypes = [POINTER(c_int)]
    def readFrame(self):
        return self.lib.call_readframe()
    def decode(self):
        return self.lib.call_dec()
    def release(self):
        self.lib.release()

# example
mvObj = MvDumper('/home/user/mv-get-realtime/extract_mvs.so')
while (mvObj.readFrame() >= 0):
    ret = mvObj.decode()
    if (ret < 0):
        break
mvObj.release()
