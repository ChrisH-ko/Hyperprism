import copy
from .path import Path

class Model():
    def __init__(self, chip):
        self.chip = chip
        self.paths = self.load_paths(chip)
        self.intersections = 0
    
    def load_paths(self, chip):
        """
        Prepare dict with paths from netlist.
        """
        paths = {}

        for net in self.get_nets():
            value = Path(chip.netlist[net])
            key = value.connection.id

            paths[key] = value
        
        return paths
    
    def add_path(self, id, path):
        """
        Add a completed path to the corresponding net.
        """
        if id is not path.connection.id:
            print("id and path do not match")
        elif path.complete():
            k = self.count_intersections(path)
            self.paths[id] = path
            self.intersections += k
        else:
            print("incomplete path")
    
    def complete_connection(self, net_id):
        """
        Check if a net has been completed.
        """
        return self.paths[net_id].complete()

    def valid_moves(self, path):
        """
        Return the valid moves that can be taken from a path.
        """
        chip = self.chip

        # Get the current position, possible moves and target gate.
        current_node = path.current_node()
        moves = path.moves()
        target = path.connection.end.position

        # Filter out moves to the wrong gate or not in the chip's dimensions.
        valid_moves = [p for p in moves if chip.check_valid_pos(p) or p == target]

        # Filter out moves that would cause a collision with another path.
        valid_moves = self.filter_collisions(current_node, valid_moves)

        return valid_moves
    
    def count_intersections(self, path):
        """
        Count the number of unique intersections a path introduces.
        """
        id = path.connection.id
        path_a = path.segments

        other_paths = self.get_nets()
        other_paths.remove(id)

        crossings = set()
        for id in other_paths:
            path_b = self.paths[id].wires()

            # Check if the two paths contain matching positions.
            crossing = [xy for xy in path_a if xy in path_b]
            crossings.update(crossing)
        
        k = len(crossings)

        return k
    
    def filter_collisions(self, current_node, moves):
        """
        Filter out moves that would cause a collision with another path.
        """
        for net in self.get_nets():
            path = self.paths[net]
            segments = path.segments

            # Check if another path contains the current node
            if current_node in segments:
                # Get the neighbouring nodes in the other path
                neighbours = path.neighbours(current_node)

                # A move cannot be a neighbouring node in the other path.
                moves = [x for x in moves if x not in neighbours]
        
        return moves
    
    def path_cost(self, path):
        """
        Calculate the cost a path would add to the chip if it were added.
        """
        k = self.count_intersections(path)
        return len(path) + k * 300
    
    def total_cost(self):
        """
        Calculate the total cost of the paths.
        """
        total_length = 0
        for net in self.get_nets():
            total_length += len(self.paths[net])
        
        k = self.intersections

        return total_length + k * 300
    
    def net_completion(self):
        """
        return the ratio of completed connections.
        """
        complete_nets = 0
        total_nets = len(self.chip.netlist)

        for net in self.chip.netlist:
            if self.complete_connection(net):
                complete_nets += 1
        
        return complete_nets / total_nets
    
    def get_nets(self):
        """
        Return the nets in the netlist.
        """
        return self.chip.get_nets()

    def copy_model(self):
        """
        Copies a model from itself.
        """
        new_model = copy.copy(self)
        new_model.paths = copy.copy(self.paths)
        new_model.intersections = copy.copy(self.intersections)

        for net in new_model.chip.netlist:
            new_model.paths[net] = self.paths[net].copy_path()
        
        return new_model
    
    def show_netlist(self):
        """
        Print the path of each net and the total cost.
        """
        id = self.chip.id
        net_id = self.chip.net_id

        for net in self.chip.netlist:
            print(self.chip.netlist[net], self.paths[net])
        print(f"chip_{id}_net_{net_id}", self.total_cost())