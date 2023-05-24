import time
import pygame
from os import getcwd
from packages.objects.bloom_factory import BloomFactory
from packages.utilities.parser_functions import get_wave_list_from_file, get_waypoints_list


globals_variables = {
    "max_fps":0,
    "resolution": (800, 600)
}

def main():
    last_time = time.time()
    
    pygame.init()
    pygame.display.set_caption("OpenBloons")
    pygame.display.init()
    pygame.font.init()
    pygame_clock = pygame.time.Clock()
    current_path = f"{getcwd()}\data"

    # loading custom icon_________________________________________________________________
    game_icon = pygame.image.load(f'{current_path}\imgs\icon.png')
    pygame.display.set_icon(game_icon)
    
    surface = pygame.display.set_mode(
        globals_variables["resolution"],
        vsync=0
    )
    
    map_track = get_waypoints_list(f"{current_path}\config\map_config\map1.txt")
    blooms_track = get_wave_list_from_file(f"{current_path}\config\wave_config\easy.txt")
    
    bloom_factory = BloomFactory(blooms_track, map_track)
            
    running = True
    while running:
        dt = (time.time() - last_time)
        dt *= 60
        last_time = time.time()

        
        surface.fill((0, 0, 0))
        
        # #Debug UI________________________________
        for item in map_track:
            item.draw(surface)
        # bloom_factory.draw(surface)
        #________________________________________
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    globals_variables["max_fps"] = 10
                if event.key == pygame.K_f:
                    globals_variables["max_fps"] = 60
                if event.key == pygame.K_g:
                    globals_variables["max_fps"] = 90
            
        bloom_factory.run_map(surface, dt)
        
        pygame.display.set_caption(f"OpenBloons : {pygame_clock.get_fps()}")
        pygame.display.update()
        pygame_clock.tick(globals_variables["max_fps"])
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()