from cache.Enums import BlockStates, TransactionType, Instructions


class CacheBlock:

    def __init__(self, number):
        self.currentTag = None
        self.data = hex(0)
        self.LRU = 1
        self.blockNumber = number
        self.state = BlockStates.INVALID

    def changeStateByTransaction(self, transType, fromMem):

        if transType.value == TransactionType.READ_MISS.value and self.state.value == BlockStates.INVALID:
            if fromMem:
                self.state = BlockStates.EXCLUSIVE
            else:
                self.state = BlockStates.SHARED

        elif transType.value == TransactionType.WRITE_MISS.value and self.state.value == BlockStates.INVALID:
            self.state = BlockStates.MODIFIED



    def changeStateByInstruction(self, instr):
        if instr.value == Instructions.WRITE:
            if self.state.value == BlockStates.OWNED:
                self.state = BlockStates.MODIFIED



    def __str__(self):
        return str(self.blockNumber) + "|" + str(self.currentTag) + "|" + str(self.data)  + "|" + str(self.state)
