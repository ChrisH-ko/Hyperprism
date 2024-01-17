import random

def random_astar(chip):
    connections = list(chip.netlist.connections.keys())

    random.shuffle(connections)

    return connections