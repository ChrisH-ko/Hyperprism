class Connection():
    def __init__(self, gate_a, gate_b):
        self.start = gate_a
        self.end = gate_b
        self.path = [gate_a.pos]
    
    def cost(self):
        return len(self.path)
    
