import csv

from .connection import Connection

class Netlist():
    def __init__(self, net_id, netlist):
        self.id = net_id
        self.connections = self.load_connections(netlist)
    
    def load_connections(self, netlist):
        connections = {}

        with open(netlist, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                a = row['chip_a']
                b = row['chip_b']

                connections[(a, b)] = Connection(a, b)
        
        return connections