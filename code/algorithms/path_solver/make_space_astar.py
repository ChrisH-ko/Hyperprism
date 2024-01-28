import numpy as np

from .standard_astar_alg import Standard_pathwise_astar
from code.algorithms.functions.manhattan_distance import manhattan

class Make_Space(Standard_pathwise_astar):
    def update_queue_and_archive(self, path, cost, heuristic):
        position = path.current_node()

        if position not in self.cheapest_path:
            self.cheapest_path[position] = path
            self.queue.add(position, cost+heuristic)

    def path_cost(self, path):
        return len(path)/10 + 300 * self.model.count_intersections(path)
    
    def heuristic(self, path):
        current_z = path.current_node()[2]

        height_discount = -current_z
        low_prio_manhattan = 0.1*manhattan(path)
        target_pitfall = self.gauss_vicinity(path)

        return height_discount + low_prio_manhattan + target_pitfall
    
    def gauss_vicinity(self, path):
        x, y, _ = path.current_node()
        x0, y0, _ = path.connection.end.position

        num = (x - x0)**2 + (y - y0)**2
        return -10 * np.exp(-(num/0.5)) + 10
    
    def __repr__(self):
        return "Make_Space_Astar"