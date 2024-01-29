from .net_solver import Net_Solver
from code.algorithms.functions.priority_queue import Priority_Queue

class Hardest_Net_Order(Net_Solver):
    """
    Netsolver that connects the nets in order of those 
    that concern the gates with the mose connections.
    """
    def get_net_order(self):
        nets = self.model.get_nets()

        # Sort the gates.
        gates = self.sort_hardest_gates(nets)

        return self.sort_nets(gates, nets)

    def sort_hardest_gates(self, nets):
        """
        Returns the gates, sorted by how much connections they have.
        The more connections, the higher the index of a gate.
        """
        gates = Priority_Queue()
        
        # Count the nets each gate is involved in.
        for gate in self.model.chip.gates.keys():
            connections = 0

            for net in nets:
                if gate == net[0] or gate == net[1]:
                    connections += 1
            
            # Add the gates to the priority queue.
            # The more connections, the higher the index.
            gates.add(gate, connections)
        
        return gates.get_all()
    
    def sort_nets(self, gates, nets):
        """
        Returns the sorted netlist, by how much connections their gates have.

        nets are sorted by their highest priority gate and the priority of their
        other gate.
        """
        order = Priority_Queue()
        for net in nets:
            i = gates.index(net[0])
            j = gates.index(net[1])

            order.add(net, -(2**i + 2**j))

        return order.get_all()
