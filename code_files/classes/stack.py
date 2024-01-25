class Stack(object):
    def __init__(self):
        """post : creates an empty LIFO stack """
        self._stack: list = []

    def push (self, x):
        """ post : places x on top of the stack """
        self._stack.append(x)

    def pop (self):
        """ pre : self.size() > 0
        post : removes and returns the top element of
        the stack """
        assert self.size() > 0
        return self._stack.pop()

    def top (self):
        """ pre : self.size() > 0
        post : returns the t op element of the stack without
        removing it """
        assert self.size() > 0
        return self._stack[-1]

    def size (self):
        """ post : returns the number of elements in the stack """
        return len(self._stack)