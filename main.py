from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import shortest_first_solver as sfs
from code.algorithms.netlist_solver import hardest_first_solver as hfs
from code.algorithms.netlist_solver import hillclimber as hc
from code.algorithms.netlist_solver import simulated_annealing as sa

from code.analysis import test1000 as test

if __name__ == "__main__":
    chip_id = 2
    net_id = 9

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    # Create a chip and load in a netlist from our data
    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)

    # Create a model from our chip to create the connections in
    model = mod.Model(test_chip)
    # ------------------------ Random order astar -------------------
    rno = ns.Random_Net_Order(model)
    rno.run()
    print("Cost:", rno.cost(), str(rno.completion()*100) + '%% complete')
    print("Intersections:", len(rno.model.intersections), '\n')
    print(rno.nets)
    vis.vis_solver(rno)

    # ------------------------ shortest first astar -----------------
    # sno = sfs.Shortest_Net_Order(model, 0)
    # sno.run(pathfinder='standard')
    # print(sno.cost(), str(sno.completion()*100) + '%% complete')
    # print("Intersections:", sno.model.intersections, '\n')
    # vis.vis_solver(sno)

    # ------------------------ hardest first astar ------------------
    hno = hfs.Hardest_Net_Order(model)
    hno.run(pathfinder='make_space')
    print("Cost:", hno.cost(), str(hno.completion()*100) + '%% complete')
    print("Intersections:", len(hno.model.intersections), '\n')
    vis.vis_solver(hno)

    # ------------------------ reconnect astar ----------------------
    reconnected = sfs.Shortest_Net_Order(hno.model)
    reconnected.run(pathfinder='standard', from_scratch=False)
    print("Cost:", reconnected.cost(), str(reconnected.completion()*100) + '%% complete')
    print("Intersections:", len(reconnected.model.intersections), '\n')
    vis.vis_solver(reconnected)

    # ------------------------ hillclimber --------------------------
    # climber = hc.Hillclimber(rno)
    # climber.run(1, verbose=True)
    # best = climber.best_solution
    # print("Cost:", best.cost(), str(best.completion()*100) + '%% complete')
    # print("Intersections:", len(best.model.intersections), '\n')
    # vis.vis_solver(best)
    # display.cost_decrease(climber)

    # ------------------------ simmulated annealing -----------------
    # simmaneal = sa.Simulated_Annealing(hno, temperature=1500)
    # simmaneal.run(100, pathfinder='make_space', from_scratch=True, verbose=True)
    # best = simmaneal.best_solution
    # print("Cost:", best.cost(), str(best.completion()*100) + '%% complete')
    # print("Intersections:", len(best.model.intersections), '\n')
    # vis.vis_solver(best)
    # display.cost_decrease(simmaneal)

    # ------------------------ baseline test ------------------------
    baseline_test = False
    if baseline_test:
        m, costs, comp = test.run_n(model, ns.Random_Net_Order, 200, save=True)
        display.distribution(costs)
        print(m.nets)
        vis.vis_solver(m)
    
    # data = "outputs/test200.txt"
    # display.distribution(display.load_txt(data))