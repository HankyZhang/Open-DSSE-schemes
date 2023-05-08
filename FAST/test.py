import numpy as np
import random
import time
import binascii
from encAlgo import *
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

file_data_arr =  [i for i in range(10000, 110000, 10000)]

class Client:
    def __init__(self):
        self.dic = {}
        self.AESKey = '123456'
        self.fidKey = 'password'
        self.encAlgo = encAlgo() #H1 H2:sha256 F P:AES
        self.Count = {}

    def Update(self, ind, keyword ,op):
        hw = self.encAlgo.get_str_sha1_secret_str(keyword)[:20]
        tw = self.encAlgo.F1(self.fidKey, hw)[:20]
        st = self.Count.get(keyword, 'NULL')
        if st == 'NULL':
            r1 = random.getrandbits(90)
            stc = str(r1).zfill(32)
            c = 0
        else:
            stc = st[0]
            c = st[1]

        r2 = random.getrandbits(90)
        kc1 = str(r2).zfill(32)
        stc1 = self.encAlgo.encrypt_oracle(kc1, stc)
        self.Count[keyword] = [stc1, c+1]

        mask = self.encAlgo.H2(tw + stc1)[:38]

        value = str(ind).zfill(5) + str(op) + kc1
        e = self.encAlgo.x_o_r(mask, value).zfill(38)[-38:]
        u = self.encAlgo.H1(tw + stc1)[:20]
        self.dic[u] = e
        return [u,e]



    def delete_file(self):
        for i in range(1000, 11000, 1000):
            filename = 'deletion_' + str(i) + ".txt"
            file = open(filename, 'w')
            file.write('Deletion\n')
            for j in range(i):
                deletion = self.Update(1, str(j), 1)
                for k in deletion:
                    file.write(k + '\n')
            file.close()
            print(f'{os.path.getsize(filename) / 1024} KB')




if __name__=='__main__':
    c = Client()
    c.delete_file()