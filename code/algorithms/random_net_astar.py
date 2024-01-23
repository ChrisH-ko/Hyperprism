import random
import tqdm

from .standard_astar_alg import Standard_pathwise_astar, standard_astar

class Random_Order_Astar():
    def __init__(self, model):
        self.model = model.copy_model()
        self.nets = self.shuffle_nets()

    def shuffle_nets(self):
        nets = list(self.model.get_nets())
        random.shuffle(nets)
        return nets
    
    def cost(self):
        return self.model.total_cost()
    
    def completion(self):
        return self.model.net_completion()
    
    def run(self):
        for net in tqdm.tqdm(self.nets):
            path = self.model.paths[net]
            solver = Standard_pathwise_astar(self.model, path)
            solver.run()
            new_path = solver.solution
            self.model.paths[net] = new_path