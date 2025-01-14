import pygame
from game import Game
import sys
from scoreboard import *
from settings import *
pygame.init()
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, callback):
        super().__init__()
        self.callback = callback
        self.normal_image = pygame.Surface([200, 50]).convert_alpha()
        self.normal_image.fill((5, 5, 5))
        self.normal_image.fill((5, 5, 5), (10, 10, 200, 50))
        pygame.font.init()
        self.hover_image = self.normal_image.copy()
        self.hover_image.fill((5, 5, 5), (10, 10, 200, 50))

        self.font = pygame.font.SysFont("calibr", 20)
        text_surface = self.font.render(text, True, (0, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = self.normal_image.get_rect().center
        self.normal_image.blit(text_surface, text_rect)
        text_rect = text_surface.get_rect()
        text_rect.center = self.hover_image.get_rect().center
        self.hover_image.blit(text_surface, text_rect)
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, mouse_pressed):
        if mouse_pressed and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.callback()


class Mainmenu():
    def __init__(self, display, height, width):
        self.display = display
        self.background = pygame.image.load("assets/background.jpg").convert()  # Preload and convert for optimization
        self.background = pygame.transform.scale(self.background, (height, width))
        self.all_sprites = pygame.sprite.Group()  # this groups together all the sprites created making it easier to
        self.playing = False
        self.buttons = [
            Button(350, 250, "Single Player ", self.player_1),
            Button(350, 350, "Two Player ", self.player_2),
            Button(350, 450, "Quit ", self.quit),
            Button(350,550,"settings",self.setting)

        ]
        for button in self.buttons:
            self.all_sprites.add(button)
        self.height = height
        self.width = width
        self.player_2_game = False

        self.logo_image = pygame.image.load ("assets/logo.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (350, 150))
        logo_rect = self.logo_image.get_rect
      

    def display_logo(self):
        self.logo_rect = self.logo_image.get_rect(center=(350, 150))

    def setting(self):
        settings_menu = settings()
        settings_menu.run(self)

    def play(self):
        player2_scores.player2_score = 0
        player1_scores.player1_score = 0
        self.startup_sound = pygame.mixer.Sound("assets//startup.wav")
        self.startup_sound.play()
        self.soundtrack.stop()
        new_game = Game(self.display, self.height, self.width, self.player_2_game)
        new_game.run(self.player_2_game)
        
        
        

    def get_screen_height(self):
        return self.height

    def get_screen_width(self):
        return self.width

    def quit(self):
        self.playing = False
        pygame.quit()
        sys.exit()
        
     

    def player_1(self):
        player1_scores.player1_score = 0
        self.player_2_game = False
        self.play()
        return self.player_2_game

    def player_2(self):
        player2_scores.player2_score = 0
        self.player_2_game = True
        self.play()
        return self.player_2_game,player2_scores.player2_score

    
    def run(self):
        # main game loop
        self.playing = True  # This makes it so that the game runs automatically on start

        try:    
            self.game = Game(self.display,self.height,self.width,self.player_2_game)
            self.playing = True  # This makes it so that the game runs automatically on start
            if self.playing == True:
                self.soundtrack = pygame.mixer.Sound("Soundtrack.mp3")
                self.soundtrack.play()
            
            while self.playing:
            
                self.game.paused = False
                pygame.joystick.init()
                self.joysticks = [pygame.joystick.Joystick(x) for x in range  (pygame.joystick.get_count())]

                for event in pygame.event.get(pygame.QUIT):  # Only handle Quit events
                    self.quit()
                    pygame.display.quit()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.game.paused = False
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
                        if event.key == pygame.K_1:
                            self.player_1()
                        if event.key == pygame.K_2:
                            self.player_2()

                    if event.type == pygame.JOYBUTTONDOWN:
                        print(event)
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.update(pygame.mouse.get_pressed()[0])
                        
                    self.display.blit(self.background,(0,0))
                    self.all_sprites.draw(self.display)
                    self.display.blit(self.logo_image, (295,130))
                    pygame.display.flip()  # Using flip() instead of update() for full display update
        except pygame.error:
            pass