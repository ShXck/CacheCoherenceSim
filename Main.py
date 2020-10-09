from gui import GUI
from mainmem.MainMemory import MainMemory
from processor.Processor import Processor
from bus.Bus import Bus
import threading


mainMem = MainMemory(16)
mainMem.print()
lock = threading.Lock()
proc1 = Processor(1, mainMem.getAvailableAddresses(), lock)
proc2 = Processor(2, mainMem.getAvailableAddresses(), lock)
proc3 = Processor(3, mainMem.getAvailableAddresses(), lock)

bus = Bus([proc1, proc2, proc3], mainMem)

t1 = threading.Thread(target=proc1.startProcessor, args=(bus,))
t2 = threading.Thread(target=proc2.startProcessor, args=(bus,))
t3 = threading.Thread(target=proc3.startProcessor, args=(bus,))
t1.start()
t2.start()
t3.start()

'''
proc2 = Processor(2, mainMem.getAvailableAddresses())

t1 = threading.Thread(target=proc1.startProcessor, args=(bus,))
t2 = threading.Thread(target=proc2.startProcessor, args=(bus,))
t3 = threading.Thread(target=proc3.startProcessor, args=(bus,))

t1.start()
t2.start()
t3.start()
'''

#gui = GUI.GUI()

#gui.startGUI(mainMem.memBlocks)