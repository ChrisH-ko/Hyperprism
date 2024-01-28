import random
import tqdm

from code.algorithms.path_solver.standard_astar_alg import Standard_pathwise_astar
from code.algorithms.path_solver.make_space_astar import Make_Space

from code.visualization import visualize as vis

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
            old_path = self.model.paths[net]

            path = old_path.blank_copy_path()
            self.model.remove_path(net)

            solver = self.pathfinder(self.model, path)
            solver.run()
            new_path = solver.solution

            if old_path.complete():
                self.compare_paths(old_path, new_path)
            else:
                self.model.add_path(net, new_path)
    
    def compare_paths(self, old_path, new_path):
        net = old_path.connection.id

        if new_path.complete():
            old_cost = self.model.path_cost(old_path)
            new_cost = self.model.path_cost(new_path)

            if new_cost < old_cost:
                self.model.add_path(net, new_path)
                return
        
        self.model.add_path(net, old_path)


class Random_Net_Order(Net_Solver):
    def get_net_order(self):
        nets = list(self.model.get_nets())
        random.shuffle(nets)
        return nets