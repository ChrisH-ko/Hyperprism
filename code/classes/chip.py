import csv

from .gate import Gate
from .netlist import Netlist
from .connection import Connection

class Chip():
    def __init__(self, chip_id, chip_file, net_id, netlist):
        self.id = chip_id
        self.net_id = net_id
        self.gates = self.load_gates(chip_file)
        self.netlist = self.load_netlist(netlist)
        self.intersections = 0

    def load_gates(self, chip_file):
        gates = {}
        with open(chip_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                id = row['chip']
                pos = (int(row['x']), int(row['y']))

                gates[id] = Gate(id, pos)
        
        return gates


    def load_netlist(self, net_id, netlist):
        connections = {}

        with open(netlist, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                a = int(row['chip_a'])
                b = int(row['chip_b'])

                connections[(a, b)] = Connection(self.gates[a], self.gates[b])
        
        return connections
    
    def __repr__(self):
        return 'test'