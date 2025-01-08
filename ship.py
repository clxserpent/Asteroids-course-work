from typing import Any
import pygame
import math
import time
import Meteor
from scoreboard import *
from util import load_save
from powerups import powerup
import sys
PLAYER_1_STARTING_X_POS = 400
PLAYER_1_STARTING_Y_POS = 300

PLAYER_2_STARTING_X_POS = 600
PLAYER_2_STARTING_Y_POS = 300

SHIP_HEIGHT = 50
SHIP_WIDTH = 50





class Bullet(pygame.sprite.Sprite):
    def __init__(self,x, y, direction,game,player2):
        super().__init__()

        self.x = x
        self.y = y
        self.game = game
        self.asteroid = Asteroid(self.game)
        self.player2 = player2
        self.direction = direction
        self.thrust = 10
        self.lifespan = 500
        self.orig_image = pygame.Surface([20, 3], pygame.SRCALPHA)
        pygame.draw.rect(self.orig_image, (255, 255, 0), (0, 0, 20, 3))
        self.image = pygame.transform.rotate(self.orig_image, self.direction)
        self.rect = self.image.get_rect(center=(self.x, self.y))
       
        self.laser_sound = pygame.mixer.Sound("assets//p.wav")
        self.laser_sound.play()

    def update(self):
        self.ship = Ship(self.game,self.player2)
        self.y += self.thrust * math.sin(math.radians(-self.direction))
        self.x += self.thrust * math.cos(math.radians(-self.direction))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.lifespan -= self.thrust
   
        if self.lifespan < 0:
            self.kill()
        
        hit_list = pygame.sprite.spritecollide(self, self.game.asteroid_sprites, False, pygame.sprite.collide_mask)
        if hit_list:
            for asteroid in hit_list:
                asteroid.update()
                asteroid.hit()
                if self.player2:
                    if self.asteroid.size == 0:
                            player2_scores.player2_score += 2
                    else:
                        player2_scores.update()
                else:
                    if  self.asteroid.size == 0:
                        player1_scores.player1_score += 2
                    player1_scores.update()
                player2_scores.player1_score = player1_scores.player1_score 
                player1_scores.player2_score == player2_scores.player2_score
            self.kill()

