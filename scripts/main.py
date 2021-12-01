import pygame, sys
from settings import WIDTH, HEIGHT
from player import Player
from carrot import Carrot
from box import Box

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bombs & Carrots!")
clock = pygame.time.Clock()

player = Player((100, 300))

# Events
def events():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 

            # Make a explosion
            print("boom")

            # Destroy bomb
            player.bombs.clear()

            # Destroy Boxess

            pygame.time.set_timer(pygame.USEREVENT, 0)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main():

    # Game Setup
    
    carrot = Carrot((700, 300))
    box = Box((200, 200))

    # Game Loop
    while True:
        events()

        # Update        
        player.update()

        # Draw
        if (len(player.bombs) > 0):
            WIN.blit(player.bombs[0].image, player.bombs[0].rect)

        WIN.blit(carrot.image, carrot.rect)
        WIN.blit(box.image, box.rect)
        WIN.blit(player.image, player.rect)
        

        # Final Stuff
        pygame.display.update()
        clock.tick(60)
        WIN.fill('black')


if __name__ == "__main__":
    main()