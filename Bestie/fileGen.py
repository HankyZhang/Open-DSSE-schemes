import numpy as np
from hashids import Hashids
import random
import time, datetime
N=35
count=1



def readGenDict():
   ID_dict = {}
   file_path = './Document/ID_gen.txt'
   file = open(file_path)
   while 1:
      line = file.readline()
      if not line:
         break
      temp = line.strip().split(' ')
      ID_dict[temp[0]] = temp[1:len(temp)]
   file.close()
   ID_list=[]
   for key in sorted(ID_dict.keys()):
      ID_list.append(key)
   return ID_dict,ID_list

def genFile(count,ID_dict,timeStamp):
   ulr='./Document/ID_'+str(count)+'.txt'
   file=open(ulr,'w')

   key = ID_dict.keys()
   # legth = random.randint(1, len(key))

   legth = len(key)
   key_list = random.sample(list(key), k=legth)
   result = {}
   #print(legth)
   for temp in key_list:
      tmp = ID_dict[temp]
      if tmp[2] == 'int':
         result[temp] = random.randint(int(tmp[0]), int(tmp[1]))
      elif tmp[2] == 'float':
         result[temp] = round(random.uniform(int(tmp[0]), int(tmp[1])), 1)
   #print(result)

   file.write(str(timeStamp)+'\n')
   for k,v in result.items():
      file.write(f"{k},{v}\n".format(k,v))
   file.close()

def addTimeStamp(count):
   # 字符类型的时间
   tss1 = '2020-1-1 00:00:00'

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



if __name__=='__main__':
   ID_dict ,ID_list= readGenDict()
   for i in range(1000):
      timeStamp=addTimeStamp(i)
      #timeStamp=i * 86400
      genFile(i,ID_dict,timeStamp)


