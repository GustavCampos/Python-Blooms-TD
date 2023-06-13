import pygame

from packages.objects.bloom.bloom import Bloom
from math import atan, degrees, pi

class Raycast(object):
    def __init__(self, x: int, y: int, bloom_to_track: Bloom):
        self.vector = pygame.Vector2(x, y)
        self.bloom_to_track = bloom_to_track
        
    def get_angle(self):
        bloom_vector = self.bloom_to_track.vector
        
        normalized_target_xy =  [
            bloom_vector.x - self.vector.x,
            bloom_vector.y - self.vector.y
        ]
        
        angle_tangent = (normalized_target_xy[0] / normalized_target_xy[1])
        return_angle = atan(angle_tangent)
        
        print(f'ridian: {return_angle}\ndegree: {degrees(return_angle)}')
        return return_angle 
        
    def match_distance(self, distance) -> bool:
        distance_squared = pow(distance, 2)
        
        calculated_distance = self.vector.distance_squared_to(self.bloom_to_track.vector)
        
        # print(f'current: {calculated_distance}, reference: {distance_squared}')
        
        if calculated_distance <= distance_squared:
            return True
        
        return False
    
    def draw(self, surface) -> None:
        pygame.draw.line(
            surface, 
            (255,255,255), 
            self.vector.xy,
            self.bloom_to_track.vector.xy
        )