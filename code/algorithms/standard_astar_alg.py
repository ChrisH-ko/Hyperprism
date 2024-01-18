import copy

def standard_astar(chip, queue, heuristic):
    archive = set()

    while len(queue) > 0:
        
        while queue[0] in archive:
            queue.pop(0)
        
        path = queue.pop(0)
        archive.add(path)

        moves = chip.valid_moves(path)

        for x in moves:
            child = copy.deepcopy(path)
            child.move(x)
            child.heuristic = len(child) + manhattan(child)

            if len(queue) == 0:
                queue.append(child)
            else:
                for i in range(len(queue)):
                    if child.heuristic <= queue[i].heuristic:
                        queue.insert(i, child)
                        break
        
        if queue[0].valid():
            id = queue[0].id

            chip.netlist[id] = queue[0]

            queue = [net for net in queue if id != net.id]


def manhattan(net):
    
    a = net.path[-1]
    b = net.end.position

    m_distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return m_distance