import pygame
from packages.objects.bloom import Bloom

class BloomRed(Bloom):
    def __init__(self, size: int, color: pygame.Color, x: int, y: int,
                track_map_stage: int = 0, track_map_stage_range: float = 0) -> None:
        super().__init__(size, color, x, y, track_map_stage, track_map_stage_range)