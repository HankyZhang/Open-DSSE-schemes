
import numpy as np
import random
from encAlgo import *
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)
from genTrap import *


class CUpdate:
    def __init__(self):
        self.dic = {}
        self.dataset = {}
        self.AESKey = '123456'
        self.fidKey = 'password'
        self.CLen = 1200
        self.KW = {}
        self.encAlgo = encAlgo()

    def Hd(self, ctr, h):
        for i in range(ctr):
            h = self.encAlgo.get_str_sha1_secret_str(h)[:20]
        return h

    def encID(self, fidKey, AESKey, count):   #加密ID
        value = encAlgo().encrypt_oracle(AESKey, count)
        key = encAlgo().F2(fidKey, count)[-20:]
        return key,value

    def Update(self,stw,dicw,ind):
        key = self.encAlgo.get_str_sha1_secret_str(stw+'0')[:20]
        value = dicw.get(key,'NULL')
        if value == 'NULL':
            mask = self.encAlgo.get_str_sha1_secret_str(stw+'1')[:40]

            idKey, idValue = self.encID(self.fidKey, self.AESKey, str(ind)+'1')  # msg的大小要根据文件总数调节
            dicw[idKey] = idValue

            # str_ind = str(ind).zfill(10)
            eva = idKey +'00000000000000000000'
            value = self.encAlgo.x_o_r(mask, eva).zfill(40)
            dicw[key] = value
        else:
            r = random.getrandbits(32)
            str_r = str(r).zfill(20)
            mask = self.encAlgo.get_str_sha1_secret_str(stw+'1')[:40]

            idKey, idValue = self.encID(self.fidKey, self.AESKey, str(ind) + '1')  # msg的大小要根据文件总数调节
            dicw[idKey] = idValue


            value3 = self.encAlgo.x_o_r(mask, idKey +str_r)
            dicw[key] = value3
            key1 = self.encAlgo.get_str_sha1_secret_str(str_r+'0')[:20]
            mask1 = self.encAlgo.get_str_sha1_secret_str(str_r+'1')[:40]
            mask2 = self.encAlgo.get_str_sha1_secret_str(stw + '1')[:40]
            value1 = self.encAlgo.x_o_r(mask1, mask2).zfill(40)
            value2 = self.encAlgo.x_o_r(value, value1).zfill(40)
            dicw[key1] = value2
        return dicw


    def Merge(self, dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def chain(self,  universal_dict, file_data ):  #生成链
        dic = {}
        ctr = self.CLen
        number_circle = 1


        for keyword in universal_dict:
            i = 0
            while i < file_data:
                if ctr == 0:
                    ctr = self.CLen
                    list = searchServer().search(keyword, self.dataset, 1, number_circle)
                    number_circle = number_circle + 1
                    self.dataset = {}
                    ktw = self.encAlgo.F1(self.fidKey, keyword + str(number_circle))[:20]
                    stw = self.Hd(ctr, ktw)
                    self.KW[keyword] = stw
                    dic[keyword] = {}
                    for j in list:
                        dic[keyword] = self.Update(stw, dic[keyword], j)
                        self.dataset = self.Merge(self.dataset, dic[keyword])
                    ctr = ctr - 1
                    self.KW.pop(keyword)
                else:
                    for j in range(10000):
                        count = universal_dict[keyword][i + j]

                        stw = self.KW.get(keyword, 'NULL')
                        if stw == 'NULL':
                            ktw = self.encAlgo.F1(self.fidKey, keyword + str(number_circle))[:20]
                            stw = self.Hd(ctr, ktw)
                            self.KW[keyword] = stw
                            dic[keyword] = {}
                        dic[keyword] = self.Update(stw, dic[keyword], count)
                        self.dataset = self.Merge(self.dataset, dic[keyword])
                    ctr = ctr - 1
                    self.KW.pop(keyword)
                    i = i + 10000

        return self.dataset, ctr, number_circle




