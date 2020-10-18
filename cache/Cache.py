from bus.Transaction import BusTransaction
from cache.CacheController import CacheController
from cache.CacheSet import CacheSet
from cache.Enums import BlockState, TransactionType


class L1Cache:

    def __init__(self, blockQty, addrLen, dataSize, assoc):
        self.controller = CacheController(dataSize, blockQty, addrLen, assoc)

        self.sets = []

        guiNum = 0

        for _ in range(self.controller.setsQty):
            self.sets.append(CacheSet(int(blockQty / self.controller.setsQty)))

        for set in self.sets:
            for block in set.blocks:
                block.setGUInumber(guiNum)
                guiNum += 1

    def readValue(self, memAddr):
        '''
        Tries to read value from cache.
        :param memAddr: Address of main memory.
        :return: whether or not the value was read.
        '''
        tag, index, offset = self.controller.processAddress(memAddr)

        found, block = self.getCacheBlock(tag)

        if found and block.state.value != BlockState.INVALID.value:
            print("Block is valid -> Data: ", block.data)
            # Marks the block read as recently used.
            block.LRU = 0
            # Marks the other as least recently used.
            self.sets[int(index)].blocks[not block.blockNumber].LRU = 1
            return True
        else:
            return False

    def updateBlock(self, trans, transResp, bus, gui):
        '''
        Updates all the information of a block.
        :param transResp: transaction response.
        '''
        # Check if block addr is already in cache
        inCache, blockCache = self.getCacheBlock(transResp.addr)
        # gets index of block
        setIndex = self.controller.mapAddress(transResp.addr)

        if not inCache:
            blockCache = self.sets[setIndex].getReplacementBlock()

            # if the block being replaced contains valid data, update the block to memory
            if blockCache.state.value == BlockState.MODIFIED.value or blockCache.state.value == BlockState.OWNED.value:
                print("Writing back to memory")
                bus.writeToMemory(blockCache.currentTag, blockCache.data)
                gui.updateMemoryBlock(int(blockCache.currentTag, 2), blockCache.data)

        # Update block's data
        blockCache.data = transResp.data
        blockCache.currentTag = transResp.addr
        blockCache.LRU = 0
        # Set the other block as the least recently used.
        self.sets[setIndex].blocks[not blockCache.blockNumber].LRU = 1

        gui.updateBlockAddr(trans.sender, blockCache.guiNum, blockCache.currentTag)
        gui.updateBlockValue(trans.sender, blockCache.guiNum, blockCache.data)

        if trans.transType.value == TransactionType.READ_MISS.value:
            if transResp.fromMemory:
                # Response came from memory, so it's exclusive
                gui.updateBlockState(trans.sender, blockCache.guiNum, "E")
                blockCache.state = BlockState.EXCLUSIVE
            else:
                # otherwise, came from another cache
                gui.updateBlockState(trans.sender, blockCache.guiNum, "S")
                blockCache.state = BlockState.SHARED

        elif trans.transType.value == TransactionType.WRITE_MISS.value:
            blockCache.data = trans.writeValue
            blockCache.state = BlockState.MODIFIED
            gui.updateBlockValue(trans.sender, blockCache.guiNum, blockCache.data)
            gui.updateBlockState(trans.sender, blockCache.guiNum, "M")

    def writeValue(self, memAddr, writeVal, gui, procId, bus):
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
            if block.state.value == BlockState.EXCLUSIVE.value or block.state.value == BlockState.MODIFIED.value:
                # if block is exclusive no need to invalidate the other caches, just write the value
                gui.updateBlockValue(procId, block.guiNum, writeVal)
                block.data = hex(int(writeVal, 16))
                block.state = BlockState.MODIFIED
                gui.updateBlockState(procId, block.guiNum, "M")
                # The block is now dirty.
                block.dirty = True
                return False, TransactionType.NO_TRANS

            # Checks if the block is shared. If so, invalidate other caches.
            elif block.state.value == BlockState.SHARED.value or block.state.value == BlockState.OWNED.value:
                print("Invalidate other caches at " + addr)
                gui.updateBlockValue(procId, block.guiNum, writeVal)
                # Generate transaction to invalidate other caches
                block.data = hex(int(writeVal, 16))
                gui.updateBlockState(procId, block.guiNum, "M")
                block.state = BlockState.MODIFIED
                #TODO: Change was made here
                return True, TransactionType.INVALIDATE

            elif block.state.value == BlockState.INVALID.value:
                # block was found but it has and invalid data.
                return True, TransactionType.WRITE_MISS
        else:
            # Block is not in this cache, write miss is produced
            return True, TransactionType.WRITE_MISS

    def changeLRUstate(self, block):
        setIndex = self.controller.mapAddress(block.currentTag)
        block.LRU = 0
        self.sets[setIndex].blocks[not block.blockNumber].LRU = 1


    def getCacheBlock(self, tag):
        '''
        Checks if a memory Address has already been mapped to cache.
        :param tag: tag of address
        :return: wether or not is in cache and the block data in case the block was found.
        '''

        for set in self.sets:
            for block in set.blocks:
                if block.currentTag == tag:
                    return True, block

        return False, None

    def __str__(self):
        strCache = ""
        for set in self.sets:
            for block in set.blocks:
                strCache += str(block) + "\n"

        return strCache
