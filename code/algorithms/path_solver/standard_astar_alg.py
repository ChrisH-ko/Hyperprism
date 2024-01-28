from code.algorithms.functions.manhattan_distance import manhattan
from code.algorithms.functions.priority_queue import Priority_Queue

class Standard_pathwise_astar():
    def __init__(self, model, path):
        self.model = model
        self.start = path.connection.start.position
        self.goal = path.connection.end.position

        self.queue = Priority_Queue()
        self.queue.add(self.start, manhattan(path))

        self.lowest_cost = dict()
        self.lowest_cost[self.start] = 0
        self.cheapest_path = dict()
        self.cheapest_path[self.start] = path

        self.solution = path

    def get_path_extensions(self, path):
        moves = self.model.valid_moves(path)
        return moves
    
    def apply_new_moves(self, path, moves):
        for a in moves:
            child = path.copy_path()
            child.move(a)

            cost = self.path_cost(child)
            heuristic = self.heuristic(child)

            self.update_queue_and_archive(child, cost, heuristic)
    
    def update_queue_and_archive(self, path, cost, heuristic):
        position = path.current_node()

        if position not in self.lowest_cost or cost < self.lowest_cost[position]:
            self.lowest_cost[position] = cost
            self.cheapest_path[position] = path
            self.queue.add(position, cost+heuristic)
    
    def path_cost(self, path):
        return self.model.path_cost(path)

    def heuristic(self, path):
        return manhattan(path)

    def run(self):
        while self.queue.not_empty():
            position = self.queue.get()

            if position == self.goal:
                self.solution = self.cheapest_path[position]
                break

            path = self.cheapest_path[position]

            new_moves = self.get_path_extensions(path)

            self.apply_new_moves(path, new_moves)