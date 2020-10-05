from mainmem.MemBlock import MemBlock


class MainMemory:

    def __init__(self, blockQty):
        '''
        Constructor
        :param blockQty: number of blocks of main memory.
        '''

        self.memBlocks = []

        for i in range(blockQty):
            self.memBlocks.append(MemBlock(format(i, 'b')))

    def getAvailableAddresses(self):
        '''
        Obtains the memory addresses of the blocks
        :return: list of addresses of main memory
        '''
        return [i.addr for i in self.memBlocks]
