from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis

from code.algorithms import random_astar_depth as rad

if __name__ == "__main__":
    chip_id = 0
    net_id = 3

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)
    model = mod.Model(test_chip)

    rad.random_astar(model)
    model.print_netlist()
    vis.visualize(model)