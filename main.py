from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms import random_net_astar as rna
from code.algorithms import shortest_first_astar as sfa
from code.analysis import test1000 as test

if __name__ == "__main__":
    chip_id = 0
    net_id = 3

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    # Create a chip and load in a netlist from our data
    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)

    # Create a model from our chip to create the connections in
    model = mod.Model(test_chip)
    model2 = model.copy_model()
    model3 = model.copy_model()

    # ------------------------ Random order astar-------------------
    rna.random_astar(model)
    print(model.total_cost(), str(model.net_completion()*100) + '%% complete')
    vis.visualize(model)

    # ------------------------ shortest first astar-----------------
    sfa.short_first_astar(model2)
    print(model2.total_cost(), str(model2.net_completion()*100) + '%% complete')
    vis.visualize(model2)

    # ------------------------ baseline test -----------------------
    baseline_test = False
    if baseline_test:
        m, costs, comp = test.run_1000(model3, rna.random_astar, save=True)
        display.distribution(costs)