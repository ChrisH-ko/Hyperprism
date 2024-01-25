from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import shortest_first_solver as sfs
from code.algorithms.netlist_solver import hardest_first_solver as hfs

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
    # ------------------------ Random order astar -------------------
    # rno = ns.Random_Net_Order(model)
    # rno.run()
    # print(rno.cost(), str(rno.completion()*100) + '%% complete')
    # vis.vis_solver(rno)

    # ------------------------ shortest first astar -----------------
    # sno = sfs.Shortest_Net_Order(model)
    # sno.run()
    # print(sno.cost(), str(sno.completion()*100) + '%% complete')
    # vis.vis_solver(sno)

    # ------------------------ hardest first astar ------------------
    hno = hfs.Hardest_Net_Order(model)
    hno.run()
    print(hno.nets)
    print(hno.cost(), str(hno.completion()*100) + '%% complete')
    vis.vis_solver(hno)


    # ------------------------ baseline test ------------------------
    baseline_test = False
    if baseline_test:
        m, costs, comp = test.run_n(model, ns.Random_Net_Order, 100, save=True)
        display.distribution(costs)
        vis.visualize(m)