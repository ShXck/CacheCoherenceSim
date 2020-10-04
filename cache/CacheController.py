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

    def GetParams(self):
        '''
        Obtains cache parameters
        :return: tuple with offset length, number of sets, index length and tag length.
        '''
        return self.offsetLen, self.setsQty, self.indexLen, self.tagLen

    def ProcessAddress(self, memAddr):
        '''
        Decompose the main memory address into tag, set  index and offset
        :param memAddr: main memory address
        :return: tuple with tag, index and offset
        '''
        tag = memAddr[0:self.tagLen]
        index = memAddr[self.tagLen:self.tagLen + self.indexLen]
        offset = memAddr[self.tagLen + self.indexLen: self.tagLen + self.indexLen + self.offsetLen]
        return tag, index, offset
