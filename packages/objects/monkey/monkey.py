import pygame

class Monkey(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect()