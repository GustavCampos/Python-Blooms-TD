import pygame
from os import getcwd
from os.path import join as path_join
class Bloom(pygame.sprite.Sprite):
    def __init__(self, track_map: list, 
                 color: pygame.Color, 
                 image: pygame.Surface,
                 velocity: int=1, 
                 current_target: int=1,
                 custom_x: int=-1, 
                 custom_y: int=-1) -> None:
        super().__init__()
        
        #Manually Defined Attributes
        self.track_map = track_map
        self.color = color
        self.velocity = velocity
        self.current_target = current_target
                
        #Automatically Defined Attributes
        self.image = image
        self.active = True
        
        x = custom_x if custom_x > -1 else track_map[0].x
        y = custom_y if custom_y > -1 else track_map[0].y
        
        self.vector = pygame.Vector2(x, y)
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def draw(self, surface) -> None:
        self.image.blit(surface, self.rect, self.rect)
        # pygame.draw.rect(surface, self.color, self.rect)
        
    def move(self, delta_time) -> None|list:
        bloom_reached_end = (self.current_target >= len(self.track_map))
        
        if bloom_reached_end:    
            return self.win()
        
        target_waypoint = self.track_map[self.current_target]
        
        #Move Bloom_______________________________________________
        self.vector.move_towards_ip(
            pygame.Vector2(target_waypoint.x, target_waypoint.y),
            self.velocity * delta_time
        )
        
        self.rect.center = [self.vector.x, self.vector.y]
        #_________________________________________________________
        
        x_reached = self.vector.x == target_waypoint.x
        y_reached = self.vector.y == target_waypoint.y
        if x_reached and y_reached:
            self.current_target += 1
    
    def win(self) -> None:
        self.active = False