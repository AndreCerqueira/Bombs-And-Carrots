import pygame

carrot_size = 48

class Carrot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        self.image = pygame.transform.scale(pygame.image.load("assets/items/carrot.png"), (carrot_size, carrot_size))
        self.rect = self.image.get_rect(topleft = pos)

    