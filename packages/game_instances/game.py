import os
import time
import pygame
from packages.enumerations.map_mode import MapMode
from packages.game_instances.map_instance import MapInstance
from packages.graphics.button import Button

class Game:
    def __init__(self, CONFIG_OPT) -> None:     
        self.GLOBAL_COLOR_KEY_VALUE = (138, 111, 48)   
        self.clock = pygame.time.Clock()
        self.current_path = os.getcwd()
        self.game_icon = pygame.image.load(os.path.join(self.current_path, 'data', 'imgs', 'icon.png'))
    
        self.display_surface = pygame.display.set_mode(
            [int(CONFIG_OPT["DISPLAY"]["SCREEN_WIDTH"]), int(CONFIG_OPT["DISPLAY"]["SCREEN_HEIGHT"])],
            vsync=int(CONFIG_OPT["DISPLAY"]["VSYNC_OPTION"])
        )
        
        self.CONFIG_OPTIONS = CONFIG_OPT
        self.game_is_running = True
        self.last_time = time.time()
    
        pygame.display.set_icon(self.game_icon)
        
    
    def reset_surface(self) -> None:
        self.display_surface.fill((0,0,0))
        
        
    def calculate_delta_time(self) -> float:
        delta_time = (time.time() - self.last_time)
        delta_time *= 60
        self.last_time = time.time()
        
        return delta_time
    
    
    def loop_setdown(self):
        pygame.display.update()
        self.clock.tick(int(self.CONFIG_OPTIONS["DISPLAY"]["MAX_FPS"]))
        pygame.display.set_caption(f"OpenBloons : {self.clock.get_fps()}")
    
    
    def run(self) -> None:
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        
        self.main_menu() 
        
        pygame.font.quit()
        pygame.display.quit()
        pygame.quit()
    
    
    #TODO: Needs to refactor later        
    def main_menu(self) -> None:
        display_middle = self.display_surface.get_width() / 2
        bottom = self.display_surface.get_height()
        
        level_button = Button(0, (bottom - 150), 'LEVELS')
        level_button.x = (display_middle - (level_button.surface.get_width() + 10))
        config_button = Button((display_middle + 10), (bottom - 150), 'CONFIG')
        
        button_group = pygame.sprite.Group(level_button, config_button)
        
        while self.game_is_running:
            delta_time = self.calculate_delta_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if level_button.check_collide(*event.pos):
                            self.level_select_menu()
                        if config_button.check_collide(*event.pos):
                            self.configuration_menu()
            
            self.display_surface.fill((0, 0, 0))
            button_group.update(self.display_surface)
            self.loop_setdown()
        
    def level_select_menu(self) -> None:
        display_middle = self.display_surface.get_width() / 2
        bottom = self.display_surface.get_height()
        
        map_1_button = Button(0, (bottom - 150), 'MAP 1')
        map_1_button.x = (display_middle - (map_1_button.surface.get_width() + 10))
        back_button = Button((display_middle + 10), (bottom - 150), 'BACK')
        
        button_group = pygame.sprite.Group(map_1_button, back_button)
        
        while self.game_is_running:
            delta_time = self.calculate_delta_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False 
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    return
                if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                    if map_1_button.check_collide(*event.pos):
                        map_instance = MapInstance(
                            self, 
                            MapMode.EASY,
                            os.path.join(self.current_path, 'data', 'config', 'map_config', 'map1.txt'),
                            os.path.join(self.current_path, 'data', 'config', 'wave_config', 'easy.txt'),
                            os.path.join(self.current_path, 'data', 'imgs', 'color_picker_tester.png'),
                            os.path.join(self.current_path, 'data', 'imgs', 'map_test.png')
                        )
                        
                        map_instance.run()

                    if back_button.check_collide(*event.pos):
                        return
            
            self.display_surface.fill((0, 0, 0))
            button_group.update(self.display_surface)
            self.loop_setdown()
        
    def configuration_menu(self) -> None:
        while self.game_is_running:
            delta_time = self.calculate_delta_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    
            self.display_surface.fill((0, 0, 0))
            self.loop_setdown()
                
                    
    #Getters and Setters____________________________
    def get_game_is_running(self) -> bool:
        return self.game_is_running
    
    def set_game_is_running(self, bool: bool) -> None:
        self.game_is_running = bool