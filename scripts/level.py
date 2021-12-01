import pygame
import random
from settings import *
from player import Player
from box import Box
from pytmx.util_pygame import load_pygame
    
class Level():
    def __init__(self, level_data, surface):
        super().__init__()

        self.tmxdata = load_pygame("assets/levels/level_data/map_0.tmx")
        self.display_surface = surface 
        self.setup_level(level_data)


    def insert_carrot(self, carrot):
        self.carrot = carrot


    def setup_level(self,layout):
        self.boxes = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.player_obj = []

        # Setup Boxes and Player
        x, y = 0, 0
        offset = pygame.math.Vector2(0, 0)
        for row_index, row in enumerate(layout):
            offset.y += TILE_OFFSET * 2
            offset.x = 0
            for col_index,cell in enumerate(row):
                offset.x += TILE_OFFSET * 2

                if cell == 'X':
                    
                    x = col_index * tile_size + WIDTH_OFFSET + offset.x
                    y = row_index * tile_size + HEIGHT_OFFSET + offset.y

                    box = Box((x,y))
                    self.boxes.add(box)

                if cell == '1' or cell == '2':
                    x = col_index * tile_size + WIDTH_OFFSET + offset.x - 30
                    y = row_index * tile_size + HEIGHT_OFFSET + offset.y - 60
                    
                    player_sprite = Player((x,y), cell)
                    self.player_obj.append(player_sprite)
                    self.player.add(player_sprite)


    def draw_map(self):
        for layer in self.tmxdata:
            for tile in layer.tiles():
                x_pixel = tile[0] * 32
                y_pixel = tile[1] * 32
                self.display_surface.blit(tile[2], (x_pixel, y_pixel))


    def horizontal_movement_collision(self):

        for player in self.player.sprites():
            player.rect.x += player.direction.x * player.speed
        
            for sprite in self.boxes.sprites():
                rect = sprite.rect
                temp_rect = pygame.Rect(sprite.rect)
                temp_rect.x = (rect.x - 30)
                temp_rect.y = (rect.y - 60)
                if temp_rect.colliderect(player.rect):
                    if player.direction.x < 0: 
                        player.rect.left = temp_rect.right
                        player.on_left = True
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:
                        player.rect.right = temp_rect.left
                        player.on_right = True
                        self.current_x = player.rect.right

            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

            # Check Collision with borders
            if player.rect.x < BORDER_X_MIN:
                player.rect.left = BORDER_X_MIN
            if player.rect.x > BORDER_X_MAX:
                player.rect.left = BORDER_X_MAX


    def vertical_movement_collision(self):

        for player in self.player.sprites():
            player.rect.y += player.direction.y * player.speed

            for sprite in self.boxes.sprites():
                rect = sprite.rect
                temp_rect = pygame.Rect(sprite.rect)
                temp_rect.x = (rect.x - 30)
                temp_rect.y = (rect.y - 60)
                if temp_rect.colliderect(player.rect):
                    if player.direction.y > 0: 
                        player.rect.bottom = temp_rect.top
                        player.on_down = True
                        self.current_y = player.rect.bottom
                    elif player.direction.y < 0:
                        player.rect.top = temp_rect.bottom
                        player.on_top = True
                        self.current_y = player.rect.top

            if player.on_down and (player.rect.bottom < self.current_y or player.direction.y >= 0):
                player.on_down = False
            if player.on_top and (player.rect.top > self.current_y or player.direction.y <= 0):
                player.on_top = False

            # Check Collision with borders
            if player.rect.y < BORDER_Y_MIN:
                player.rect.top = BORDER_Y_MIN
            if player.rect.y > BORDER_Y_MAX:
                player.rect.top = BORDER_Y_MAX


    def pre_run(self):
        self.boxes.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.draw_map()
        self.boxes.draw(self.display_surface)
        self.player.update(self.display_surface)
        self.player.draw(self.display_surface)


    def run(self):

        # Update
        self.boxes.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        # Draw
        self.draw_map()
        self.display_surface.blit(self.carrot.image, self.carrot.rect)
        self.boxes.draw(self.display_surface)
        self.player.update(self.display_surface)
        self.player.draw(self.display_surface)
