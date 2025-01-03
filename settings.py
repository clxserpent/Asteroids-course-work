import pygame
import sys
class settings():
    def __init__(self):
        self.playing = False
        self.music = False
        self.display = pygame.display.set_mode((900,600))
        self.background = pygame.image.load("assets/black.png")
        self.all_sprites = pygame.sprite.Group()
    def Button_names(self):
        from mainMenu import Button
        self.buttons = [
            Button(350,250,"controls",self.controls),
            Button(350,350,"music toggle",self.music_bool)
            ]
        
    def controls(self):
        pass
    
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
            
            self.display.blit(self.background,(0,0))
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
settings_menu = settings()