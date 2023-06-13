import pygame
from packages.objects.bullet.bullet import Bullet

from packages.utilities.classes.raycast import Raycast

class Monkey(pygame.sprite.Sprite):
    def __init__(self, x, y, 
                 size: int=30, 
                 attack_speed: int=3, 
                 damage: int=1,
                 shoot_range: int=500,
                 velocity: int=10,
                 pierce: int=3,
                 pass_when_die: bool=False
                ) -> None:
        super().__init__()
        
        rect = pygame.Rect(0, 0, size, size)
        rect.center = [x,y]
        self.rect = rect
        
        self.color = (148, 81, 5)
        
        self.attack_speed = attack_speed * 60
        self.attack_offset = 0
        self.damage = damage
        self.shoot_range = shoot_range
        self.velocity = velocity
        self.pierce = pierce
        self.pass_when_die = pass_when_die
        
        self.raycasts = []
        
    def update(self, delta_time: float, 
               surface: pygame.Surface, 
               bloom_group: pygame.sprite.Group, 
               bullet_group: pygame.sprite.Group) -> None:
        
        if (self.attack_offset) >= self.attack_speed:
            self.manage_raycasts(bloom_group)
            self.shoot(bullet_group)
            self.attack_offset = 0
            
            
        for raycast in self.raycasts:
            raycast.draw(surface)
            
        # pygame.draw.circle(
        #     surface, 
        #     pygame.color.Color(0, 0, 0, 10), 
        #     self.rect.center, 
        #     self.shoot_range,
            
        # )
        pygame.draw.rect(surface, self.color, self.rect)
        self.attack_offset += delta_time
        
    def manage_raycasts(self, bloom_group: pygame.sprite.Group) -> None:
        for bloom in bloom_group:
            bloom_added = False
            for raycast in self.raycasts:
                if raycast.bloom_to_track == bloom:
                    bloom_added = True
                elif raycast.bloom_to_track not in bloom_group:
                    self.raycasts.remove(raycast)
                    del raycast
                    
            if not bloom_added:
                raycast = Raycast(
                    self.rect.centerx, 
                    self.rect.centery,
                    bloom
                )
                
                self.raycasts.append(raycast)

    
    def shoot(self, bullet_group: pygame.sprite.Group) -> None:
        for raycast in self.raycasts:
            bloom_in_range = raycast.match_distance(self.shoot_range)
                        
            if bloom_in_range:
                new_bullet = Bullet(
                    raycast.vector.x, 
                    raycast.vector.y,
                    raycast.get_angle(),
                    self.shoot_range + 100,
                    self.velocity,
                    self.damage,
                    self.pierce,
                    self.pass_when_die
                )
                
                bullet_group.add(new_bullet)
                return