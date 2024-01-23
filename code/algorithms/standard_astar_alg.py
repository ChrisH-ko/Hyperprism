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