"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame
 
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        
        #Unique Color to remove Background
        self.color_key = (138,111,48) 
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.set_colorkey(self.color_key)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Return the image
        return pygame.Surface.convert_alpha(image)