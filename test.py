import os
import pygame
from packages.utilities.functions.parser_functions import get_waypoints_list

globals_variables = {
    "max_fps": 60,
    "resolution": (800, 600)
}

pygame.init()
pygame.font.init()
pygame_clock = pygame.time.Clock()
surface = pygame.display.set_mode(
    globals_variables["resolution"]
)

file_path = f"{os.getcwd()}\config\level_config\map1.txt"

jorge = get_waypoints_list(file_path)

for item in jorge:
    print(item["vm"])

pygame.font.quit()
pygame.display.quit()
pygame.quit()

