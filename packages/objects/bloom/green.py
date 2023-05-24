import pygame
from packages.objects.bloom.bloom import Bloom

class BloomGreen(Bloom):
    def __init__(self, track_map: list, current_target: int = 1,
                 custom_x: int = -1, custom_y: int = -1) -> None:
        super().__init__(
            track_map=track_map, 
            color=pygame.Color(0, 255, 0), 
            size=20,
            velocity=1.1, 
            current_target=current_target,
            custom_x=custom_x,
            custom_y=custom_y
        )