from .functions.manhattan_distance import manhattan

def standard_astar(model, queue):
    archive = set()

    while len(queue) > 0:
        
        while queue[0].current_node in archive:
            queue.pop(0)
        
        path = queue.pop(0)
        archive.add(path.current_node())

        moves = model.valid_moves(path)
        new_moves = [x for x in moves if x not in archive]
        archive.update(new_moves)

        for x in new_moves:
            child = path.copy_path()
            child.move(x)
            child.heuristic = model.path_cost(child) + manhattan(child)

            if len(queue) == 0:
                queue.append(child)
            else:
                for i in range(len(queue)):
                    if child.heuristic <= queue[i].heuristic:
                        queue.insert(i, child)
                        break
                queue.append(child)
        
        if len(queue) > 0:
            if queue[0].complete():
                id = queue[0].connection.id
                model.add_path(id, queue[0])
                queue = [path for path in queue if id != path.connection.id]

class Standard_pathwise_astar():
    def __init__(self, model, path):
        self.model = model
        self.queue = [path]
        self.archive = set(path.current_node())
        self.solution = None

    def remove_visited_nodes(self):
        while self.queue[0].current_node in self.archive:
            self.queue.pop(0)
        
    def get_path_extensions(self, path):
        moves = self.model.valid_moves(path)
        new_moves = [a for a in moves if a not in self.archive]
        self.archive.update(new_moves)
        return new_moves
    
    def apply_new_moves(self, path, moves):
        for a in moves:
            child = path.copy_path()
            child.move(a)
            child.heuristic = self.model.path_cost(child) + manhattan(child)

            self.update_queue(child)
    
    def update_queue(self, path):
        for i in range(len(self.queue)):
            if path.heuristic <= self.queue[i].heuristic:
                self.queue.insert(i, path)
                break
        if path not in self.queue:
            self.queue.append(path)

    def check_solution(self):
        if len(self.queue) > 0:
            if self.queue[0].complete():
                id = self.queue[0].connection.id
                self.solution = self.queue[0]
                self.queue = [path for path in self.queue if id != path.connection.id]

    def run(self):
        while len(self.queue) > 0:
            self.remove_visited_nodes()

            path = self.queue.pop(0)
            new_moves = self.get_path_extensions(path)

            self.apply_new_moves(path, new_moves)

            self.check_solution()