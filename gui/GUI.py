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
        self.mainMemRects = []
        self.busComms = []

    def startGUI(self, memBlocks):

        self.drawMainMemBlocks(16)
        self.drawBusComms()
        self.drawText(memBlocks)

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
            newRect = pygame.draw.rect(self.gameWindow, white, (x, y, rectWidth, rectHeight))
            self.mainMemRects.append(newRect)
            y += 35

    def drawBusComms(self):
        # Bus
        busRect = pygame.draw.rect(self.gameWindow, lightOrange, (400, 50, 40, 600))
        self.busComms.append(busRect)

        # draw main to bus rect
        main2BusRect = pygame.draw.rect(self.gameWindow, lightOrange, (280, 330, 120, 20))
        self.busComms.append(main2BusRect)

        y_comm = 80

        for _ in range(4):
            busComm = pygame.draw.rect(self.gameWindow, lightOrange, (440, y_comm, 150, 20))
            self.busComms.append(busComm)
            y_comm += 170


    def drawCacheBlocks(self, blockNumber):
        # TODO: Implement
        return


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
