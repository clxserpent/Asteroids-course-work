import pygame
import random
import math
class powerup(pygame.sprite.Sprite):
    def __init__(self,powerup,x,y):
        super().__init__()
        self.powerup_width = 40
        self.powerup_height = 40
        self.powerup_x = random.randint(0,900)
        self.powerup_y = 0
        self.Powerupimg = pygame.image.load("assets/Rapidfire.png")
        self.powerup = powerup
        if self.powerup == "Rapidfire":
            self.Powerupimg = pygame.image.load("assets/Rapidfire.png")
        if self.powerup == "icepower":
            self.Powerupimg = pygame.image.load("assets/icepower.png")
        self.powerup_x = x
        self.powerup_y = y

        self.scale_image = pygame.transform.scale(self.Powerupimg,(self.powerup_width , self.powerup_height))
        self.image = self.scale_image
        self.thrust =  1
        self.direction = 270
        self.rect = self.image.get_rect(center=(self.powerup_x,self.powerup_y))
    def update(self): 
        self.powerup_x += self.thrust * math.cos(math.radians(-self.direction))  # Move at the correct speed for the x_axis
            # if at an angle Move at the correct speed for the y_axis if at an angle
        self.powerup_y += self.thrust * math.sin(math.radians(-self.direction))
        self.rect = self.image.get_rect(center=(self.powerup_x,self.powerup_y))
        if self.powerup_y > 600:
            self.kill()
        
    
