import math


class CacheController:

    def __init__(self, dataSize, blockQty, addrLen, assoc):
        '''
        Constructor.
        :param dataSize: size of cache block size in Bytes.
        :param blockQty: quantity of blocks in the L1 Cache.
        :param addrLen: size of memory address in bits.
        :param assoc: cache associativity.
        '''

        self.offsetLen = int(math.log2(dataSize))
        self.setsQty = int((2 * blockQty) / (assoc * dataSize))
        self.indexLen = int(math.log2(self.setsQty))
        self.tagLen = int(addrLen - self.offsetLen - self.indexLen)

    def mapAddress(self, addr):
        setIndex = int(addr) % 2

        # TODO: Bug here for short memory addresses
        return setIndex

    def processAddress(self, memAddr):
        '''
        Decompose the main memory address into tag, set  index and offset
        :param memAddr: main memory address
        :return: tuple with tag, index and offset
        '''
        tag = memAddr
        index = memAddr[self.tagLen:self.tagLen + self.indexLen]
        offset = memAddr[self.tagLen + self.indexLen: self.tagLen + self.indexLen + self.offsetLen]
        return tag, index, offset
