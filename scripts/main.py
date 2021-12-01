import pygame, sys
from settings import WIDTH, HEIGHT, level_map
from level import Level
from carrot import Carrot
from explosion import Explosion

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("assets/fonts/prstart.ttf", 20)
pygame.display.set_caption("Bombs & Carrots!")
clock = pygame.time.Clock()

level = Level(level_map, WIN)
explosionList = [[],[]]

# Events
def events():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 

            for player in level.player_obj:
                if player.bombing == True:

                    # Get Bomb Position
                    x = player.bombs[0].rect.x - 30
                    y = player.bombs[0].rect.y - 30
                    id = int(player.id)-1

                    # Create Explosion
                    explosion = Explosion((x, y))
                    explosionList[id].append(explosion)
                    
                    # Destroy bomb
                    level.player_obj[id].bombs.clear()
                    level.player_obj[id].bombing = False

                    # Get the bomb area
                    destruction_area = pygame.Rect(explosion.rect)
                    destruction_area.width -= 20
                    destruction_area.height -= 20
                    destruction_area.x += 20
                    destruction_area.y += 20

                    # Destroy Boxes
                    for box in level.boxes.sprites():
                        if destruction_area.colliderect(box.rect):
                            box.kill()

            pygame.time.set_timer(pygame.USEREVENT, 0)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main():

    # Main Menu Fase
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Create UI
        logo = pygame.transform.scale(pygame.image.load("assets/ui/logo.png"), (344, 152))
        play_text = FONT.render("Press any button to Start!", True, 'white')

        # Display UI
        WIN.blit(logo, (WIDTH/2 - logo.get_width()/2 , 50))

        WIN.blit(play_text, (WIDTH/2-play_text.get_width()/2, HEIGHT-200))

        # Close UI
        if pygame.mouse.get_pressed()[0]:
            menu = False

        pygame.display.update()
        clock.tick(60)
        WIN.fill('black')

    # Delay
    pygame.time.delay(300)

    # Setup Game Fase
    game_start = False
    level.pre_run()
    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        text = FONT.render("Select a box and hide your Carrot!", True, 'white')
        WIN.blit(text, (WIDTH/2-text.get_width()/2, 30))

        for box in level.boxes.sprites():
            # Destroy Boxes
            if pygame.mouse.get_pressed()[0] and box.rect.collidepoint(pygame.mouse.get_pos()):
                #box.kill()
                carrot = Carrot((box.rect.x, box.rect.y))
                level.insert_carrot(carrot)
                game_start = True

        pygame.display.update()
        clock.tick(60)


    # Game Loop
    while True:
        events()
        
        level.run()

        # Draw the explosions
        if len(explosionList[0]) > 0:
            for explosion in explosionList[0]:
                explosion.update(0.25)
                WIN.blit(explosion.image, explosion.rect)

        if len(explosionList[1]) > 0:
            for explosion in explosionList[1]:
                explosion.update(0.25)
                WIN.blit(explosion.image, explosion.rect)


        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()