from .standard_astar_alg import Standard_pathwise_astar
from code.algorithms.functions.manhattan_distance import manhattan

class Make_Space(Standard_pathwise_astar):
    def update_queue_and_archive(self, path):
        position = path.current_node()
        cost = self.model.path_cost(path)
        heuristic = self.heuristic(path)

        if position not in self.lowest_cost:
            self.lowest_cost[position] = cost
            self.cheapest_path[position] = path
            self.queue.add(position, cost+heuristic)
    
    def heuristic(self, path):
        current_z = path.current_node()[2]
        prev_z = path.segments[-2][2]

        if current_z > prev_z:
            return 0

        return 20*manhattan(path) + 200*(7-current_z)
    
    def __repr__(self):
        return "Make_Space_Astar"