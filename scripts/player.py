import pygame
from pygame import sprite
from utilis import import_folder
from bomb import Bomb

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.bombs = []

        # Player image and animations
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'walk-front'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # Player Transform
        self.width = 100
        self.height = 100

        # Player Movement
        self.speed = 8
        self.direction = pygame.math.Vector2(0,0)


    def import_character_assets(self):
        character_path = 'assets/sprites/other/hero/'
        self.animations = {'idle-front':[],'walk-front':[],'walk-back':[],'walk-side':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def animate(self):
        animation = self.animations[self.status]

		# loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        flip = False
        if self.direction.x < 0:
            flip = True

        self.image = pygame.transform.flip(pygame.transform.scale(image, (self.width, self.height)), flip, False)
        

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Get the direction
        if keys[pygame.K_a]: # Left
            self.direction.x = -self.speed
        if keys[pygame.K_d]: # Right
            self.direction.x = self.speed
        if keys[pygame.K_w]: # Up
            self.direction.y = -self.speed
        if keys[pygame.K_s]: # Down
            self.direction.y = self.speed

        # Remove speed if its not moving
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = 0
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = 0

        # Drop Bomb
        if keys[pygame.K_SPACE]:
            self.drop_bomb()

        # Add the direction to the player
        self.rect.topleft += self.direction


    def get_status(self):

        if (self.direction.x < 0):
            self.status = 'walk-side'
        elif (self.direction.x > 0):
            self.status = 'walk-side'   
        elif (self.direction.y > 0):
            self.status = 'walk-front'   
        elif (self.direction.y < 0): 
            self.status = 'walk-back'  
        else:
            self.status = 'idle-front'  


    def drop_bomb(self):
        if (len(self.bombs) == 0):
            x = self.rect.x + 30
            y = self.rect.y + self.height/2
            bomb = Bomb((x, y))
            self.bombs.append(bomb)
            pygame.time.set_timer(pygame.USEREVENT, 1000)


    def update(self):
        self.get_input()
        self.get_status()
        self.animate()

        

    #def draw():
