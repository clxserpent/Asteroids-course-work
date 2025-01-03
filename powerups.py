import pygame

class IcePower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.icepower = pygame.image.load("assets//icepower.png")
        self.icepowere = pygame.transform.scale(self.icepower,(100,100))

