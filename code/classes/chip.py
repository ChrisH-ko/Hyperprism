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
        gates = {}
        with open(chip_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                id = int(row['chip'])
                pos = (int(row['x']), int(row['y']))

                gates[id] = Gate(id, pos)
        
        return gates


    def load_netlist(self, netlist):
        connections = {}

        with open(netlist, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                a = int(row['chip_a'])
                b = int(row['chip_b'])

                connections[(a, b)] = Connection((a, b), self.gates[a], self.gates[b])
        
        return connections

    def load_dim(self):
        gates_x = [self.gates[i].position[0] for i in self.gates]
        gates_y = [self.gates[i].position[1] for i in self.gates]

        return ((0, 0), (max(gates_x)+1, max(gates_y)+1))
    
    def __repr__(self):
        return 'test'