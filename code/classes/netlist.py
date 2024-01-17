from .connection import Connection

class Netlist():
    def __init__(self, net_id, netlist):
        self.id = net_id
        self.connections = self.load_connections(netlist)
    
    def load_connections(self, netlist):
        pass