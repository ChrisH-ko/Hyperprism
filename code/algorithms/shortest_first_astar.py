import tqdm

from .standard_astar_alg import Standard_pathwise_astar, standard_astar
from .functions.manhattan_distance import manhattan

class shortest_first_astar():
    def __init__(self, model):
        self.model = model.copy_model()
        self.nets = self.sort_nets()
    
    def sort_nets(self):
        nets = []

        for net in self.model.get_nets():
            path  = self.model.paths[net]
            path.heuristic = manhattan(path)

            for i in range(len(nets)):
                if path.heuristic <= nets[i].heuristic:
                    nets.insert(i, path)
                    break
            if path not in nets:
                nets.append(path)
        
        return nets
    
    def cost(self):
        return self.model.total_cost()
    
    def completion(self):
        return self.model.net_completion()
    
    def run(self):
        for path in tqdm.tqdm(self.nets):
            solver = Standard_pathwise_astar(self.model, path)
            solver.run()
            new_path = solver.solution
            self.model.add_path(new_path.connection.id, new_path)