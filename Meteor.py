import pygame
import math
import random
import threading
import time
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1,6):
            img = pygame.image.load(f"assets/exp{num}.png")
            img = pygame.transform.scale(img,(100,100))
            self.images.append(img)
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0 
        
    def update(self):
        explosion_speed = 1
        self.counter +=1

        if self.counter >= explosion_speed and self.index <  len(self.images) -1:
            self.counter = 0
            self.index += 1 
            self.image = self.images[self.index]
        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,game,size=2,position=None):
        super().__init__()
        self.game = game
        self.size = size
        if position is None:
            self.x = random.randint(5,900)
            self.y = random.randint(5,600)
        else:
            self.x=position[0]
            self.y=position[1]
        self.direction = random.randint(0,360)
        self.thrust =  1
        self.image = pygame.image.load(f"assets//asteroid{self.size}.png")        
        self.Pause = False
        self.explosion_sound = pygame.mixer.Sound("assets/bangLarge.wav")
        #Begin thread to move at start of init block
        self.update_thread = threading.Thread(target=self.update_position)
        self.update_thread.daemon = True
        self.update_thread.start()


    def update_position (self):
        #will only move when  #self.Pause is false (i alrdy added the relevant code to the game when you press t and f)
        while self.Pause == False:
            self.x += self.thrust * math.cos(math.radians(-self.direction))  # Move at the correct speed for the x_axis
            # if at an angle Move at the correct speed for the y_axis if at an angle
            self.y += self.thrust * math.sin(math.radians(-self.direction)) 
            self.rect = self.image.get_rect(center=(self.x,self.y))
            self.handle_screen_wrap()
            time.sleep(0.01)
    def pause(self):
        self.Pause = True

    def unpause(self):
        self.Pause = False
    def update(self):
        '''
        This method is needed so i can reference allsprites.update() and not have to iterate through the class
        as update_position handles the movment logic and calling that on every frame would create a billion threads
        e.g the game would explode
        :return:
        '''
        pass  # The update logic is handled in a separate thread
    def handle_screen_wrap(self):
        screen_width = 600  #hard coding rather than getting on each cycle from game clas
        screen_height = 900

        if self.x > screen_width * 1.5:
            self.x = 0
        elif self.x < 0:
            self.x = screen_width * 1.5
        if self.y > screen_height * 0.7:
            self.y = 0
        elif self.y < 0:
            self.y = screen_height * 0.7
    def hit(self):
        if self.size > 0:
            for _ in range(2):
                asteroid = Asteroid(self.game, self.size - 1,(self.x,self.y))
                self.game.all_sprites.add(asteroid)
                self.game.asteroid_sprites.add(asteroid)
        self.pause = True
        explosion = Explosion(self.x,self.y)
        self.game.all_sprites.add(explosion)
        self.explosion_sound.play()
        self.kill()