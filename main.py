import pygame
from os import getcwd
from packages.utilities.way_point import WayPoint
from packages.objects.bloom import Bloom
from packages.objects.bloom_factory import BloomFactory
from packages.utilities.parser_functions import get_wave_list_from_file, get_waypoints_list


globals_variables = {
    "max_fps": 1,
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
    
    current_path = getcwd()
    map_track = get_waypoints_list(f"{current_path}\config\level_config\map1.txt")
    blooms_track = get_wave_list_from_file(f"{current_path}\config\wave_config\easy.txt")
    
    bloom_factory = BloomFactory(blooms_track, map_track)
        
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
            
        bloom_factory.run_map(surface)
        
        # print(pygame_clock.get_fps())
        pygame.display.update()
        pygame_clock.tick(globals_variables["max_fps"])
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()