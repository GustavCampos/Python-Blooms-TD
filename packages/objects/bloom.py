import pygame
from packages.utilities.way_point import WayPoint
from packages.utilities.math_functions import bezier_curve
from packages.utilities.generic_class import GenericClass

class Bloom:
    def __init__(self,track_map: list, color: pygame.Color, 
                 size: int=20, velocity: int=1,
                 track_map_stage: int=0, track_map_stage_range: float=0) -> None:
        #Manually Defined Attributes
        self.track_map = track_map
        self.size = size
        self.color = color
        self.velocity = velocity
        self.track_map_stage = track_map_stage
        self.track_map_stage_range = track_map_stage_range
                
        #Automatically Defined Attributes
        self.location = GenericClass({
            "x": track_map[track_map_stage]["ip"].x, 
            "y": track_map[track_map_stage]["ip"].y
        })
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
        
        #TODO remove this line later
        # current_stage_dict["vm"] = 1
        
        self.track_map_stage_range += ((current_stage_dict['vm']/1000) * self.velocity)
                   
        
    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)