import pygame
from math import degrees


##FOR GOD SAKE, PLEASE, DONT TOUCH THIS!!!!!!_________________________________
def rotate_image_by_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    
    #This function only rotates based on a degree in a clockwise direction
    converted_degree = (- degrees(angle))

    rot_image = pygame.transform.rotate(image, converted_degree)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
#_____________________________________________________________________________