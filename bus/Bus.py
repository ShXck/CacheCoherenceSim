from bus.TransactionResponse import TransactionResponse
from cache.Enums import TransactionState, TransactionType, BlockStates


class Bus:

    def __init__(self, processors, memory):
        self.listeningProcessors = processors
        self.mainMem = memory
        self.transactions = []

        self.workingTransaction = None

    def updateWorkingTransaction(self):
        # Checks if there is no transaction on the bus
        if len(self.transactions) > 0 and self.workingTransaction is None:
            self.workingTransaction = self.transactions.pop(0)

        # There is a transaction on the bus
        elif self.workingTransaction is not None:
            trans, resp = self.workingTransaction
            # checks if transaction has been resolved by any prodessor or memory
            if resp.state.value == TransactionState.RESOLVED.value and resp.read and len(self.transactions) > 0:
                # Updates the working transaction
                self.workingTransaction = self.transactions.pop(0)
            elif resp.state.value == TransactionState.RESOLVED.value and resp.read and len(self.transactions) == 0:
                # since there was no other transactions, value goes back to None
                self.workingTransaction = None

    def addTransaction(self, transaction):
        '''
        Sets the current transaction of the bus.
        :param transaction: transaction to be processed.
        '''
        self.transactions.append((transaction, TransactionResponse(transaction.addr)))


    def invalidateBlock(self, addr, transOwner, gui):
        for processor in self.listeningProcessors:
            if processor.id != transOwner:
                for set in processor.l1Cache.sets:
                    for block in set.blocks:
                        if block.currentTag == addr:
                            block.state = BlockStates.INVALID
                            gui.updateBlockState(processor.id, block.guiNum, "I")



    def updateTransaction(self, procId):

        # Increment the accesses for the transaction
        if procId not in self.workingTransaction[0].accessed:
            self.workingTransaction[0].accessed.append(procId)

        maxAccesses = len(self.listeningProcessors) - 1

        trans, resp = self.workingTransaction

        if trans.transType.value == TransactionType.READ_MISS.value or trans.transType.value == TransactionType.WRITE_MISS.value:
            if len(trans.accessed) == maxAccesses and resp.state.value == TransactionState.UNRESOLVED.value:
                # if no cache found the data, go for memory
                memData = self.mainMem.getMemData(trans.addr)
                self.workingTransaction[1].state = TransactionState.RESOLVED
                self.workingTransaction[1].data = memData
                self.workingTransaction[1].fromMemory = True

        elif trans.transType.value == TransactionType.INVALIDATE.value:
            if len(trans.accessed) == maxAccesses and resp.state.value == TransactionState.UNRESOLVED.value:
                # all caches have invalidated their blocks if it was needed
                self.workingTransaction[1].state = TransactionState.RESOLVED
                #self.workingTransaction[1].read = True


    def writeToMemory(self, addr, value):
        '''
        Writes a new value to a block in memory.
        :param addr: address of block.
        :param value: new value.
        '''
        self.mainMem.updateMemoryBlock(addr, value)


    def printTrans(self):
        s = ""
        for trans, resp in self.transactions:
            s += str(trans)
            s += " /// \n"

        print(s)







