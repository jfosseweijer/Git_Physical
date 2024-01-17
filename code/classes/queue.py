class Queue:

    def __init__(self):
        self._data = []

    # add element to back of queue
    def enqueue(self, element) -> None:
        self._data.append(element)

    # remove and return element from front of queue
    def dequeue(self):
        assert self.size() > 0
        return self._data.pop(0)
    
    # return size of the queue
    def size(self):
        return len(self._data)
    
    # peeks at the first position in the queue without removing is
    def peek_front(self):
        return self._data[0]
    
    def peek_back(self):
        return self._data[-1]
    
    # empties the queue
    def empty(self):
        self._data = []