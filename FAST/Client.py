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

    def add_file(self, universal_dict):
        for keyword in universal_dict:
            for ind in universal_dict[keyword]:
                self.Update(ind, keyword, 1)
        return self.dic

    def delete_file(self, keyword, ind):
        self.Update(ind, keyword, 0)
        return self.dic

    def client_search(self, keyword):
        hw = self.encAlgo.get_str_sha1_secret_str(keyword)[:20]
        tw = self.encAlgo.F1(self.fidKey, hw)[:20]
        st = self.Count.get(keyword, 'NULL')
        if st == 'NULL':
            return 0
        else:
            return tw, st[0], st[1]
    def server_search(self, tw, stc, c):
        delete = []
        idList = []
        i = c
        while i > 0:
            u = self.encAlgo.H1(tw + stc)[:20]
            e = self.dic[u]
            mask = self.encAlgo.H2(tw + stc)[:38]

            value = self.encAlgo.x_o_r(e, mask).zfill(38)
            ind = int(value[:5])
            op = value[5:6]
            ki = value[-32:]
            if op == '0':
                delete.append(ind)
            else:
                if ind in delete:
                    delete.remove(ind)
                else:
                    idList.append(ind)
            stc = self.encAlgo.decrypt_oralce(ki, stc)
            i = i - 1
        return idList

if __name__=='__main__':
    filename1 = "search_time2.txt"
    file1 = open(filename1, 'w')
    cc = Client()
    for i in range(1000):
        keyword = str(i)
        for j in range(1000):
            dic = cc.delete_file(keyword,str(j))
    for dic in cc.dic:
        file1.write(dic, cc.dic[dic])

    file1.close()

    # filename1 = "search_time2.txt"
    # file1 = open(filename1, 'w')
    #
    # for file_data in file_data_arr:
    #     counter = 10
    #
    #     filename = "inverted_index_" + str(file_data) + ".txt"
    #     universal_dict = {}
    #     with open(filename, "r") as f:
    #         for line in f:
    #             values = line.split(" ")
    #             universal_dict[values[0]] = []
    #             for i in values[1:len(values)]:
    #                 universal_dict[values[0]].append(i)  # 所有的关键字对应文件
    #
    #     keyword = 'Subject'
    #     count = 0
    #     total_consump1 = 0.0
    #     total_consump2 = 0.0
    #     while count < counter:
    #         Sumtime_index = 0
    #         begin_time_index = time.time()
    #         cc = Client()
    #         cc.add_file(universal_dict)
    #         end_time_index = time.time()
    #         Sumtime_index += (end_time_index - begin_time_index)
    #         total_consump1 += Sumtime_index
    #
    #         cc.delete_file(keyword, 3)
    #
    #         Sumtime_search = 0
    #         begin_time_search = time.time()
    #         tw, stc, c= cc.client_search(keyword)
    #         idList = cc.server_search(tw, stc, c)
    #
    #         end_time_search = time.time()
    #         Sumtime_search += (end_time_search - begin_time_search)
    #         total_consump2 += Sumtime_search
    #         count += 1
    #     avg1 = (total_consump1 / counter)
    #     print("avg_index_time:" + str(avg1))
    #     avg2 = (total_consump2 / counter)
    #     print("avg_search_time:" + str(avg2))
    #     file1.write('FileNumber:' + str(file_data) + '   avg_index_time:' + str(avg1) + '\n')
    #     file1.write('FileNumber:' + str(file_data) + '  avg_search_time:' + str(avg2) + '\n')
    #     file1.write('--------------\n')
    #     print(idList)
    #     print(len(idList))
    #     print('------------')
    #
    # file1.close()


