class Connection():
    def __init__(self, id, gate_a, gate_b):
        self.id = id
        self.start = gate_a
        self.end = gate_b
        self.path = [gate_a.position]

        self.heuristic = 0
    
    def valid(self):
        start = self.start.position
        end = self.end.position

        if self.path[0] == start and self.path[-1] == end:
            return True
        else:
            return False
    
    def moves(self):
        x, y = self.path[-1]

        next_state = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]

        valid_moves = [x for x in next_state if x not in self.path]

        return valid_moves
    
    def move(self, x):
        if x in self.moves():
            self.path.append(x)

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self.path]) + "]"
    
    def __len__(self):
        return len(self.path) - 1
    
