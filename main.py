from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms import random_net_astar as rna
from code.algorithms import shortest_first_astar as sfa
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
    # ------------------------ Random order astar-------------------
    rod = rna.Random_Order_Astar(model)
    rod.run()
    print(rod.cost(), str(rod.completion()*100) + '%% complete')
    vis.visualize(rod)

    # ------------------------ shortest first astar-----------------
    sa = sfa.shortest_first_astar(model)
    sa.run()
    print(sa.cost(), str(sa.completion()*100) + '%% complete')
    vis.visualize(sa)

    # ------------------------ baseline test -----------------------
    baseline_test = False
    if baseline_test:
        m, costs, comp = test.run_1000(model, rna.Random_Order_Astar, save=True)
        display.distribution(costs)