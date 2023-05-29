import pygame
from packages.objects.bloom.red import BloomRed
from packages.objects.bloom.green import BloomGreen
from packages.objects.bloom.blue import BloomBlue


class BloomFactory:
    def __init__(self, level_spawns: list[dict], waypoints_map: list) -> None:
        ##Manually defined Attributes
        self.level_spawns = level_spawns
        self.map = waypoints_map
        
        
        ##Automatacally defined attributes
        self.x = waypoints_map[0].x
        self.y = waypoints_map[0].y
        self.color = pygame.Color(255, 0, 255)
        
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        
        self.created_blooms = pygame.sprite.Group()
        self.current_wave  = 0
        self.current_bloom = 0
        self.current_bloom_quantity = 1
        self.current_frame = 0
        
    def draw(self, surface: pygame.display) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        
        
    def draw_running_blooms(self, surface, delta_time) -> None:
        for bloom in self.created_blooms:            
            if bloom.active:
                blooms_created = bloom.move(delta_time)
                
                if (blooms_created):
                    self.created_blooms.add(*blooms_created)
                    
            else:
                bloom.kill()
                 
                if len(self.created_blooms.sprites()) == 0:
                    self.current_bloom = 0
                    self.current_wave += 1
                    
        self.created_blooms.draw(surface)

            
    def run_map(self, surface, delta_time) -> None:
        all_waves_iterated = (self.current_wave >= len(self.level_spawns))
        
        if not all_waves_iterated:
            current_wave = self.level_spawns[self.current_wave]
            self.run_wave(current_wave, delta_time)
        
        self.draw_running_blooms(surface, delta_time)
    
    
    def run_wave(self, current_wave: list, delta_time):
        all_blooms_created = (self.current_bloom >= len(current_wave))
        
        if not all_blooms_created:
            current_bloom = current_wave[self.current_bloom]
            
            frame_interval_completed = self.check_frame_interval(current_bloom, delta_time)
            if frame_interval_completed:
                self.create_bloom(current_bloom)
                go_next_bloom = self.check_bloom_quantity(current_bloom)
                
                if go_next_bloom:
                    self.current_bloom += 1

    def check_bloom_quantity(self, current_bloom: dict) -> bool:
        all_blooms_created = (
            self.current_bloom_quantity >= int(current_bloom["quantity"])
        )
        
        if all_blooms_created:
            self.current_bloom_quantity = 1
            return True
        else:
            self.current_bloom_quantity += 1
            return False
    
    
    def check_frame_interval(self, current_bloom: dict, delta_time) -> bool:       
        current_bloom_framerate = (int(current_bloom["framerate"]))
        
        all_frames_waited = (self.current_frame >= current_bloom_framerate)

        if all_frames_waited:
            self.current_frame = 0
            return True
        
        self.current_frame += delta_time
        return False
        

    def create_bloom(self, bloom: dict):
        match bloom["bloom"]:
            case "red":
                created_bloom = BloomRed(self.map)
            case "green":
                created_bloom = BloomGreen(self.map)
            case "blue":
                created_bloom = BloomBlue(self.map)
                
        self.created_blooms.add(created_bloom)