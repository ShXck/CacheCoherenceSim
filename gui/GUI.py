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
        self.gameWindow = pygame.display.set_mode((1280, 680))
        pygame.display.set_caption("Cache Coherence Simulation Software")
        self.clock = pygame.time.Clock()

        self.memBlocksTexts = []
        self.p1CacheBlocksText = []
        self.p2CacheBlocksText = []
        self.p3CacheBlocksText = []
        self.p4CacheBlocksText = []

        self.p1CacheStatesText = []
        self.p2CacheStatesText = []
        self.p3CacheStatesText = []
        self.p4CacheStatesText = []

        self.p1CacheAddrText = []
        self.p2CacheAddrText = []
        self.p3CacheAddrText = []
        self.p4CacheAddrText = []

        self.p1LastInstr = None
        self.p1GenInstr = None
        self.p2LastInstr = None
        self.p2GenInstr = None
        self.p3LastInstr = None
        self.p3GenInstr = None
        self.p4LastInstr = None
        self.p4GenInstr = None



    def startGUI(self, memBlocks):

        self.drawMainMemBlocks(16)
        self.drawBusComms()
        self.drawStaticText(memBlocks)
        self.drawCacheBlocks(4)
        self.drawMemBlockDataText(memBlocks)
        self.drawInstrText()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def updateBlockValue(self, procId, blockNumberGUI, newValue):

        dataFont = pygame.font.SysFont('consolas', 20)

        if procId == 1:
            self.p1CacheBlocksText[blockNumberGUI] = dataFont.render(str(newValue), True, black)
            self.gameWindow.blit(self.p1CacheBlocksText[blockNumberGUI],
                                 self.p1CacheBlocksText[blockNumberGUI].get_rect())
        elif procId == 2:
            self.p2CacheBlocksText[blockNumberGUI] = dataFont.render(str(newValue), True, black)
            self.gameWindow.blit(self.p2CacheBlocksText[blockNumberGUI],
                                 self.p2CacheBlocksText[blockNumberGUI].get_rect())
        elif procId == 3:
            self.p3CacheBlocksText[blockNumberGUI] = dataFont.render(str(newValue), True, black)
            self.gameWindow.blit(self.p3CacheBlocksText[blockNumberGUI],
                                 self.p3CacheBlocksText[blockNumberGUI].get_rect())
        else:
            self.p4CacheBlocksText[blockNumberGUI] = dataFont.render(str(newValue), True, black)
            self.gameWindow.blit(self.p4CacheBlocksText[blockNumberGUI],
                                 self.p4CacheBlocksText[blockNumberGUI].get_rect())

    def updateBlockState(self, procId, blockNumberGUI, newState):
        dataFont = pygame.font.SysFont('consolas', 20)

        if procId == 1:
            self.p1CacheStatesText[blockNumberGUI] = dataFont.render(newState, True, black)
            self.gameWindow.blit(self.p1CacheStatesText[blockNumberGUI],
                                 self.p1CacheStatesText[blockNumberGUI].get_rect())
        elif procId == 2:
            self.p2CacheStatesText[blockNumberGUI] = dataFont.render(newState, True, black)
            self.gameWindow.blit(self.p2CacheStatesText[blockNumberGUI],
                                 self.p2CacheStatesText[blockNumberGUI].get_rect())
        elif procId == 3:
            self.p3CacheStatesText[blockNumberGUI] = dataFont.render(newState, True, black)
            self.gameWindow.blit(self.p3CacheStatesText[blockNumberGUI],
                                 self.p3CacheStatesText[blockNumberGUI].get_rect())
        else:
            self.p4CacheStatesText[blockNumberGUI] = dataFont.render(newState, True, black)
            self.gameWindow.blit(self.p4CacheStatesText[blockNumberGUI],
                                 self.p4CacheStatesText[blockNumberGUI].get_rect())

    def updateBlockAddr(self, procId, blockNumberGUI, newAddr):
        dataFont = pygame.font.SysFont('consolas', 20)

        if procId == 1:
            self.p1CacheAddrText[blockNumberGUI] = dataFont.render(newAddr, True, black)
            self.gameWindow.blit(self.p1CacheAddrText[blockNumberGUI],
                                 self.p1CacheAddrText[blockNumberGUI].get_rect())
        elif procId == 2:
            self.p2CacheAddrText[blockNumberGUI] = dataFont.render(newAddr, True, black)
            self.gameWindow.blit(self.p2CacheAddrText[blockNumberGUI],
                                 self.p2CacheAddrText[blockNumberGUI].get_rect())
        elif procId == 3:
            self.p3CacheAddrText[blockNumberGUI] = dataFont.render(newAddr, True, black)
            self.gameWindow.blit(self.p3CacheAddrText[blockNumberGUI],
                                 self.p3CacheAddrText[blockNumberGUI].get_rect())
        else:
            self.p4CacheAddrText[blockNumberGUI] = dataFont.render(newAddr, True, black)
            self.gameWindow.blit(self.p4CacheAddrText[blockNumberGUI],
                                 self.p4CacheAddrText[blockNumberGUI].get_rect())


    def updateGenInstr(self, procId, instr):
        instrFont = pygame.font.SysFont('consolas', 20)

        if procId == 1:
            self.p1GenInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p1GenInstr, self.p1GenInstr.get_rect())
        elif procId == 2:
            self.p2GenInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p2GenInstr, self.p2GenInstr.get_rect())
        elif procId == 3:
            self.p3GenInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p3GenInstr, self.p3GenInstr.get_rect())
        else:
            self.p4GenInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p4GenInstr, self.p4GenInstr.get_rect())

    def updateLastInstr(self, procId, instr):
        instrFont = pygame.font.SysFont('consolas', 20)

        if procId == 1:
            self.p1LastInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p1LastInstr, self.p1LastInstr.get_rect())
        elif procId == 2:
            self.p2LastInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p2LastInstr, self.p2LastInstr.get_rect())
        elif procId == 3:
            self.p3LastInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p3LastInstr, self.p3LastInstr.get_rect())
        else:
            self.p4LastInstr = instrFont.render(instr, True, lightOrange)
            self.gameWindow.blit(self.p4LastInstr, self.p4LastInstr.get_rect())


    def drawMemBlockDataText(self, memBlocks):
        dataFont = pygame.font.SysFont('consolas', 20)

        x = 180
        y = 100

        for i in memBlocks:
            memBlockValue = dataFont.render(str(i.data), True, black)
            self.memBlocksTexts.append(memBlockValue)
            memBlockTextRect = memBlockValue.get_rect()
            memBlockTextRect.center = (x, y)
            self.gameWindow.blit(memBlockValue, memBlockTextRect)
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
        dataFont = pygame.font.SysFont('consolas', 20)

        x = 590
        y = 30

        blockNumber = 0
        cacheIndex = 1

        rectWidth = 200
        rectHeight = 30

        for _ in range(blockQty):
            for _ in range(blockQty):

                cacheBlockValue = dataFont.render(hex(0), True, black)
                cacheBlockState = dataFont.render("I", True, black)
                cacheBlockAddr = dataFont.render("0x", True, black)
                cacheBlockNumber = dataFont.render(str(blockNumber), True, black)

                if cacheIndex == 1:
                    self.p1CacheBlocksText.append(cacheBlockValue)
                    self.p1CacheStatesText.append(cacheBlockState)
                    self.p1CacheAddrText.append(cacheBlockAddr)
                elif cacheIndex == 2:
                    self.p2CacheBlocksText.append(cacheBlockValue)
                    self.p2CacheStatesText.append(cacheBlockState)
                    self.p2CacheAddrText.append(cacheBlockAddr)
                elif cacheIndex == 3:
                    self.p3CacheBlocksText.append(cacheBlockValue)
                    self.p3CacheStatesText.append(cacheBlockState)
                    self.p3CacheAddrText.append(cacheBlockAddr)
                else:
                    self.p4CacheBlocksText.append(cacheBlockValue)
                    self.p4CacheStatesText.append(cacheBlockState)
                    self.p4CacheAddrText.append(cacheBlockAddr)

                cacheBlockTextRect = cacheBlockValue.get_rect()
                cacheBlockTextRect.center = (x + 105, y + 16)

                cacheBlockStateRect = cacheBlockState.get_rect()
                cacheBlockStateRect.center = (x + 220, y + 16)

                cacheBlockAddrRect = cacheBlockAddr.get_rect()
                cacheBlockAddrRect.center = (x + 253, y + 16)

                cacheBlockNumberRect = cacheBlockNumber.get_rect()
                cacheBlockNumberRect.center = (x + 300, y + 16)

                pygame.draw.rect(self.gameWindow, white, (x, y, rectWidth, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 205, y, rectWidth - 170, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 240, y, rectWidth - 160, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 285, y, rectWidth - 170, rectHeight))
                self.gameWindow.blit(cacheBlockValue, cacheBlockTextRect)
                self.gameWindow.blit(cacheBlockState, cacheBlockStateRect)
                self.gameWindow.blit(cacheBlockAddr, cacheBlockAddrRect)
                self.gameWindow.blit(cacheBlockNumber, cacheBlockNumberRect)

                if blockNumber == 0:
                    blockNumber = 1
                else:
                    blockNumber = 0

                y += 35
            y += 25
            cacheIndex += 1

    def drawInstrText(self):

        instrFont = pygame.font.SysFont('consolas', 20)

        x = 1037
        y = 80

        for i in range(4):
            genInstr = instrFont.render('No instruction', True, lightOrange)
            lastInstr = instrFont.render('No instruction', True, lightOrange)

            if i == 0:
                self.p1GenInstr = genInstr
                self.p1LastInstr = lastInstr
            elif i == 1:
                self.p2GenInstr = genInstr
                self.p2LastInstr = lastInstr
            elif i == 2:
                self.p3GenInstr = genInstr
                self.p3LastInstr = lastInstr
            else:
                self.p4GenInstr = genInstr
                self.p4LastInstr = lastInstr

            genInstrRect = genInstr.get_rect()
            genInstrRect.midleft = (x, y)

            lastInstrRect = lastInstr.get_rect()
            lastInstrRect.midleft = (x, y + 40)

            self.gameWindow.blit(genInstr, genInstrRect)
            self.gameWindow.blit(lastInstr, lastInstrRect)

            y += 165

    def drawStaticText(self, memBlocks):
        font = pygame.font.Font('C:\\Users\\DELL\\Desktop\\Proyecto1-Arqui\\gui\\fonts\\BebasNeue.ttf', 32)
        addrFont = pygame.font.SysFont('consolas', 20)

        mainMemText = font.render('Main Memory', True, red)
        mainMemTextRect = mainMemText.get_rect()
        mainMemTextRect.center = (180, 50)

        busText = font.render('Bus', True, white)
        busText = pygame.transform.rotate(busText, 90)
        busTextRect = busText.get_rect()
        busTextRect.center = (420, 340)

        self.gameWindow.blit(busText, busTextRect)
        self.gameWindow.blit(mainMemText, mainMemTextRect)

        y_addr = 97

        for block in memBlocks:
            addrText = addrFont.render(hex(int(block.addr, 2)), True, white)
            addrTextRect = addrText.get_rect()
            addrTextRect.center = (45, y_addr)
            self.gameWindow.blit(addrText, addrTextRect)
            y_addr += 35

        y_proc = 45
        for i in range(1, 5):
            proccessor = "P"
            procText = font.render(proccessor + str(i), True, lightOrange)
            procTextRect = procText.get_rect()
            procTextRect.center = (930, y_proc)

            lastInstr = font.render("Last Instr:", True, white)
            lastInstrRect = procText.get_rect()
            lastInstrRect.center = (930, y_proc + 35)

            genInstr = font.render("Gen Instr:", True, white)
            genInstrRect = procText.get_rect()
            genInstrRect.center = (930, y_proc + 70)


            self.gameWindow.blit(procText, procTextRect)
            self.gameWindow.blit(lastInstr, lastInstrRect)
            self.gameWindow.blit(genInstr, genInstrRect)

            y_proc += 165



