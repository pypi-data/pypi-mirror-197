import numpy as np

def stateBoundary(x):
    x_bound = np.empty((x[0, :].size, 2))
    x_name = []  # Just a dummy variable to enter the sampling function
    for i in range(x[0, :].size):
        x_bound[i, 0] = np.min(x[:, i])
        x_bound[i, 1] = np.max(x[:, i])
        if x_bound[i, 0] == x_bound[i, 1]:
            x_bound[i, 0] = x_bound[i, 0] - 0.1 * x_bound[i, 0]
            x_bound[i, 1] = x_bound[i, 1] + 0.1 * x_bound[i, 1]
        if i == 0:  ###Filling the dummy variable
            x_name.append("First")
        else:
            x_name.append("Other")
    return x_bound, x_name