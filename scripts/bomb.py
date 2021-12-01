import pygame

bomb_size = 48

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/items/bomb.png"), (bomb_size, bomb_size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        pass