class Connection():
    def __init__(self, id, gate_a, gate_b):
        self.id = id
        self.start = gate_a
        self.end = gate_b

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return str(self.start.id) + " - " + str(self.end.id)
    
