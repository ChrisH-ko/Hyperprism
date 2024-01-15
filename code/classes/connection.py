from .path import Path

class Connection():
    def __init__(self, gate_a, gate_b):
        self.gates = (gate_a, gate_b)
        self.path = None
    
