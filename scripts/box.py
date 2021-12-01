import pygame

box_size = 48

class Box(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/items/box.png"), (box_size, box_size))
        self.rect = self.image.get_rect(topleft = pos)