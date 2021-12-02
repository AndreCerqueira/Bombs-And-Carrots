import pygame

carrot_size = 48
box_size = 48
rock_size = 64
bomb_size = 48

class Carrot(pygame.sprite.Sprite):
    def __init__(self, pos, id):
        super().__init__()
        
        self.image = pygame.transform.scale(pygame.image.load("assets/items/carrot.png"), (carrot_size, carrot_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.id = id


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/items/bomb.png"), (bomb_size, bomb_size))
        self.rect = self.image.get_rect(topleft = pos)

        self.cooldown = 50
        self.last = 0


class Box(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/items/box.png"), (box_size, box_size))
        self.rect = self.image.get_rect(topleft = pos)


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/items/rock.png"), (rock_size, rock_size))
        self.rect = self.image.get_rect(topleft = pos)