class Ship(pygame.sprite.Sprite):
    def __init__(self, game, player_2):
        super().__init__()
        self.game = game
        self.SpawnProtection= 100
        self.ProtectionCountdown = self.SpawnProtection
        self.height = SHIP_HEIGHT
        self.width = SHIP_WIDTH
        self.player_2_status = player_2
        self.x_pos = 0
        self.y_pos = 0
        self.time = 0
        self.startTime = time.monotonic()
        self.power_up_start_time = 0
        self.paused = False
        if not self.player_2_status:
            self.x_pos = PLAYER_1_STARTING_X_POS
            self.y_pos = PLAYER_1_STARTING_Y_POS
        else:
            self.x_pos = PLAYER_2_STARTING_X_POS
            self.y_pos = PLAYER_2_STARTING_Y_POS
        self.player_lives = 3
        self.direction = 0  # angle ship is facing
        self.thrust = 0  # speed to apply to our current position
        self.rotation = 0  # amount of rotation to apply to our current direction
        self.last_shot = 0
        self.bulletcooldown = 0.5
      
        if not self.player_2_status:
            self.orig_image = pygame.image.load("assets/Rocket Ship.png")
        else:
            self.orig_image = pygame.image.load("assets/download-removebg-preview.png")
        self.scale_image = pygame.transform.scale(self.orig_image, (self.width, self.height))
        self.orig_image = self.scale_image
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.all_sprites = pygame.sprite.Group()
        self.power_up_duration = 10000  # 10 seconds
            
        self.controls = {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d
        }

    def update(self):
        if not self.player_2_status:
            self.handle_input_player_1()
        else:
            self.handle_input_player_2()
        self.rotate_and_move()
        self.check_collisions()
        if self.x_pos > self.game.get_screen_width() * 1.5:
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = self.game.get_screen_width() * 1.5
        if self.y_pos > self.game.get_screen_height() * 0.7:
            self.y_pos = 0 
        elif self.y_pos < 0:
            self.y_pos = self.game.get_screen_height() * 0.7


    def handle_input_player_1(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls["UP"]]:
            self.thrust += 0.12
        if keys[self.controls["LEFT"]]:
            self.rotation += 0.2
        if keys[self.controls["DOWN"]]:
            self.thrust -= 0.12
        if keys[self.controls["RIGHT"]]:
            self.rotation -= 0.2
        if keys[pygame.K_SPACE]:
            self.fire_bullet()


     


    def handle_input_player_2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.thrust += 0.12
        if keys[pygame.K_LEFT]:
            self.rotation += 0.2
        if keys[pygame.K_DOWN]:
            self.thrust -= 0.12
        if keys[pygame.K_RIGHT]:
            self.rotation -= 0.2
        if keys[pygame.K_RCTRL]:
            self.fire_bullet()

    def rotate_and_move(self):
        self.rotation /= 1.05  # make the rotation value smaller to better work with updating our position
        self.thrust /= 1.05  # make the thrust value smaller to better work with updating our position. Not too fast.
        self.x_pos += self.thrust * math.cos(math.radians(-self.direction))  # Move at the correct speed for the x_axis
                                                                                    # if at an angle
        self.y_pos += self.thrust * math.sin(math.radians(-self.direction))  # Move at the correct speed for the y_axis if at an angle
        self.direction += self.rotation  # rotation of the sprite
        self.image = pygame.transform.rotate(self.orig_image, self.direction - 90)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))



               

    def fire_bullet(self):
        if time.time() - self.last_shot > self.bulletcooldown:
            my_bullet = Bullet(self.x_pos, self.y_pos, self.direction,self.game,self.player_2_status)
            self.game.all_sprites.add(my_bullet)
            self.last_shot = time.time()
    def set_position(self):
        if self.player_2_status == False:
            self.x_pos = PLAYER_1_STARTING_X_POS
            self.y_pos = PLAYER_1_STARTING_Y_POS
        else:
            self.x_pos = PLAYER_2_STARTING_X_POS
            self.y_pos = PLAYER_2_STARTING_Y_POS
        self.game.all_sprites.draw(self.game.display)
    def check_player(self):
        return self.player_2_status
    
    def check_collisions(self):
        asteroid_hit_list = pygame.sprite.spritecollide(self, self.game.asteroid_sprites, False, pygame.sprite.collide_mask)
        Rapidfire_hit_list = pygame.sprite.spritecollide(self,self.game.Rapidfirelists,True,pygame.sprite.collide_mask)
        icepower_hit_list = pygame.sprite.spritecollide(self,self.game.icepowerlists,True,pygame.sprite.collide_mask)
        self.time_delta = time. monotonic() - self.startTime

        if self.ProtectionCountdown:
            self.ProtectionCountdown -= 1
        else:
            if asteroid_hit_list:
                explosion = Explosion(self.x_pos,self.y_pos)
                self.game.all_sprites.add(explosion)
                self.explosion_sound = pygame.mixer.Sound("assets/bangLarge.wav")
                self.explosion_sound.play()
                self.player_lives -= 1 
                self.ProtectionCountdown = self.SpawnProtection
                while self.player_lives > 0:
                    self.set_position()
                    break
                if self.player_lives == 0:
                    self.kill()
                 
        if Rapidfire_hit_list:
            self.power_up_start_time = pygame.time.get_ticks()
            self.bulletcooldown = 0.3
        if icepower_hit_list:
            self.power_up_start_time = pygame.time.get_ticks()
            try:
                self.all_sprites.pause()
            except AttributeError: # paused all movement
                pass
            self.game.pause_menu(self.player_2_status)

        self.elapsed_time = pygame.time.get_ticks() - self.power_up_start_time
        if self.elapsed_time >= self.power_up_duration:
        # Deactivate the power-up
            self.bulletcooldown = 0.5
            self.paused = False





            
                
            
                
            


                       
            



                    