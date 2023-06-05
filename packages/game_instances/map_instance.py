import os
import pygame
from math import radians
from packages.graphics.sprite_sheet import SpriteSheet
from packages.objects.bloom_factory import BloomFactory
from packages.objects.bullet.bullet import Bullet
from packages.objects.monkey.monkey_placeholder import MonkeyPlaceholder
import packages.utilities.functions.parser_functions as parser
from packages.enumerations.map_mode import MapMode


class MapInstance:
    def __init__(self,
                 game_object,
                 map_mode: MapMode,
                 way_points_path,
                 colision_map_path,
                 map_image_path) -> None:
        #Manually Created Attributes
        self.game_object = game_object
        
        #Automatcally Created Attributes 
        bloom_track_path = os.path.join(os.getcwd(), 'data', 'config', 'wave_config', 'normal_game.txt')
                
        self.gold = 650

        #Dificult Based variables_________________
        match map_mode:
            case MapMode.EASY:                
                self.life = 200
                
            case MapMode.MEDIUM:                
                self.life = 150
                
            case MapMode.HARD:                
                self.life = 100
                
            case MapMode.INPOPABBLE:                
                self.life = 1
                
            case MapMode.CHIMPS:                
                self.life = 1
        #_________________________________________
                
                
        map_proportion = 3/2 
        
        display_width = game_object.display_surface.get_width()
        display_height = game_object.display_surface.get_height()
        display_scale_resolution = display_width / display_height
        
        self.render_16x9 = display_scale_resolution >= (16 / 9)
        self.map_x_axis = 0 # X distance from border to render the map
        
        
        if self.render_16x9:
            map_by_hud_proportion = 52/60
            map_width = display_width * map_by_hud_proportion
            
            reference_surface = pygame.Surface((
                map_width, 
                map_width / map_proportion
            ))
        else:
            map_by_hud_proportion = 21/24
            map_height = display_height * map_by_hud_proportion
            
            reference_surface = pygame.Surface((
                map_height * map_proportion, 
                map_height  
            ))
            
            #Centralize map x axis ___________________________________________________________
            display_width_midpoint = round(self.game_object.display_surface.get_width() / 2)
            rect = reference_surface .get_rect()
            rect.centerx = display_width_midpoint
            self.map_x_axis = rect.x
            #_________________________________________________________________________________
        
        map_image = pygame.image.load(map_image_path).convert()
        self.surface_map_image = pygame.transform.smoothscale(map_image, reference_surface.get_size())
        
        colision_map = pygame.image.load(colision_map_path).convert()
        self.surface_colision_map = game_object.display_surface.copy()
        self.surface_colision_map.blit(
            pygame.transform.smoothscale(colision_map, reference_surface.get_size()), 
            (self.map_x_axis, 0)
        )
        
        self.surface_bloom = reference_surface.copy()
        self.surface_bloom.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)
        
        self.surface_bullet = reference_surface.copy()
        self.surface_bullet.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)
        
        self.surface_monkey = reference_surface.copy()
        self.surface_monkey.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)
        
        self.surface_hud = reference_surface.copy()
        self.surface_hud.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)            
                
        #Track for Blooms
        self.map_track, self.rp_list = parser.get_waypoints_list(way_points_path, self.surface_map_image)
        
        #Wave disposition
        self.bloom_track = parser.get_wave_list_from_file(bloom_track_path)
        
        #HUD variables_________________________________________________________________________________
        sprite_sheet = SpriteSheet(os.path.join(os.getcwd(), "data", 'imgs', 'bloom-spritesheet.png'))
        icons_size = round(display_height * 0.05)
        
        coin_image = pygame.Surface.convert_alpha(sprite_sheet.get_image(96,0,32,32))
        self.coin_image = pygame.transform.scale(coin_image, (icons_size, icons_size))
        
        heart_image = pygame.Surface.convert_alpha(sprite_sheet.get_image(96,32,32,32))
        self.heart_image = pygame.transform.scale(heart_image, (icons_size, icons_size))

        
        #Font object
        self.font = pygame.font.Font(
            os.path.join(os.getcwd(), 'data', 'font', 'ReemKufiFun-VariableFont_wght.ttf'), 
            round(icons_size * 0.8)
        )
        #______________________________________________________________________________________________
        
    
    def update_hud(self) -> pygame.Surface:
        self.surface_hud.fill(self.surface_hud.get_colorkey())
        map_slice = round(self.surface_hud.get_width() * 0.15)
        
        life_quantity = self.font.render(str(self.life), False, (255,255,255))
        coin_quantity = self.font.render(str(self.gold), False, (255, 255, 255))
        
        self.surface_hud.blit(self.heart_image, (10, 10))
        self.surface_hud.blit(life_quantity, (self.heart_image.get_width(), 10))
        self.surface_hud.blit(self.coin_image, (map_slice + 10, 10))
        self.surface_hud.blit(coin_quantity, (
            map_slice + self.coin_image.get_width() + 10,
            10
        ))
        
    
    def run(self):
        bloom_factory = BloomFactory(self.bloom_track, self.map_track)
        
        #Sprite Groups_______________________________________________________________________
        bullet_group = pygame.sprite.Group()
        monkey_placeholder_group = pygame.sprite.Group()
        #____________________________________________________________________________________
        
        
        while self.game_object.get_game_is_running():
            delta_time = self.game_object.calculate_delta_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_object.set_game_is_running(False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        monkey_placeholder = MonkeyPlaceholder('jorge', self.surface_colision_map)
                        monkey_placeholder_group.add(monkey_placeholder)
                    if event.button == 3:
                        mx, my = pygame.mouse.get_pos()
                        
                        bullet = Bullet(mx, my, radians(180), 1000, 10)
                        bullet_group.add(bullet)
            
            #Render Frame_______________________________________________________________________
            self.game_object.display_surface.fill((0, 0, 0))
            self.surface_bloom.fill(self.surface_bloom.get_colorkey())
            self.surface_bullet.fill(self.surface_bullet.get_colorkey())
            self.surface_monkey.fill(self.surface_monkey.get_colorkey())
            
            bloom_factory.run_map(
                self.surface_bloom,
                delta_time
            )
            
            bullet_group.update(bloom_factory.created_blooms, delta_time)
            bullet_group.draw(self.surface_bullet)
            
            monkey_placeholder_group.update(self.surface_monkey)
            
            self.update_hud()
            
            self.game_object.display_surface.blit(self.surface_map_image, (self.map_x_axis,0))
            self.game_object.display_surface.blit(self.surface_bloom.convert_alpha(), (self.map_x_axis,0))
            self.game_object.display_surface.blit(self.surface_bullet.convert_alpha(), (self.map_x_axis,0))
            self.game_object.display_surface.blit(self.surface_monkey.convert_alpha(), (self.map_x_axis,0))
            self.game_object.display_surface.blit(self.surface_hud.convert_alpha(), (self.map_x_axis, 0))
            #___________________________________________________________________________________
                    
            self.game_object.loop_setdown()
            