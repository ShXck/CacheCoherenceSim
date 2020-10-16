import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

ORANGE = (229, 126, 57)


class Button:

    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):

        self.text = text
        self.command = command

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(WHITE)

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(ORANGE)

        self.image_clicked = pygame.Surface((width, height))
        self.image_clicked.fill(RED)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        self.consolas = pygame.font.SysFont('consolas', 32)

        text_image = self.consolas.render(text, True, BLACK)
        text_rect = text_image.get_rect(center=self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        self.image_clicked.blit(text_image, text_rect)

        # you can't use it before `blit`
        self.rect.topleft = (x, y)

        self.hovered = False
        self.clicked = False

    def update(self):

        if self.hovered:
            self.image = self.image_hovered
        elif self.clicked:
            self.image = self.image_clicked
        else:
            self.image = self.image_normal

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.clicked = not self.clicked
                if self.command:
                    self.command()
