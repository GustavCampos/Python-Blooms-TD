import pygame
from packages.objects.monkey.monkey import Monkey


class DartlingMonkey(Monkey):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)    