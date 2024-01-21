import copy

class Path():
    def __init__(self, connection):
        self.connection = connection
        self.segments = [connection.start.position]

        self.heuristic = 0
    
    def complete(self):
        net = self.connection
        start = net.start.position
        end = net.end.position

        if self.segments[0] == start and self.segments[-1] == end:
            return True
        else:
            return False

    def moves(self):
        x, y = self.segments[-1]

        next_state = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]

        valid_moves = [x for x in next_state if x not in self.segments]

        return valid_moves

    def move(self, x):
        if x in self.moves():
            self.segments.append(x)
    
    def current_node(self):
        return self.segments[-1]
    
    def wires(self):
        if self.complete():
            return self.segments[1:-1]
        
        return self.segments[1:]
    
    def neighbours(self, node):
        i = self.segments.index(node)

        pre, suc = i-1, i+1

        neighbours = []
        if pre >= 0:
            neighbours.append(self.segments[pre])
        
        if suc < len(self.segments):
            neighbours.append(self.segments[suc])
        
        return neighbours

    def copy_path(self):
        new_path = copy.copy(self)
        new_path.segments = copy.copy(self.segments)

        return new_path
    
    def __len__(self):
        return len(self.segments) - 1

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self.segments]) + "]"