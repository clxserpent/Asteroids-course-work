import pygame.sprite
from Meteor import *
from game import *
from ship import *


class Asteroid_Manager:
    def __init__(self, game,asteroid):
        self.game = game
        self.ship = Ship(self.game,False)
        self.asteroid = asteroid
        self.spawned_asteroid = Asteroid(self.game,self.asteroid.size,(random.randint(5,900),random.randint(5,600)))
        self.all_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()
    def spawn(self):
        self.game.all_sprites.add(self.spawned_asteroid)
        self.game.asteroid_sprites.add(self.spawned_asteroid)


    def get_screen_height(self):
        return self.game.height

    def get_screen_width(self):
        return self.game.width


