import matplotlib.pyplot as plt

import matplotlib.patches as patches
from matplotlib.path import Path

def visualize(chip):

    gates_x = [chip.gates[i].position[0] for i in chip.gates]
    gates_y = [chip.gates[i].position[1] for i in chip.gates]

    plt.scatter(gates_x, gates_y)
    plt.xlim(0, max(gates_x)+1.05)
    plt.ylim(-0.05, max(gates_y)+1)

    ax = plt.gca()
    for net in chip.netlist:
        path = chip.netlist[net].path

        path = Path(path)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)



    plt.box(False)
    plt.tick_params(length=0, width=0, labelsize=0)
    plt.grid()

    ax.set_aspect("equal")
    ax.set_xticks([i for i in range(0, max(gates_x)+2)])
    ax.set_yticks([i for i in range(0, max(gates_y)+2)])
    ax.set_axisbelow(True)
    plt.show()