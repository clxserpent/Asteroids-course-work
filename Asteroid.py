# TODO: setup keybind settings
# TODO: setup music settings
# TODO: scoreboard increases 2 points for medium asteroid 3 points for small asteroid
# TODO : fix asteroid spawning on player
# TODO: POWERUPS

#  import pygame
height = 900  # set the height for the 1
width= 600  # sets the width for the display window
from mainMenu import *
pygame.init()
width = 600
height = 900
pygame_icon = pygame.image.load("AS.ico") # sets  window icon as icon picture
pygame.display.set_icon(pygame_icon) # displays icon on window
display = pygame.display.set_mode((height,width))  # takes the height and weight and uses pygames axis to make a display
pygame.display.set_caption("Asteroids")  # labels the window asteroids
ast = Mainmenu(display, height, width) 
ast.run()                 