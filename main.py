import configparser
import os
import pygame
import time
import packages.utilities.functions.parser_functions as parser
from packages.objects.bullet.bullet import Bullet
from packages.objects.bloom_factory import BloomFactory

from math import radians
from random import randint


GLOBAL_COLOR_KEY_VALUE = (138, 111, 48)

CONFIG_OPT = configparser.ConfigParser()
CONFIG_OPT.read(os.path.join(os.getcwd(), 'config.ini'))


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
    
    display_surface = pygame.display.set_mode(
        [int(CONFIG_OPT["DISPLAY"]["SCREEN_WIDTH"]), int(CONFIG_OPT["DISPLAY"]["SCREEN_HEIGHT"])],
        vsync=int(CONFIG_OPT["DISPLAY"]["VSYNC_OPTION"])
    )
    
    surface_map = pygame.Surface((
        display_surface.get_height() * (4/3), 
        display_surface.get_height()
    ))
    
    surface_blooms = surface_map.convert_alpha().copy()
    surface_blooms.set_colorkey(GLOBAL_COLOR_KEY_VALUE)
    
    surface_bullet = surface_map.convert_alpha().copy()
    surface_bullet.set_colorkey(GLOBAL_COLOR_KEY_VALUE)
    
    
    # loading test map for color picker feature___________________________________________
    color_picker_tester = pygame.image.load(os.path.join(current_path, 'data', 'imgs', 'map_test.png'))

    
    map_track, rp_list = parser.get_waypoints_list(
        os.path.join(current_path, 'data', 'config', 'map_config', 'map1.txt'), surface_map
    )
    blooms_track = parser.get_wave_list_from_file(
        os.path.join(current_path, 'data', 'config', 'wave_config', 'easy.txt')
    )
    
    bloom_factory = BloomFactory(blooms_track, map_track)
    
    
    #Bullet Test_________________________________________________________________________
    bullet_group = pygame.sprite.Group()
    #____________________________________________________________________________________
            
    last_time = time.time()
    running = True
    while running:
        dt = (time.time() - last_time)
        dt *= 60
        last_time = time.time()

        #Reset Screen Image_______________________________________
        display_surface.fill((0, 0, 255))
        surface_map.fill((0,0,0))
        surface_map.blit(color_picker_tester, (0,0))
        #_________________________________________________________
        
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONUP:
                
                if event.button == 3:  # Verifica se o botão direito do mouse foi pressionado
                    mouse_x, mouse_y = event.pos
                    
                    mouse_x_p = (mouse_x * 100) / surface_map.get_width()
                    mouse_y_p = (mouse_y * 100) / surface_map.get_height()
                    
                    pixel_color = surface_map.get_at((mouse_x, mouse_y)) # identifica a cor do pixel
                    print("Posição do clique: x =", mouse_x_p, "y =", mouse_y_p)
                    print("Cor do pixel:", pixel_color)
                
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    
                    # angle = randint(0, 359)
                    angle = 180
                    
                    bullet = Bullet(mouse_x, mouse_y, radians(angle), 1000, 10)
                    bullet_group.add(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    CONFIG_OPT['DISPLAY']= {"max_fps": 10}
                if event.key == pygame.K_2:
                    CONFIG_OPT['DISPLAY']= {"max_fps": 60}                    
                if event.key == pygame.K_3:
                    CONFIG_OPT['DISPLAY']= {"max_fps": 90}                    
                if event.key == pygame.K_4:
                    CONFIG_OPT['DISPLAY']= {"max_fps": 0}                    
        
        #Screen Update__________________________________________________________   
        surface_blooms.fill(surface_blooms.get_colorkey())
        surface_bullet.fill(surface_bullet.get_colorkey())
        
        bloom_factory.run_map(surface_blooms, dt)
        bullet_group.update(bloom_factory.created_blooms, dt)
        bullet_group.draw(surface_bullet)
        
        display_surface.blit(surface_map, (0,0))
        display_surface.blit(surface_blooms.convert_alpha(), (0,0))
        display_surface.blit(surface_bullet.convert_alpha(), (0,0))

        # #Debug UI________________________________
        for item in map_track:
            item.draw(display_surface)
        for item in rp_list:
            item.draw(display_surface)
        #________________________________________
        
        
        pygame.display.update()
        #_______________________________________________________________________
        
        pygame_clock.tick(int(CONFIG_OPT["DISPLAY"]["MAX_FPS"]))
        pygame.display.set_caption(f"OpenBloons : {pygame_clock.get_fps()}")
                
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()


if __name__ == "__main__":
    main()