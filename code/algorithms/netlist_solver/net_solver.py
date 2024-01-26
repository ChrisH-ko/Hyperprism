import random
import tqdm

from code.algorithms.path_solver.standard_astar_alg import Standard_pathwise_astar
from code.algorithms.path_solver.make_space_astar import Make_Space

pathfinders = [Standard_pathwise_astar, Make_Space]

class Net_Solver():
    def __init__(self, model, pathfinder=0, verbose=True):
        self.model = model.copy_model()
        self.nets = self.get_net_order()
        self.verbose = verbose
        self.pathfinder = pathfinders[pathfinder]

    def get_net_order(self):
        return list(self.model.paths.values)
    
    def cost(self):
        return self.model.total_cost()
    
    def completion(self):
        return self.model.net_completion()
    
    def run(self):
        print('pathfinder:')
        if self.verbose:
            nets = tqdm.tqdm(self.nets)
        else:
            nets = self.nets

        for net in nets:
            path = self.model.paths[net]

            if path.complete():
                path = path.blank_copy_path()
                self.model.remove_path(net)

            solver = self.pathfinder(self.model, path)
            solver.run()
            new_path = solver.solution
            self.model.add_path(net, new_path)

class Random_Net_Order(Net_Solver):
    def get_net_order(self):
        nets = list(self.model.get_nets())
        random.shuffle(nets)
        return nets