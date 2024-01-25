from .net_solver import Net_Solver
from code.algorithms.functions.priority_queue import Priority_Queue

class Hardest_Net_Order(Net_Solver):
    def get_net_order(self):
        nets = self.model.get_nets()

        gates = Priority_Queue()
        order = Priority_Queue()

        for gate in self.model.chip.gates.keys():
            connections = 0
            for net in nets:
                if gate == net[0] or gate == net[1]:
                    connections += 1
            
            gates.add(gate, connections)
        
        gates = gates.get_all()
        print(gates)

        for net in nets:
            i = gates.index(net[0])
            j = gates.index(net[1])
            order.add(net, -(2**i + 2**j))

        return order.get_all()