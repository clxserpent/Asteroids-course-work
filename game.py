import pygame
import sys
from Meteor import Asteroid
from ship import Ship
from scoreboard import *
from Asteroid_manager import *
from settings import *
class Game:
    def __init__(self, display, height, width, player2):
        self.paused = None
        self.display = display
        self.keys = pygame.key.get_pressed()
        self.white = (255, 255, 255)
        self.endgame_sound = pygame.mixer.Sound("assets//endgame.wav")
        self.player_1 = Ship(self, False)
        self.player_2 = Ship(self,True)
        self.asteroid = Asteroid(self)
        self.Rapidfirelists = pygame.sprite.Group()
        self.icepowerlists = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()
        self.powerup_spawned = False
        self.P1PowerUpLastScore = 0 
        self.P2PowerUpLastScore = 0
        if player2: 
            self.all_sprites.add(self.player_2,self.player_1)
        else:
            self.all_sprites.add(self.player_1)
        self.all_sprites.add(self.asteroid)
        self.asteroid_sprites.add(self.asteroid)
        self.background = pygame.image.load("assets/space.png")
        self.background = pygame.transform.scale(self.background, (height, width))

        self.clock = pygame.time.Clock()
        self.playing = True
        self.height = height
        self.width = width
        pygame.font.init()
        self.bigtext = pygame.font.SysFont("calibr", 100)
        self.textfont = pygame.font.SysFont("calibr", 40)
        self.display_quit = self.textfont.render("press Q to quit", 1, (255, 255, 255))
        self.display_menu = self.textfont.render("Press G to go to main menu", 1, (255, 255, 255))
        self.display_restart = self.textfont.render("Press C to restart", 1, (255, 255, 255))
        self.asteroid_reload = 500
        self.asteroid_block = self.asteroid_reload

        self.gameover = False
    
    def GameoverMenu(self,player2):
        self.player2 = player2
        self.display.blit(self.background,(0,0))
        self.DisplayGameover = self.bigtext.render("Gameover",1,(255,0,0))
        self.display.blit(self.DisplayGameover,(300,50))
        self.display.blit(self.display_restart, (15, 200))
        self.display.blit(self.display_quit, (15, 300))
        self.display.blit(self.display_menu, (15, 400))
        for event in pygame.event.get():  # Only handle Quit events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.gameover = False
                    pygame.quit()
                    sys.exit

                elif event.key == pygame.K_c:
                    self.playing = False  
                    player1_scores.player1_score = 0 
                    player2_scores.player2_score = 0 
                    new_game = Game(self.display, self.height, self.width, self.player2)
                    new_game.run(self.player2)
                elif event.key == pygame.K_g:
                    self.gameover = False
            if self.gameover == False:
                break
            try:
                 pygame.display.update()
            except pygame.error:
                pass

    def pause_menu(self,player2):
        self.paused = True
        self.player2 = player2
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        try:
                            self.all_sprites.unpause()
                        except AttributeError: #once again pausing all asteroid threaded movment
                            pass
                        self.paused = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit
                    elif event.key == pygame.K_c:
                        self.playing = False  
                        player1_scores.player1_score = 0 
                        player2_scores.player2_score = 0 
                        new_game = Game(self.display, self.height, self.width, self.player2)
                        new_game.run(self.player2)
                    elif event.key == pygame.K_g:
                        self.paused = False
                        self.playing = False
            self.display_continue = self.textfont.render("Press F to continue", 1, (255, 255, 255))
            self.pause_text = self.bigtext.render("paused", 1, (255, 255, 0))
            self.display.blit(self.background,(0,0))
            self.display.blit(self.display_continue,(15,200))
            self.display.blit(self.pause_text,(250,15))
            self.display.blit(self.display_restart, (15, 300))
            self.display.blit(self.display_quit, (15, 400))
            self.display.blit(self.display_menu, (15, 500))           
            
            pygame.display.update()

    def run(self, player2):
        # Main game loop
        from settings import settings
        self.playing = True 

        while self.playing:
            player1_scores.highscore = player2_scores.highscore
            player2_scores.highscore = player1_scores.highscore
            if self.asteroid_block:
                self.asteroid_block -= 1 
            else:
                Aster = Asteroid_Manager(self,self.asteroid)
                Aster.spawn()
                self.asteroid_block = self.asteroid_reload
                pygame.display.update()

            if not player2:
                if player1_scores.player1_score >= self.P1PowerUpLastScore + 2 and player1_scores.player1_score >= 2  and player1_scores.player1_score != self.P1PowerUpLastScore:
                    Power = powerup_manager(self,"icepower")
                    Power.spawn()
                    self.P1PowerUpLastScore = player1_scores.player1_score
            if player2:
                if player1_scores.player1_score >= self.P1PowerUpLastScore + 10 and player1_scores.player1_score >= 10  and player1_scores.player1_score != self.P1PowerUpLastScore:
                    Power = powerup_manager(self,"Rapidfire")
                    Power.spawn()
                    self.P1PowerUpLastScore = player1_scores.player1_score
                if player2_scores.player2_score >= self.P2PowerUpLastScore + 10 and player2_scores.player2_score >= 10  and player2_scores.player2_score != self.P2PowerUpLastScore:
                    Power = powerup_manager(self,"Rapidfire")
                    Power.spawn()
                    self.P2PowerUpLastScore = player2_scores.player2_score
            for event in pygame.event.get():  # Only handle Quit events
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                    sys.exit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        try:
                            self.all_sprites.pause()
                        except AttributeError: # paused all movement
                            pass
                        self.pause_menu(player2)
                            

            self.display.blit(self.background, (0, 0))
            self.clock.tick(120)  # Cap the FPS at 60
            self.all_sprites.update()
            self.Rapidfirelists.update()
            self.icepowerlists.update()
 

            try:
                self.all_sprites.draw(self.display)
                self.Rapidfirelists.draw(self.display)
                self.icepowerlists.draw(self.display)
            except:
                pass
            if not player2:
                player1_scores.updatefile()
                if self.player_1.player_lives == 0:
                    self.gameover = True
                    break
            self.score_text = self.textfont.render(f"p1 score:{player1_scores.player1_score}", 1, (255, 255, 255))
            self.display.blit(self.score_text,(15,10))
            self.highscoreText = self.textfont.render(f"highscore:{player1_scores.highscore}" , 1 ,(255,255,255))
            self.player1_lives_display = self.textfont.render(f"player1 lives: {self.player_1.player_lives}", 1, (255, 255, 255))
            self.display.blit (self.player1_lives_display, (15,550))
                
            player1_scores.highscore = player2_scores.highscore

            if player2:
                self.P2ScoreText = self.textfont.render(f"p2 score: {player2_scores.player2_score}",1, (255,255,255))
                self.display.blit(self.P2ScoreText,(300,10))
                player2_scores.updatefile()
                self.highscoreText = self.textfont.render(f"highscore:{player1_scores.highscore}" , 1 ,(255,255,255))
                self.player2_live_display = self.textfont.render(f"player2 lives: {self.player_2.player_lives}", 1, (255, 255, 255))
                self.display.blit(self.player2_live_display,(300,550))
            self.display.blit(self.highscoreText,(500,10))
            
            if self.player_1.player_lives ==0 and self.player_2.player_lives == 0:
                self.gameover = True
                break
    
            pygame.display.update()
        if self.gameover == True:
            self.gameover_sound = pygame.mixer.Sound("assets//endgame.wav")
            self.gameover_sound.play()
        while self.gameover:
            self.GameoverMenu(player2)
            try:
                pygame.display.update()
            except pygame.error:
                pass


    def get_screen_height(self):
        try:
            return self.height
        except AttributeError:
            pass # this is only needed to initalize the window once initalized Game object has no attribute height /width

    def get_screen_width(self):
        try:
            return self.width
        except AttributeError:
            pass
