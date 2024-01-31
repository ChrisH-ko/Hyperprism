import copy
import csv

from .path import Path

class Model():
    """
    Model class that will contain the chip and the paths that formthe solution.
    """
    def __init__(self, chip):
        self.chip = chip
        self.paths = self.load_paths(chip)

        self.intersections = {}
        self.n_intersections = 0
        self.intersection_cost = 300
    
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
        if id != path.connection.id:
            print("id and path do not match")
        elif path.complete():
            k, crossings = self.find_intersections(path)
            self.paths[id] = path

            self.update_intersections(crossings, id)
            self.n_intersections += k
        else:
            print("incomplete path")
    
    def remove_path(self, id):
        """
        Remove the segments of a path from the model.
        """
        self.paths[id] = self.paths[id].blank_copy_path()

        # Remove the path from the intersection dictionary
        for pos in self.intersections:
            if id in self.intersections[pos]:
                self.intersections[pos].remove(id)
                self.n_intersections = self.n_intersections - 1
            
        self.intersections = {pos:nets for pos, nets in self.intersections.items() if len(nets) > 1}
    
    def update_intersections(self, crossings, id):
        """
        Update the intersection dictionary with a path and the intersections it has.
        """
        for pos in crossings:
            # Add the location of the crossing to the keys if it does not exist
            if pos not in self.intersections:
                self.intersections[pos] = crossings[pos]
            
            # Add the path to an existing crossing if it already exists.
            if id not in self.intersections[pos]:
                self.intersections[pos].append(id)

    def lower_bound_cost(self):
        """
        Return the lower bound of the total cost. The cost if every
        net had the shortest possible connection.
        """
        lowest_cost = 0

        for net in self.get_nets():
            shortest_path = self.paths[net].lowest_length()
            lowest_cost += shortest_path

        return lowest_cost

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
    
    def find_intersections(self, path):
        """
        Find the unique intersections a path introduces.
        """
        id = path.connection.id
        path_a = path.segments

        other_paths = self.get_nets()
        other_paths.remove(id)

        crossings = {}
        for id in other_paths:
            path_b = self.paths[id].wires()

            # Check if the two paths contain matching positions.
            crossing = {pos:[id] for pos in path_a if pos in path_b}
            crossings.update(crossing)
        
        k = len(crossings)
        return k, crossings
    
    def count_intersections(self, path):
        """
        Return the amount of intersections a path would introduce.
        """
        return self.find_intersections(path)[0]
    
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
        return len(path) + k * self.intersection_cost
    
    def total_cost(self):
        """
        Calculate the total cost of the paths.
        """
        total_length = 0
        for net in self.get_nets():
            total_length += len(self.paths[net])
        
        k = self.n_intersections

        return total_length + k * self.intersection_cost
    
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

    def complete(self):
        """
        Check if this model's solution is valid.
        """
        if self.net_completion() == 1:
            return True
        return False
    
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
        new_model.paths = {net_id: path.copy_path() for net_id, path in self.paths.items()}
        
        new_model.intersections = copy.copy(self.intersections)
        
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
    
    def write_output(self):
        """
        Write this model's solution to an output file.
        """
        if not self.complete():
            raise Exception("This model is not a complete solution.")
        
        file = 'outputs/models/output.csv'

        with open(file, 'w') as f:
            writer = csv.writer(f)

            writer.writerow(['net', 'wires'])

            for net in self.get_nets():
                writer.writerow([str(net), str(self.paths[net].segments)])
            
            writer.writerow([f'chip_{self.chip.id}_net_{self.chip.net_id}', self.total_cost()])
        
        f.close()
