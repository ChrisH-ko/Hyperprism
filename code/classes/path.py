import copy

from code.algorithms.functions.manhattan_distance import manhattan

class Path():
    def __init__(self, connection):
        self.connection = connection
        self.segments = [connection.start.position]
    
    def lowest_length(self):
        """
        Return the lowest possible path length.
        """
        return manhattan(self)
    
    def complete(self):
        """
        Check if the path has reached its destination.
        """
        net = self.connection
        start = net.start.position
        end = net.end.position

        # First and last of element need to be the start and end gate.
        if self.segments[0] == start and self.segments[-1] == end:
            return True
        else:
            return False

    def moves(self):
        """
        Return the possible moves from the current node in the path.
        """
        x, y, z = self.segments[-1]

        next_state = [(x,y,z+1), (x,y,z-1), (x+1,y,z), (x,y+1,z), (x-1,y,z), (x,y-1,z)]

        # Filter out positions we have already visited.
        valid_moves = [x for x in next_state if x not in self.segments]

        return valid_moves

    def move(self, x):
        """
        Extend the path if the move is valid.
        """
        if x in self.moves():
            self.segments.append(x)
    
    def current_node(self):
        """
        Return the current node on the path.
        """
        return self.segments[-1]
    
    def wires(self):
        """
        Return the path segments, excluding the gates.
        i.e. the 'wires'.
        """
        if self.complete():
            return self.segments[1:-1]
        
        return self.segments[1:]
    
    def neighbours(self, node):
        """
        Given a node in the path, return its neighbours.
        """
        if node not in self.segments:
            print("This node is not in this path.")
            return
        
        # Get the node's index.
        i = self.segments.index(node)
        # Get the indices of the neighbours.
        pre, suc = i-1, i+1

        neighbours = []
        # Check if the neighbours' indices are in range.
        if pre >= 0:
            neighbours.append(self.segments[pre])
        if suc < len(self.segments):
            neighbours.append(self.segments[suc])
        
        return neighbours

    def copy_path(self):
        """
        Copies a path from itself.
        """
        new_path = copy.copy(self)
        new_path.segments = copy.copy(self.segments)

        return new_path
    
    def blank_copy_path(self):
        """
        Return a a fresh coppy of itself.
        """
        blank_copy = copy.copy(self)
        blank_copy.segments = [blank_copy.connection.start.position]
        return blank_copy
    
    def __len__(self):
        """
        Return the length of the path. That is, the number
        of wires.
        """
        return len(self.segments) - 1

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return "[" + ", ".join([str(x) for x in self.segments]) + "]"