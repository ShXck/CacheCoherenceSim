from gui import GUI
from mainmem.MainMemory import MainMemory

mainMem = MainMemory(16)

gui = GUI.GUI()

gui.startGUI(mainMem.memBlocks)