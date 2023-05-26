"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame
 
class SpriteSheet(object):
    def __init__(self, file_name): 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        
        #Unique Color to remove Background
        self.color_key = (138,111,48) 
 
 
    def get_image(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        image.fill(self.color_key)
 
        # Copy the sprite from the large sheet onto the smaller image
        image.set_colorkey(self.color_key)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Return the image
        return pygame.Surface.convert_alpha(image)