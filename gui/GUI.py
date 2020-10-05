import sys
import pygame

blue = (0, 0, 255)
white = (255, 255, 255)
red = (255, 0, 0)
lightOrange = (229, 126, 57)


class GUI:

    def __init__(self):
        pygame.init()
        self.gameWindow = pygame.display.set_mode((1280, 680))
        pygame.display.set_caption("Cache Coherence Simulation Software")
        self.clock = pygame.time.Clock()

    def startGUI(self, memBlocks):

        self.drawMainMemBlocks(16)
        self.drawBusComms()
        self.drawText(memBlocks)
        self.drawCacheBlocks(4)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

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

    def drawCacheBlocks(self, blockNumber):
        x = 590
        y = 30

        rectWidth = 200
        rectHeight = 30

        for _ in range(blockNumber):
            for _ in range(blockNumber):
                pygame.draw.rect(self.gameWindow, white, (x, y, rectWidth, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 205, y, rectWidth - 170, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 240, y, rectWidth - 160, rectHeight))
                pygame.draw.rect(self.gameWindow, white, (x + 285, y, rectWidth - 170, rectHeight))
                y += 35
            y += 25

    def drawText(self, memBlocks):
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



