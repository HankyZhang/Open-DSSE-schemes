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

    # def readDict(self ):
    #     f1 = open('./Document/ID_dict.txt')  # 打开名为matrix1的TXT数据文件
    #     lines1 = f1.readlines()  # 把全部数据文件读到一个列表lines1中
    #     List = []
    #     for line in lines1:  # 把lines1中的数据逐行读出来
    #         list = line.strip('\n')  # 处理逐行数据；strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的数据返回到list列表中
    #         List.append(list)
    #     return List
    # def readFile(self,count, keyList):
    #     ulr = './Document/ID_' + str(count) + '.txt'
    #     keywords = []  # 初始化空数组
    #
    #     index_List = []
    #     file = open(ulr)
    #
    #     lines1 = file.readlines()  # 把全部数据文件读到一个列表lines1中
    #     timeStamp = lines1[0].strip('\n')
    #
    #     for line in lines1[1:len(lines1)]:  # 把lines1中的数据逐行读出来
    #         list1 = line.strip('\n').split(',')  # 处理逐行数据；strip表示把头尾的'\n'去掉
    #         keywords.append(list1[0])
    #         index = keyList.index(list1[0])
    #         index_List.append(index)
    #     return keywords, index_List, timeStamp


    def add_file(self, universal_dict):
        # self.keyList = self.readDict()
        for i in range(10000):
            self.update(1,'Subject',i)


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



    def delete_file(self, keyword, ind):
        self.update(0, keyword, ind)

    def client_search1(self, keyword):
        c_update = self.Count[keyword][0]
        c_search = self.Count[keyword][1]

        str_c_search = str(int(c_search)).zfill(5)
        K_w = self.encAlgo.F1(self.fidKey, keyword + str_c_search)[:20]
        K_w_2 = self.encAlgo.F1(self.fidKey, keyword + str(-1).zfill(5))[:20]

        I_grp_w = self.encAlgo.F2(K_w_2, '000000000')
        return c_update, K_w, I_grp_w

    def server_search(self, c_update, K_w, I_grp_w):
        DD = []
        self.GRP[I_grp_w] = []
        i = c_update
        while i > 0:
            LD = self.encAlgo.F3(K_w, str(i))[:41]
            L = LD[:self.lam]
            Ds = LD[-1*(self.slam):]
            D = self.dic[L][0]
            C = self.dic[L][1]
            value0 = self.encAlgo.x_o_r(D, Ds).zfill(21)[-21:]
            op = value0[: 1 ]
            X = value0[1 - 1*self.slam :]
            if op == '0':
                DD.append(X)
                for item in self.GRP[I_grp_w]:
                    for item in item.items():
                        if item[0] == X:
                            self.GRP[I_grp_w].pop(item)
                            break

            else:
                if X not in DD:
                    dict = {}
                    dict[X] = C
                    self.GRP[I_grp_w].append(dict)
            i = i - 1
        self.dic = {}
        return self.GRP[I_grp_w]
    def client_search2(self, keyword, GRP):
        idList = []
        for i in GRP:
            for key in i:
                dec = i[key]
                id = self.encAlgo.decrypt_oralce(self.AESKey, dec)
                idList.append(id)
        self.Count[keyword][0] = 0
        self.Count[keyword][1] += 1
        return idList
if __name__=='__main__':
    filename1 = "search_time3.txt"
    file1 = open(filename1, 'w')

    file_data = 10000
    filename = "inverted_index_" + str(file_data) + ".txt"
    universal_dict = {}
    with open(filename, "r") as f:
        for line in f:
            values = line.split(" ")
            universal_dict[values[0]] = []
            for i in values[1:len(values)]:
                universal_dict[values[0]].append(i)  # 所有的关键字对应文件
    counter = 1
    keyword = 'Subject'
    count = 0
    total_consump1 = 0.0
    total_consump2 = 0.0
    while count < counter:
        Sumtime_index = 0
        begin_time_index = time.time()
        c = Client()

        c.add_file(universal_dict)

        end_time_index = time.time()
        Sumtime_index += (end_time_index - begin_time_index)
        total_consump1 += Sumtime_index

        c.delete_file(keyword, 9)

        Sumtime_search = 0
        begin_time_search = time.time()
        c_update, K_w, I_grp_w = c.client_search1(keyword)
        GRP = c.server_search(c_update, K_w, I_grp_w)
        idList = c.client_search2(keyword, GRP)
        end_time_search = time.time()
        Sumtime_search += (end_time_search - begin_time_search)
        total_consump2 += Sumtime_search
        count += 1

    avg1 = (total_consump1 / counter)
    print("avg_index_time:" + str(avg1))
    avg2 = (total_consump2 / counter)
    print("avg_search_time:" + str(avg2))

    file1.write('NumberKeyword:40' + '\n')
    file1.write('avg_index_time:' + str(avg1) + '\n')
    file1.write('avg_search_time:' + str(avg2) + '\n')
    file1.write('--------------\n')


    print(idList)
    print(len(idList))
    print('------------')

    file1.close()