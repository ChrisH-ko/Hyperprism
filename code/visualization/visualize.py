import plotly.graph_objects as go

import matplotlib.pyplot as plt

import matplotlib.patches as patches
from matplotlib.path import Path

def visualize(model):
    chip = model.chip
    paths = model.paths

    gates_x = [chip.gates[i].position[0] for i in chip.gates]
    gates_y = [chip.gates[i].position[1] for i in chip.gates]
    gates_z = [0 for i in chip.gates]

    # plt.scatter(gates_x, gates_y)
    # plt.xlim(0, max(gates_x)+1.05)
    # plt.ylim(-0.05, max(gates_y)+1)

    fig = go.Figure()

    # fig.update_xaxes(range=[0, max(gates_x)+1], nticks=max(gates_x)+2, showticklabels=False, constrain="domain")
    # fig.update_yaxes(range=[0, max(gates_y)+1],
    #                 nticks=max(gates_y)+2,
    #                 showticklabels=False,
    #                 scaleanchor = "x",
    #                 scaleratio = 1,)
    # fig.update_zaxes(range=[0, 7])

    fig.add_trace(go.Scatter3d(x=gates_x, y=gates_y, z = gates_z,
                    mode='markers',
                    name='gates',
                    marker= dict(symbol='square')))

    # ax = plt.gca()
    for net in chip.netlist:
        path = paths[net].segments

        x = [xy[0] for xy in path]
        y = [xy[1] for xy in path]
        z = [0 for xy in path]

        fig.add_trace(go.Scatter3d(x=x, y=y, z =z,
                mode='lines',
                name=str(net),
                line = dict(color='red', width=4)))

        # path = Path(path)
        # patch = patches.PathPatch(path, facecolor='none', lw=2)
        # ax.add_patch(patch)


    fig.update_layout(
        scene = dict(
            xaxis = dict(
                range=[0, max(gates_x)+1],
                nticks=max(gates_x)+2,
                showticklabels=False,
                # constrain="domain"
            ),
            yaxis = dict(
                range=[0, max(gates_y)+1],
                nticks=max(gates_y)+2,
                showticklabels=False,
            ),
            zaxis = dict(
                range=[-1, 7],
                nticks = 9,
                showticklabels=False
            )
        )
    )
    fig.show()
    # plt.box(False)
    # plt.tick_params(length=0, width=0, labelsize=0)
    # plt.grid()

    # ax.set_aspect("equal")
    # ax.set_xticks([i for i in range(0, max(gates_x)+2)])
    # ax.set_yticks([i for i in range(0, max(gates_y)+2)])
    # ax.set_axisbelow(True)
    # plt.show()