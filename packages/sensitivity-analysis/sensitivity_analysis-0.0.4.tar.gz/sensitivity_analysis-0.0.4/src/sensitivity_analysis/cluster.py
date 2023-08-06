import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from elbowMethod import elbowMethod
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import centroid
from scipy.spatial import distance
#iter through different state combinations
def cluster(stateDatabase, situation):
    clusterDatabase = []
    clusterSensitivity = []
    stateDatabase["Cluster"] = np.zeros
    figure, axis = plt.subplots(len(pd.unique(stateDatabase['StateCombination'])), len(pd.unique(stateDatabase['Situation'])))
    
    #Predefine the array of matrices to be used in clustering
    clusterList = []
    #Predefine matrix to indicate state combination and situation
    clusterInformationList = []
    
    #get the indeces of the active states
    stateIndexing = np.empty(stateDatabase["State"].unique().size)
    for i_state, val_state in enumerate(pd.unique(stateDatabase['State'])): stateIndexing[i_state] = int(re.search(r'\d+', val_state).group())
    #get the indeces of the active parameters
    parameterIndexing = np.empty(stateDatabase["ParameterIndex"].unique().size)
    for i_parameter, val_parameter in enumerate(pd.unique(stateDatabase['ParameterIndex'])): parameterIndexing[i_parameter] = val_parameter
    
    for _, val_stateCombination in enumerate(pd.unique(stateDatabase['StateCombination'])):
        #iter through different situations
        for _, val_situation in enumerate(pd.unique(stateDatabase['Situation'])):
            stateParameterData = stateDatabase[stateDatabase["StateCombination"] == val_stateCombination][stateDatabase["Situation"] == val_situation]
            stateParameterData = stateParameterData.reset_index()
            #print (stateParameterData)
            ##Create a numpy matrix with data for later clustering
            #Predefine the matrix
            stateParameterMatrix = np.zeros((len(stateIndexing), len(parameterIndexing)))

            #Fill the matrix
            for _, row in stateParameterData.iterrows():
                            stateParameterMatrix[np.where(stateIndexing==int(re.search(r'\d+', row["State"]).group()))[0][0]-1,
                                                np.where(parameterIndexing==row["ParameterIndex"])[0][0]-1] = row["SensitivityIndex"]
            clusterList.append(stateParameterMatrix)
            clusterInformationList.append(np.array([[val_stateCombination, val_situation, stateParameterMatrix.mean()]]))
    clusterArray = np.zeros((len(clusterList), len(clusterList[0][:, 0]), len(clusterList[0][0, :])))
    #clusterInformation = np.zeros((len(clusterList), 3))
    clusterInformation = np.zeros((len(clusterList), 4))
    for i_condition, conditionMatrix in enumerate(clusterList):
        clusterArray[i_condition] = conditionMatrix
        clusterInformation[i_condition, :3] = clusterInformationList[i_condition]
        
        
    ##cluster the data using hierarchical clustering to see similar state derivatives
    # generate the linkage matrix
    
    


    # get the distance matrix
    distanceMatrix = distance.pdist([clusterArray[i_condition, :, :].flatten() for i_condition, _ in enumerate(clusterArray[:, 0, 0])])

    linkageMatrix = linkage(distanceMatrix, method='single', metric='euclidean')

    k = elbowMethod(linkageMatrix, distance.squareform(distanceMatrix))
    
    #plot cluster results

    clusterLabel = np.transpose(fcluster(linkageMatrix, k, criterion='maxclust'), axes=None)
    clusterInformation[:, 3] = clusterLabel
    clusterDatabase = pd.DataFrame(
        {
            "StateCombination": np.array(["X_combination{}".format(i_stateCombination)for i_stateCombination in
                                          clusterInformation[:, 0]]),
            "Situation": np.array([situation[int(i_situation)] for i_situation in clusterInformation[:, 1]]),
            "SensitivityIndex": clusterInformation[:, 2],
            "Cluster": clusterInformation[:, 3],
        }
    )
    #get the centroids of the clusters
    uniqueLabel = np.unique(clusterInformation[:, 3])
    centroid = np.empty((len(uniqueLabel), 3))
    
    for i_label, val_label in enumerate(uniqueLabel):
        centroid[i_label, 0] = val_label
        centroid[i_label, 1] = np.mean(clusterInformation[np.where(clusterInformation[:,3] == i_label), 2])
    
    centroidDatabase = pd.DataFrame(
        {
            "Cluster": centroid[:, 0],
            "SensitivityIndex": centroid[:, 1],
        }
    )
    
    return clusterDatabase, centroidDatabase





"""
            for _, row in stateParameterData.iterrows():
                stateParameterMatrix[np.where(stateIndexing==int(re.search(r'\d+', row["State"]).group()))[0][0]-1,
                                    np.where(parameterIndexing==row["ParameterIndex"])[0][0]-1] = row["SensitivityIndex"]

            ##cluster the data using hierarchical clustering to see similar state derivatives
            # generate the linkage matrix
            linkageMatrix = linkage(stateParameterMatrix, method='single', metric='euclidean')

            k = elbowMethod(axis[i_stateCombination, i_situation], situation[val_situation], val_stateCombination, linkageMatrix, stateParameterMatrix)
            
            #plot cluster results

            clusterLabel = fcluster(linkageMatrix, k, criterion='maxclust')
            currentSensitivity = np.empty(len(np.unique(clusterLabel)))
            cluster = np.empty(len(stateParameterData['State']))
            
            for index, row in stateParameterData.iterrows():
                cluster[index] = clusterLabel[np.where(stateIndexing==int(re.search(r'\d+', row["State"]).group()))[0][0]-1]
            
            #add the new column to database
            stateParameterData["Cluster"] = cluster.astype(int)
            for i_cluster, val_cluster in enumerate(np.unique(clusterLabel)):
                clusterDataSet = stateParameterData[stateParameterData['Cluster'] == val_cluster]
                elementSensitivity= 0
                elementCount = 0
                for _, row_dataPoint in clusterDataSet.iterrows():
                    elementSensitivity += row_dataPoint['SensitivityIndex']
                    elementCount += 1
                currentSensitivity[i_cluster] = elementSensitivity / elementCount
                
                
            #stateDatabase[stateDatabase["StateCombination"] == val_stateCombination][stateDatabase["Situation"] ==
            #                                                                        val_situation]["Cluster"] = stateParameterData["Cluster"]
            currentDatabase = pd.DataFrame(
                {
                    "State": stateIndexing,
                    "Cluster":clusterLabel,
                }
            )
            clusterDatabase.append(currentDatabase)
            
            clusterSensitivity.append(
                pd.DataFrame(
                    {
                        "cluster": np.unique(clusterLabel),
                        "Sensitivity": currentSensitivity,
                    }
                    )
            )
    clusterDatabase = pd.concat(clusterDatabase)
    clusterSensitivity = pd.concat(clusterSensitivity)
    # Combine all the operations and display
   # plt.show()
   
    return clusterArray, clusterInformation"""