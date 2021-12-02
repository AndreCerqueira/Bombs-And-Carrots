import pygame
from utilis import import_folder
from items import Bomb

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, id, points):
        super().__init__()

        self.bombing = False
        self.id = id
        #self.carrots = []
        self.points = points
        
        # Player Keys
        if id == '1':
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.up = pygame.K_w
            self.down = pygame.K_s
            self.attack = pygame.K_LSHIFT
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.up = pygame.K_UP
            self.down = pygame.K_DOWN
            self.attack = pygame.K_RSHIFT

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

        self.on_left = False
        self.on_right = False
        self.on_down = False
        self.on_top = False

        # Player Movement
        self.speed = 4
        self.direction = pygame.math.Vector2(0,0)


    def import_character_assets(self):
        character_path = 'assets/player_' + self.id + '/'
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
        if keys[self.left]: # Left
            self.direction.x = -1
        if keys[self.right]: # Right
            self.direction.x = 1
        if keys[self.up]: # Up
            self.direction.y = -1
        if keys[self.down]: # Down
            self.direction.y = 1

        # Remove speed if its not moving
        if not keys[self.left] and not keys[self.right]:
            self.direction.x = 0
        if not keys[self.up] and not keys[self.down]:
            self.direction.y = 0

        # Drop Bomb
        if keys[self.attack]:
            self.drop_bomb()


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
        if not self.bombing:
            x = self.rect.x + 30
            y = self.rect.y + self.height/2

            self.bomb = Bomb((x, y))
            self.bombing = True


    def update(self):
        self.get_input()
        self.get_status()
        self.animate()


