import pygame
from os import getcwd
from os.path import join as path_join
from packages.graphics.sprite_sheet import SpriteSheet


class Bloom(pygame.sprite.Sprite):
    def __init__(self, track_map: list, 
                 color: pygame.Color, 
                 image: pygame.Surface,
                 damage: int,
                 life: int=1,
                 velocity: int=1, 
                 current_target: int=1,
                 custom_x: int=-1, 
                 custom_y: int=-1) -> None:
        super().__init__()
        
        #Manually Defined Attributes
        self.track_map = track_map
        self.color = color
        self.damage = damage
        self.life = life
        self.velocity = velocity
        self.current_target = current_target
                
        #Automatically Defined Attributes
        sprite_sheet = SpriteSheet(path_join(getcwd(), "data", 'imgs', 'bloom-spritesheet.png'))
        pop_image = pygame.Surface.convert_alpha(sprite_sheet.get_image(0, 64, 32, 32))
        self.popimage = pop_image
        self.image = image
        self.active = True
        self.death_duration = 3 #Duration frame quantity for death animation
        self.death_frame = 0
        self.is_dying = False
        self.winner = False
        self.return_blooms = None
        
        x = custom_x if custom_x > -1 else track_map[0].x
        y = custom_y if custom_y > -1 else track_map[0].y
        
        self.vector = pygame.Vector2(x, y)
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def draw(self, surface) -> None:
        self.image.blit(surface, self.rect, self.rect)

        
    def move(self, delta_time) -> None|list:
        if self.is_dying:
            if self.death_frame >= self.death_duration:
                self.set_active(False)
                return self.return_blooms
            else:
                self.death_frame += delta_time
        else:
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
            
            
    def deal_damage(self, damage) -> bool:
        self.life -= damage
        return (self.life <= 0)
    
    def start_death(self):
        self.is_dying = True
        self.image = self.popimage
        
      
    def win(self) -> None:
        self.set_win(True)
        self.set_active(False)
    
    
    ##Getters and Setters____________________________________________
    def set_active(self, bool: bool) -> None: self.active = bool
    def get_active(self) -> bool: return self.active
    
    def set_win(self, bool: bool) -> None: self.winner = bool
    def get_win(self) -> bool: return self.winner
    
    def get_damage(self) -> int: return self.damage