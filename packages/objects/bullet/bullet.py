import pygame
from os import getcwd
from os.path import join as path_join
from packages.graphics.sprite_sheet import SpriteSheet
from math import radians, cos, sin
from packages.utilities.functions.image_functions import rotate_image_by_center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, shoot_angle: float, shoot_range: int, velocity: int=1, damage: int=1) -> None:
        super().__init__()
        
        #Manually Created Attributes
        self.shoot_range = shoot_range
        self.velocity = velocity
        self.damage = damage
        
        
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

        return_gold = 0         
        for bloom in pygame.sprite.spritecollide(self, bloom_sprite_group, False):
            if not bloom.is_dying:
                return_gold += bloom.deal_damage(self.damage)
            
        map_instance.set_gold(map_instance.get_gold() + return_gold) 