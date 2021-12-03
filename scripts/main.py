import pygame, sys, os
from settings import WIDTH, HEIGHT
from level import Level
from items import Carrot
from explosion import Explosion

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("assets/fonts/prstart.ttf", 20)
pygame.display.set_caption("Bombs & Carrots!")
clock = pygame.time.Clock()

# Game setup
level = Level(WIN)
explosionList = [[],[]]

# Game UI
FONT_SCORE = pygame.font.Font("assets/fonts/prstart.ttf", 20)
FONT_SCORER = pygame.font.Font("assets/fonts/prstart.ttf", 40)
carrot_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_carrot.png"), (48, 48))
player_1_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_player1.png"), (21*2.5, 16*2.5))
player_2_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_player2.png"), (21*2.5, 16*2.5))
backgound_music = pygame.mixer.Sound(os.path.join("assets/sounds/background.mp3"))

# Events
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Main Menu Fase
def main_menu():

    # Variables
    menu = True
    play_text_y = HEIGHT-200
    text_speed = 0.7

    # Create UI
    play_text = FONT.render("Press left click to Start!", True, 'white')
    logo = pygame.transform.scale(pygame.image.load("assets/ui/logo.png"), (344, 152))

    backgound_music.play(-1)
    backgound_music.set_volume(1)

    while menu:
        events()

        # Text Movement
        if (play_text_y < HEIGHT-215 or play_text_y > HEIGHT-185):
            text_speed *= -1
        play_text_y -= text_speed

        # Display UI
        WIN.blit(logo, (WIDTH/2 - logo.get_width()/2 , 50))
        WIN.blit(play_text, (WIDTH/2-play_text.get_width()/2, play_text_y))

        # Close UI
        if pygame.mouse.get_pressed()[0]:
            menu = False

        pygame.display.update()
        clock.tick(60)
        WIN.fill('black')


# Setup Game Fase
def setup_game_menu():

    # Variables
    game_start = False 
    level.pre_run()
    carrot_count = 0
    player_color = (95, 205, 228)

    # Create UI
    text_0 = FONT.render("Player " + str(carrot_count+1), True, player_color)
    text_1 = FONT.render("         select a box and hide your Carrot!", True, 'white')

    while not game_start:
        events()

        text_0 = FONT.render("Player " + str(carrot_count+1), True, player_color)
        WIN.blit(text_1, (WIDTH/2-text_1.get_width()/2, 30))
        WIN.blit(text_0, (WIDTH/2-text_1.get_width()/2, 30))
        game_ui()

        for box in level.boxes.sprites():
            if pygame.mouse.get_pressed()[0] and box.rect.collidepoint(pygame.mouse.get_pos()):
                #box.kill()
                carrot = Carrot((box.rect.x, box.rect.y), carrot_count)
                level.insert_carrot(carrot)
                carrot_count += 1
                player_color = (220, 50, 86)
                level.pre_run()
                pygame.time.delay(300)
                if carrot_count == 2:
                    game_start = True

        pygame.display.update()
        clock.tick(60)


# Game UI
def game_ui():
    
    score = [0,0]
    for player in level.player_obj:
        score[int(player.id)-1] = FONT_SCORE.render("x" + str(player.points), True, 'black')

    WIN.blit(player_1_icon, (10, 15))
    WIN.blit(carrot_icon, (60, 10))
    WIN.blit(score[0], (105, 20 + score[0].get_height()/2))

    WIN.blit(player_2_icon, (WIDTH - 60, 15))
    WIN.blit(carrot_icon, (WIDTH - 110, 10))
    WIN.blit(score[1], (WIDTH - 110 - score[1].get_width(), 20 + score[1].get_height()/2))


# Main Game
def main():

    # First Menus
    main_menu()
    pygame.time.delay(300)
    setup_game_menu()

    # Game Loop
    while True:
        events()
        
        level.run()

        # Draw the in game UI
        game_ui()

        # Check if its needed to reset the level
        if len(level.carrots) < 2:
            
            # Draw win popup
            #temp = FONT_SCORER.render("PLAYER 1 FOUND IT!!", 1, 'black')
            #WIN.blit(temp, (300, 300))

            level.reset_level()
            setup_game_menu()

        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()