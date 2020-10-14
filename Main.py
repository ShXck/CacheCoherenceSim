from gui import GUI
from mainmem.MainMemory import MainMemory
from processor.Processor import Processor
from bus.Bus import Bus
import threading


mainMem = MainMemory(16)

gui = GUI.GUI()

#mainMem.print()
lock = threading.Lock()
proc1 = Processor(1, mainMem.getAvailableAddresses(), lock, gui)
proc2 = Processor(2, mainMem.getAvailableAddresses(), lock, gui)
proc3 = Processor(3, mainMem.getAvailableAddresses(), lock, gui)
proc4 = Processor(4, mainMem.getAvailableAddresses(), lock, gui)

bus = Bus([proc1, proc2], mainMem)

t1 = threading.Thread(target=proc1.startProcessor, args=(bus,))
t2 = threading.Thread(target=proc2.startProcessor, args=(bus,))
t3 = threading.Thread(target=proc3.startProcessor, args=(bus,))
t4 = threading.Thread(target=proc4.startProcessor, args=(bus,))
t1.start()
t2.start()
#t3.start()
#t4.start()

gui.setMemInitialValues(mainMem.memBlocks)
gui.startGUI()