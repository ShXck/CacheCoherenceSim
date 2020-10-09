from cache.Enums import BlockStates


class CacheBlock:

    def __init__(self, number):
        self.currentTag = None
        self.data = hex(0)
        self.LRU = 1
        self.blockNumber = number
        self.state = BlockStates.INVALID

    def __str__(self):
        return str(self.blockNumber) + "|" + str(self.currentTag) + "|" + str(self.data)  + "|" + str(self.state)
