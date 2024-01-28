import plotly.graph_objects as go

import matplotlib.pyplot as plt

import matplotlib.patches as patches
from matplotlib.path import Path

def visualize(model):
    total_cost = model.total_cost()

    chip = model.chip
    chip_id = chip.id
    netlist_id = chip.net_id
    intersections = model.intersections

    paths = model.paths

    gates_x = [chip.gates[i].position[0] for i in chip.gates]
    gates_y = [chip.gates[i].position[1] for i in chip.gates]
    gates_z = [chip.gates[i].position[2] for i in chip.gates]
    gate_text = [str(chip.gates[i].id) for i in chip.gates]
    gate_h = ['id: ' + txt for txt in gate_text]

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(x=gates_x, y=gates_y, z = gates_z,
                    mode='markers+text',
                    name='gates',
                    text=gate_text,
                    hovertext=gate_h,
                    textposition='top left',
                    textfont=dict(
                        size=18
                        ),
                    marker= dict(
                        symbol='square',
                        color='red')))

    for i, net in enumerate(chip.netlist):
        if i % 2 == 0:
            clr = '#0749b3'
        else:
            clr = '#56a9d6'
        
        path = paths[net].segments

        x = [xy[0] for xy in path]
        y = [xy[1] for xy in path]
        z = [xy[2] for xy in path]

        fig.add_trace(go.Scatter3d(x=x, y=y, z =z,
                mode='lines',
                name=str(net),
                line = dict(color=clr, width=4)))
        
    int_x = [pos[0] for pos in intersections]
    int_y = [pos[1] for pos in intersections]
    int_z = [pos[2] for pos in intersections]
    int_text = [str(intersections[pos] for pos in intersections)]

    fig.add_trace(go.Scatter3d(x=int_x, y=int_y, z = int_z,
                    mode='markers',
                    name='intersections',
                    hovertext=int_text,
                    marker= dict(
                        symbol= 'x',
                        color='#f500e0',
                        size=6,
                        line=dict(
                            color='MediumPurple',
                            width=2
                        ))))

    fig.update_layout(
        title=dict(
            text=f"""   Chip {chip_id} <br>
                        Netlist #{netlist_id} <br>
                        Total cost: {total_cost} <br>
                        Intersections: {len(intersections)}""",
            xanchor='right',
            yanchor='top',
            x = 0.5,
            y = 0.9),
        font=dict(
            size=16
        ),
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

def vis_solver(solver):
    visualize(solver.model)