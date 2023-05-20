import pygame
from random import randint


class Bloom:
    def __init__(self, size: int, color: pygame.Color, velocity: int) -> None:
        self.size = size
        self.velocity = velocity
        
        surface = pygame.display.get_surface()
        x_max_value = surface.get_width() - self.size
        y_max_value = surface.get_height() - self.size
        
        self.location = (randint(0 , x_max_value), randint(0, y_max_value))
        self.color = color
        
        self.rect = pygame.Rect(
            self.location[0], 
            self.location[-1],
            self.size,
            self.size
        )
        
    def move(self, direction: str):
        print(direction)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)