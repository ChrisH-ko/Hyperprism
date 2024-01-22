class Gate():
    def __init__(self, id, position):
        self.id = id
        self.position = position
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return str(self.id)
