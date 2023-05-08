import numpy as np
from hashids import Hashids
import random
import time, datetime
import os
N=40
count=1



def readGenDict():
   ID_list = []
   file_path = './ID_dict.txt'
   file = open(file_path)
   while 1:
      line = file.readline()
      if not line:
         break
      ID_list.append(line.strip().split('\n')[0])
   file.close()
   return ID_list

def addTimeStamp(count):
   # 字符类型的时间
   tss1 = '2021-1-1 00:00:00'

   # 转为时间数组
   timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
   # print(timeArray)
   # timeArray可以调用tm_year等
   # print(timeArray.tm_year)  # 2013
   # 转为时间戳
   timeStamp = int(time.mktime(timeArray))
   #print(timeStamp1)  # 1381419600
   timeStamp = count * 360 + timeStamp
   # print(int(time.time()))

   '''
     # 使用datetime
     timeStamp = 1381419600
     dateArray = datetime.datetime.fromtimestamp(timeStamp)
     otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
     print(otherStyleTime)  # 2013--10--10 23:40:00
     '''

   # 使用time
   #timeArray = time.localtime(timeStamp3)
   #otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
   #print(otherStyleTime)  # 2013--10--10 23:40:00
   #print(timeStamp)
   return timeStamp



def genFile(numFileFolder,ID_list):

   count = 0
   timecount = 0
   for i in range(numFileFolder):
      fileNumber = random.randint(1, 100)
      folderDir = './folder/document' + str(i)
      os.makedirs(folderDir)
      for j in range(fileNumber):
         timecount =timecount +1
         timeStamp = addTimeStamp(timecount)
         ulr = folderDir  +'/ID_' + str(count) + '.txt'
         count = count +1
         file = open(ulr, 'w')


         legth = random.randint(1, len(ID_list))

         key_list = random.sample(ID_list, k=legth)

         for i in key_list:
            file.write(i + '\n')

         file.close()


if __name__=='__main__':
   ID_list= readGenDict()

   genFile(100,ID_list)


