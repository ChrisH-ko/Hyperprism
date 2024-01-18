def manhattan(net):
    
    a = net.path[-1]
    b = net.end.position

    m_distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return m_distance