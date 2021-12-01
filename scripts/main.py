import pygame, sys
from settings import WIDTH, HEIGHT, level_map
from level import Level
from explosion import Explosion

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bombs & Carrots!")
clock = pygame.time.Clock()

level = Level(level_map, WIN)
explosionList = []

# Events
def events():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 

            # Make a explosion
            x = level.player_obj.bombs[0].rect.x - 30
            y = level.player_obj.bombs[0].rect.y - 30
            explosion = Explosion((x, y))
            explosionList.append(explosion)
            
            # Destroy bomb
            level.player_obj.bombs.clear()

            # Destroy Boxes
            destruction_area = pygame.Rect(explosion.rect)
            destruction_area.width -= 20
            destruction_area.height -= 20

            destruction_area.x += 20
            destruction_area.y += 20

            for box in level.boxes.sprites():
                if destruction_area.colliderect(box.rect):
                    box.kill()

            pygame.time.set_timer(pygame.USEREVENT, 0)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main():

    # Game Loop
    while True:
        events()

        level.run()

        #explosion.update(1)
        if len(explosionList) > 0:
            for explosion in explosionList:
                explosion.update(0.25)
                WIN.blit(explosion.image, explosion.rect)

        # Final Stuff
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()