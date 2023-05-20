from random import randint
import pygame
from packages.objects.bloom import Bloom


def main():
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    pygame_clock = pygame.time.Clock()
    
    surface = pygame.display.set_mode((800, 600))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        bloom = Bloom(
            10,
            pygame.Color(
                randint(0, 255), 
                randint(0, 255), 
                randint(0, 255)
            )
        )
        
        print(pygame_clock.get_fps())
        bloom.draw(surface)
        pygame.display.update()
        pygame_clock.tick(3000)
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()