import pygame
from packages.utilities.way_point import WayPoint
from packages.objects.bloom import Bloom
from packages.objects.bloom_factory import BloomFactory


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
    
    bloom_factory = BloomFactory(map_track)
        
    running = True
    while running:
        surface.fill((0, 0, 0))
        
        # #Debug UI________________________________
        for stage in map_track:
            for key, item in stage.items():
                if (key != "vm"):
                    item.draw(surface)
        bloom_factory.draw(surface)
        #________________________________________
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
        bloom_factory.create_wave(bloom_wave_1, 10)
        bloom_factory.draw_running_blooms(surface)
        
        # print(pygame_clock.get_fps())
        pygame.display.update()
        pygame_clock.tick(globals_variables["max_fps"])
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()