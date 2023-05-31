import pygame


class WayPoint:
    def __init__(self, x: int, y: int, surface: pygame.Surface) -> None:
        if (1 < x) or (x < 0) or (1 < y) or (y < 0):
            raise AttributeError("x and y need to be beetween 0 and 1")
        
        self.color = (255, 0, 0)
        self.percentage_x = x
        self.percentage_y = y
        self.x = round(surface.get_width() * x)
        self.y = round(surface.get_height() * y)
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        self.rect.center = [self.x, self.y]
        
    def draw(self, surface: pygame.display) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        
class ReferenceWayPoint(WayPoint):
    def __init__(self, x: int, y: int, surface: pygame.Surface) -> None:
        super().__init__(x, y, surface)
        self.color = (0, 0, 255)        
        
        
class GeneratedWayPoint(WayPoint):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.color = (165, 255, 253)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        self.rect.center = [self.x, self.y]
        
        