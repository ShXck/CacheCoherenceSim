from gui import GUI
from mainmem.MainMemory import MainMemory
from processor.Processor import Processor
from bus.Bus import Bus
import threading


mainMem = MainMemory(16)
bus = Bus([], mainMem)
proc1 = Processor(1, mainMem.getAvailableAddresses())
proc2 = Processor(2, mainMem.getAvailableAddresses())
proc3 = Processor(3, mainMem.getAvailableAddresses())

t1 = threading.Thread(target=proc1.startProcessor, args=(bus,))
t2 = threading.Thread(target=proc2.startProcessor, args=(bus,))
t3 = threading.Thread(target=proc3.startProcessor, args=(bus,))

t1.start()
t2.start()
t3.start()

#gui = GUI.GUI()

#gui.startGUI(mainMem.memBlocks)