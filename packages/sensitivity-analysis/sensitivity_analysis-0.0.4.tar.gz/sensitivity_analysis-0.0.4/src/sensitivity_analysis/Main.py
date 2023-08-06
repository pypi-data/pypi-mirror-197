# -*- coding: utf-8 -*-
import math
import numpy as np
from SALib.sample import morris as ms
from SALib.analyze import morris as ma

import pandas as pd


from vehiclemodels.parameters_vehicle2 import parameters_vehicle2
from vehiclemodels.init_mb import init_mb
from analysis import analysis
from stateBoundary import stateBoundary
from getAttribute import getAttribute
from resultPlot import resultPlot
from cluster import cluster
import testing

"""
Created on Thu Sep 29 13:34:20 2022

@author: Youssef Ibrahim
"""

# load parameters
p = parameters_vehicle2()

delta0 = 0
vel0 = 15
Psi0 = 0
dotPsi0 = 0
beta0 = 0
sy0 = 0
initialState = [
    0,
    sy0,
    delta0,
    vel0,
    Psi0,
    dotPsi0,
    beta0,
]
## initial state for simulation
# x0_ST = init_st(initialState)  # initial state for single-track model
x0_MB = init_mb(initialState, p)  # initial state for multi-body model

# Sensitivity analysis
## SA parameters
noTrajectory = 10  # Number of trajectories to generate
noLevel = 4  # Number of levels
confidenceLevel = 0.95  # Confidence interval level

parameterAttribute, parameter = getAttribute(p)
parameterAttribute = np.array(parameterAttribute)
parameter = np.array(parameter)

parameter_max = np.zeros(np.size(parameter))
parameter_min = np.zeros(np.size(parameter))

# Adjust small values
for i in range(np.size(parameter)):
    if abs(parameter[i]) < 0.1:
        parameter_max[i] = 100
        parameter_min[i] = -100
    elif parameter[i] >= 0:
        parameter_max[i] = parameter[i] * 100
        parameter_min[i] = parameter[i] * -100
    else:
        parameter_min[i] = parameter[i] * 100
        parameter_max[i] = parameter[i] * -100
bound = np.empty((np.size(parameter), 2))
bound[:, 0] = parameter_min
bound[:, 1] = parameter_max

attributeList = parameterAttribute.tolist()
bounds = bound.tolist()

## Analysis
problem = {"num_vars": np.size(parameter), "names": attributeList, "bounds": bound}

parameterMatrix = ms.sample(problem, noTrajectory, num_levels=noLevel)

# getting boundaries of states
x = testing.cornering_left()
x_bound, x_name = stateBoundary(x)


# sampling system states
noStateCombinations = 5
xMatrix = np.empty((noStateCombinations+1, len(x_bound[:, 0])))

for i_stateCombination in range(noStateCombinations):
    xMatrix[i_stateCombination, :] = x_bound[:, 0] + (i_stateCombination/noStateCombinations)*(x_bound[:, 1] - x_bound[:, 0])
xMatrix[-1, :] = x_bound[:, 1] 

stateCombinationName = []
for i_stateCombination, _ in enumerate(x_bound[:, 0]):
    stateCombinationName.append("stateCombination_{}".format(i_stateCombination))
stateCombination = pd.DataFrame(xMatrix, columns = stateCombinationName)
# Create a matrix for the attribute assignment
attributeAssign = np.empty((len(parameterAttribute), 1))
for i_attr_assign in range(len(parameterAttribute)):
    attributeAssign[i_attr_assign] = i_attr_assign

stateDatabase, simulation = analysis(problem, x_bound, xMatrix, parameterMatrix, parameterAttribute, attributeList)

# Getting situation names for the plot
situation = []
for attr in simulation.Situation.__dict__:
    if callable(getattr(simulation.Situation, attr)):
        situation.append(attr)

clusterDatabase, centroidDatabase = cluster(stateDatabase, situation)
resultPlot(clusterDatabase)
clusterDatabase.to_excel(excel_writer="C:/Users/youss/clusterDatabase-14.03.2023.xlsx", sheet_name='clusterDatabase')
stateCombination.to_excel(excel_writer="C:/Users/youss/clusterDatabase-14.03.2023.xlsx", sheet_name='stateCombination')
clusterDatabase.to_excel(excel_writer="C:/Users/youss/clusterDatabase-14.03.2023.xlsx", sheet_name='clusterDatabase')