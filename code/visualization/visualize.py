import plotly.graph_objects as go

import matplotlib.pyplot as plt

import matplotlib.patches as patches
from matplotlib.path import Path

def visualize(model):
    chip = model.chip
    paths = model.paths

    gates_x = [chip.gates[i].position[0] for i in chip.gates]
    gates_y = [chip.gates[i].position[1] for i in chip.gates]
    gates_z = [chip.gates[i].position[2] for i in chip.gates]
    gate_ids = ['id: ' + str(chip.gates[i].id) for i in chip.gates]

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(x=gates_x, y=gates_y, z = gates_z,
                    mode='markers',
                    name='gates',
                    text=gate_ids,
                    marker= dict(symbol='square')))

    for i, net in enumerate(chip.netlist):
        if i % 2 == 0:
            clr = 'magenta'
        else:
            clr = 'red'
        
        path = paths[net].segments

        x = [xy[0] for xy in path]
        y = [xy[1] for xy in path]
        z = [xy[2] for xy in path]

        fig.add_trace(go.Scatter3d(x=x, y=y, z =z,
                mode='lines',
                name=str(net),
                line = dict(color=clr, width=4)))

    fig.update_layout(
        scene = dict(
            xaxis = dict(
                range=[0, max(gates_x)+1],
                nticks=max(gates_x)+2,
                showticklabels=False
            ),
            yaxis = dict(
                range=[0, max(gates_y)+1],
                nticks=max(gates_y)+2,
                showticklabels=False
            ),
            zaxis = dict(
                range=[-1, 7],
                nticks = 9,
                showticklabels=False
            ),
            aspectmode='data'
        ),
        showlegend=False
    )
    fig.show()