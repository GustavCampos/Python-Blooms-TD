import pygame
from packages.objects.bloom import Bloom


class BloomFactory:
    def __init__(self, level_spawns: list[dict], waypoints_map: list[dict]) -> None:
        ##Manually defined Attributes
        self.level_spawns = level_spawns
        self.map = waypoints_map
        
        
        ##Automatacally defined attributes
        self.x = waypoints_map[0]["ip"].x
        self.y = waypoints_map[0]["ip"].y
        self.color = pygame.Color(255, 0, 255)
        
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        
        self.created_blooms = []
        self.current_wave  = 0
        self.current_bloom = 0
        self.current_bloom_quantity = 1
        
    def draw(self, surface: pygame.display) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        
    def draw_running_blooms(self, surface) -> None:
        for bloom in self.created_blooms:
            bloom.move()
            bloom.draw(surface)
        
            
    def run_map(self, surface) -> None:
        if (len(self.level_spawns) > self.current_wave): 
            current_wave_blooms = self.level_spawns[self.current_wave]        
            current_bloom = current_wave_blooms[self.current_bloom]
            
            match current_bloom["bloom"]:
                case "red":
                    color = pygame.Color(255, 0, 0)
                case "green":
                    color = pygame.Color(0, 255, 0)
                case "blue":
                    color = pygame.Color(0, 0, 255)
                    
            current_bloom_object = Bloom(self.map, color)
            self.created_blooms.append(current_bloom_object)
        
            self.current_bloom += 1
            
            if (len(self.level_spawns[self.current_wave]) <= self.current_bloom):
                self.current_wave += 1
                self.current_bloom = 0
        
        self.draw_running_blooms(surface)