from mainmem import MemBlock as mblock


class MainMemory:

    def __init__(self, blockQty):
        '''
        Constructor
        :param blockQty: number of blocks of main memory.
        '''

        self.memBlocks = []

        for i in range(blockQty):
            self.memBlocks.append(mblock.MemBlock(format(i, 'b')))

    def print(self):
        for i in range(len(self.memBlocks)):
            print(self.memBlocks[i].addr)