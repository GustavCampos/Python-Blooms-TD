import pygame
from packages.graphics.sprite_sheet import SpriteSheet
from packages.objects.bloom.bloom import Bloom
from os import getcwd
from os.path import join as path_join
from packages.objects.bloom.green import BloomGreen
from packages.objects.bloom.red import BloomRed

class BloomBlue(Bloom):
    def __init__(self, track_map: list, map_surface: pygame.Surface, current_target: int = 1,
                 custom_x: int = -1, custom_y: int = -1) -> None:
        sprite_sheet = SpriteSheet(path_join(getcwd(), "data", 'imgs', 'bloom-spritesheet.png'))
        image = pygame.Surface.convert_alpha(sprite_sheet.get_image(64,0,32,32))
        
        super().__init__(
            damage=3,
            image=image,
            track_map=track_map, 
            color=pygame.Color(0, 255, 0), 
            velocity=3, 
            current_target=current_target,
            custom_x=custom_x,
            custom_y=custom_y,
            map_surface=map_surface
        )
        
        
    def deal_damage(self, damage) -> dict:
        return_list = {
            'gold': 0,
            'blooms': None
        }
        
        die = super().deal_damage(damage)
        
        if die:
            spawn_green = (self.life >= -1)
            spawn_red = (self.life >= -2)
            
            if spawn_green:
                return_list['blooms'] = [
                    BloomGreen(
                        self.track_map, 
                        self.map_surface,
                        self.current_target, 
                        self.vector.x, 
                        self.vector.y
                    )
                ]
                return_list['gold'] += 1
                
            elif spawn_red:
                return_list['blooms'] = [
                    BloomRed(
                        self.track_map, 
                        self.map_surface,
                        self.current_target, 
                        self.vector.x, 
                        self.vector.y
                    )
                ]
                return_list['gold'] += 2

            self.start_death()
        
        self.return_blooms = return_list['blooms']    
        return return_list