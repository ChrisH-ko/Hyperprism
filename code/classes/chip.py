import csv

from .gate import Gate
from .netlist import Netlist

class Chip():
    def __init__(self, chip_id, chip_file, net_id, netlist):
        self.id = chip_id
        self.gates = self.load_gates(chip_file)
        self.netlist = self.load_netlist(net_id, netlist)
        self.intersections = 0

    def load_gates(self, chip_file):
        gates = {}
        with open(chip_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                id = row['chip']
                pos = (row['x'], row['y'])

                gates[id] = Gate(id, pos)
        
        return gates


    def load_netlist(self, net_id, netlist):
        return Netlist(net_id, netlist)
    
    def __repr__(self):
        return 'test'