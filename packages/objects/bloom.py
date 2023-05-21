import pygame
from packages.utilities.math_functions import bezier_curve
from math import sin, cos, radians, ceil

class Bloom:
    def __init__(self, size: int, color: pygame.Color, velocity: int, x: int, y:int, direction: float=0) -> None:
        self.size = size
        self.velocity = velocity
        self.direction = direction
        self.location = (x, y)
        self.color = color
        
        self.rect = pygame.Rect(
            self.location[0], 
            self.location[-1],
            self.size,
            self.size
        )
        
        self.vector = pygame.math.Vector2()
        
    def move(self, point1, point2, referencePoint, range_value):
        result_tuple = bezier_curve(point1, point2, referencePoint, range_value)
        
        self.rect = self.rect.move(
            result_tuple[0] - self.rect.x,
            result_tuple[-1] - self.rect.y,
        )
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)