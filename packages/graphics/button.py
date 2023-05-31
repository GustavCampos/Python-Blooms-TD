import os
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(
            self, x, y, message, 
            width=0, 
            height=0, 
            size=30,
            color=(255, 255, 255),
            background_offset=10,
            background_color=(0, 0, 0),
            border_size=2,
            border_color=(255, 255, 255)
        ) -> None:
        super().__init__()
        
        self.x = x
        self.y = y
        
        font = pygame.font.Font(
            os.path.join(os.getcwd(), 'data', 'font', 'ReemKufiFun-VariableFont_wght.ttf'), 
            size
        )
        font_surface = font.render(message, False, color).convert_alpha()
        font_surface_width, font_surface_height = font_surface.get_size()
        
        automatic_total_width = font_surface_width + background_offset
        automatic_total_height = font_surface_height + round(background_offset / 2)
        
        background_surface = pygame.Surface((
            width if width > automatic_total_width else automatic_total_width,
            height if height > automatic_total_height else automatic_total_height
        ))
        
        background_surface_width, background_surface_height = background_surface.get_size()
        
        #Border Surface____________________________________
        self.surface = pygame.Surface(( 
            background_surface_width + (border_size * 2),
            background_surface_height + (border_size * 2)
        ))
        #__________________________________________________
        
        font_rect = font_surface.get_rect()
        background_surface_rect = background_surface.get_rect()
        
        font_rect.center = background_surface_rect.center
        
        background_surface.fill(background_color)
        background_surface.blit(
            font_surface.convert_alpha(),
            (font_rect.x, font_rect.y)
        )
        
        self.surface.fill(border_color)
        self.surface.blit(background_surface, (border_size, border_size))
    
    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        
    def update(self, surface) -> None:
        self.draw(surface)
    
    def check_collide(self, x, y) -> bool:
        rect = pygame.Rect(
            self.x, 
            self.y, 
            self.surface.get_width(),
            self.surface.get_height()
        )
        
        return rect.collidepoint(x, y)