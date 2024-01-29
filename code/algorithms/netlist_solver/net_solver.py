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
    """
    Netlist solver that connects the netlist of the chip in a given order.
    """
    def __init__(self, model, nets=None):
        self.model = model.copy_model()

        # Uses the standard netlist order of the chip if none is given.
        self.nets = nets
        if nets is None:
            self.nets = self.get_net_order()
    
    def get_net_order(self):
        """
        Load the net order from the netlist in the model.
        """
        return list(self.model.get_nets())
    
    def cost(self):
        """
        Return the cost of a solution.
        """
        return self.model.total_cost()
    
    def completion(self):
        """
        Return the fraction of complete connections of the solution.
        """
        return self.model.net_completion()
    
    def connect_net(self, net, pathfinder):
        """
        Connect a net with a given pathfinder.
        """
        # Save and remove the old net to compare with the new one.
        old_path = self.model.paths[net]
        self.model.remove_path(net)

        path = old_path.blank_copy_path()

        # Connect the net with a pathfinder
        solver = pathfinders[pathfinder](self.model, path)
        solver.run()
        new_path = solver.solution

        return old_path, new_path
    
    def run(self, from_scratch=True, pathfinder='standard', verbose=True):
        """
        Connect the nets in a given order with a given pathfinder.
        Can also reconnect the nets if the model already contains a solution.
        """
        # Adds progress bar to for-loop if verbose is True.
        nets = self.check_verbose(pathfinder, verbose)

        # If from_scratch is True, removes any existing paths in the model.
        if from_scratch:
            self.wipe_model()
        
        # Connect the nets in order.
        for net in nets:
            old_path, new_path = self.connect_net(net, pathfinder)

            # Keeps the old path if the new path is worse.
            if old_path.complete():
                self.compare_paths(old_path, new_path)
            else:
                self.model.add_path(net, new_path)
    
    def compare_paths(self, old_path, new_path):
        """
        Compare two paths of the same net and keeps the cheapest one.
        """
        net = old_path.connection.id

        if new_path.complete():
            old_cost = self.model.path_cost(old_path)
            new_cost = self.model.path_cost(new_path)

            if new_cost < old_cost:
                self.model.add_path(net, new_path)
                return
        
        self.model.add_path(net, old_path)
    
    def check_verbose(self, pathfinder, verbose):
        """
        Returns the net order with a progress bar if verbose is True.
        """
        if verbose:
            print(f'pathfinder: {pathfinder}')
            return tqdm.tqdm(self.nets)
        return self.nets
    
    def wipe_model(self):
        """
        Remove any existing paths in the model.
        """
        for net in self.nets:
            self.model.remove_path(net)
    
    def results(self):
        """
        Print the results of the model's solution.
        """
        if self.completion() == 0:
            raise Exception('Solver not run yet.')
        
        print("Cost:", self.cost(), str(self.completion()*100) + '%% complete')
        print("Intersections:", len(self.model.intersections), '\n')


class Random_Net_Order(Net_Solver):
    """
    Netlist solver that connects the nets in the netlist in a random order.
    """
    def get_net_order(self):
        """
        Returns a shuffles netlist.
        """
        nets = list(self.model.get_nets())
        random.shuffle(nets)
        return nets