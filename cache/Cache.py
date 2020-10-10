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

        found, block = self.getCacheBlock(tag)

        if found and block.state != BlockStates.INVALID:
            print("Block is valid -> Data: ", block.data)
            # Marks the block read as recently used.
            block.LRU = 0
            # Marks the other as least recently used.
            self.sets[int(index)].blocks[not block.blockNumber].LRU = 1
            return True
        else:
            return False

    def setBlockData(self, addr, writeVal, fromMem):
        '''
        Updates data of block, although it assumes the block is valid and updated.
        :param addr: address of block.
        :param writeVal: new value.
        :return:
        '''
        index = self.controller.mapAddress(addr)

        for block in self.sets[index].blocks:
            if block.currentTag == addr:
                # updates block data
                block.data = writeVal
                # Change the LRU value of the blocks
                block.LRU = 0
                self.sets[index].blocks[not block.blockNumber].LRU = 1

                if block.state.value == BlockStates.SHARED:
                    block.state = BlockStates.MODIFIED
                    return True
                else:
                    return False

    def updateBlock(self, trans, transResp, bus):
        '''
        Updates all the information of a block.
        :param transResp: transaction response.
        '''
        # Check if block addr is already in cache
        inCache, blockCache = self.getCacheBlock(transResp.addr)

        if not inCache:
            # Map new block to cache
            setIndex = self.controller.mapAddress(transResp.addr)
            blockCache = self.sets[setIndex].getReplacementBlock()
            # Set the other block as the least recently used.
            self.sets[setIndex].blocks[not blockCache.blockNumber].LRU = 1

            # if the block being replaced contains valid data, update the block to memory
            if blockCache.state != BlockStates.INVALID:
                # TODO: CHECK IF THIS IS BEING DONE
                print("Writing back to memory")
                bus.writeToMemory(transResp.addr, transResp.data)

        # Update block's data
        blockCache.data = transResp.data
        blockCache.currentTag = transResp.addr
        blockCache.LRU = 0

        blockCache.changeStateByTransaction(trans.transType, transResp.fromMem)

        # Checks if the response came from main memory
        if transResp.fromMem:
            blockCache.state = BlockStates.EXCLUSIVE
        # Response came from other cache, so it is modified and other caches must be invalidated.
        else:
            # TODO: create a transaction for invalidation to other caches.
            blockCache.state = BlockStates.MODIFIED

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
                print("Writing to exclusive block at " + addr)
                # if block is exclusive no need to invalidate the other caches, just write the value
                block.data = hex(int(writeVal, 16))
                return False, TransactionType.NO_TRANS
            elif block.state.value == BlockStates.SHARED:
                print("Invalidate other caches at " + addr)
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

    def __str__(self):
        strCache = ""
        for set in self.sets:
            for block in set.blocks:
                strCache += str(block) + "\n"

        return strCache
