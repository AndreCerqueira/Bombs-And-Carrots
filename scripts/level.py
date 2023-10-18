import pygame
import os
from random import randint
from settings import *
from player import Player
from items import Box, Rock
from explosion import Explosion
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, surface):
        super().__init__()

        self.tmxdata = load_pygame("../assets/levels/level_data/map_0.tmx")
        self.display_surface = surface
        self.carrots = []
        self.explosionList = []
        self.setup_level(levels[randint(0, 4)])

        self.explosion_sound = pygame.mixer.Sound(os.path.join("../assets/sounds/explosion.mp3"))
        self.explosion_sound.set_volume(0.05)

    def insert_carrot(self, carrot):
        self.carrots.append(carrot)

    def setup_level(self, layout):
        self.boxes = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

        try:
            backup_points = (self.player_obj[0].points, self.player_obj[1].points)
        except:
            backup_points = (0, 0)

        self.player = pygame.sprite.Group()
        self.player_obj = []

        # Setup Boxes and Player
        x, y = 0, 0
        offset = pygame.math.Vector2(0, 0)
        for row_index, row in enumerate(layout):
            offset.y += TILE_OFFSET * 2
            offset.x = 0
            for col_index, cell in enumerate(row):
                offset.x += TILE_OFFSET * 2

                if cell == 'C':

                    x = col_index * tile_size + WIDTH_OFFSET + offset.x
                    y = row_index * tile_size + HEIGHT_OFFSET + offset.y

                    box = Box((x, y))
                    self.boxes.add(box)

                elif cell == 'R':

                    x = col_index * tile_size + WIDTH_OFFSET + offset.x - 10
                    y = row_index * tile_size + HEIGHT_OFFSET + offset.y - 10

                    rock = Rock((x, y))
                    self.rocks.add(rock)

                elif cell == '1' or cell == '2':

                    x = col_index * tile_size + WIDTH_OFFSET + offset.x - 0
                    y = row_index * tile_size + HEIGHT_OFFSET + offset.y - 30

                    player_sprite = Player((x, y), cell, backup_points[int(cell) - 1])
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

            all_sprites = pygame.sprite.Group()
            all_sprites.add(self.boxes)
            all_sprites.add(self.rocks)

            for sprite in all_sprites.sprites():
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

            all_sprites = pygame.sprite.Group()
            all_sprites.add(self.boxes)
            all_sprites.add(self.rocks)

            for sprite in all_sprites.sprites():
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
        self.rocks.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)

    def carrot_player_collision(self):

        for carrot in self.carrots:
            rect = carrot.rect
            temp_rect = pygame.Rect(carrot.rect)
            temp_rect.x = (rect.x - 30)
            temp_rect.y = (rect.y - 60)

            for player in self.player_obj:
                if player.rect.colliderect(temp_rect):
                    if int(player.id) - 1 != carrot.id:
                        player.points += 1
                        self.carrots.remove(carrot)

    def reset_level(self):
        self.carrots.clear()
        self.setup_level(levels[randint(0, 4)])

    def run(self):

        # Update
        self.boxes.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.carrot_player_collision()

        # Draw
        self.draw_map()
        for carrot in self.carrots:
            self.display_surface.blit(carrot.image, carrot.rect)
        self.boxes.draw(self.display_surface)
        self.rocks.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)

        # Bombs
        for player in self.player_obj:
            try:
                if player.bombing:
                    self.bomb_timer(player)
                    self.display_surface.blit(player.bomb.image, player.bomb.rect)
            except:
                pass

        # Explosions
        for explosion in self.explosionList:
            explosion.update(0.25)
            self.display_surface.blit(explosion.image, explosion.rect)

    def bomb_timer(self, player):

        if player.bomb.last <= player.bomb.cooldown:
            player.bomb.last += 1
        else:
            self.explosion(player)

    def explosion(self, player):

        # Get Bomb Position
        x = player.bomb.rect.x - 30
        y = player.bomb.rect.y - 30

        # Create Explosion
        self.explosion_sound.play()
        explosion = Explosion((x, y))
        self.explosionList.append(explosion)

        # Destroy bomb
        player.bombing = False

        # Get the bomb area
        destruction_area = pygame.Rect(explosion.rect)
        destruction_area.width -= 20
        destruction_area.height -= 20
        destruction_area.x += 20
        destruction_area.y += 20

        # Destroy Boxes
        for box in self.boxes.sprites():
            if destruction_area.colliderect(box.rect):
                box.kill()
