import csv

from .gate import Gate
from .connection import Connection

class Chip():
    def __init__(self, chip_id, chip_file, net_id, netlist):
        self.id = chip_id
        self.net_id = net_id
        self.gates = self.load_gates(chip_file)
        self.netlist = self.load_netlist(netlist)
        self.dim = self.load_dim()

    def load_gates(self, chip_file):
        """
        Load the gates onto the chip.
        """
        gates = {}
        with open(chip_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                id = int(row['chip'])
                pos = (int(row['x']), int(row['y']), 0)

                gates[id] = Gate(id, pos)
        
        return gates

    def load_netlist(self, netlist):
        """
        Load the netlist onto the chip.
        """
        connections = {}

        with open(netlist, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                a = int(row['chip_a'])
                b = int(row['chip_b'])

                connections[(a, b)] = Connection((a, b), self.gates[a], self.gates[b])
        
        return connections

    def load_dim(self):
        """
        Return the coordinates that encloses the chip.
        Includes the 7 extra layers on the z-axis.
        """
        gates_x = [self.gates[i].position[0] for i in self.gates]
        gates_y = [self.gates[i].position[1] for i in self.gates]

        return ((0, 0, 0), (max(gates_x)+1, max(gates_y)+1, 7))
    
    def get_nets(self):
        """
        Returns the nets in the netlist.
        """
        return [net for net in self.netlist]
    
    def check_valid_pos(self, pos):
        """
        Check if a position is in the range of the chip and not occupied
        by an existing gate.
        """
        gates = [self.gates[i].position for i in self.gates]
        lower, upper = self.load_dim()

        if pos in gates:
            return False
        
        for i, l, u in zip(pos, lower, upper):
            if i < l or u < i:
                return False
        
        return True
        
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        gates = 'Gates: ' + str(len(self.gates))
        netlist = '\nNetlist: '

        for net in self.get_nets():
            netlist += '\n' + str(net)

        return gates + netlist