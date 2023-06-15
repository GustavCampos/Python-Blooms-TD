import pygame

from packages.objects.bloom.bloom import Bloom
from math import atan, degrees, pi

class Raycast(object):
    def __init__(self, x: int, y: int, bloom_to_track: Bloom):
        self.vector = pygame.Vector2(x, y)
        self.bloom_to_track = bloom_to_track
        
    def get_angle(self):
        bloom_vector = self.bloom_to_track.vector
        
        normalized_x = bloom_vector.x - self.vector.x
        normalized_y = bloom_vector.y - self.vector.y
                
        #This calculate arctan(opossite/adjacent) in formed triangle
        #But this only returns the variation from radian 0 (-pi to pi)
        angle = atan(normalized_y / normalized_x)
        
        #To get the right angle when normalized_x is negative
        #We add half circle to the given variation above
        return angle if normalized_x >= 0 else (angle + pi)
        
    def match_distance(self, distance) -> bool:
        distance_squared = pow(distance, 2)
        
        calculated_distance = self.vector.distance_squared_to(self.bloom_to_track.vector)
        
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