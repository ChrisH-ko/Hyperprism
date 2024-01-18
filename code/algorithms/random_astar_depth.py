import random
from .standard_astar_alg import standard_astar

def random_astar(chip):
    connections = list(chip.netlist.keys())

    random.shuffle(connections)

    for net in connections:
        queue = [chip.netlist[net]]
        standard_astar(chip, queue, 'manhattan')