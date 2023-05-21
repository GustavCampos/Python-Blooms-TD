from random import random
import pygame
from math import radians
from packages.utilities.way_point import WayPoint
from packages.objects.bloom import Bloom

globals_variables = {
    "max_fps": 60,
    "resolution": (800, 600)
}



def main():
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    pygame_clock = pygame.time.Clock()
    
    surface = pygame.display.set_mode(
        globals_variables["resolution"]
    )
    
    wp_1 = WayPoint(0.1, 0.1)
    wp_2 = WayPoint(0.9, 0.9)
    wp_3 = WayPoint(0.4, 0.4)    
    
    # print(degree_variation)  
    
    WayPoint_range = 0
        
    running = True
    while running:
        surface.fill((0, 0, 0))
        wp_1.draw(surface)
        wp_2.draw(surface)
        wp_3.draw(surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
        try:
            # print(bloom.direction)
            bloom.move((wp_1.x, wp_1.y), (wp_2.x, wp_2.y), (wp_3.x, wp_3.y), WayPoint_range)
            bloom.draw(surface)
        except NameError:
            bloom = Bloom(
                20, 
                pygame.Color(0, 255, 0), 
                1, 
                wp_1.x, wp_1.y
            )
        
        # print(pygame_clock.get_fps())
        pygame.display.update()
        pygame_clock.tick(globals_variables["max_fps"])
        WayPoint_range += 0.01
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()