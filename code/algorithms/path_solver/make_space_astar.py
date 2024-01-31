import numpy as np

from .standard_astar_alg import Standard_pathwise_astar
from code.algorithms.functions.manhattan_distance import manhattan

class Make_Space(Standard_pathwise_astar):
    """
    Path solver/finder which serves as a variation to the standard A* algorithm.

    Tries to connect two gates of a given net with a path that makes a lot of room
    for the other nets. Rather than using the manhattan distance as a heuristic,
    This algorithm employs a specific heuristic function that prioritizes paths
    that try to avoid being close to other gates, even if shorter paths exist.
    """
    def __init__(self, model, path):
        super().__init__(model, path)

        self.other_gates = self.load_other_gate_positions()
        self.adjacent_to_gates = self.load_adjacent_to_gates()
    
    
    def load_other_gate_positions(self):
        """
        Load the positions of all gates on the chip not involved in this path.
        """
        gates = self.model.chip.get_gates()
        gate_positions = [gate.position for gate in gates]

        # Remove the gates from this net
        gate_positions.remove(self.start)
        gate_positions.remove(self.goal)
        return gate_positions
    

    def load_adjacent_to_gates(self):
        """
        Return a list with all the positions adjacent to a gate not
        involved in our net.
        """
        positions = []
        for gate in self.other_gates:
            x = gate[0]
            y = gate[1]
            z = gate[2]

            positions.extend([(x,y,z+1), (x,y,z-1), (x+1,y,z), (x,y+1,z), (x-1,y,z), (x,y-1,z)])
        
        return positions
    

    def update_queue_and_archive(self, path, cost, heuristic):
        """
        Add a path to the queue and archive according to their cost and heuristic.
        Don't ignore a path if a shorter one happens to exists.
        """
        position = path.current_node()

        if position not in self.cheapest_path:
            self.cheapest_path[position] = path
            self.queue.add(position, cost+heuristic)


    def path_cost(self, path):
        """
        Return the current cost of a path.
        For the purpose of allowing paths to be longer than required,
        discount the cost of the pathlength.
        """
        length_discount = 10
        n = len(path)/length_discount

        k = self.model.count_intersections(path)
        return n + k * self.model.intersection_cost
    

    def heuristic(self, path):
        """
        Return the current heuristic value of a path.
        The heuristic funtion is made up of four parts.

        1. A height discount, prioritizing going up as much as possible
        2. A low priority manhattan distance,
            if there are no other improvements to be made, moves close to the destination.
        3. A steep 'pitfall' on the x and y position of the destionation.
            if a move lands the path in the pitfall, it costs a lot to get out.
        4. A penalty for sticking too close to a different gate.
        """
        current_node = path.current_node()
        current_z = current_node[2]

        # 1
        height_discount = -current_z

        # 2
        manhattan_prio = 0.1
        low_prio_manhattan = manhattan_prio * manhattan(path)

        # 3
        target_pitfall = self.gauss_vicinity(path)

        # 4
        touching_other_gate_penalty = self.check_adjacency_gate(current_node)

        return height_discount + low_prio_manhattan + target_pitfall + touching_other_gate_penalty
    

    def gauss_vicinity(self, path):
        """
        Heuristic function to act as a pitfall using a gauss function.
        Moves outside the target area gain roughly the same heuristic score.
        Moves in the target area gain a much lower score, lowest on the target
        area itself.

        i.e. once the target area has been reached, it gets hard to leave said area.
        """
        x, y, _ = path.current_node()

        # target area.
        x0, y0, _ = path.connection.end.position

        base_score = 10

        num = (x - x0)**2 + (y - y0)**2
        return -10 * np.exp(-(num/0.5)) + base_score
    

    def check_adjacency_gate(self, node):
        """
        To avoid staying close to gates from other nets, returns a heuristic value
        of the cost of an intersection if this node borders a gate.

        In other words, we are assuming that this path might cause a collision by sticking
        this close to another gate.
        """
        positions = self.adjacent_to_gates

        if node in positions:
            return self.model.intersection_cost
        return 0
    

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return "Make_Space_Astar"