import numpy as np
from numba import njit




# class DECOUPLE():
#     def __init__(self, A, ql, qh):
#         self.A = A
#         self.ql = ql 
#         self.qh = qh 
    
#     def decouple_it_(self):
#         # print(self.A, self.ql, self.qh)
#         self.A, self.ql, self.qh = decouple_it(self.A, self.ql, self.qh)
#         # print(self.A, self.ql, self.qh)
#         return self.A, self.ql, self.qh


@njit()
def sortmatrices(A, ql, qh):
    j = 0
    for i in np.diag(A):
        if i == 0:
            counter = 0
            for arr in A[:, j]:
                if arr != 0 and A[j, counter] != 0:
                    Ac = A.copy()
                    qlc = ql.copy()
                    qhc = qh.copy()
                    A[counter] = Ac[j]
                    A[j] = Ac[counter]
                    ql[counter] = qlc[j]
                    ql[j] = qlc[counter]
                    qh[counter] = qhc[j]
                    qh[j] = qhc[counter]
                    break
                counter += 1
        j += 1
    return A, ql, qh

@njit()
def sortmines(A, ql, qh, arg1, arg2):
    # print(A, ql, qh, arg1, arg2)
    A[arg1, :] -= (A[arg1, arg2]/A[arg2, arg2])*A[arg2, :]
    ql[arg1] -= (A[arg1, arg2]/A[arg2, arg2])*ql[arg2]
    qh[arg1] -= (A[arg1, arg2]/A[arg2, arg2])*qh[arg2]
    return A, ql, qh

@njit()
def normali(A, ql, qh):
    for i in range(A.shape[0]):
        ql[i] /= abs(A[i, i])
        qh[i] /= abs(A[i, i])
        sign = np.sign(A[i, i])
        if sign >= 0:
            pass
        else:
            switchq(ql, qh, i)
        A[i, i] /= A[i, i]
    return A, ql, qh

@njit()
def switchq(ql, qh, arg):
    a = ql[arg]
    ql[arg] = qh[arg]
    qh[arg] = a
    return (ql, qh)

@njit()
def decouple_it(A, ql, qh):
    iter_num = A.shape[0]**2-A.shape[0]
    shape = A.shape[0]
    arg1_list = np.zeros((iter_num))
    arg2_list = np.zeros((iter_num))
    counter = 0
    for i in range(shape):
        for j in range(i):
            arg1_list[counter] = i
            counter += 1

    for i in range(shape):
        for j in range(i):
            arg1_list[counter]= shape-i-1
            counter += 1

    counter = 0
    for i in range(shape):
        for j in range(i):
            arg2_list[counter] = j
            counter += 1
    
    for i in range(shape):
        for j in range(i):
            arg2_list[counter] = shape-j-1
            counter += 1
        

    for i  in range(iter_num):
        A, ql, qh = sortmatrices(A, ql, qh) 
        arg1d = int(arg1_list[i])
        arg2d = int(arg2_list[i])
        A, ql, qh = sortmines(A, ql, qh, arg1=arg1d, arg2=arg2d)

    A, ql, qh = normali(A, ql, qh)
    return A, ql, qh

class Decouppling():
    def __init__(self, A, ql, qh):
        self.A = A
        self.ql = ql 
        self.qh = qh 
    
    def decouple_it_(self):
        # print(self.A, self.ql, self.qh)
        self.A, self.ql, self.qh = decouple_it(self.A, self.ql, self.qh)
        # print(self.A, self.ql, self.qh)
        return self.A, self.ql, self.qh
