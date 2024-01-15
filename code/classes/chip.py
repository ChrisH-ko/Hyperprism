from .gate import Gate
from .connection import Connection
from .path import Path

class Chip():
    def __init__(self, gate_file, netlist):
        self.gates = self.load_gates(gate_file)
        self.connections = self.load_connections(netlist)
        self.intersections = 0
    
    def load_gates(self, gates):
        pass

    def load_connections(self, netlist):
        pass