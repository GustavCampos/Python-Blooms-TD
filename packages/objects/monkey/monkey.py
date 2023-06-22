import pygame
from packages.objects.bullet.bullet import Bullet
from packages.utilities.classes.raycast import Raycast

class Monkey(pygame.sprite.Sprite):
    def __init__(self, x, y, 
                 map_surface: pygame.Surface,
                 size: int=30, 
                 attack_speed: float=3, #Seconds between each attack
                 damage: int=1,
                 shoot_range: float=0.2,
                 bullet_velocity: int=10,
                 pierce: int=3,
                 pass_when_die: bool=False
                ) -> None:
        super().__init__()
        
        self.map_surface = map_surface
        
        rect = pygame.Rect(0, 0, size, size)
        rect.center = [x,y]
        self.rect = rect
        
        self.color = (148, 81, 5)
        self.range_color = (50, 50, 50)
        
        #Shoot range is a given percentage of map height
        self.shoot_range = map_surface.get_height() * shoot_range
        
        
        
        self.attack_speed = attack_speed * 60
        self.attack_offset = self.attack_speed
        self.damage = damage
        self.bullet_velocity = bullet_velocity
        self.pierce = pierce
        self.pass_when_die = pass_when_die
        
        self.raycasts = []
        
    def update(self, delta_time: float, 
               surface: pygame.Surface, 
               bloom_group: pygame.sprite.Group, 
               bullet_group: pygame.sprite.Group,
               debug_mode: bool=True) -> None:
        
        if (self.attack_offset) >= self.attack_speed:
            self.manage_raycasts(bloom_group)
            shot_done = self.shoot(bullet_group)
            
            if shot_done:
                self.attack_offset = 0
            
        #Debug for raycast________________________________________________________________
        if debug_mode:
            for raycast in self.raycasts:
                raycast.draw(surface)
        #_________________________________________________________________________________
                    
        pygame.draw.circle(
            surface, 
            pygame.color.Color(10, 10, 10), 
            self.rect.center, 
            self.shoot_range,  
        )

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

    
    def shoot(self, bullet_group: pygame.sprite.Group) -> bool:
        for raycast in self.raycasts:
            bloom_in_range = raycast.match_distance(self.shoot_range)
                        
            if bloom_in_range:
                new_bullet = Bullet(
                    raycast.vector.x, 
                    raycast.vector.y,
                    raycast.get_angle(),
                    self.shoot_range + 100,
                    self.bullet_velocity,
                    self.damage,
                    self.pierce,
                    self.pass_when_die
                )
                
                bullet_group.add(new_bullet)
                return True
            
        return False