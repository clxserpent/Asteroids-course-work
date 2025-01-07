import pygame
import sys
from ControlHandler import Controls_Handler
from util import load_save

class settings():
    def __init__(self):
        self.playing = False
        self.music = False
        self.controls_bool = False
        self.display = pygame.display.set_mode((900,600))
        self.background = pygame.image.load("assets/black.png")
        self.all_sprites = pygame.sprite.Group()
        self.save = load_save()
        self.control_handler = Controls_Handler(self.save)
    def Button_names(self):
        from mainMenu import Button
        self.buttons = [
            Button(350,250,"controls",self.controls),
            Button(350,350,"music toggle",self.music_bool)
            ]
        
    def controls(self):
    
        self.display.fill((0,0,200))
        self.control_handler.render(self.display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mouse_pos = pygame.mouse.get_pos()
        for self.button in self.buttons:
            if self.button.rect.collidepoint(mouse_pos):
                self.button.update(pygame.mouse.get_pressed()[0])
        pygame.display.flip()

    
    def music_bool(self):
        self.music = not self.music
        if self.music == False:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
        self.music != self.music
        
            

    
    def run(self,mainmenu):
        self.playing = True
        self.mainmenu = mainmenu
        while self.playing:
            self.Button_names()
            for self.button in self.buttons:
                self.all_sprites.add(self.button)
            
            self.display.fill((0,0,100))
            self.all_sprites.draw(self.display)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.mainmenu.run()
            mouse_pos = pygame.mouse.get_pos()
            for self.button in self.buttons:
                if self.button.rect.collidepoint(mouse_pos):
                    self.button.update(pygame.mouse.get_pressed()[0])
            
            pygame.display.flip()
