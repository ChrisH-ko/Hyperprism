from .standard_astar_alg import standard_astar
from .functions.manhattan_distance import manhattan

def short_first_astar(model):
    chip = model.chip
    paths = model.paths

    connections = model.get_nets()

    queue = []
    for net in connections:
        path = paths[net]
        path.heuristic = manhattan(path)

        for i in range(len(queue)):
            if path.heuristic <= queue[i].heuristic:
                queue.insert(i, path)
                break
        if path not in queue:
            queue.append(path)
    
    for path in queue:
        standard_astar(model, [path])

