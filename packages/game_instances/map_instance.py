from math import radians
import os
import pygame
from packages.objects.bloom_factory import BloomFactory
from packages.objects.bullet.bullet import Bullet
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
        
          
        reference_surface = pygame.Surface((
            game_object.display_surface.get_height() * (3/2), 
            game_object.display_surface.get_height()  
        ))
        
        map_image = pygame.image.load(map_image_path).convert()
        self.surface_map_image = pygame.transform.scale(map_image, reference_surface.get_size())
        
        
        collision_map = pygame.image.load(colision_map_path).convert()
        self.surface_colision_map = pygame.transform.scale(collision_map, reference_surface.get_size())
        
        self.surface_bloom = reference_surface.copy()
        self.surface_bloom.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)
        
        self.surface_bullet = reference_surface.copy()
        self.surface_bullet.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)
        
        self.surface_monkey = reference_surface.copy()
        self.surface_monkey.set_colorkey(game_object.GLOBAL_COLOR_KEY_VALUE)                    
                
        #Track for Blooms
        self.map_track, self.rp_list = parser.get_waypoints_list(way_points_path, self.surface_map_image)
        
        #Wave disposition
        self.bloom_track = parser.get_wave_list_from_file(bloom_track_path)
    
    def run(self):
        bloom_factory = BloomFactory(self.bloom_track, self.map_track)
        
        #Bullet Test_________________________________________________________________________
        bullet_group = pygame.sprite.Group()
        #____________________________________________________________________________________
        
        
        while self.game_object.get_game_is_running():
            delta_time = self.game_object.calculate_delta_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_object.set_game_is_running(False)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    
                    # angle = randint(0, 359)
                    angle = 180
                    
                    bullet = Bullet(mouse_x, mouse_y, radians(angle), 1000, 10)
                    bullet_group.add(bullet)
                    
            
            #Render Frame_______________________________________________________________________
            self.game_object.display_surface.fill((0, 0, 0))
            self.surface_bloom.fill(self.surface_bloom.get_colorkey())
            self.surface_bullet.fill(self.surface_bullet.get_colorkey())
            
            bloom_factory.run_map(
                self.surface_bloom,
                delta_time
            )
            
            bullet_group.update(bloom_factory.created_blooms, delta_time)
            bullet_group.draw(self.surface_bullet)
            
            self.game_object.display_surface.blit(self.surface_map_image, (0,0))
            self.game_object.display_surface.blit(self.surface_bloom.convert_alpha(), (0,0))
            self.game_object.display_surface.blit(self.surface_bullet.convert_alpha(), (0,0))
            #___________________________________________________________________________________
                    
            self.game_object.loop_setdown()
            