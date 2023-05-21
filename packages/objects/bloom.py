import pygame
from packages.utilities.way_point import WayPoint
from packages.utilities.math_functions import bezier_curve
from packages.utilities.generic_class import GenericClass

class Bloom:
    def __init__(self, size: int, color: pygame.Color, x: int, y: int,
                 track_map_stage: int=0, track_map_stage_range: float=0, velocity=1) -> None:
        #Manually Defined Attributes
        self.size = size
        self.color = color
        self.location = GenericClass({"x": x, "y": y})
        self.velocity = velocity
                
        #Automatically Defined Attributes
        self.track_map_stage = track_map_stage
        self.track_map_stage_range = track_map_stage_range
        self.rect = pygame.Rect(
            self.location.x, 
            self.location.y,
            self.size,
            self.size
        )
        
    def move(self) -> None:
        track_stage_are_finished = (self.track_map_stage_range > 1)
        if (track_stage_are_finished):
            self.track_map_stage_range = 0
            self.track_map_stage += 1
        
        all_track_stages_were_iterated = (self.track_map_stage >= len(self.track_map))
        if (all_track_stages_were_iterated):
            del self
        
        current_stage_dict = self.track_map[self.track_map_stage]
        
        initial_point = (current_stage_dict['ip'].x, current_stage_dict['ip'].y) 
        final_point = (current_stage_dict['fp'].x, current_stage_dict['fp'].y) 
        reference_point = (current_stage_dict['rp'].x, current_stage_dict['rp'].y) 
        
        result_tuple = bezier_curve(initial_point, final_point, reference_point, self.track_map_stage_range)
        
        self.rect = self.rect.move(
            result_tuple[0] - self.rect.x,
            result_tuple[-1] - self.rect.y,
        )
        
        self.track_map_stage_range += ((current_stage_dict['vm']/1000) * self.velocity)
                   
        
    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)