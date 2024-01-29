from .net_solver import Net_Solver

from code.algorithms.functions.manhattan_distance import manhattan
from code.algorithms.functions.priority_queue import Priority_Queue

class Shortest_Net_Order(Net_Solver):
    """
    Netlist solver that solves the nets starting 
    from those whose gates are closest to each other.
    """
    def get_net_order(self):
        """
        Returns the order the nets should be solved in.
        """
        return self.sort_net_distance()
    
    def sort_net_distance(self):
        """
        Sorts the nets and returns their order.
        """
        nets = Priority_Queue()

        for net in self.model.get_nets():
            path = self.model.paths[net]
            nets.add(net, manhattan(path))
        
        return nets.get_all()
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return 'Shortest_Net_First'