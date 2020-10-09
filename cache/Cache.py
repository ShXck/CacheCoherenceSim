from cache.CacheController import CacheController
from cache.CacheSet import CacheSet
from cache.Enums import BlockStates, TransactionType


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

        ret, block = self.getCacheBlock(tag)

        if ret and block.state != BlockStates.INVALID:
            print("Block is valid -> Data: ", block.data)
            return True
        else:
            return False

    def updateBlock(self, transResp):
        '''
        Updates all the information of a block.
        :param transResp: transaction response.
        '''
        # Check if block addr is already in cache but it is invalid
        isInCache, blockCache = self.getCacheBlock(transResp.addr)

        if not isInCache:
            # Map new block to cache
            setIndex = self.controller.mapAddress(transResp.addr)
            blockCache = self.sets[setIndex].getReplacementBlock()
            # TODO: Write to memory here if block being replaced is not invalid

        blockCache.data = transResp.data
        blockCache.currentTag = transResp.addr
        blockCache.LRU = 0

        # Checks if the response came from main memory
        if transResp.fromMem:
            blockCache.state = BlockStates.EXCLUSIVE
        # Response came from other cache
        else:
            blockCache.state = BlockStates.SHARED


    def writeValue(self, memAddr, writeVal):
        '''
        Tries to write the value in cache.
        :param memAddr: address of main memory.
        :param writeVal: new value for the block.
        :return: tuple of the form (needTransaction, typeOfTransaction)
        '''
        addr, index, offset = self.controller.processAddress(memAddr)

        found, block = self.getCacheBlock(addr)

        if found:
            # Block containing the address was found in cache.
            if block.state.value == BlockStates.EXCLUSIVE.value:
                # if block is exclusive no need to invalidate the other caches, just write the value
                block.data = hex(int(writeVal, 16))
                return False, TransactionType.NO_TRANS
            elif block.state.value == BlockStates.SHARED:
                # Generate transaction to invalidate other caches
                block.data = hex(int(writeVal, 16))
                block.state = BlockStates.MODIFIED
                return True, TransactionType.INVALIDATE
        else:
            # Block is not in this cache, write miss is produced
            return True, TransactionType.WRITE_MISS




    def getCacheBlock(self, tag):
        '''
        Checks if a memory Address has already been mapped to cache.
        :param tag: tag of address
        :return: wether or not is in cache and the block data in case the block was found.
        '''

        for set in self.sets:
            for block in set.blocks:
                if block.currentTag == tag and block.state != BlockStates.INVALID:
                    return True, block

        return False, None
