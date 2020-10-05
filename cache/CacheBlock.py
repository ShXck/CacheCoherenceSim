from cache.States import States


class CacheBlock:

    def __init__(self, number):
        self.validBit = 0
        self.currentTag = None
        self.data = hex(0)
        self.LRU = 0
        self.blockNumber = number
        self.state = States.INVALID
        
