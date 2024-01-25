class Node():
    def __init__(self, item, value):
        self.item = item
        self.value = value
    
    def __repr__(self):
        return repr(self.item)

class Priority_Queue():
    def __init__(self):
        self.queue = []
    
    def add(self, item, value):
        queue_item = Node(item, value)

        for i in range(len(self.queue)):
            if value <= self.queue[i].value:
                self.queue.insert(i, queue_item)
                return
        self.queue.append(queue_item)
    
    def get(self):
        return self.queue.pop(0).item
    
    def get_all(self):
        return [elem.item for elem in self.queue]
    
    def not_empty(self):
        if len(self.queue) == 0:
            return False
        return True
