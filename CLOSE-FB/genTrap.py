import numpy as np
from CUpdate import *
import time
from encAlgo import *
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)




file_data_arr =  [10000]

def Merge( dict1, dict2):
    res = {**dict1, **dict2}
    return res


class searchServer:
    def __init__(self):
        self.AESKey = '123456'
        self.list = []
        self.CLen = 1200
        self.encAlgo = encAlgo()
        self.fidKey = 'password'

    def Hd(self, ctr, h):
        for i in range(ctr):
            h = self.encAlgo.get_str_sha1_secret_str(h)[:20]
        return h

    def CSearch(self,EDB, CLen,ctr,stw,number_circle):
        res = []
        j = ctr
        while j <= CLen:
            key = self.encAlgo.get_str_sha1_secret_str(stw + '0')[:20]
            value = EDB.get(key, 'NULL')
            if value != 'NULL':
                mask = self.encAlgo.get_str_sha1_secret_str(stw + '1')[:40]
                msgr = self.encAlgo.x_o_r(value, mask).zfill(40)

                msg = msgr[-40:-20]
                rt = msgr[-20:]

                while rt != '00000000000000000000':
                    idValue = EDB[msg]
                    AESvalue = encAlgo().decrypt_oralce(self.AESKey, idValue)
                    id = AESvalue[:-1]
                    op = AESvalue[-1]
                    if op == '1':
                        res.append(int(id))

                    key = self.encAlgo.get_str_sha1_secret_str(rt + '0')[:20]
                    value1 = EDB[key]
                    mask1 = self.encAlgo.get_str_sha1_secret_str(rt + '1')[:40]
                    msgr1 = self.encAlgo.x_o_r(value1, mask1).zfill(40)
                    msg = msgr1[-40:-20]
                    rt = msgr1[-20:]

                idValue = EDB[msg]
                AESvalue = encAlgo().decrypt_oralce(self.AESKey, idValue)
                id = AESvalue[:-1]
                op = AESvalue[-1]
                if op == '1':
                    res.append(int(id))
            j = j + 1
            stw = self.encAlgo.get_str_sha1_secret_str(stw)[:20]

        return res

    def search(self,keyword,EDB,ctr,number_circle):
        ktw = encAlgo().F1(self.fidKey , keyword+str(number_circle))[:20]
        begin_time_1 = time.time()
        stw = self.Hd(ctr,ktw)[:20]
        end_time_1 = time.time()
        print(end_time_1 - begin_time_1)
        List = self.CSearch(EDB, self.CLen,ctr,stw,number_circle)
        return List

if __name__=='__main__':

    filename1 = "search_time3.txt"
    file1 = open(filename1, 'w')

    for file_data in file_data_arr:

        counter = 1
        keyword = 'Subject'
        number_circle = 1



        ctr = 1200

        count = 0
        total_consump = 0.0


        filename = "inverted_index_" + str(file_data) + ".txt"
        universal_dict = {}
        with open(filename, "r") as f:
            for line in f:
                values = line.split(" ")
                universal_dict[values[0]] = []
                for i in values[1:len(values)]:
                    universal_dict[values[0]].append(i)  # 所有的关键字对应文件

        while count < counter:
            dictw = {}
            Sumtime_index = 0
            begin_time_index = time.time()

            a = CUpdate()
            dictw, ctr, number_circle = a.chain(universal_dict, file_data )


            end_time_index = time.time()
            Sumtime_index += (end_time_index - begin_time_index)
            total_consump += Sumtime_index
            count += 1
        avg = (total_consump / counter)
        print("avg_index_time:" + str(avg))
        file1.write('FileNumber:' + str(file_data) + '   avg_index_time:'+ str(avg) + '\n')
        print(ctr)
        count = 0
        total_consump = 0.0
        while count < counter:
            Sumtime_search = 0
            begin_time_search = time.time()

            list = searchServer().search(keyword, dictw, ctr + 1, number_circle)
            end_time_search = time.time()
            Sumtime_search += (end_time_search - begin_time_search)
            total_consump += Sumtime_search
            count += 1

        avg = (total_consump / counter)
        print("avg_search_time:" + str(avg))
        file1.write('FileNumber:'+ str(file_data) + '  avg_search_time:' + str(avg) + '\n')
        file1.write('--------------\n')
        print(list)
        print(len(list))
    file1.close()


