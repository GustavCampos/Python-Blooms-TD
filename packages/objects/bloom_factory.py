import pygame
from copy import deepcopy as copy_object


class BloomFactory:
    def __init__(self, level_spawns: list[dict], waypoints_map: list[dict]) -> None:
        self.map = waypoints_map
        self.x = waypoints_map[0]["ip"].x
        self.y = waypoints_map[0]["ip"].y
        self.color = pygame.Color(255, 0, 255)
        
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        
        
    def draw(self, surface: pygame.display) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        
    def draw_running_blooms(self, surface) -> None:
        for bloom in self.created_blooms:
            bloom.move()
            bloom.draw(surface)
        
            
    def spawn_blooms(self) -> None:
        
        return