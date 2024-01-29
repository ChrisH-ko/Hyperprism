import random
import tqdm

from code.algorithms.path_solver.standard_astar_alg import Standard_pathwise_astar
from code.algorithms.path_solver.make_space_astar import Make_Space

from code.visualization import visualize as vis

pathfinders = {
    'random':'', 
    'standard':Standard_pathwise_astar,
    'make_space': Make_Space
    }

random.seed(0)

class Net_Solver():
    def __init__(self, model, nets=None):
        self.model = model.copy_model()

        self.nets = nets
        if nets is None:
            self.nets = self.get_net_order()
    
    def get_net_order(self):
        return list(self.model.get_nets())
    
    def cost(self):
        return self.model.total_cost()
    
    def completion(self):
        return self.model.net_completion()
    
    def connect_net(self, net, pathfinder):
        old_path = self.model.paths[net]
        path = old_path.blank_copy_path()

        self.model.remove_path(net)

        solver = pathfinders[pathfinder](self.model, path)
        solver.run()
        new_path = solver.solution

        return old_path, new_path
    
    def run(self, from_scratch=True, pathfinder='standard', verbose=True):
        nets = self.check_verbose(pathfinder, verbose)

        if from_scratch:
            self.wipe_model()
        
        for net in nets:
            old_path, new_path = self.connect_net(net, pathfinder)

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
    
    def check_verbose(self, pathfinder, verbose):
        if verbose:
            print(f'pathfinder: {pathfinder}')
            return tqdm.tqdm(self.nets)
        return self.nets
    
    def wipe_model(self):
        for net in self.nets:
            self.model.remove_path(net)


class Random_Net_Order(Net_Solver):
    def get_net_order(self):
        nets = list(self.model.get_nets())
        random.shuffle(nets)
        return nets