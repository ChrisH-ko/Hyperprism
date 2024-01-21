import random
from .standard_astar_alg import standard_astar

from code.visualization import visualize as vis

def random_astar(model):
    chip = model.chip
    paths = model.paths

    connections = list(chip.netlist.keys())

    random.shuffle(connections)

    for net_id in connections:
        queue = [paths[net_id]]
        standard_astar(model, queue)