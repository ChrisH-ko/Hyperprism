import matplotlib.pyplot as plt

def visualize(chip):

    gates_x = [chip.gates[i].position[0] for i in chip.gates]
    gates_y = [chip.gates[i].position[1] for i in chip.gates]

    _ = plt.scatter(gates_x, gates_y)
    _ = plt.xlim(0, max(gates_x)+1)
    _ = plt.ylim(0, max(gates_y)+1)


    _ = plt.box(False)
    _ = plt.tick_params(length=0, width=0, labelsize=0)
    _ = plt.grid()

    _ = plt.show()
    return gates_x, gates_y