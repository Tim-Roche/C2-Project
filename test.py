import numpy as np

A = [[1,2,3],[1,2,3]]
mask = [[0,0,0],[1,1,1]]

res = np.multiply(A, mask)
print(res)