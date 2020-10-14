import sys
import pygame

blue = (0, 0, 255)
white = (255, 255, 255)
red = (255, 0, 0)
lightOrange = (229, 126, 57)
black = (0, 0, 0)


class GUI:

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.gameWindow = pygame.display.set_mode((1280, 680))
        pygame.display.set_caption("Cache Coherence Simulation Software")
        self.clock = pygame.time.Clock()

        # Strings of the values in main memory
        self.memBlocksTexts = []
        # Strings of data in the four blocks of cache
        self.p1CacheValuesText = ["0x0", "0x0", "0x0", "0x0"]
        self.p2CacheValuesText = ["0x0", "0x0", "0x0", "0x0"]
        self.p3CacheValuesText = ["0x0", "0x0", "0x0", "0x0"]
        self.p4CacheValuesText = ["0x0", "0x0", "0x0", "0x0"]

        # Strings of the states of the blocks
        self.p1CacheStatesText = ["I", "I", "I", "I"]
        self.p2CacheStatesText = ["I", "I", "I", "I"]
        self.p3CacheStatesText = ["I", "I", "I", "I"]
        self.p4CacheStatesText = ["I", "I", "I", "I"]

        # Strings of the addresses of the block
        self.p1CacheAddrText = ["0x", "0x", "0x", "0x"]
        self.p2CacheAddrText = ["0x", "0x", "0x", "0x"]
        self.p3CacheAddrText = ["0x", "0x", "0x", "0x"]
        self.p4CacheAddrText = ["0x", "0x", "0x", "0x"]

        self.p1LastInstr = "Test"
        self.p1GenInstr = "Test"
        self.p2LastInstr = "Test"
        self.p2GenInstr = "Test"
        self.p3LastInstr = "Test"
        self.p3GenInstr = "Test"
        self.p4LastInstr = "Test"
        self.p4GenInstr = "Test"

        self.consolas = pygame.font.SysFont('consolas', 20)
        self.customFont = pygame.font.Font('C:\\Users\\DELL\\Desktop\\Proyecto1-Arqui\\gui\\fonts\\BebasNeue.ttf', 32)

    def setMemInitialValues(self, memblocks):
        for i in memblocks:
            self.memBlocksTexts.append(i.data)


    def startGUI(self):

        while True:
            self.gameWindow.fill(black)

            self.drawMainMemBlocks(16)
            self.drawBusComms()
            self.drawStaticText()
            self.drawCacheBlocks(4)
            self.drawMemBlockDataText()
            self.drawLastInstrText()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def drawLastInstrText(self):
        y_gen = 75
        y_last = 110
        # Updates P1 current generated instruction
        self.gameWindow.blit(self.consolas.render(self.p1GenInstr, True, lightOrange), (1037, y_gen))
        # Updates P1 last generated instruction
        self.gameWindow.blit(self.consolas.render(self.p1LastInstr, True, lightOrange), (1037, y_last))

        # Updates P2 current generated instruction
        self.gameWindow.blit(self.consolas.render(self.p2GenInstr, True, lightOrange), (1037, y_gen + 165))
        # Updates P2 last generated instruction
        self.gameWindow.blit(self.consolas.render(self.p2LastInstr, True, lightOrange), (1037, y_last + 165))

        # Updates P3 current generated instruction
        self.gameWindow.blit(self.consolas.render(self.p3GenInstr, True, lightOrange), (1037, y_gen + 2*165))
        # Updates P3 last generated instruction
        self.gameWindow.blit(self.consolas.render(self.p3LastInstr, True, lightOrange), (1037, y_last + 2*165))

        # Updates P4 current generated instruction
        self.gameWindow.blit(self.consolas.render(self.p4GenInstr, True, lightOrange), (1037, y_gen + 3*165))
        # Updates P4 last generated instruction
        self.gameWindow.blit(self.consolas.render(self.p4LastInstr, True, lightOrange), (1037, y_last + 3*165))


    def updateBlockValue(self, procId, blockNumberGUI, newValue):
        if procId == 1:
            self.p1CacheValuesText[blockNumberGUI] = newValue
        elif procId == 2:
            self.p2CacheValuesText[blockNumberGUI] = newValue
        elif procId == 3:
            self.p3CacheValuesText[blockNumberGUI] = newValue
        else:
            self.p4CacheValuesText[blockNumberGUI] = newValue


    def updateBlockState(self, procId, blockNumberGUI, newState):
        if procId == 1:
            self.p1CacheStatesText[blockNumberGUI] = newState
        elif procId == 2:
            self.p2CacheStatesText[blockNumberGUI] = newState
        elif procId == 3:
            self.p3CacheStatesText[blockNumberGUI] = newState
        else:
            self.p4CacheStatesText[blockNumberGUI] = newState

    def updateBlockAddr(self, procId, blockNumberGUI, newAddr):
        if procId == 1:
            self.p1CacheAddrText[blockNumberGUI] = newAddr
        elif procId == 2:
            self.p1CacheAddrText[blockNumberGUI] = newAddr
        elif procId == 3:
            self.p1CacheAddrText[blockNumberGUI] = newAddr
        else:
            self.p1CacheAddrText[blockNumberGUI] = newAddr


    def updateGenInstr(self, procId, instr):
        if procId == 1:
            self.p1GenInstr = instr
        elif procId == 2:
            self.p2GenInstr = instr
        elif procId == 3:
            self.p3GenInstr = instr
        else:
            self.p4GenInstr = instr


    def updateLastInstr(self, procId, instr):
        if procId == 1:
            self.p1LastInstr = instr
        elif procId == 2:
            self.p2LastInstr = instr
        elif procId == 3:
            self.p3LastInstr = instr
        else:
            self.p4LastInstr = instr

    def updateMemoryBlock(self, index, newValue):
        self.memBlocksTexts[index] = newValue

    def drawMemBlockDataText(self):
        x = 140
        y = 87

        for i in self.memBlocksTexts:
            self.gameWindow.blit(self.consolas.render(i, True, black), (x, y))
            y += 35

    def drawMainMemBlocks(self, blockNumber):

        x = 80
        y = 80

        rectWidth = 200
        rectHeight = 30

        for _ in range(blockNumber):
            pygame.draw.rect(self.gameWindow, white, (x, y, rectWidth, rectHeight))
            y += 35

    def drawBusComms(self):
        # Bus
        pygame.draw.rect(self.gameWindow, lightOrange, (400, 50, 40, 600))

        # draw main to bus rect
        pygame.draw.rect(self.gameWindow, lightOrange, (280, 330, 120, 20))

        y_comm = 80

        for _ in range(4):
            pygame.draw.rect(self.gameWindow, lightOrange, (440, y_comm, 150, 20))
            y_comm += 170

    def drawCacheBlocks(self, blockQty):

        x = 590
        y = 30

        blockNumber = 0

        rectWidth = 200
        rectHeight = 30

        for i in range(blockQty):
            for j in range(blockQty):

                # Draws cache blocks rectangles
                pygame.draw.rect(self.gameWindow, white, (x, y, rectWidth, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 205, y, rectWidth - 170, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 240, y, rectWidth - 160, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 285, y, rectWidth - 170, rectHeight))

                # Draws cache for processor 1
                if i == 0:
                    self.gameWindow.blit(self.consolas.render(self.p1CacheValuesText[j], True, black), (x + 80, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p1CacheStatesText[j], True, black), (x + 215, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p1CacheAddrText[j], True, black), (x + 244, y + 7))
                # Draws cache for processor 2
                elif i == 1:
                    self.gameWindow.blit(self.consolas.render(self.p2CacheValuesText[j], True, black), (x + 80, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p2CacheStatesText[j], True, black), (x + 215, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p2CacheAddrText[j], True, black), (x + 244, y + 7))
                # Draws cache for processor 3
                elif i == 2:
                    self.gameWindow.blit(self.consolas.render(self.p3CacheValuesText[j], True, black), (x + 80, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p3CacheStatesText[j], True, black), (x + 215, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p3CacheAddrText[j], True, black), (x + 244, y + 7))
                # Draws cache for processor 4
                else:
                    self.gameWindow.blit(self.consolas.render(self.p4CacheValuesText[j], True, black), (x + 80, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p4CacheStatesText[j], True, black), (x + 215, y + 7))
                    self.gameWindow.blit(self.consolas.render(self.p4CacheAddrText[j], True, black), (x + 244, y + 7))

                self.gameWindow.blit(self.consolas.render(str(blockNumber), True, black), (x + 293, y + 7))


                if blockNumber == 0:
                    blockNumber = 1
                else:
                    blockNumber = 0

                y += 35
            y += 25


    def drawStaticText(self):

        # Main Memory title
        self.gameWindow.blit(self.customFont.render('Main Memory', True, red), (110, 40))

        # Bus Text
        busText = self.customFont.render('Bus', True, white)
        busText = pygame.transform.rotate(busText, 90)
        self.gameWindow.blit(busText, (405, 340))

        y_addr = 87

        # Draws main memory addresses
        for block in range(16):
            self.gameWindow.blit(self.consolas.render(bin(block), True, white), (10, y_addr))
            y_addr += 35


        y_proc = 30
        proccessor = "P"

        for i in range(1, 5):
            # Processor number
            self.gameWindow.blit(self.customFont.render(proccessor + str(i), True, lightOrange), (915, y_proc))

            # Last instruction title
            self.gameWindow.blit(self.customFont.render("Last Instr:", True, white), (915, y_proc + 70))

            # Gen instr title
            self.gameWindow.blit(self.customFont.render("Gen Instr:", True, white), (915, y_proc + 35))

            y_proc += 165
