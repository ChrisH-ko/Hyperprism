from .gate import Gate
from .connection import Connection
from .path import Path

class Chip():
    def __init__(self, chip_id, chip_file, net_id, netlist):
        self.id = chip_id
        self.gates = self.load_gates(chip_file)
        self.netlist = self.load_netlist(net_id, netlist)
        self.intersections = 0

    def load_gates(self, chip_file):
        pass

    def load_netlist(self, net_id, netlist):
        pass