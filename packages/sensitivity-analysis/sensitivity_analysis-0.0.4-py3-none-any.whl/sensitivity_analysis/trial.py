import numpy as np

x = np.array([[0, 1, 2, 3], [0, 5, 6, 7], [8, 9, 10, 11]])
print(x[np.where(x[:, 0]==0)])
print(x)
print(x.mean())

