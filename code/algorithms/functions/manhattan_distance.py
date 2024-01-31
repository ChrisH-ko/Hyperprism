def manhattan(path):
    """
    Calculates the manhattan distance from the end of a path to its goal
    """
    a = path.segments[-1]
    b = path.connection.end.position

    m_distance = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
    return m_distance