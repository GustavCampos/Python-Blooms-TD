from random import random
import pygame
from math import radians, sqrt
from packages.utilities.way_point import WayPoint
from packages.objects.bloom import Bloom

globals_variables = {
    "max_fps": 60,
    "resolution": (800, 600)
}



def main():
    pygame.init()
    pygame.display.set_caption("OpenBloons")
    pygame.display.init()
    pygame.font.init()
    pygame_clock = pygame.time.Clock()

    # loading custom icon
    game_icon = pygame.image.load('imgs\icon.png')
    pygame.display.set_icon(game_icon)
    
    surface = pygame.display.set_mode(
        globals_variables["resolution"]
    )
    
    wp_1 = WayPoint(0.01, 0.01)
    wp_2 = WayPoint(0.2, 0.2)
    wp_3 = WayPoint(0.2, 0.01, True)
    wp_4 = WayPoint(0.9, 0.2)
    wp_5 = WayPoint(0.55, 0.9, True)
    
    map_track = [{
        "ip": wp_1,
        "fp": wp_2,
        "rp": wp_3,
        "vm": 10
    },{
        "ip": wp_2,
        "fp": wp_4,
        "rp": wp_5,
        "vm": 3 
    }] 
    
    # print(degree_variation)  
        
    running = True
    while running:
        surface.fill((0, 0, 0))
        for stage in map_track:
            for key, item in stage.items():
                if (key != "vm"):
                    item.draw(surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
        try:
            # print(bloom.direction)
            bloom.move()
            bloom.draw(surface)
        except NameError:
            bloom = Bloom(20, pygame.Color(0, 255, 0), 1, map_track)
        
        # print(pygame_clock.get_fps())
        pygame.display.update()
        pygame_clock.tick(globals_variables["max_fps"])
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()