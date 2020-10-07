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

    def getMemData(self, addr):
        '''
        Retrieves a value from main memory.
        :param addr: block address
        :return: memory data.
        '''
        for block in self.memBlocks:
            if block.addr == addr:
                return block.data

        raise Exception("Memory Address does not match with any block.")

    def print(self):
        for i in self.memBlocks:
            print(i.addr + " - " + str(i.data))
