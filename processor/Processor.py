from threading import Lock

from bus.Transaction import BusTransaction
from cache.Cache import L1Cache
from processor.InstructionGenerator import InstructionGenerator
from cache.Enums import Instructions, BlockStates, TransactionState, TransactionType
import time


class Processor:

    def __init__(self, id, mainAddresses, lock):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)
        self.lock = lock
        self.waiting = False

    def startProcessor(self, bus):
        while True:
            # check bus here
            self.snoop(bus)
            if not self.waiting:
                currentInstr = self.instrGen.generateInstruction(self.id)
                print("\nP" + str(self.id) + " issued instruction: " + currentInstr)
                self.handleInstruction(currentInstr, bus)
            else:
                print("\nP" + str(self.id) + " is waiting")

            time.sleep(2)

    def handleInstruction(self, instr, bus):
        '''
        Reads an instruction and do the operations needed to execute it.
        :param instr: Instruction issued by the processor.
        :param bus: Shared bus among processors.
        '''
        splitInstr = instr.split(" ")
        if splitInstr[1] == Instructions.READ.value:
            if not self.l1Cache.readValue(splitInstr[2]):
                # Read miss is detected, so halt the instruction generation until miss is resolved.
                self.waiting = True
                self.lock.acquire()
                # Creates the new transaction to send into the bus
                busTrans = BusTransaction(self.id, splitInstr[2], TransactionType.READ_MISS)
                # Sends transaction to the bus
                bus.addTransaction(busTrans)
                self.lock.release()

        elif splitInstr[1] == Instructions.WRITE.value:
            needTrans, transType = self.l1Cache.writeValue(splitInstr[2], splitInstr[3])
            if needTrans:
                busTrans = BusTransaction(self.id, splitInstr[2], transType, writeVal=hex(int(splitInstr[3], 16)))
                self.lock.acquire()
                bus.addTransaction(busTrans)
                self.lock.release()
                self.waiting = True

    def snoop(self, bus):
        '''
        Snoops on the bus to see if there are transactions that affects the processor.
        :param bus: common bus among processors and main memory.
        '''
        for trans, resp in bus.transactions:
            #print("\nP" + str(self.id) + " read: " + str(trans) + " and " + str(resp))
            # checks if it is a read miss that this processor issued
            if trans.transType.value == TransactionType.READ_MISS.value:
                # Process transaction result
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    # Update block that caused a READ MISS
                    self.l1Cache.updateBlock(trans, resp, bus)
                    resp.read = True
                    print("\nReading value from transaction " + str(trans) + " [P" + str(self.id) + "]")
                    print(self.l1Cache)
                    # Transaction is complete
                    self.lock.acquire()
                    bus.updateTransactions()
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID:
                        print("\nFound value on my cache [P" + str(self.id) + "] on the RM")
                        resp.data = block.data
                        resp.state = TransactionState.RESOLVED
                        resp.fromMem = False
                        block.state = BlockStates.SHARED
                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    self.lock.release()

            # Case of invalidation due to a modification in another cache
            elif trans.transType.value == TransactionType.INVALIDATE.value:
                if trans.sender != self.id:
                    print("\nInvalidating my block [P" + str(self.id) + "]")
                    found, block = self.l1Cache.getCacheBlock(trans.addr)

                    if found:
                        # invalidates the block
                        block.state = BlockStates.INVALID

                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    bus.updateTransactions()
                    self.lock.release()

            # Case of write miss
            elif trans.transType.value == TransactionType.WRITE_MISS.value:
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    self.l1Cache.updateBlock(trans, resp, bus)
                    resp.read = True
                    needTrans = self.l1Cache.setBlockData(trans.addr, trans.writeValue, resp.fromMem)
                    print("\nReading value from transaction " + str(trans) + " [P" + str(self.id) + "]")
                    print(self.l1Cache)
                    # Transaction is complete
                    self.lock.acquire()
                    bus.updateTransactions()
                    # Now that the cache has updated the value of the block, invalidate other caches if needed
                    if needTrans:
                        busTrans = BusTransaction(self.id, trans.addr, TransactionType.INVALIDATE)
                        bus.addTransaction(busTrans)
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID:
                        print("\nFound value on my cache [P" + str(self.id) + "] on the WM for " + str(trans))
                        resp.data = block.data
                        resp.state = TransactionState.RESOLVED
                        resp.fromMem = False
                        block.state = BlockStates.SHARED

                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    self.lock.release()
