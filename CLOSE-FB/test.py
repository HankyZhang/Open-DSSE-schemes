from encAlgo import *
def find_all_index(arr, item):
    return [i for i, a in enumerate(arr) if a == item]

def Hd(ctr, h):
    for i in range(ctr):
        h = encAlgo().get_str_sha1_secret_str(h)
    return h

if __name__ == '__main__':
    DW={'a': 1, 'd': 2, 'b': '3'}
    age = DW.get('c', 'NULL')
    stw = Hd(5, 'c332')
    print(stw)