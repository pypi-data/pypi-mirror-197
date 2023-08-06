import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from Simulation import Simulation
def resultPlot(clusterDatabase):
    """
    # Plotting results of the simulation

    # Creating plot
    plot = go.Figure()
    plot.add_trace(
    go.Scatter3d(
        x=stateDatabase["State"],
        y=stateDatabase["Parameter"],
        z=stateDatabase["SensitivityIndex"],
        mode="markers",
        marker_size=4,
        marker_line_width=1,
        name="Simulation results",
        )
    )

    plot.update_layout(
        width=800,
        height=800,
        autosize=True,
        showlegend=True,
        scene=dict(
            xplotis=dict(title="State", titlefont_color="black"),
            yplotis=dict(title="Parameter", titlefont_color="black"),
            zplotis=dict(title="SensitivityIndex", titlefont_color="black"),
        ),
        font=dict(family="Gilroy", color="black", size=12),
    )
    #plot.show()

    plotSituation = go.Figure()



    # Plotting clustered data according to situations
    plotSituation = go.Figure()
    for i_situation in stateDatabase[~stateDatabase.duplicated("Situation")]["Situation"]:
        new_row = {
            "State": "Centroid",
            "ParameterIndex": None,
            "Parameter": "Centroid",
            "SensitivityIndex": stateDatabase.loc[
                stateDatabase["Situation"] == i_situation, "SensitivityIndex"
            ].mean(),
            "StateCombination": None,
            "Situation": i_situation,
        }
        stateDatabase = stateDatabase.append(new_row, ignore_index=True)
    
    for C in list(stateDatabase.Situation.unique()):
        plotSituation.add_trace(
            go.Scatter3d(
                x=stateDatabase[stateDatabase.Situation == C]["State"],
                y=stateDatabase[stateDatabase.Situation == C]["Parameter"],
                z=stateDatabase[stateDatabase.Situation == C]["SensitivityIndex"], mode="markers",
                marker=dict(symbol=np.where(stateDatabase[stateDatabase.Situation == C]["State"] ==
                                            "Centroid", "cross", "circle",
                                            )
                            ), marker_size=4, marker_line_width=1, name=situation[C],
                )
            )
    plotSituation.update_layout(
        width=800,
        height=800,
        autosize=True,
        showlegend=True,
        scene=dict(
            xplotis=dict(title="State", titlefont_color="black"),
            yplotis=dict(title="Parameter", titlefont_color="black"),
            zplotis=dict(title="SensitivityIndex", titlefont_color="black"),
            ),
        font=dict(family="Gilroy", color="black", size=12),
        )
    #plotSituation.show()
    
    plotStateCombination = go.Figure()
    # Plotting clustered data according to statecombinations
    for i_combination in stateDatabase[~stateDatabase.duplicated("StateCombination")][
        "StateCombination"
        ]:
        new_row = {
            "State": "Centroid",
            "ParameterIndex": None,
            "Parameter": "Centroid",
            "SensitivityIndex": stateDatabase.loc[
                stateDatabase["StateCombination"] == i_combination, "SensitivityIndex"
                ].mean(),
            "StateCombination": i_combination,
            "Situation": None,
            }
        stateDatabase = stateDatabase.append(new_row, ignore_index=True)
    for C in list(stateDatabase.StateCombination.unique()):
        
        plotStateCombination.add_trace(
            go.Scatter3d(
                x=stateDatabase[stateDatabase.StateCombination == C]["State"],
                y=stateDatabase[stateDatabase.StateCombination == C]["Parameter"],
                z=stateDatabase[stateDatabase.StateCombination == C]["SensitivityIndex"],
                mode="markers",
                marker=dict(
                    symbol=np.where(
                        stateDatabase[stateDatabase.StateCombination == C]["State"]
                        == "Centroid",
                        "cross",
                        "circle",
                        )
                    ),
                marker_size=4,
                marker_line_width=1,
                name="State Combination: " + str(C),
                )
            )

    plotStateCombination.update_layout(
        width=800,
        height=800,
        autosize=True,
        showlegend=True,
        scene=dict(
            xplotis=dict(title="State", titlefont_color="black"),
            yplotis=dict(title="Parameter", titlefont_color="black"),
            zplotis=dict(title="SensitivityIndex", titlefont_color="black"),
        ),
        font=dict(family="Gilroy", color="black", size=12),
    )
    #plotStateCombination.show()
    
    plot = go.Figure()
    plot.add_trace(
    go.Scatter3d(
        x=clusterDatabase["State"],
        y=clusterDatabase["Parameter"],
        z=clusterDatabase["SensitivityIndex"],
        mode="markers",
        marker_size=4,
        marker_line_width=1,
        name="Simulation results",
        )
    )

    plot.update_layout(
        width=800,
        height=800,
        autosize=True,
        showlegend=True,
        scene=dict(
            xplotis=dict(title="State", titlefont_color="black"),
            yplotis=dict(title="Parameter", titlefont_color="black"),
            zplotis=dict(title="SensitivityIndex", titlefont_color="black"),
        ),
        font=dict(family="Gilroy", color="black", size=12),
    )
    plot.show()
    """
    
    # Plotting clustered data for each situation/state combination
    plotCluster = go.Figure()
    
    for C in list(clusterDatabase.Cluster.unique()):
        plotCluster.add_trace(
            go.Scatter3d(
                x=clusterDatabase[clusterDatabase.Cluster == C]["StateCombination"],
                y=clusterDatabase[clusterDatabase.Cluster == C]["Situation"],
                z=clusterDatabase[clusterDatabase.Cluster == C]["SensitivityIndex"], mode="markers",
                marker=dict(symbol="circle"), marker_size=4, marker_line_width=1, name="Cluster_{}".format(C),
            )
        )

        
    plotCluster.update_layout(
        width=800,
        height=800,
        autosize=True,
        showlegend=True,
        scene=dict(
            xaxis=dict(title="StateCombination", titlefont_color="black"),
            yaxis=dict(title="Situation", titlefont_color="black"),
            zaxis=dict(title="SensitivityIndex", titlefont_color="black"),
            ),
        font=dict(family="Gilroy", color="black", size=12),
        )
    plotCluster.show()
    
    