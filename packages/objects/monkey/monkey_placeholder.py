import pygame
from packages.objects.monkey.monkey import Monkey

class MonkeyPlaceholder(pygame.sprite.Sprite):
    def __init__(self, monkey: str,  colision_surface: pygame.Surface, place_color=pygame.Color(0, 255, 0)) -> None:
        super().__init__()
        
        self.monkey = monkey
        self.place_color = place_color
        
        self.colision_surface = colision_surface
        
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.surface = pygame.Surface((32, 32))
        self.surface.fill((255, 255, 255))
        self.surface.set_alpha(200)
        
        pygame.mouse.set_visible(False)
        
    def draw(self, surface: pygame.Surface, is_coliding: bool) -> None:
        fill_color = (255, 0, 0) if is_coliding else (255, 255, 255)
        self.surface.fill(fill_color)
        
        surface.blit(self.surface, (self.rect.x,self.rect.y))

        
    def update(self, surface: pygame.Surface) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = [mouse_x, mouse_y]
        
        colision_subsurface = self.colision_surface.subsurface(self.rect)
        
        #Treshold need to be this value to work to return a valid count bit value (1024)_____________________________
        colision_mask = pygame.mask.from_threshold(colision_subsurface, self.place_color, (10, 10, 10, 255))
        #________________________________________________________________________________________________________________
        
        mouse_buttons = pygame.mouse.get_pressed()
        if not (mouse_buttons[0]):
            pygame.mouse.set_visible(True)
            self.kill()
            return
            
        is_coliding = colision_mask.count() != 1024
                    
        self.draw(surface, is_coliding)
        
    def spawn_monkey(self):
        pass