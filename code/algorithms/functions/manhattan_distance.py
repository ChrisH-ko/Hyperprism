def manhattan(path):
    
    a = path.segments[-1]
    b = path.connection.end.position

    m_distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return m_distance