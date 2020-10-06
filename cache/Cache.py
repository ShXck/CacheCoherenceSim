from cache.CacheController import CacheController
from cache.CacheSet import CacheSet
from cache.Enums import BlockStates


class L1Cache:

    def __init__(self, blockQty, addrLen, dataSize, assoc):
        self.controller = CacheController(dataSize, blockQty, addrLen, assoc)

        self.sets = []

        for _ in range(self.controller.setsQty):
            self.sets.append(CacheSet(int(blockQty / self.controller.setsQty)))

    def readValue(self, memAddr):
        '''
        Tries to read value from cache.
        :param memAddr: Address of main memory.
        :return: whether or not the value was read.
        '''
        tag, index, offset = self.controller.processAddress(memAddr)

        if self.isInCache(tag):
            blockData = self.sets[index].getBlockValue(tag)
            print("Block is valid -> Data: ", blockData)
            return True
        else:
            return False

    def writeValue(self, memAddr, writeVal):
        procAddr = self.controller.processAddress(memAddr)

    def isInCache(self, tag):
        '''
        Checks if a memory Address has already been mapped to cache.
        :param tag: tag of address
        :return: wether or not is in cache.
        '''

        for set in self.sets:
            for block in set.blocks:
                if block.currentTag == tag and block.state != BlockStates.INVALID:
                    return True

        return False
