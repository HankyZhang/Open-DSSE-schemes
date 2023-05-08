import numpy as np
import random
import time
from encAlgo import *
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

file_data_arr =  [i for i in range(10000, 110000, 10000)]

class Client:
    def __init__(self):
        self.dic = {}
        self.dataset = {}
        self.AESKey = '123456'
        self.fidKey = 'password'
        self.Count = {}
        self.CDB ={}
        self.GRP ={}
        self.encAlgo = encAlgo()
        self.lam = 20
        self.slam = 21

    def update(self, op, keyword, id):
        value = self.Count.get(keyword, 'NULL')
        if value == 'NULL':
            self.Count[keyword] = [0, 0]
            c_update = 0
            c_search = 0
        else:
            c_update = self.Count[keyword][0]
            c_search = self.Count[keyword][1]

        self.Count[keyword][0] = c_update + 1
        c_update = c_update + 1
        str_c_search = str(int(c_search)).zfill(5)
        K_w = self.encAlgo.F1(self.fidKey, keyword + str_c_search)[:20]
        K_w_2 = self.encAlgo.F1(self.fidKey, keyword + str(-1).zfill(5))[:20]

        value0 = self.encAlgo.F3(K_w, str(c_update))[:41]
        G_Kw_id = self.encAlgo.F2(K_w_2, str(id))[:20]
        mask = '000000000000000' + str(op) + G_Kw_id
        value1 = self.encAlgo.x_o_r(value0, mask).zfill(41)[-41:]
        L = value1[:self.lam]
        D = value1[-1*(self.slam):]

        C =  self.encAlgo.encrypt_oracle(self.AESKey, str(id))

        self.dic[L] = [D, C]
        return [L,D,C]

    def add_file(self, universal_dict):
        for keyword in universal_dict:
            for ind in universal_dict[keyword]:
                self.update(1, keyword, ind)
        return self.dic

    def delete_file(self):
        for i in range(1000, 11000, 1000):
            filename = 'deletion_' + str(i) + ".txt"
            file = open(filename, 'w')
            file.write('Deletion\n')
            for j in range(i):
                deletion = self.update(0, str(j), 1)
                for k in deletion:
                    file.write(k + '\n')
            file.close()
            print(f'{os.path.getsize(filename) / 1024} KB')

if __name__=='__main__':
   c = Client()
   c.delete_file()