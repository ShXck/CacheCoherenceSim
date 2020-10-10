from bus.TransactionResponse import TransactionResponse
from cache.Enums import TransactionState, TransactionType


class Bus:

    def __init__(self, processors, memory):
        self.listeningProcessors = processors
        self.mainMem = memory
        self.transactions = []

    def addTransaction(self, transaction):
        '''
        Sets the current transaction of the bus.
        :param transaction: transaction to be processed.
        '''
        self.transactions.append((transaction, TransactionResponse(transaction.addr)))

    def updateTransaction(self, transaction, procId):
        trans, resp = transaction
        if procId not in trans.accessed:
            trans.accessed.append(procId)
        accesses = len(self.listeningProcessors) - 1

        if trans.transType.value == TransactionType.READ_MISS.value or trans.transType.value == TransactionType.WRITE_MISS.value:
            if len(trans.accessed) == accesses and resp.state.value == TransactionState.UNRESOLVED.value:
                #print("Gotta go to memory boy")
                # if no cache found the data, go for memory
                memData = self.mainMem.getMemData(trans.addr)
                #print("Memory data: " + str(memData) + " at " + trans.addr)
                resp.state = TransactionState.RESOLVED
                resp.data = memData
                resp.fromMem = True

        elif trans.transType.value == TransactionType.INVALIDATE.value:
            if trans.accessCount == accesses and resp.state.value == TransactionState.UNRESOLVED.value:
                # all caches have invalidated their blocks if it was needed
                resp.state = TransactionState.RESOLVED
                resp.read = True


    def updateTransactions(self):
        '''
        Removes transactions that are resolved and have been access by the processor that produced the transaction.
        '''
        self.transactions = [(trans, resp) for trans, resp in self.transactions if resp.state.value == TransactionState.UNRESOLVED.value and not resp.read]

    def writeToMemory(self, addr, value):
        '''
        Writes a new value to a block in memory.
        :param addr: address of block.
        :param value: new value.
        '''
        self.mainMem.updateMemoryBlock(addr, value)






