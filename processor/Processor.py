from bus.Transaction import BusTransaction
from cache.Cache import L1Cache
from processor.InstructionGenerator import InstructionGenerator
from cache.Enums import Instructions, BlockStates, TransactionState, TransactionType
import time


class Processor:

    def __init__(self, id, mainAddresses, lock, gui):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)
        self.lock = lock
        self.waiting = False

        self.lastInstr = None
        self.currentInstr = None

        self.gui = gui

        self.strId = "P" + str(id)

    def startProcessor(self, bus):
        while True:

            if self.gui.running and self.gui.start:
                # snoop
                self.snoop(bus)

                if not self.waiting:
                    if self.gui.instructionText.split(" ")[0] == self.strId:
                        currentInstr = self.gui.instructionText
                        print(str(self.id) + " read instr from input: " + currentInstr)
                        self.gui.instructionText = ""
                    else:
                        currentInstr = self.instrGen.generateInstruction(self.id)
                        print(str(self.id) + " issued instruction: " + currentInstr)

                    self.handleInstruction(currentInstr, bus)
                    self.currentInstr = currentInstr
                    self.gui.updateGenInstr(self.id, currentInstr)


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
            needTrans, transType = self.l1Cache.writeValue(splitInstr[2], splitInstr[3], self.gui, self.id, bus)
            if needTrans:
                # Either a write miss or a invalidation transaction will be generated.
                busTrans = BusTransaction(self.id, splitInstr[2], transType, writeVal=hex(int(splitInstr[3], 16)))
                self.lock.acquire()
                bus.addTransaction(busTrans)
                self.lock.release()
                self.waiting = True

        else:
            self.lastInstr = instr
            self.gui.updateLastInstr(self.id, self.lastInstr)

    def snoop(self, bus):
        '''
        Snoops on the bus to see if there are transactions that affects the processor.
        :param bus: common bus among processors and main memory.
        '''
        # Updates the bus current working transaction
        self.lock.acquire()
        bus.updateWorkingTransaction()
        self.lock.release()

        if bus.workingTransaction is not None:
            trans, resp = bus.workingTransaction
            # checks if it is a read miss that this processor issued
            if trans.transType.value == TransactionType.READ_MISS.value:
                # Process transaction result
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    # Update block that caused a READ MISS
                    self.l1Cache.updateBlock(trans, resp, bus, self.gui)

                    # Transaction is complete, mark it as received and read
                    self.lock.acquire()
                    bus.workingTransaction[1].read = True
                    self.lock.release()

                    # Processor can keep on generating instructions
                    self.waiting = False
                    self.lastInstr = self.currentInstr
                    self.gui.updateLastInstr(self.id, self.lastInstr)

                # READ MISS was not caused on this cache, so search and see if this cache have the value requested
                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    # if the cache has the block and is valid
                    if found and block.state.value != BlockStates.INVALID.value:
                        # mark the block as recently used.
                        self.l1Cache.changeLRUstate(block)

                        self.lock.acquire()
                        # Add data to the read miss request.
                        bus.workingTransaction[1].updateResponse(block.data, False)
                        self.lock.release()

                        # Update state, if it was modified change it to OWNED, if it was owned or shared leave it as it is.
                        if block.state.value == BlockStates.MODIFIED.value:
                            self.gui.updateBlockState(self.id, block.guiNum, "O")
                            block.state = BlockStates.OWNED
                        # if it was exclusive, now it is shared
                        elif block.state.value == BlockStates.EXCLUSIVE.value:
                            self.gui.updateBlockState(self.id, block.guiNum, "S")
                            block.state = BlockStates.SHARED

                    self.lock.acquire()
                    bus.updateTransaction(self.id)
                    self.lock.release()

            # Case of invalidation caused by a modification in another cache
            elif trans.transType.value == TransactionType.INVALIDATE.value:
                if trans.sender != self.id:

                    found, block = self.l1Cache.getCacheBlock(trans.addr)

                    if found:
                        # invalidates the block
                        block.state = BlockStates.INVALID
                        self.gui.updateBlockState(self.id, block.guiNum, "I")
                        self.l1Cache.changeLRUstate(block)

                    self.lock.acquire()
                    bus.updateTransaction(self.id)
                    self.lock.release()
                else:
                    if resp.state.value == TransactionState.RESOLVED.value:
                        # Transaction is complete, mark it as received and read
                        self.lock.acquire()
                        bus.workingTransaction[1].read = True
                        self.lock.release()

                        # Processor can keep on generating instructions
                        self.waiting = False
                        self.lastInstr = self.currentInstr
                        self.gui.updateLastInstr(self.id, self.lastInstr)


            # Case of write miss
            elif trans.transType.value == TransactionType.WRITE_MISS.value:
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    self.l1Cache.updateBlock(trans, resp, bus, self.gui)
                    # Transaction is complete, mark it as received and read
                    self.lock.acquire()
                    bus.workingTransaction[1].read = True
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                    self.lastInstr = self.currentInstr
                    self.gui.updateLastInstr(self.id, self.lastInstr)

                elif trans.sender != self.id and resp.state.value == TransactionState.UNRESOLVED.value:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID.value:

                        self.lock.acquire()
                        # updates transaction result data
                        bus.workingTransaction[1].updateResponse(block.data, False)
                        self.lock.release()

                        # Invalidate the block since other processor is trying to write it.
                        block.state = BlockStates.INVALID
                        bus.invalidateBlock(block.currentTag, trans.sender, self.gui)
                        self.gui.updateBlockState(self.id, block.guiNum, "I")
                        self.l1Cache.changeLRUstate(block)

                    self.lock.acquire()
                    bus.updateTransaction(self.id)
                    self.lock.release()
