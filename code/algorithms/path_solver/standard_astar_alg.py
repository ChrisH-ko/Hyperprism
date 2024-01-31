from code.algorithms.functions.manhattan_distance import manhattan
from code.algorithms.functions.priority_queue import Priority_Queue

class Standard_pathwise_astar():
    """
    Path solver/finder which connects two gates from a given net and chip
    via their cheapest available path using A*.

    This baseline algorithm makes use of the manhattan distance between
    the current end of a path and the destination.
    """
    def __init__(self, model, path):
        self.model = model
        self.start = path.connection.start.position
        self.goal = path.connection.end.position

        # Queue to get the paths that should be expanded first
        self.queue = Priority_Queue()
        self.queue.add(self.start, manhattan(path))

        # Dictionaries to save which positions have already been
        # visited and how to best reach them.
        self.lowest_cost = dict()
        self.lowest_cost[self.start] = 0

        self.cheapest_path = dict()
        self.cheapest_path[self.start] = path

        self.solution = path


    def get_path_extensions(self, path):
        """
        Returns a path's valid moves.
        """
        moves = self.model.valid_moves(path)
        return moves
    

    def apply_new_moves(self, path, moves):
        """
        Extends a path with the given moves and appropriately 
        adds the extensions to the queue and archive 
        """
        for a in moves:
            child = path.copy_path()
            child.move(a)

            cost = self.path_cost(child)
            heuristic = self.heuristic(child)

            self.update_queue_and_archive(child, cost, heuristic)
    

    def update_queue_and_archive(self, path, cost, heuristic):
        """
        Add a path to the queue and archive according to their cost and heuristic.
        """
        position = path.current_node()

        if position not in self.lowest_cost or cost < self.lowest_cost[position]:
            self.lowest_cost[position] = cost
            self.cheapest_path[position] = path
            self.queue.add(position, cost+heuristic)
    

    def path_cost(self, path):
        """
        Return the current cost of a path.
        """
        return self.model.path_cost(path)


    def heuristic(self, path):
        """
        Return the current heuristic value of a path.
        The baseline algorithm makes use of the manhattan distance.
        """
        return manhattan(path)


    def run(self):
        """
        Extend the path from the starting position, prioritizing paths with the
        lowest sum of cost and heuristic.
        """
        while self.queue.not_empty():
            position = self.queue.get()

            # Stop if the end gate has been reached.
            if position == self.goal:
                self.solution = self.cheapest_path[position]
                break

            path = self.cheapest_path[position]

            # Get possible extensions of the current path.
            new_moves = self.get_path_extensions(path)

            # Apply those extensions and measure their performance.
            self.apply_new_moves(path, new_moves)