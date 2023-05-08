import numpy as np
from genTrapdoor import *
from genIndex import *

from encAlgo import *


np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

class searchServer:
    def __init__(self,dataset,encMatrix,trapMatrix):
        self.dataset = dataset
        self.encMatrix = encMatrix
        self.trapMatrix = trapMatrix
        self.AESKey = '123456'
        self.fidKey = 'password'

    def encID(self, fidKey, AESKey, count):   #加密ID
        value = encAlgo().encrypt_oracle(AESKey, count)
        key = encAlgo().F2(fidKey, count)[-10:]
        return key,value

    def search(self,file_data):
        k = 0

        sum_time_matrix = 0

        begin_time_matrix = time.time()
        for i in self.encMatrix.keys():
            if i != 'Subject':
                flag = 0
                for j in self.trapMatrix:
                    resultMatrix = np.dot(self.encMatrix[i], j)
                    tril = np.ndarray.trace(resultMatrix)
                    if (tril > 0):
                        flag = 1
                        key = str(int(tril)).zfill(10)
                        break
                if (flag == 1):
                    break
                k = k + 1
                if(k == 20000):
                    break

        i = 'Subject'
        for j in self.trapMatrix:
            resultMatrix = np.dot(self.encMatrix[i], j)
            tril = np.ndarray.trace(resultMatrix)
            if (tril > 0):
                key = str(int(tril)).zfill(10)
                break

        end_time_matrix = time.time()
        sum_time_matrix = end_time_matrix - begin_time_matrix
        idList = []
        msgKey, msgValue = self.encID(self.fidKey, self.AESKey, '10000000')


        while key != '0000000000':
            # if num == 64000:
            #     break
            # num = num + 1
            key_ = encAlgo().get_str_sha1_secret_str(key + '0')[:10]
            value_ = self.dataset[key_]
            mask = encAlgo().get_str_sha1_secret_str(key + '1')[:20]
            encValue = encAlgo().x_o_r(mask, value_).zfill(20)[-20:]
            idKey = encValue[-20:-10]
            key = encValue[-10:]
            idValue = self.dataset[idKey]
            if idValue!= msgValue:
                id = encAlgo().decrypt_oralce(self.AESKey, idValue)

                idList.append(int(id))
            if len(idList) == file_data:
                break
        return idList,sum_time_matrix


if __name__=='__main__':
    filename1 = "search_time5.txt"
    file1 = open(filename1, 'w')

    for file_data in file_data_arr:
        counter = 1

        filename = "inverted_index_" + str(file_data) + ".txt"
        universal_dict = {}
        with open(filename, "r") as f:
            for line in f:
                values = line.split(" ")
                universal_dict[values[0]] = []
                for i in values[1:len(values)]:
                    universal_dict[values[0]].append(i)  # 所有的关键字对应文件
        count = 0
        total_consump = 0.0
        while count < counter:
            Sumtime_index = 0

            begin_time_index = time.time()

            dataset, Matrix = genIndex().Index(universal_dict,file_data)

            end_time_index = time.time()
            Sumtime_index += (end_time_index - begin_time_index)
            total_consump += Sumtime_index
            count += 1

        avg = (total_consump / counter)
        print("avg_index_time:" + str(avg))
        file1.write('FileNumber:' + str(file_data) + '   avg_index_time:' + str(avg) + '\n')

        matrix = genTrapdoor('Subject').genTrap()
        count = 0
        total_consump = 0.0
        counter = 10
        while count < counter:
            Sumtime_search = 0
            begin_time_search = time.time()
            idList,sum_time_matrix = searchServer(dataset, Matrix, matrix).search(file_data)
            end_time_search = time.time()
            Sumtime_search += (end_time_search - begin_time_search)
            total_consump += Sumtime_search
            count += 1

        avg = (total_consump / counter)
        print("avg_search_time:" + str(avg))
        print("matrix_time: "+ str(sum_time_matrix))
        file1.write('FileNumber:' + str(file_data) + '  avg_search_time:' + str(avg) + '\n')
        file1.write('sum_time_matrix:' + str(sum_time_matrix) + '\n')
        file1.write('--------------\n')
        print(len(idList))
        print(idList)
    file1.close()