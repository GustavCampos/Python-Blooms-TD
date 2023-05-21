import pygame


class WayPoint:
    def __init__(self, x: int, y: int, use_as_reference: bool=False) -> None:
        if (1 < x) or (x < 0) or (1 < y) or (y < 0):
            raise AttributeError("x and y need to be beetween 0 and 1")
        
        surface = pygame.display.get_surface()
        
        self.color = (255, 0, 0) if not use_as_reference else (0, 0, 255)
        self.percentage_x = x
        self.percentage_y = y
        self.x = round(surface.get_width() * x)
        self.y = round(surface.get_height() * y)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        
    def draw(self, surface: pygame.display) -> None:
        pygame.draw.rect(surface, self.color, self.rect)