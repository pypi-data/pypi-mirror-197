from copy import copy


class CacheQueue:
    def __init__(self) -> None:
        self.cache = {}
        self.queue = None


    def _next(self):
        while True:
            index = next(self.queue)
            if index in self.cache:
                return index
    

    def _pop(self):
        if self.queue is None:
            self.queue = iter(copy(self.cache))
        try:
            return self.cache[self._next()]
        except StopIteration:
            self.queue = iter(copy(self.cache))
            return None
    

    def _pop_index(self):
        if self.queue is None:
            self.queue = iter(copy(self.cache))
        try:
            return self._next()
        except StopIteration:
            self.queue = iter(copy(self.cache))
            return None
    
    
    def delete(self, index)->bool:
        if index in self.cache:
            del self.cache[index]
            return True
        else:
            return False
    