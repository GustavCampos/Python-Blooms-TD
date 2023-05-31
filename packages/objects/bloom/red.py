import pygame
from packages.objects.bloom.bloom import Bloom
from os import getcwd
from os.path import join as path_join
from packages.graphics.sprite_sheet import SpriteSheet

class BloomRed(Bloom):
    def __init__(self, track_map: list, current_target: int = 1,
                 custom_x: int = -1, custom_y: int = -1) -> None:
        sprite_sheet = SpriteSheet(path_join(getcwd(), "data", 'imgs', 'bloom-spritesheet.png'))
        image = pygame.Surface.convert_alpha(sprite_sheet.get_image(0, 0, 32, 32))
        
        super().__init__(
            image=image,
            track_map=track_map, 
            color=pygame.Color(0, 255, 0), 
            velocity=1.1, 
            current_target=current_target,
            custom_x=custom_x,
            custom_y=custom_y
        )
        