import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import cophenet as cop
from scipy.spatial.distance import pdist
from detailDendrogram import detailDendrogram

def elbowMethod(linkageMatrix, distanceMatrix):
    correlationIndex, coph_dists = cop(linkageMatrix, pdist(distanceMatrix))
    
    detailDendrogram(
        linkageMatrix,
        truncate_mode='lastp',
        p=12,
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
        annotate_above=10,  # useful in small plots so annotations don't overlap
        )

    last = linkageMatrix[-10:, 2]
    last_rev = last[::-1]
    idxs = np.arange(1, len(last) + 1)
    plt.plot(idxs, last_rev)

    acceleration = np.diff(last, 2)  # 2nd derivative of the distances
    acceleration_rev = acceleration[::-1]
    plt.plot(idxs[:-2] + 1, acceleration_rev)
    #plt.show()
    k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
    return k