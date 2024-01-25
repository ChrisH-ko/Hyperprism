from .net_solver import Net_Solver

from code.algorithms.functions.manhattan_distance import manhattan
from code.algorithms.functions.priority_queue import Priority_Queue

class Shortest_Net_Order(Net_Solver): 
    def get_net_order(self):
        nets = Priority_Queue()

        for net in self.model.get_nets():
            path = self.model.paths[net]
            nets.add(net, manhattan(path))
        
        return nets.get_all()