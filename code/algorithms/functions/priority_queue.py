class Node():
    """
    Class used to store objects and their priority value.
    """
    def __init__(self, item, value):
        self.item = item
        self.value = value
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return repr(self.item)


class Priority_Queue():
    """
    Priority queue class used in some of the algorithms.
    Acts as a list that sorts its contents based on a given priority value.
    """
    def __init__(self):
        self.queue = []
    
    def add(self, item, value):
        """
        Add the given item in the queue according to the given value.
        """
        queue_item = Node(item, value)

        # Try to insert the item before an item with an equal or higher value.
        for i in range(len(self.queue)):
            if value <= self.queue[i].value:
                self.queue.insert(i, queue_item)
                return
        # Append it to the end if no other item in the queue has a higher value.
        self.queue.append(queue_item)
    
    def get(self):
        """
        Remove and return the item with the highest priority.
        """
        return self.queue.pop(0).item
    
    def get_all(self):
        """
        Return all items sorted on their priority.
        """
        return [elem.item for elem in self.queue]
    
    def not_empty(self):
        """
        Check if the queue is empty.
        """
        if len(self.queue) == 0:
            return False
        return True
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return str([(elem.item, elem.value) for elem in self.queue])