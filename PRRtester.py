""""
def PRR(values, names):
    normRank = []
    numOfRegions = len(names)
    values, names = zip(*sorted(zip(values,names), reverse=True))
    PRRlist = []
    for rank in range(1,len(values)+1):
        percentageRegionRank = 1.1-rank/numOfRegions
        PRRlist.append(percentageRegionRank)
    names, PRRlist = zip(*sorted(zip(names,PRRlist)))
    return(PRRlist, names)

names  = [1, 2, 3, 4, 5]
values = [10, 20, 5, 100, 2]
PRRlists, names = PRR(values, names)

print(names)
print(PRRlists)
 
"""
import numpy as np
A = [1,2,3,4,5,6,7,8,9]
r = np.reshape(A, (3,3), order="F")
print(r.tolist())