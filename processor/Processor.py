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

        self.lastInstr = None
        self.currentInstr = None

    def startProcessor(self, bus):
        while True:
            # snoop
            self.snoop(bus)

            if not self.waiting:
                currentInstr = self.instrGen.generateInstruction(self.id)
                print("\nP" + str(self.id) + " issued instruction: " + currentInstr)
                self.handleInstruction(currentInstr, bus)
                self.currentInstr = currentInstr
            else:
                print("-----------------------------------------------")
                print("\nP" + str(self.id) + " is waiting")
                #bus.printTrans()
                print("-----------------------------------------------")

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
                # Either a write miss or a invalidation transaction will be generated.
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
                    retVal = self.l1Cache.updateBlock(trans, resp, bus)
                    print("-----------------------------------------------")
                    print("\nReading value from transaction " + str(trans) + " [P" + str(self.id) + "]")
                    print(self.l1Cache)
                    print("-----------------------------------------------")
                    # Transaction is complete
                    self.lock.acquire()
                    resp.read = True
                    bus.updateTransactions()
                    if retVal is not None:
                        bus.addTransaction(retVal)
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                    self.lastInstr = self.currentInstr
                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID.value:
                        self.l1Cache.changeLRUstate(block)
                        print("\nFound value on my cache [P" + str(self.id) + "] on the RM for " + str(trans))
                        resp.updateResponse(block.data, False)
                        # Update state, if it was modified change to OWNED, if it was owned or shared leave it as it is.
                        if block.state.value == BlockStates.MODIFIED.value:
                            block.state = BlockStates.OWNED
                        elif block.state.value == BlockStates.EXCLUSIVE.value:
                            block.state = BlockStates.SHARED

                    # TODO: should go in a else(?)
                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    self.lock.release()

            # Case of invalidation due to a modification in another cache
            elif trans.transType.value == TransactionType.INVALIDATE.value:
                if trans.sender != self.id:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)

                    if found:
                        print("-------------------------------------------------------------")
                        print("\nInvalidating my block [P" + str(self.id) + "]" + trans.addr + " cuz " + str(trans))
                        print(self.l1Cache)
                        print("-------------------------------------------------------------")
                        # invalidates the block
                        block.state = BlockStates.INVALID
                        self.l1Cache.changeLRUstate(block)

                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    bus.updateTransactions()
                    self.lock.release()

            # Case of write miss
            elif trans.transType.value == TransactionType.WRITE_MISS.value:
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    retVal = self.l1Cache.updateBlock(trans, resp, bus)
                    print("-----------------------------------------------")
                    print("\nReading value from transaction " + str(trans) + " [P" + str(self.id) + "]")
                    print(self.l1Cache)
                    print("-----------------------------------------------")
                    # Transaction is complete
                    self.lock.acquire()
                    resp.read = True
                    bus.updateTransactions()
                    if retVal is not None:
                        bus.addTransaction(retVal)
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                    self.lastInstr = self.currentInstr
                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID.value:
                        print("\nFound value on my cache [P" + str(self.id) + "] on the WM for " + str(trans))
                        resp.updateResponse(block.data, False)
                        # Invalidate the block since other processor is trying to write it.
                        block.state = BlockStates.INVALID
                        self.l1Cache.changeLRUstate(block)

                    self.lock.acquire()
                    bus.updateTransaction((trans, resp), self.id)
                    self.lock.release()
