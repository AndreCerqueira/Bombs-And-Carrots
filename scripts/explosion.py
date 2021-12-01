import pygame
from utilis import import_folder_explosion

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.sprites = import_folder_explosion("assets/effects/explosion/")
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, speed):

        # Animation
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.image.fill((0,0,0,0))
            self.kill()
        else:
            self.image = self.sprites[int(self.current_sprite)]

        