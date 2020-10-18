from cache.Enums import BlockState, TransactionType, Instructions


class CacheBlock:

    def __init__(self, number):
        self.currentTag = None
        self.data = hex(0)
        self.LRU = 1
        self.blockNumber = number
        self.state = BlockState.INVALID
        self.guiNum = None

    def setGUInumber(self, guiNumber):
        self.guiNum = guiNumber

    def changeStateByTransaction(self, transType, fromMem):

        if transType.value == TransactionType.READ_MISS.value and self.state.value == BlockState.INVALID:
            if fromMem:
                self.state = BlockState.EXCLUSIVE
            else:
                self.state = BlockState.SHARED

        elif transType.value == TransactionType.WRITE_MISS.value and self.state.value == BlockState.INVALID:
            self.state = BlockState.MODIFIED



    def changeStateByInstruction(self, instr):
        if instr.value == Instructions.WRITE:
            if self.state.value == BlockState.OWNED:
                self.state = BlockState.MODIFIED



    def __str__(self):
        return str(self.blockNumber) + "|" + str(self.currentTag) + "|" + str(self.data)  + "|" + str(self.state)
