import os 
import pygame
import time
import packages.utilities.parser_functions as parser
from packages.objects.bloom_factory import BloomFactory


config_opt = parser.get_config_dict(os.path.join(os.getcwd(), 'config.cfg'))
print(config_opt.sections())

def main():    
    pygame.init()
    pygame.display.set_caption("OpenBloons")
    pygame.display.init()
    pygame.font.init()
    pygame_clock = pygame.time.Clock()
    current_path = os.getcwd()

    # loading custom icon_________________________________________________________________
    game_icon = pygame.image.load(os.path.join(current_path, 'data', 'imgs', 'icon.png'))
    pygame.display.set_icon(game_icon)
    
    surface = pygame.display.set_mode(
        [config_opt["DEFAULT"]["WIDTH"], config_opt["RESOLUTION"]["HEIGHT"]],
        vsync=config_opt["vsync_opt"]
    )
    
    map_track = get_waypoints_list(
        os.path.join(current_path, 'data', 'config', 'map_config', 'map1.txt')
    )
    blooms_track = get_wave_list_from_file(
        os.path.join(current_path, 'data', 'config', 'wave_config', 'easy.txt')
    )
    
    bloom_factory = BloomFactory(blooms_track, map_track)
            
    last_time = time.time()
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
                if event.key == pygame.K_1:
                    config_opt["max_fps"] = 10
                if event.key == pygame.K_2:
                    config_opt["max_fps"] = 60
                if event.key == pygame.K_3:
                    config_opt["max_fps"] = 90
                if event.key == pygame.K_4:
                    config_opt["max_fps"] = 0
            
        bloom_factory.run_map(surface, dt)
        
        pygame.display.set_caption(f"OpenBloons : {pygame_clock.get_fps()}")
        pygame.display.update()
        pygame_clock.tick(config_opt["max_fps"])
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()