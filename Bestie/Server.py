import numpy as np
import random
from encAlgo import *
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

class Server:
    def __init__(self, Count, dic):
        self.dic = dic
        self.dataset = {}
        self.AESKey = '123456'
        self.fidKey = 'password'
        self.Count = {}
        self.CDB ={}
        self.GRP ={}
        self.encAlgo = encAlgo()
        self.lam = 10
        self.slam = 11
        self.Count = Count
        self.GRP = {}


