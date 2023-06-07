import pygame
from os import getcwd
from os.path import join as path_join
from packages.graphics.sprite_sheet import SpriteSheet
from math import radians, cos, sin
from packages.utilities.functions.image_functions import rotate_image_by_center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, 
                 shoot_angle: float, 
                 shoot_range: int, 
                 velocity: int=1, 
                 damage: int=1, 
                 pierce: int=1, 
                 pass_when_die: bool=True) -> None:
        super().__init__()
        
        #Manually Created Attributes
        self.shoot_range = shoot_range
        self.velocity = velocity
        self.damage = damage
        self.pierce = pierce
        self.pass_when_die = pass_when_die
        
        #Automatcally Created Attributes
        sprite_sheet = SpriteSheet(path_join(getcwd(), "data", 'imgs', 'bloom-spritesheet.png'))
        
        self.image = pygame.Surface.convert_alpha(sprite_sheet.get_image(0, 32, 32, 32))
        self.image = rotate_image_by_center(self.image, shoot_angle)
        self.rect = self.image.get_rect()
        self.rect.center =  [x, y]
        self.vector = pygame.Vector2((x, y))
        
        self.target_vector = pygame.math.Vector2(
            self.vector.x + (cos(shoot_angle) * shoot_range), #x_axis
            self.vector.y + (sin(shoot_angle) * shoot_range)  #y_axis
        )
        
        self.damaged_blooms = []

    
    def draw(self, surface: pygame.Surface) -> None:
        self.image.blit(surface, self.rect, self.rect)
        
        
    def move(self, delta_time) -> None:
        bullet_reached_end = (
            self.vector.x == self.target_vector.x and
            self.vector.y == self.target_vector.y
        )
        
        if bullet_reached_end:    
            self.kill()
            del self
            return
        
        #Move Bullet_______________________________________________
        self.vector.move_towards_ip(
            self.target_vector,
            self.velocity * delta_time
        )
        
        self.rect.center = [self.vector.x, self.vector.y]
        
    def update(self, map_instance, bloom_sprite_group, delta_time) -> int:
        self.move(delta_time)

        #Calculate colisions and gold gain
        return_gold = 0         
        for bloom in pygame.sprite.spritecollide(self, bloom_sprite_group, False):
            if not bloom.is_dying and bloom not in self.damaged_blooms:
                damage_response = bloom.deal_damage(self.damage) 
                
                return_gold = return_gold + damage_response['gold']
                
                self.damaged_blooms.append(bloom)
                if damage_response['blooms']:
                    self.damaged_blooms.append(*damage_response['blooms'])
                    
                bloom_alive = (damage_response['blooms'] != None)
                if not self.pass_when_die or (self.pass_when_die and bloom_alive):
                    self.calculate_penetration()
                    
        map_instance.set_gold(map_instance.get_gold() + return_gold) 
        
    def calculate_penetration(self):
        if self.pierce == 1:
            self.kill()
            del self
        else:
            self.pierce -= 1
        
    
    #Getters and Setters__________________________________________________________________________
    def get_damage(self) -> int: return self.damage
    def set_damage(self, value) -> None: self.damage = value