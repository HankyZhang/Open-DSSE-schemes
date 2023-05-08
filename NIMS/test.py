import time
from encAlgo import *
import os


def encID(fidKey, AESKey, count):  # 加密ID
    value = encAlgo().encrypt_oracle(AESKey, count)
    key = encAlgo().F2(fidKey, count)[-10:]
    return key, value
if __name__=='__main__':
    #test().genTimeStamp()
    for i in range(1):
        filename = 'deletion_'+ str(i) +".txt"
        file = open(filename, 'w')
        file.write('Deletion\n')
        for j in range(i):
            msgKey, msgValue = encID('password', '123456', str(j))

            file.write(msgKey + '\n')
        file.close()
        print(f'{os.path.getsize(filename)} B')



