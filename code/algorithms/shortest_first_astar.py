import tqdm

from .standard_astar_alg import Standard_pathwise_astar
from .functions.manhattan_distance import manhattan
from .functions.priority_queue import Priority_Queue
from code.visualization import visualize as vis


class Shortest_first_astar():
    def __init__(self, model):
        self.model = model.copy_model()
        self.nets = self.sort_nets()
    
    def sort_nets(self):
        nets = Priority_Queue()

        for net in self.model.get_nets():
            path  = self.model.paths[net]

            nets.add(path, manhattan(path))
        
        return nets.get_all()
    
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