import copy
from .path import Path

class Model():
    def __init__(self, chip):
        self.chip = chip
        self.paths = self.load_paths(chip)
        self.intersections = 0
    

    def load_paths(self, chip):
        paths = {}

        for net in chip.netlist:
            value = Path(chip.netlist[net])
            key = value.connection.id

            paths[key] = value
        
        return paths
    

    def add_path(self, id, path):
        if id is not path.connection.id:
            print("id and path do not match")
        elif path.complete():
            k = self.check_intersections(path)
            self.paths[id] = path
            self.intersections += k
        else:
            print("incomplete path")
    
    def complete_connection(self, net_id):
        return self.paths[net_id].complete()
    

    def valid_moves(self, path):
        chip = self.chip
        gates = [chip.gates[i].position for i in chip.gates]

        moves = path.moves()
        current_node = path.current_node()
        target = path.connection.end.position

        gates.remove(target)

        valid_moves = [p for p in moves if p not in gates]

        l, u = chip.dim
        valid_moves = [p for p in valid_moves if p[0] >= l[0] and p[1] >= l[1]]
        valid_moves = [p for p in valid_moves if p[0] <= u[0] and p[1] <= u[1]]

        valid_moves = self.check_collisions(current_node, valid_moves)

        return valid_moves
    

    def check_intersections(self, path):
        id = path.connection.id
        path_a = path.segments

        other_paths = [id for id in self.chip.netlist]
        other_paths.remove(id)

        crossings = set()
        for id in other_paths:
            path_b = self.paths[id].wires()

            crossing = [xy for xy in path_a if xy in path_b]
            crossings.update(crossing)
        
        k = len(crossings)

        return k
    

    def check_collisions(self, current_node, moves):
        for net in self.chip.netlist:
            path = self.paths[net]
            segments = path.segments

            if current_node in segments:
                neighbours = path.neighbours(current_node)

                moves = [x for x in moves if x not in neighbours]
        
        return moves
    

    def path_cost(self, path):
        k = self.check_intersections(path)
        return len(path) + k * 300
    

    def total_cost(self):
        chip = self.chip

        total_length = 0
        for net in chip.netlist:
            total_length += len(self.paths[net])
        
        k = self.intersections

        return total_length + k * 300
    

    def net_completion(self):
        complete_nets = 0
        total_nets = len(self.chip.netlist)

        for net in self.chip.netlist:
            if self.complete_connection(net):
                complete_nets += 1
        
        return complete_nets / total_nets

    def copy_model(self):
        new_model = copy.copy(self)

        for net in self.chip.netlist:
            new_model.paths[net] = self.paths[net].copy_path
        
        return new_model
    
    def print_netlist(self):
        id = self.chip.id
        net_id = self.chip.net_id

        for net in self.chip.netlist:
            print(self.chip.netlist[net], self.paths[net])
        print(f"chip_{id}_net_{net_id}", self.total_cost())