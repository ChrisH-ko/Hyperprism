from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms import random_astar_depth as rad
from code.analysis import test1000 as test

if __name__ == "__main__":
    chip_id = 1
    net_id = 4

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    # Create a chip and load in a netlist from our data
    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)

    # Create a model from our chip to create the connections in
    model = mod.Model(test_chip)
    blank = model.copy_model()

    # ------------------------ Random order astar-------------------
    rad.random_astar(model)
    # model.print_netlist()
    print(model.total_cost(), str(model.net_completion()*100) + '%% complete')
    vis.visualize(model)

    # ------------------------ baseline test -----------------------
    #m, costs, comp = test.run_1000(blank, rad.random_astar)
    #display.test_data(comp, costs)