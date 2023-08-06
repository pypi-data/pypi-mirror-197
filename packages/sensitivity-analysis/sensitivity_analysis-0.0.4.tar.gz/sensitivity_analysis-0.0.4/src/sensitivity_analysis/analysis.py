import numpy as np
from SALib.analyze import morris as ma
import math
from Simulation import Simulation
import pandas as pd

def analysis(problem, x_bound, xMatrix, parameterMatrix, parameterAttribute, attributeList):
    # load simulation
    simulation = Simulation(xMatrix[0], parameterMatrix, parameterAttribute)
    
    si_state = []
    for i_test in range(len(x_bound[:, 0])):
        si_state.append([])

    # Now looping through different state combinations
    for i in range(np.size(xMatrix[:, 0])):
        si_i = []
        df_si_i = []
        # simulate
        simulation = Simulation(xMatrix[i], parameterMatrix, parameterAttribute)
        X_dot = simulation.__allSituations__()
        # Now looping through situations
        for j, _ in enumerate(X_dot):
            X_dot_situation = X_dot[j]
            # Now looping through different states (outputs)
            si_j = []
            for k, _ in enumerate(X_dot_situation[0]):
                si_k = ma.analyze(
                    problem, parameterMatrix, X_dot_situation[:, k], print_to_console=False
                )
                si_k["stateCombination"] = i
                si_k["situation"] = j
                # Now eliminate parameters that have no effect
                i_zero = []
                for ind_s, _ in enumerate(si_k["mu"]):
                    if (
                        (si_k["mu"][ind_s] == 0 or math.isnan(si_k["mu"][ind_s]))
                        and (
                            si_k["mu_star"][ind_s] == 0
                            or math.isnan(si_k["mu_star"][ind_s])
                        )
                        and (si_k["sigma"][ind_s] == 0 or math.isnan(si_k["sigma"][ind_s]))
                        and (
                            si_k["mu_star_conf"][ind_s] == 0
                            or math.isnan(si_k["mu_star_conf"][ind_s])
                        )
                    ):
                        i_zero.append(ind_s)
                si_k["mu"] = np.delete(si_k["mu"], i_zero)
                si_k["mu_star"] = np.delete(si_k["mu_star"], i_zero)
                si_k["sigma"] = np.delete(si_k["sigma"], i_zero)
                si_k["mu_star_conf"] = np.delete(si_k["mu_star_conf"], i_zero)
                for i_del in reversed(i_zero):
                    del si_k["names"][i_del]

                for i_test, _ in enumerate(si_k["mu_star"]):
                    si_state[k].append(
                        [
                            si_k["names"][i_test],
                            si_k["mu_star"][i_test],
                            si_k["stateCombination"],
                            si_k["situation"],
                        ]
                    )

                si_k = pd.DataFrame(si_k)
                si_j.append(si_k)

            df_si_i.append(pd.concat(si_j))
            si_i.append(si_j)
        si = pd.concat(df_si_i)

    noActiveState = len(si_state)
    stateDatabase = []
    for i_empty in reversed(range(len((si_state)))):
        if len(si_state[i_empty]) == 0:
            si_state.remove(si_state[i_empty])
            noActiveState -= 1
        else:
            for i_point in si_state[i_empty]:
                stateDatabase.append(
                    [
                        "x" + str(i_empty),
                        attributeList.index(i_point[0]),
                        i_point[0],
                        i_point[1],
                        i_point[2],
                        i_point[3],
                    ]
                )

    ## Gettig a Dataframe of the results
    stateDatabase = np.array(stateDatabase)
    stateDatabase = pd.DataFrame(
        {
            "State": stateDatabase[:, 0],
            "ParameterIndex": stateDatabase[:, 1].astype(int),
            "Parameter": stateDatabase[:, 2],
            "SensitivityIndex": stateDatabase[:, 3].astype(float),
            "StateCombination": stateDatabase[:, 4].astype(int),
            "Situation": stateDatabase[:, 5].astype(int),
        }
    )
    #stateDatabase = stateDatabase.iloc[::-1]
    return stateDatabase, simulation